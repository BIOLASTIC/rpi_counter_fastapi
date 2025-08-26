import asyncio
import uuid
import json
from collections import deque
from typing import Dict, Deque, List, Optional, Any, TYPE_CHECKING
import httpx
import cv2
import numpy as np
from pathlib import Path
import redis.asyncio as redis
from sqlalchemy.orm.attributes import flag_modified

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.models.detection import DetectionEventLog
from config import settings
from app.services.audio_service import AsyncAudioService
from app.services.llm_service import LlmApiService

# --- FIX: Use TYPE_CHECKING to prevent circular import at runtime ---
if TYPE_CHECKING:
    from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode

PROJECT_ROOT = Path(__file__).parent.parent.parent

class QcApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=20.0)

    async def predict(self, model_id: str, serial_number: str, image_bytes: bytes) -> Optional[Dict[str, Any]]:
        try:
            files = {"image": ("capture.jpg", image_bytes, "image/jpeg")}
            data = {"model_id": model_id, "serial_no": serial_number}
            response = await self.client.post("/predict", files=files, data=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"ERROR during AI API call for {model_id}: {e}")
            return None

class AsyncDetectionService:
    def __init__(self, modbus_controller: AsyncModbusController, camera_manager: AsyncCameraManager, orchestration_service: "AsyncOrchestrationService", redis_client: redis.Redis, conveyor_settings, db_session_factory, active_camera_ids: List[str], audio_service: AsyncAudioService, llm_service: LlmApiService):
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._redis = redis_client
        self._conveyor_config = conveyor_settings
        self._get_db_session = db_session_factory
        self._active_camera_ids = active_camera_ids
        self._audio_service = audio_service
        self._llm_service = llm_service
        self._qc_api_service = QcApiService(base_url=settings.AI_API.BASE_URL)
        self._in_flight_objects: Deque[str] = deque()
        self._stalled_product_timers: Dict[str, asyncio.TimerHandle] = {}
        self._entry_sensor_is_blocked = False

    def get_in_flight_count(self) -> int:
        return len(self._in_flight_objects)

    async def reset_state(self):
        self._in_flight_objects.clear()
        for timer in self._stalled_product_timers.values(): timer.cancel()
        self._stalled_product_timers.clear()
        self._entry_sensor_is_blocked = False

    async def _handle_stalled_product(self, serial_number: str):
        self._stalled_product_timers.pop(serial_number, None)
        if serial_number in self._in_flight_objects:
            self._in_flight_objects.remove(serial_number)
            await self._orchestration.trigger_run_failure(f"Stalled product detected: {serial_number}")
    
    def _annotate_image_from_results(self, image_path: str, api_responses: List[Optional[Dict[str, Any]]]) -> str:
        try:
            if not Path(image_path).exists():
                print(f"ANNOTATION ERROR: Source image file not found at {image_path}")
                return image_path
            image = cv2.imread(image_path)
            if image is None: return image_path
            
            original_path = Path(image_path)
            annotated_dir = original_path.parent / "annotated"
            annotated_dir.mkdir(parents=True, exist_ok=True)

            for api_response in api_responses:
                if api_response is None: continue
                detections = api_response.get("detections", [])
                for detection in detections:
                    box_points = detection.get("coordinates", {}).get("obb_points", [])
                    if box_points and len(box_points) == 8:
                        contour = np.array(box_points, dtype=np.int32).reshape(4, 2)
                        cv2.polylines(image, [contour], True, (36, 255, 12), 2)
                        label = f"{detection.get('class_name', 'N/A')} ({detection.get('confidence', 0):.2f})"
                        cv2.putText(image, label, (contour[0][0], contour[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

            save_path = str(annotated_dir / original_path.name)
            cv2.imwrite(save_path, image)
            relative_path = Path(save_path).relative_to(PROJECT_ROOT / "web")
            return f"/{relative_path.as_posix()}"
        except Exception as e:
            print(f"FATAL ERROR during image annotation: {e}")
            return image_path

    def _combine_api_responses(self, api_responses: List[Optional[Dict[str, Any]]]) -> Dict[str, Any]:
        combined_summary = {
            "overall_status": "REJECT", "reject_reason": "Analysis failed or no objects detected.",
            "qc_details": None, "category_details": None, "llm_summary": None, "all_detections": []
        }
        
        qc_response = next((r for r in api_responses if r and 'yolo11m_qc' in r.get('model_id', '')), None)
        category_response = next((r for r in api_responses if r and 'yolo11m_categories' in r.get('model_id', '')), None)
        llm_response = next((r for r in api_responses if r and 'analysis' in r), None)

        if qc_response and qc_response.get("detections"):
            qc_detections = sorted(qc_response.get("detections", []), key=lambda d: d.get('confidence', 0), reverse=True)
            primary_qc = qc_detections[0]
            combined_summary["qc_details"] = {"type": primary_qc.get("class_name", "Unknown"), "confidence": round(primary_qc.get("confidence", 0), 4)}
            if "ACCEPT" in primary_qc.get("class_name", ""):
                combined_summary["overall_status"] = "ACCEPT"; combined_summary["reject_reason"] = None
            else:
                combined_summary["overall_status"] = "REJECT"; combined_summary["reject_reason"] = primary_qc.get("class_name", "Unknown Defect")
            combined_summary["all_detections"].extend(qc_response["detections"])

        if category_response and category_response.get("detections"):
            cat_detections = sorted(category_response.get("detections", []), key=lambda d: d.get('confidence', 0), reverse=True)
            primary_cat = cat_detections[0]
            combined_summary["category_details"] = {"type": primary_cat.get("class_name", "Unknown"), "confidence": round(primary_cat.get("confidence", 0), 4)}
            combined_summary["all_detections"].extend(category_response["detections"])
            
        if llm_response:
            combined_summary["llm_summary"] = llm_response.get('analysis', {}).get('plain_text_summary')

        return combined_summary

    async def _run_qc_and_update_db(self, detection_log_id: int, serial_number: str, web_image_path: str, full_image_path: str, image_bytes: bytes):
        if not await self._audio_service._get_config("YOLO_ENABLED", settings.AI_STRATEGY.YOLO_ENABLED): return

        tasks = [
            self._qc_api_service.predict(model_id, serial_number, image_bytes)
            for model_id in settings.AI_API.QC_MODEL_IDS
        ]
        api_responses = await asyncio.gather(*tasks)
        
        yolo_results_for_llm = self._combine_api_responses(api_responses)
        
        if await self._audio_service._get_config("LLM_ITEM_ANALYSIS_ENABLED", settings.AI_STRATEGY.LLM_ITEM_ANALYSIS_ENABLED):
            llm_payload = {"qc_summary": yolo_results_for_llm}
            llm_response = await self._llm_service.analyze_item(
                item_data=llm_payload,
                language=await self._audio_service._get_config("LANGUAGE", settings.AI_STRATEGY.LANGUAGE),
                word_count=await self._audio_service._get_config("LLM_ITEM_WORD_COUNT", settings.AI_STRATEGY.LLM_ITEM_WORD_COUNT)
            )
            if llm_response: api_responses.append(llm_response)

        analysis_summary = self._combine_api_responses(api_responses)
        
        await self._orchestration.on_item_inspected(
            qc_status=analysis_summary["overall_status"],
            defects=analysis_summary["reject_reason"],
            type=analysis_summary.get("category_details", {}).get("type", "Unknown"),
            count=self._orchestration.get_status().get('run_progress', 0)
        )
        
        annotated_path = self._annotate_image_from_results(full_image_path, api_responses)
        
        async with self._get_db_session() as session:
            log_entry = await session.get(DetectionEventLog, detection_log_id)
            if log_entry:
                log_entry.annotated_image_path = annotated_path
                log_entry.details = analysis_summary
                flag_modified(log_entry, "details")
                await session.commit()
        
        await self._redis.publish("qc_annotated_image:new", json.dumps({
            "annotated_path": annotated_path, "results": analysis_summary
        }))

    async def handle_sensor_event(self, event: SensorEvent):
        from app.services.orchestration_service import OperatingMode
        
        if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value: return

        if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL:
            if event.new_state == SensorState.TRIGGERED and not self._entry_sensor_is_blocked:
                self._entry_sensor_is_blocked = True
                serial_number = str(uuid.uuid4())
                self._in_flight_objects.append(serial_number)
                
                loop = asyncio.get_running_loop()
                timer = loop.call_later(self._conveyor_config.MAX_TRANSIT_TIME_SEC, 
                                        lambda: asyncio.create_task(self._handle_stalled_product(serial_number)))
                self._stalled_product_timers[serial_number] = timer
                
                await self._orchestration.on_item_entered(serial_number)
                
                if settings.CAMERA_TRIGGER_DELAY_MS > 0: await asyncio.sleep(settings.CAMERA_TRIGGER_DELAY_MS / 1000.0)
                
                web_path, full_path, image_bytes = await self._camera_manager.capture_and_save_image(self._active_camera_ids[0], f'event_{serial_number}')
                
                active_run_id = self._orchestration.get_active_run_id()
                if active_run_id and web_path and full_path and image_bytes:
                    async with self._get_db_session() as session:
                        new_event = DetectionEventLog(run_log_id=active_run_id, image_path=web_path, serial_number=serial_number)
                        session.add(new_event); await session.commit(); await session.refresh(new_event)
                        asyncio.create_task(self._run_qc_and_update_db(new_event.id, serial_number, web_path, full_path, image_bytes))

            elif event.new_state == SensorState.CLEARED:
                self._entry_sensor_is_blocked = False

        elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
            if self._in_flight_objects:
                serial = self._in_flight_objects.popleft()
                if serial in self._stalled_product_timers:
                    self._stalled_product_timers.pop(serial).cancel()
                await self._orchestration.on_item_processed()