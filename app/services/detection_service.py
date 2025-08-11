"""
Manages the detection and counting workflow.
"""
import asyncio
import uuid
from collections import deque
from typing import Dict, Deque

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from app.models.database import AsyncSessionFactory
from app.models.detection import DetectionEventLog
from config import ACTIVE_CAMERA_IDS, settings

class AsyncDetectionService:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        camera_manager: AsyncCameraManager,
        orchestration_service: AsyncOrchestrationService,
        conveyor_settings,
        db_session_factory
    ):
        self._io = modbus_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._conveyor_config = conveyor_settings
        self._get_db_session = db_session_factory
        self._lock = asyncio.Lock()
        self._verbose = settings.LOGGING.VERBOSE_LOGGING
        self._output_map = settings.OUTPUTS

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
            if self._verbose: print(f"VALIDATION: {warning_msg}")

    async def _handle_stalled_product(self, box_id: str):
        async with self._lock:
            self._stalled_product_timers.pop(box_id, None)
            if box_id in self._in_flight_objects:
                self._in_flight_objects.remove(box_id)
                reason = f"Stalled product detected on conveyor (ID: {box_id})"
                print(f"DETECTION FAILURE: {reason}. Triggering run failure.")
                await self._orchestration.trigger_run_failure(reason)
            elif self._verbose:
                print(f"Stalled product timer fired for already processed Box ID {box_id}. Ignoring.")

    async def handle_sensor_event(self, event: SensorEvent):
        """The entry point for all sensor events from the Modbus Poller."""
        async with self._lock:
            # THIS IS THE SYNTAX FIX: This condition was previously malformed.
            # It now correctly checks if the mode is NOT one of the active states.
            if self._orchestration.get_status()["mode"] not in [OperatingMode.RUNNING.value, OperatingMode.POST_RUN_DELAY.value]:
                if self._stalled_product_timers:
                    for timer in self._stalled_product_timers.values():
                        timer.cancel()
                    self._stalled_product_timers.clear()
                return

            if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL:
                if event.new_state == SensorState.TRIGGERED:
                    # Don't log a new box if the system is in the post-run delay phase
                    if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value:
                        return
                        
                    self._entry_timestamps[event.sensor_id] = event.timestamp
                    box_id = str(uuid.uuid4())
                    self._in_flight_objects.append(box_id)
                    
                    timeout_sec = self._conveyor_config.MAX_TRANSIT_TIME_SEC
                    loop = asyncio.get_running_loop()
                    timer_handle = loop.call_later(
                        timeout_sec,
                        lambda: asyncio.create_task(self._handle_stalled_product(box_id))
                    )
                    self._stalled_product_timers[box_id] = timer_handle
                    
                    if self._verbose: print(f"DETECTION: New box ID {box_id}. Stalled timer set for {timeout_sec}s.")
                    
                    if settings.CAMERA_TRIGGER_DELAY_MS > 0:
                        await asyncio.sleep(settings.CAMERA_TRIGGER_DELAY_MS / 1000.0)
                    
                    image_path = None
                    if ACTIVE_CAMERA_IDS:
                        image_path = await self._camera_manager.capture_and_save_image(ACTIVE_CAMERA_IDS[0], f'event_{box_id}')
                    
                    active_run_id = self._orchestration.get_active_run_id()
                    if active_run_id:
                        try:
                            async with self._get_db_session() as session:
                                new_event = DetectionEventLog(run_log_id=active_run_id, image_path=image_path)
                                session.add(new_event)
                                await session.commit()
                        except Exception as e:
                            print(f"ERROR: Could not log detection event to database: {e}")
                
                elif event.new_state == SensorState.CLEARED:
                    await self._check_sensor_block_time(event)

            elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                if self._in_flight_objects:
                    exiting_box_id = self._in_flight_objects.popleft()
                    
                    timer_to_cancel = self._stalled_product_timers.pop(exiting_box_id, None)
                    if timer_to_cancel:
                        timer_to_cancel.cancel()
                        if self._verbose: print(f"DETECTION: Box {exiting_box_id} confirmed exit. Stalled timer cancelled.")
                    
                    await self._orchestration.on_exit_sensor_triggered()
                    await self._orchestration.on_box_processed()
                else:
                    print("DETECTION WARNING: Exit sensor triggered, but no objects were tracked in-flight.")