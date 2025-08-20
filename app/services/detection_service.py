# rpi_counter_fastapi-apintrigation/app/services/detection_service.py

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
from app.services.audio_service import AsyncAudioService

PROJECT_ROOT = Path(__file__).parent.parent.parent

class QcApiService:
    """A client to interact with the external YOLOv11 OBB AI API System."""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=20.0)

    async def predict(
        self, image_path: str, serial_number: str, model_id: str
    ) -> Optional[Dict[str, Any]]:
        url = "/predict"
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
                files = {"image": (Path(image_path).name, image_bytes, "image/jpeg")}
                data = {"model_id": model_id, "serial_no": serial_number}
                
                print(f"AI API Request: Uploading {Path(image_path).name} for model: {model_id}")
                response = await self.client.post(url, files=files, data=data)
                response.raise_for_status()
                print(f"AI API Response for {model_id}: Success")
                return response.json()
        except FileNotFoundError:
            print(f"FATAL FILE ERROR: The image file was not found at the path: {image_path}. Cannot send to AI.")
            return None
        except httpx.RequestError as e:
            print(f"FATAL ERROR: Could not connect to AI API at {e.request.url}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"FATAL ERROR: AI API returned status {e.response.status_code} for model {model_id}. Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"FATAL ERROR: An unexpected error occurred during AI API call for model {model_id}: {e}")
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
        active_camera_ids: List[str],
        audio_service: AsyncAudioService
    ):
        self._io = modbus_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._redis = redis_client
        self._conveyor_config = conveyor_settings
        self._get_db_session = db_session_factory
        self._active_camera_ids = active_camera_ids
        self._audio_service = audio_service
        self._lock = asyncio.Lock()
        self._verbose = settings.LOGGING.VERBOSE_LOGGING
        self._output_map = settings.OUTPUTS
        self._qc_api_service = QcApiService(base_url=settings.AI_API.BASE_URL)
        self._in_flight_objects: Deque[str] = deque()
        self._entry_timestamps: Dict[int, float] = {}
        self._stalled_product_timers: Dict[str, asyncio.TimerHandle] = {}
        self._base_travel_time_sec = 0.0
        if self._conveyor_config.SPEED_M_PER_SEC > 0:
            self._base_travel_time_sec = self._conveyor_config.CAMERA_TO_SORTER_DISTANCE_M / self._conveyor_config.SPEED_M_PER_SEC
        print(f"Detection Service: Calculated base travel time of {self._base_travel_time_sec:.2f} seconds.")

    def get_in_flight_count(self) -> int:
        return len(self._in_flight_objects)

    # --- NEW METHOD TO BE CALLED BY SYSTEM SERVICE ---
    async def reset_state(self):
        """
        Clears all internal state of the detection service, including in-flight objects.
        """
        async with self._lock:
            self._in_flight_objects.clear()
            self._entry_timestamps.clear()
            
            # Cancel any pending stall timers to prevent them from firing later
            for timer in self._stalled_product_timers.values():
                timer.cancel()
            self._stalled_product_timers.clear()
            
            print("Detection Service: Internal state has been fully reset.")
    # --- END OF NEW METHOD ---

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
    
    def _annotate_image_from_results(self, image_path: str, combined_results: Dict[str, Any]) -> str:
        try:
            image = cv2.imread(image_path)
            if image is None: return image_path

            original_path_obj = Path(image_path)
            annotated_dir = original_path_obj.parent / "annotated"
            annotated_dir.mkdir(exist_ok=True)

            def draw_obb(points_flat, color, thickness, label=""):
                if not points_flat or len(points_flat) != 8: return
                points = np.array(points_flat, np.int32).reshape((-1, 1, 2))
                cv2.polylines(image, [points], isClosed=True, color=color, thickness=thickness)
                if label:
                    label_pos = (points[0][0][0], points[0][0][1] - 10)
                    cv2.putText(image, label, label_pos, cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)

            category_summary = combined_results.get("category_summary", {})
            if category_summary.get("obb_points"):
                label = f"{category_summary.get('detected_type', 'N/A')}"
                draw_obb(category_summary["obb_points"], (255, 191, 0), 5, label)
            
            qc_summary = combined_results.get("qc_summary", {})
            if qc_summary.get("obb_points"):
                status = qc_summary.get("overall_status", "UNKNOWN")
                color = (0, 255, 0) if status == "ACCEPT" else (0, 0, 255)
                label = f"QC: {status}"
                draw_obb(qc_summary["obb_points"], color, 8, label)

            save_path = str(annotated_dir / original_path_obj.name)
            cv2.imwrite(save_path, image)
            return f"/captures/{original_path_obj.parts[-2]}/annotated/{original_path_obj.name}"
        except Exception as e:
            print(f"FATAL ERROR during image annotation: {e}")
            return image_path

    async def _run_qc_and_update_db(self, detection_log_id: int, serial_number: str, image_path: str):
        active_profile = self._orchestration.get_active_profile()
        product = active_profile.product if active_profile else None
        
        models_to_run = []
        if product:
            if product.verify_category: models_to_run.append(settings.AI_API.CATEGORY_MODEL_ID)
            if any([product.verify_category, product.verify_size, product.verify_defects, product.verify_ticks]):
                if settings.AI_API.QC_MODEL_ID not in models_to_run:
                    models_to_run.append(settings.AI_API.QC_MODEL_ID)

        if not models_to_run:
            print("No AI checks enabled for this product. Skipping AI analysis.")
            return

        full_image_path = str(PROJECT_ROOT / "web" / "static" / Path(image_path).relative_to('/'))
        
        tasks = [self._qc_api_service.predict(full_image_path, serial_number, model_id) for model_id in models_to_run]
        api_responses = await asyncio.gather(*tasks)
        
        combined_results = {"raw_responses": {}}
        
        cat_model_id = settings.AI_API.CATEGORY_MODEL_ID
        cat_index = models_to_run.index(cat_model_id) if cat_model_id in models_to_run else -1
        if cat_index != -1 and api_responses[cat_index] and api_responses[cat_index].get("detections"):
            detection = api_responses[cat_index]["detections"][0]
            combined_results["raw_responses"][cat_model_id] = api_responses[cat_index]
            combined_results["category_summary"] = {
                "detected_type": detection["class_name"], "confidence": detection["confidence"],
                "angle_degrees": detection["coordinates"]["rotated_box"]["angle_degrees"],
                "obb_points": detection["coordinates"]["obb_points"],
                "rotated_box": detection["coordinates"]["rotated_box"]
            }
            await self._audio_service.play_sound_for_event(detection["class_name"])

        qc_model_id = settings.AI_API.QC_MODEL_ID
        qc_index = models_to_run.index(qc_model_id) if qc_model_id in models_to_run else -1
        if qc_index != -1 and api_responses[qc_index] and api_responses[qc_index].get("detections"):
            detection = api_responses[qc_index]["detections"][0]
            combined_results["raw_responses"][qc_model_id] = api_responses[qc_index]
            combined_results["qc_summary"] = {
                "overall_status": detection["class_name"], "confidence": detection["confidence"],
                "angle_degrees": detection["coordinates"]["rotated_box"]["angle_degrees"],
                "obb_points": detection["coordinates"]["obb_points"]
            }
            await self._audio_service.play_sound_for_event(detection["class_name"])

        validation_results = {"checks": []}
        final_qc_status = combined_results.get("qc_summary", {}).get("overall_status", "PENDING")

        if product and "category_summary" in combined_results:
            cat_sum = combined_results["category_summary"]
            
            if product.target_angle is not None and product.angle_tolerance is not None:
                angle = cat_sum["angle_degrees"]
                is_pass = abs(angle - product.target_angle) <= product.angle_tolerance
                validation_results["checks"].append({
                    "check_type": "Angle", "status": "PASS" if is_pass else "FAIL",
                    "value": f"{angle:.2f}°", "expected": f"{product.target_angle}° ± {product.angle_tolerance}°"
                })
                if not is_pass: final_qc_status = "REJECT"

            if product.min_aspect_ratio is not None and product.max_aspect_ratio is not None:
                w = cat_sum["rotated_box"]["width"]
                h = cat_sum["rotated_box"]["height"]
                aspect_ratio = w / h if h > 0 else 0
                is_pass = product.min_aspect_ratio <= aspect_ratio <= product.max_aspect_ratio
                validation_results["checks"].append({
                    "check_type": "Aspect Ratio", "status": "PASS" if is_pass else "FAIL",
                    "value": f"{aspect_ratio:.2f}", "expected": f"{product.min_aspect_ratio} - {product.max_aspect_ratio}"
                })
                if not is_pass: final_qc_status = "REJECT"

        combined_results["validation_results"] = validation_results
        if "qc_summary" in combined_results:
            combined_results["qc_summary"]["overall_status"] = final_qc_status

        annotated_path = self._annotate_image_from_results(full_image_path, combined_results)
            
        try:
            async with self._get_db_session() as session:
                log_entry = await session.get(DetectionEventLog, detection_log_id)
                if log_entry:
                    log_entry.annotated_image_path = annotated_path
                    log_entry.details = combined_results
                    await session.commit()
        except Exception as e:
            print(f"ERROR: Could not update DB with annotated path and results: {e}")
        
        broadcast_payload = json.dumps({
            "annotated_path": annotated_path, "original_path": image_path,
            "results": combined_results
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
                    if active_run_id and image_path:
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
                        if detection_log_id:
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