# rpi_counter_fastapi-dev2/app/services/detection_service.py

import asyncio
import uuid
import json
from collections import deque
from typing import Dict, Deque, List, Optional, Any
import httpx
import cv2
import numpy as np
from pathlib import Path
import redis.asyncio as redis


from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from app.models.detection import DetectionEventLog
from config import settings

class QcApiService:
    """A client to interact with the external QC API System."""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def perform_inspection(
        self, image_path: str, serial_number: str, checks: List[str]
    ) -> Optional[Dict[str, Any]]:
        if not checks:
            return None 

        url = "/api/v1/inspection/single/upload"
        params = [("checks_to_perform", check) for check in checks]
        
        try:
            with open(image_path, "rb") as f:
                files = {"image": (Path(image_path).name, f, "image/jpeg")}
                data = {"serial_number": serial_number}
                
                print(f"QC API Request: Uploading {Path(image_path).name} for checks: {checks}")
                response = await self.client.post(url, params=params, files=files, data=data)
                response.raise_for_status()
                print("QC API Response: Success")
                return response.json()
        except httpx.RequestError as e:
            print(f"FATAL ERROR: Could not connect to QC API at {e.request.url}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"FATAL ERROR: QC API returned status {e.response.status_code}. Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"FATAL ERROR: An unexpected error occurred during QC API call: {e}")
            return None

class AsyncDetectionService:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        camera_manager: AsyncCameraManager,
        orchestration_service: AsyncOrchestrationService,
        redis_client: redis.Redis,
        conveyor_settings,
        db_session_factory,
        active_camera_ids: List[str]
    ):
        self._io = modbus_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._redis = redis_client
        self._conveyor_config = conveyor_settings
        self._get_db_session = db_session_factory
        self._active_camera_ids = active_camera_ids
        self._lock = asyncio.Lock()
        self._verbose = settings.LOGGING.VERBOSE_LOGGING
        self._output_map = settings.OUTPUTS

        self._qc_api_service = QcApiService(base_url="http://192.168.88.97:8001")

        self._in_flight_objects: Deque[str] = deque()
        self._entry_timestamps: Dict[int, float] = {}
        self._stalled_product_timers: Dict[str, asyncio.TimerHandle] = {}
        
        self._base_travel_time_sec = 0.0
        if self._conveyor_config.SPEED_M_PER_SEC > 0:
            self._base_travel_time_sec = self._conveyor_config.CAMERA_TO_SORTER_DISTANCE_M / self._conveyor_config.SPEED_M_PER_SEC
        print(f"Detection Service: Calculated base travel time of {self._base_travel_time_sec:.2f} seconds.")

    def get_in_flight_count(self) -> int:
        return len(self._in_flight_objects)

    async def _check_sensor_block_time(self, event: SensorEvent):
        start_time = self._entry_timestamps.pop(event.sensor_id, None)
        if start_time is None: return
        block_duration_ms = (event.timestamp - start_time) * 1000
        active_profile = self._orchestration.get_active_profile()
        if not (active_profile and active_profile.product): return
        product = active_profile.product
        min_time, max_time = product.min_sensor_block_time_ms, product.max_sensor_block_time_ms
        if min_time is not None and max_time is not None and not (min_time <= block_duration_ms <= max_time):
            warning_msg = f"Product size mismatch! Blocked for {block_duration_ms:.0f}ms. Expected: {min_time}-{max_time}ms."
            await self._orchestration.trigger_persistent_alarm(warning_msg)

    async def _handle_stalled_product(self, serial_number: str):
        async with self._lock:
            self._stalled_product_timers.pop(serial_number, None)
            if serial_number in self._in_flight_objects:
                self._in_flight_objects.remove(serial_number)
                reason = f"Stalled product detected on conveyor (ID: {serial_number})"
                await self._orchestration.trigger_run_failure(reason)
    
    def _annotate_image_from_results(self, image_path: str, qc_results: Dict[str, Any]) -> str:
        try:
            image = cv2.imread(image_path)
            if image is None: return image_path

            original_path_obj = Path(image_path)
            annotated_dir = original_path_obj.parent / "annotated"
            annotated_dir.mkdir(exist_ok=True)

            id_results = qc_results.get("identification_results", {})
            has_drawn_anything = False

            def draw_bounding_box(box_data, label, color, thickness, label_inside=False):
                nonlocal has_drawn_anything
                if not box_data: return
                x, y, w, h = int(box_data.get("x", 0)), int(box_data.get("y", 0)), int(box_data.get("width", 0)), int(box_data.get("height", 0))
                
                cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
                has_drawn_anything = True

                font_scale, font_thickness = 1.0, 2
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                
                if label_inside:
                    text_y = y + text_h + 10
                    cv2.rectangle(image, (x, y), (x + text_w + 10, text_y + 10), color, -1)
                    cv2.putText(image, label, (x + 5, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
                else:
                    text_y, bg_y = y - 10, y - text_h - 20
                    cv2.rectangle(image, (x, bg_y), (x + text_w + 10, text_y + 10), color, -1)
                    cv2.putText(image, label, (x + 5, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

            qc_check = id_results.get("qc")
            if qc_check and qc_check.get("overall_status"):
                color = (0, 255, 0) if qc_check['overall_status'] == "ACCEPT" else (0, 0, 255)
                draw_bounding_box(qc_check.get("bounding_box"), f"Status: {qc_check['overall_status']}", color, 10, label_inside=True)

            category_check = id_results.get("category")
            if category_check and category_check.get("detected_product_type"):
                label = f"Type: {category_check['detected_product_type']} ({category_check.get('confidence', 0):.2f})"
                draw_bounding_box(category_check.get("bounding_box"), label, (255, 0, 0), 5)

            defects = id_results.get("defects", {}).get("defects", [])
            for defect in defects:
                label = f"Defect: {defect.get('defect_type', 'N/A')} ({defect.get('confidence', 0):.2f})"
                draw_bounding_box(defect.get("bounding_box"), label, (0, 255, 255), 3)

            if not has_drawn_anything:
                cv2.putText(image, "NO DETECTIONS", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            save_path = str(annotated_dir / original_path_obj.name)
            cv2.imwrite(save_path, image)
            return f"/captures/{original_path_obj.parts[-2]}/annotated/{original_path_obj.name}"
        except Exception as e:
            print(f"FATAL ERROR during image annotation: {e}")
            return image_path

    async def _run_qc_and_update_db(self, detection_log_id: int, serial_number: str, image_path: str):
        active_profile = self._orchestration.get_active_profile()
        product = active_profile.product if active_profile else None
        
        checks = ['qc']
        if product:
            if product.verify_category: checks.append("product_category")
            if product.verify_size: checks.append("size")
            if product.verify_defects: checks.append("defects")
            if product.verify_ticks: checks.append("ticks")

        full_image_path = str(Path(settings.CAMERA_CAPTURES_DIR).parent.parent / image_path.lstrip('/'))
        qc_results = await self._qc_api_service.perform_inspection(image_path=full_image_path, serial_number=serial_number, checks=checks)
        
        annotated_path = image_path 
        if qc_results:
            annotated_path = self._annotate_image_from_results(full_image_path, qc_results)
            
        try:
            async with self._get_db_session() as session:
                log_entry = await session.get(DetectionEventLog, detection_log_id)
                if log_entry:
                    # --- THIS IS THE DEFINITIVE FIX ---
                    # Always save the 'annotated_path' that was returned from the annotation function.
                    # The flawed conditional logic has been removed.
                    log_entry.annotated_image_path = annotated_path
                    log_entry.results = qc_results
                    await session.commit()
        except Exception as e:
            print(f"ERROR: Could not update DB with annotated path and results: {e}")
        
        broadcast_payload = json.dumps({
            "annotated_path": annotated_path,
            "original_path": image_path,
            "results": qc_results
        })
        await self._redis.publish("qc_annotated_image:new", broadcast_payload)

    async def handle_sensor_event(self, event: SensorEvent):
        async with self._lock:
            if self._orchestration.get_status()["mode"] not in [OperatingMode.RUNNING.value, OperatingMode.POST_RUN_DELAY.value]:
                if self._stalled_product_timers:
                    for timer in self._stalled_product_timers.values(): timer.cancel()
                    self._stalled_product_timers.clear()
                return

            if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL:
                if event.new_state == SensorState.TRIGGERED:
                    if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value: return
                    self._entry_timestamps[event.sensor_id] = event.timestamp
                    serial_number = str(uuid.uuid4())
                    self._in_flight_objects.append(serial_number)
                    timeout_sec = self._conveyor_config.MAX_TRANSIT_TIME_SEC
                    loop = asyncio.get_running_loop()
                    timer_handle = loop.call_later(timeout_sec, lambda: asyncio.create_task(self._handle_stalled_product(serial_number)))
                    self._stalled_product_timers[serial_number] = timer_handle
                    
                    if settings.CAMERA_TRIGGER_DELAY_MS > 0: await asyncio.sleep(settings.CAMERA_TRIGGER_DELAY_MS / 1000.0)
                    
                    image_path = None
                    if self._active_camera_ids:
                        image_path = await self._camera_manager.capture_and_save_image(self._active_camera_ids[0], f'event_{serial_number}')
                    
                    active_run_id = self._orchestration.get_active_run_id()
                    if active_run_id:
                        detection_log_id = None
                        try:
                            async with self._get_db_session() as session:
                                new_event = DetectionEventLog(run_log_id=active_run_id, image_path=image_path, serial_number=serial_number)
                                session.add(new_event)
                                await session.commit()
                                await session.refresh(new_event)
                                detection_log_id = new_event.id
                        except Exception as e:
                            print(f"ERROR: Could not log detection event to database: {e}")
                        if detection_log_id and image_path:
                            asyncio.create_task(self._run_qc_and_update_db(detection_log_id, serial_number, image_path))
                
                elif event.new_state == SensorState.CLEARED:
                    await self._check_sensor_block_time(event)

            elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                if self._in_flight_objects:
                    exiting_serial_number = self._in_flight_objects.popleft()
                    timer_to_cancel = self._stalled_product_timers.pop(exiting_serial_number, None)
                    if timer_to_cancel: timer_to_cancel.cancel()
                    await self._orchestration.on_exit_sensor_triggered()
                    await self._orchestration.on_box_processed()