import asyncio
import json
from enum import Enum
from typing import Optional, Any, Dict, TYPE_CHECKING
import time
from datetime import datetime

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.modbus_controller import AsyncModbusController
from app.models.profiles import ObjectProfile
from app.models.run_log import RunLog, RunStatus
from app.models.operator import Operator
from app.models.detection import DetectionEventLog
from config import ACTIVE_CAMERA_IDS, settings
from app.services.audio_service import AsyncAudioService
from app.services.llm_service import LlmApiService
from app.websocket.connection_manager import manager as websocket_manager

if TYPE_CHECKING:
    from app.services.detection_service import AsyncDetectionService

class OperatingMode(str, Enum):
    STOPPED = "Stopped"
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED_BETWEEN_BATCHES = "Paused (Between Batches)"
    POST_RUN_DELAY = "Post-Run Delay"

def _get_summary_from_llm_response(llm_response: Dict[str, Any]) -> str | None:
    try:
        return llm_response['analysis']['plain_text_summary']
    except (KeyError, TypeError):
        return None

class AsyncOrchestrationService:
    def __init__(self, modbus_controller: AsyncModbusController, db_session_factory, redis_client: redis.Redis, app_settings, audio_service: AsyncAudioService, llm_service: LlmApiService):
        self._io = modbus_controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._settings = app_settings
        self._audio_service = audio_service
        self._llm_service = llm_service
        self._mode = OperatingMode.STOPPED
        self._lock = asyncio.Lock()
        self._active_profile: Optional[ObjectProfile] = None
        self._active_run_id: Optional[int] = None
        self._active_alarm_message: Optional[str] = None
        self._run_profile_id: Optional[int] = None
        self._run_batch_code: Optional[str] = None
        self._run_operator_name: Optional[str] = None
        self._run_operator_id: Optional[int] = None
        self._run_product_name: Optional[str] = None
        self._run_target_count: int = 0
        self._run_post_batch_delay_sec: int = 5
        self._current_count: int = 0
        self._output_map = self._settings.OUTPUTS
        self._completion_task: Optional[asyncio.Task] = None
        self._detection_service: Optional["AsyncDetectionService"] = None
        self._buzzer_queue = asyncio.Queue()
        self._buzzer_task: Optional[asyncio.Task] = None

    def set_detection_service(self, detection_service: "AsyncDetectionService"):
        self._detection_service = detection_service

    def beep_for(self, duration_ms: int):
        if duration_ms > 0:
            try: self._buzzer_queue.put_nowait(duration_ms)
            except asyncio.QueueFull: print("Buzzer queue is full.")

    async def _buzzer_manager(self):
        buzzer_off_time = 0.0
        is_buzzer_on = False
        while True:
            try:
                try:
                    duration_ms = await asyncio.wait_for(self._buzzer_queue.get(), timeout=0.05)
                    new_off_time = time.monotonic() + (duration_ms / 1000.0)
                    if new_off_time > buzzer_off_time: buzzer_off_time = new_off_time
                except asyncio.TimeoutError: pass
                current_time = time.monotonic()
                if current_time < buzzer_off_time:
                    if not is_buzzer_on: await self._io.write_coil(self._output_map.BUZZER, True); is_buzzer_on = True
                else:
                    if is_buzzer_on: await self._io.write_coil(self._output_map.BUZZER, False); is_buzzer_on = False
            except asyncio.CancelledError:
                if is_buzzer_on: await self._io.write_coil(self._output_map.BUZZER, False)
                break
            except Exception as e: print(f"Error in buzzer manager: {e}")

    def start_background_tasks(self):
        if self._buzzer_task is None or self._buzzer_task.done():
            self._buzzer_task = asyncio.create_task(self._buzzer_manager())

    def stop_background_tasks(self):
        if self._buzzer_task and not self._buzzer_task.done(): self._buzzer_task.cancel()
        if self._completion_task and not self._completion_task.done(): self._completion_task.cancel()

    async def initialize_hardware_state(self):
        await asyncio.gather(
            self._io.write_coil(self._output_map.CONVEYOR, False),
            self._io.write_coil(self._output_map.LED_GREEN, False),
            self._io.write_coil(self._output_map.LED_RED, True)
        )

    def get_active_run_id(self) -> Optional[int]: return self._active_run_id
    
    async def on_item_entered(self, serial_number: str):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            await websocket_manager.broadcast_json({"type": "new_item_entered", "data": {"serial_number": serial_number}})

    async def on_item_processed(self):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            self.beep_for(self._settings.BUZZER.EXIT_SENSOR_MS)
            self._current_count += 1
            await websocket_manager.broadcast_json({"type": "item_processed", "data": {"processed_count": self._current_count}})
            if self._run_target_count > 0 and self._current_count >= self._run_target_count:
                if self._completion_task is None or self._completion_task.done():
                    self._completion_task = asyncio.create_task(self._complete_and_loop_run_task())

    async def on_item_inspected(self, qc_status: str, **kwargs):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            audio_context = {
                "batch_id": self._run_batch_code, "product_name": self._run_product_name,
                "total_items": self._current_count, "reject_count": 0,
                **kwargs
            }
            if "ACCEPT" in qc_status.upper():
                if await self._audio_service._get_config("ALERT_ON_PASS", settings.AI_STRATEGY.ALERT_ON_PASS):
                    await self._audio_service.play_realtime_alert("PASS_TEMPLATE", **audio_context)
            else:
                if await self._audio_service._get_config("ALERT_ON_REJECT", settings.AI_STRATEGY.ALERT_ON_REJECT):
                    await self._audio_service.play_realtime_alert("REJECT_TEMPLATE", **audio_context)

    async def _trigger_persistent_alarm_nolock(self, message: str):
        if self._active_alarm_message: return
        self._active_alarm_message = message
        print(f"ORCHESTRATION ALARM: {message}")

    async def trigger_persistent_alarm(self, message: str):
        async with self._lock:
            await self._trigger_persistent_alarm_nolock(message)

    async def _acknowledge_alarm_nolock(self):
        if not self._active_alarm_message: return
        self._active_alarm_message = None
        print("Alarm acknowledged by user.")
    
    async def acknowledge_alarm(self):
        async with self._lock:
            await self._acknowledge_alarm_nolock()

    async def trigger_run_failure(self, reason: str):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            print(f"CRITICAL RUN FAILURE: {reason}.")
            await self._audio_service.play_event_from_cache("product_stalled")
            await self._update_run_log_status(RunStatus.FAILED)
            self._mode = OperatingMode.STOPPED
            await self.initialize_hardware_state()
            if self._detection_service: await self._detection_service.reset_state()
            self._active_profile, self._active_run_id = None, None
            await self._trigger_persistent_alarm_nolock(f"Run Failed: {reason}")
    
    async def start_run(self, profile_id: int, target_count: int, post_batch_delay_sec: int, batch_code: str, operator_id: int) -> bool:
        async with self._lock:
            if self._mode in [OperatingMode.RUNNING, OperatingMode.POST_RUN_DELAY]: return False
            if self._completion_task and not self._completion_task.done():
                self._completion_task.cancel()
            async with self._get_db_session() as session:
                operator = await session.get(Operator, operator_id)
                if not operator: return False
                self._run_operator_name = operator.name
            self._run_profile_id, self._run_target_count, self._run_post_batch_delay_sec, self._run_batch_code, self._run_operator_id = \
                profile_id, target_count, post_batch_delay_sec, batch_code, operator_id
            return await self._execute_start_sequence()
            
    async def _execute_start_sequence(self) -> bool:
        async with self._get_db_session() as session:
            result = await session.execute(select(ObjectProfile).options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product)).where(ObjectProfile.id == self._run_profile_id))
            profile = result.scalar_one_or_none()
        
        if not profile or not profile.camera_profile:
             await self._trigger_persistent_alarm_nolock("Failed to start: Recipe has no camera profile.")
             return False
        if not profile.product:
             await self._trigger_persistent_alarm_nolock("Failed to start: Recipe is not linked to a Product.")
             return False
        
        self._run_product_name = profile.product.name
        
        try:
            async with self._get_db_session() as session:
                new_run_log = RunLog(batch_code=self._run_batch_code, operator_id=self._run_operator_id, product_id=profile.product_id, status=RunStatus.RUNNING)
                session.add(new_run_log); await session.commit(); await session.refresh(new_run_log)
                self._active_run_id = new_run_log.id
        except Exception as e: 
            print(f"FATAL: Could not create RunLog due to database error: {e}"); 
            return False
        
        self._active_profile = profile
        await self._acknowledge_alarm_nolock()
        
        cam_settings = profile.camera_profile
        settings_payload = {"autofocus": cam_settings.autofocus, "exposure": cam_settings.exposure, "gain": cam_settings.gain, "white_balance_temp": cam_settings.white_balance_temp, "brightness": cam_settings.brightness}
        command = {"action": "apply_settings", "settings": settings_payload}
        for cam_id in ACTIVE_CAMERA_IDS:
            await self._redis.publish(f"camera:commands:{cam_id}", json.dumps(command))
        
        self._current_count = 0
        self._mode = OperatingMode.RUNNING
        await self._io.write_coil(self._output_map.LED_RED, False)
        await self._io.write_coil(self._output_map.LED_GREEN, True)
        await self._io.write_coil(self._output_map.CONVEYOR, True)
        return True

    async def _update_run_log_status(self, status: RunStatus):
        if not self._active_run_id: return
        try:
            async with self._get_db_session() as session:
                run_log = await session.get(RunLog, self._active_run_id)
                if run_log: run_log.status, run_log.end_timestamp = status, datetime.utcnow(); await session.commit()
        except Exception as e: print(f"Error updating RunLog status: {e}")

    async def _generate_and_play_summary(self):
        if not self._active_run_id: return
        llm_language = await self._audio_service._get_config("LANGUAGE", settings.AI_STRATEGY.LANGUAGE)
        word_count = await self._audio_service._get_config("LLM_SUMMARY_WORD_COUNT", settings.AI_STRATEGY.LLM_SUMMARY_WORD_COUNT)
        model_pref = await self._audio_service._get_config("SUMMARY_LLM_MODEL", settings.AI_STRATEGY.SUMMARY_LLM_MODEL)
        async with self._get_db_session() as session:
            result = await session.execute(select(DetectionEventLog).where(DetectionEventLog.run_log_id == self._active_run_id))
            run_data = [{"qc_summary": det.details} for det in result.scalars().all() if det.details]
        
        if not run_data: return
        llm_response = await self._llm_service.summarize_batch(batch_data=run_data, language=llm_language, word_count=word_count, model_preference=model_pref)
        summary_text = _get_summary_from_llm_response(llm_response)
        if summary_text: await self._audio_service.play_pipelined_summary(summary_text)

    async def _complete_and_loop_run_task(self):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            print("Orchestration: Target count reached. Entering post-run delay.")
            self._mode = OperatingMode.POST_RUN_DELAY
            await self._update_run_log_status(RunStatus.COMPLETED)
            
            reject_count = 0
            async with self._get_db_session() as session:
                result = await session.execute(select(DetectionEventLog).where(DetectionEventLog.run_log_id == self._active_run_id))
                reject_count = sum(1 for det in result.scalars().all() if det.details and "REJECT" in det.details.get("overall_status", ""))

            audio_context = {
                "batch_id": self._run_batch_code,
                "product_name": self._run_product_name,
                "total_items": self._current_count,
                "reject_count": reject_count
            }
            await self._audio_service.play_realtime_alert("BATCH_COMPLETE_TEMPLATE", **audio_context)

        await asyncio.sleep(self._settings.CONVEYOR.CONVEYOR_AUTO_STOP_DELAY_SEC)

        async with self._lock:
            if self._mode != OperatingMode.POST_RUN_DELAY: return
            print("Orchestration: Post-run delay finished. Stopping conveyor and starting batch pause.")
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            if self._detection_service: await self._detection_service.reset_state()
            if await self._audio_service._get_config("LLM_ENABLED", settings.AI_STRATEGY.LLM_ENABLED):
                asyncio.create_task(self._generate_and_play_summary())
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES

        print(f"Orchestration: Pausing for {self._run_post_batch_delay_sec} seconds before next run.")
        await asyncio.sleep(self._run_post_batch_delay_sec)

        async with self._lock:
            if self._mode != OperatingMode.PAUSED_BETWEEN_BATCHES: return
            print("Orchestration: Pause finished. Attempting to start next run.")
            for i in range(3, 0, -1):
                await self._audio_service.play_realtime_alert("NEXT_BATCH_TEMPLATE", countdown=i)
                await asyncio.sleep(1)
            if not await self._execute_start_sequence():
                print("Orchestration ERROR: Failed to automatically start the next run. Stopping.")
                await self.stop_run()

    async def stop_run(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED: return
            print(f"Orchestration: Stop command received. Current mode: {self._mode.value}")
            current_mode = self._mode
            if self._completion_task and not self._completion_task.done():
                self._completion_task.cancel()
            
            if self._active_run_id and current_mode == OperatingMode.RUNNING:
                await self._update_run_log_status(RunStatus.ABORTED)
            
            self._mode = OperatingMode.STOPPED
            self._active_profile = None; self._active_run_id = None; self._current_count = 0
            self._run_product_name = None
            self._run_operator_name = None
            self._run_batch_code = None
            
            await self.initialize_hardware_state()
            if self._detection_service: await self._detection_service.reset_state()
            print("Orchestration: System stopped and reset.")

    def get_status(self) -> dict:
        return {
            "mode": self._mode.value,
            "active_profile": self._active_profile.name if self._active_profile else "None",
            "operator_name": self._run_operator_name,
            "batch_code": self._run_batch_code,
            "run_progress": self._current_count,
            "target_count": self._run_target_count,
            "active_alarm_message": self._active_alarm_message,
        }