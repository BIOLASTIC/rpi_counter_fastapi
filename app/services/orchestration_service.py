# rpi_counter_fastapi-dev2/app/services/orchestration_service.py

"""
Service for controlling the high-level orchestration of production runs.
"""
import asyncio
import json
from enum import Enum
from typing import Optional, Any, Dict
from datetime import datetime
import time # NEW: Import time for monotonic clock

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.modbus_controller import AsyncModbusController
from app.models.profiles import ObjectProfile, Product
from app.models.run_log import RunLog, RunStatus
from app.models.event_log import EventLog, EventType
from app.models.operator import Operator
from config import ACTIVE_CAMERA_IDS, settings
from config.settings import AppSettings


class OperatingMode(str, Enum):
    STOPPED = "Stopped"
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED_BETWEEN_BATCHES = "Paused (Between Batches)"
    POST_RUN_DELAY = "Post-Run Delay"

class AsyncOrchestrationService:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        db_session_factory,
        redis_client: redis.Redis,
        app_settings: AppSettings
    ):
        self._io = modbus_controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._settings = app_settings
        self._mode = OperatingMode.STOPPED
        self._lock = asyncio.Lock()
        
        self._active_profile: Optional[ObjectProfile] = None
        self._active_product: Optional[Product] = None
        self._active_run_id: Optional[int] = None
        self._active_alarm_message: Optional[str] = None

        self._run_profile_id: Optional[int] = None
        self._run_batch_code: Optional[str] = None
        self._run_operator_id: Optional[int] = None
        self._run_operator_name: Optional[str] = None
        self._run_target_count: int = 0
        self._run_post_batch_delay_sec: int = 5
        self._current_count: int = 0
        
        self._output_map = self._settings.OUTPUTS
        
        # --- NEW: Buzzer Manager state ---
        self._buzzer_queue = asyncio.Queue()
        self._buzzer_task: Optional[asyncio.Task] = None
        # --- END NEW ---

    # --- REMOVED: The old, flawed beep function is gone ---
    # async def _trigger_timed_beep(self, duration_sec: float): ...

    # --- MODIFIED: This function now queues a request instead of creating a task ---
    def beep_for(self, duration_ms: int):
        """Queues a non-blocking beep request for the buzzer manager."""
        if duration_ms > 0:
            try:
                self._buzzer_queue.put_nowait(duration_ms)
            except asyncio.QueueFull:
                print("Buzzer queue is full, dropping request.")

    # --- NEW: The robust Buzzer Manager task ---
    async def _buzzer_manager(self):
        """A single, long-running task to manage all buzzer requests."""
        buzzer_off_time = 0.0
        is_buzzer_on = False
        
        while True:
            try:
                # Wait for a new request, but with a timeout so we can check the state
                try:
                    duration_ms = await asyncio.wait_for(self._buzzer_queue.get(), timeout=0.05)
                    new_off_time = time.monotonic() + (duration_ms / 1000.0)
                    # If the new request is longer than the current one, extend the time
                    if new_off_time > buzzer_off_time:
                        buzzer_off_time = new_off_time
                    self._buzzer_queue.task_done()
                except asyncio.TimeoutError:
                    pass

                current_time = time.monotonic()
                
                # Check if the buzzer should be on
                if current_time < buzzer_off_time:
                    if not is_buzzer_on:
                        await self._io.write_coil(self._output_map.BUZZER, True)
                        is_buzzer_on = True
                # Check if the buzzer should be off
                else:
                    if is_buzzer_on:
                        await self._io.write_coil(self._output_map.BUZZER, False)
                        is_buzzer_on = False
                        buzzer_off_time = 0.0 # Reset time
            except asyncio.CancelledError:
                # Ensure buzzer is turned off on exit
                if is_buzzer_on:
                    await self._io.write_coil(self._output_map.BUZZER, False)
                break
            except Exception as e:
                print(f"Error in buzzer manager: {e}")
                await asyncio.sleep(1) # Prevent rapid-fire error loops

    # --- NEW: Methods to start and stop background tasks for this service ---
    def start_background_tasks(self):
        """Starts the background tasks managed by this service."""
        if self._buzzer_task is None or self._buzzer_task.done():
            self._buzzer_task = asyncio.create_task(self._buzzer_manager())
            print("Orchestration Service: Buzzer manager task started.")

    def stop_background_tasks(self):
        """Stops the background tasks managed by this service."""
        if self._buzzer_task and not self._buzzer_task.done():
            self._buzzer_task.cancel()
            print("Orchestration Service: Buzzer manager task stopped.")

    # ... (the rest of the file remains exactly the same as the previous version) ...
    async def initialize_hardware_state(self):
        await self._io.write_coil(self._output_map.GATE, False)
        await self._io.write_coil(self._output_map.DIVERTER, False)
        await self._io.write_coil(self._output_map.CONVEYOR, False)
        await self._io.write_coil(self._output_map.LED_GREEN, False)
        await self._io.write_coil(self._output_map.LED_RED, True)
        await self._io.write_coil(self._output_map.BUZZER, False)

    def get_active_profile(self) -> Optional[ObjectProfile]:
        return self._active_profile

    def get_active_run_id(self) -> Optional[int]:
        return self._active_run_id

    async def on_box_processed(self):
        task_to_run = None
        async with self._lock:
            if self._mode == OperatingMode.RUNNING:
                self._current_count += 1
                if self._run_target_count > 0 and self._current_count >= self._run_target_count:
                    task_to_run = asyncio.create_task(self.complete_and_loop_run())
        if task_to_run:
            await task_to_run

    async def on_exit_sensor_triggered(self):
        self.beep_for(self._settings.BUZZER.EXIT_SENSOR_MS)

    async def trigger_persistent_alarm(self, message: str):
        self.beep_for(self._settings.BUZZER.MISMATCH_MS)
        if self._active_alarm_message: return
        self._active_alarm_message = message
        try:
            async with self._get_db_session() as session:
                log_entry = EventLog(event_type=EventType.WARNING, source="ORCHESTRATION", message=message, details={"run_log_id": self._active_run_id, "batch_code": self._run_batch_code})
                session.add(log_entry)
                await session.commit()
        except Exception as e:
            print(f"Failed to log alarm to database: {e}")

    async def trigger_run_failure(self, reason: str):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            try:
                async with self._get_db_session() as session:
                    log_entry = EventLog(event_type=EventType.ERROR, source="SYSTEM_FAILURE", message=reason, details={"run_log_id": self._active_run_id, "batch_code": self._run_batch_code})
                    session.add(log_entry)
                    await session.commit()
            except Exception as e:
                print(f"Failed to log critical failure to database: {e}")
            await self._update_run_log_status(RunStatus.FAILED)
            self._mode = OperatingMode.STOPPED
            self._active_profile, self._active_product, self._active_run_id = None, None, None
            self._run_profile_id, self._current_count, self._run_target_count = None, 0, 0
            self._run_operator_name, self._run_batch_code = None, None
            await self.initialize_hardware_state()
            await self.trigger_persistent_alarm(f"CRITICAL FAILURE: {reason}")

    async def acknowledge_alarm(self):
        if not self._active_alarm_message: return
        self._active_alarm_message = None

    async def start_run(self, profile_id: int, target_count: int, post_batch_delay_sec: int, batch_code: str, operator_id: int) -> bool:
        async with self._lock:
            if self._mode in [OperatingMode.RUNNING, OperatingMode.PAUSED_BETWEEN_BATCHES, OperatingMode.POST_RUN_DELAY]:
                return False
            async with self._get_db_session() as session:
                operator = await session.get(Operator, operator_id)
                if not operator:
                    return False
                self._run_operator_name = operator.name
            self._run_profile_id, self._run_target_count, self._run_post_batch_delay_sec, self._run_batch_code, self._run_operator_id = \
                profile_id, target_count, post_batch_delay_sec, batch_code, operator_id
            return await self._execute_start_sequence()

    async def _execute_start_sequence(self) -> bool:
        async with self._get_db_session() as session:
            result = await session.execute(
                select(ObjectProfile).options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
                .where(ObjectProfile.id == self._run_profile_id)
            )
            profile = result.scalar_one_or_none()
        if not profile or not profile.camera_profile: return False
        try:
            async with self._get_db_session() as session:
                profile_snapshot = {
                    "object_profile_name": profile.name, 
                    "product_name": profile.product.name if profile.product else "N/A",
                    "target_count": self._run_target_count 
                }
                new_run_log = RunLog(
                    batch_code=self._run_batch_code, 
                    operator_id=self._run_operator_id, 
                    product_id=profile.product_id,
                    status=RunStatus.RUNNING, 
                    object_profile_snapshot=profile_snapshot
                )
                session.add(new_run_log); await session.commit(); await session.refresh(new_run_log)
                self._active_run_id = new_run_log.id
        except Exception as e:
            print(f"FATAL: Could not create RunLog in database. Aborting run. Error: {e}"); return False
            
        self._active_profile, self._active_product = profile, profile.product
        await self.acknowledge_alarm()
        self.beep_for(self._settings.BUZZER.MANUAL_TOGGLE_MS)

        cam_settings = profile.camera_profile
        command = {"action": "apply_settings", "settings": {"autofocus": cam_settings.autofocus, "exposure": cam_settings.exposure, "gain": cam_settings.gain, "white_balance_temp": cam_settings.white_balance_temp, "brightness": cam_settings.brightness}}
        for cam_id in ACTIVE_CAMERA_IDS:
            await self._redis.publish(f"camera:commands:{cam_id}", json.dumps(command))
        
        self._current_count, self._mode = 0, OperatingMode.RUNNING
        await self._io.write_coil(self._output_map.LED_RED, False)
        await self._io.write_coil(self._output_map.LED_GREEN, True)
        await self._io.write_coil(self._output_map.CONVEYOR, True)
        return True

    async def _update_run_log_status(self, status: RunStatus):
        if not self._active_run_id: return
        try:
            async with self._get_db_session() as session:
                run_log = await session.get(RunLog, self._active_run_id)
                if run_log:
                    run_log.status, run_log.end_timestamp = status, datetime.utcnow()
                    await session.commit()
        except Exception as e:
            print(f"Error updating RunLog status: {e}")

    async def complete_and_loop_run(self):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            await self._update_run_log_status(RunStatus.COMPLETED)
            self.beep_for(self._settings.BUZZER.LOOP_COMPLETE_MS)
            self._mode = OperatingMode.POST_RUN_DELAY
            stop_delay = self._settings.CONVEYOR.CONVEYOR_AUTO_STOP_DELAY_SEC
        await asyncio.sleep(stop_delay)
        async with self._lock:
            if self._mode != OperatingMode.POST_RUN_DELAY: return
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES
            pause_delay = self._run_post_batch_delay_sec
        await asyncio.sleep(pause_delay)
        async with self._lock:
            if self._mode != OperatingMode.PAUSED_BETWEEN_BATCHES: return
            await self._execute_start_sequence()

    async def stop_run(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED: return
            if self._active_run_id and self._mode != OperatingMode.STOPPED:
                await self._update_run_log_status(RunStatus.ABORTED)
            self._mode = OperatingMode.STOPPED
            self._active_profile, self._active_product, self._active_run_id = None, None, None
            self._run_profile_id, self._current_count, self._run_target_count = None, 0, 0
            self._run_operator_name = None
            self._run_batch_code = None
            await self.acknowledge_alarm()
            await self.initialize_hardware_state()

    def get_status(self) -> dict:
        return {
            "mode": self._mode.value,
            "active_profile": self._active_profile.name if self._active_profile else "None",
            "operator_name": self._run_operator_name,
            "batch_code": self._run_batch_code,
            "run_progress": self._current_count,
            "target_count": self._run_target_count,
            "post_batch_delay_sec": self._run_post_batch_delay_sec,
            "active_alarm_message": self._active_alarm_message,
        }