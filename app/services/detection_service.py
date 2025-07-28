"""
REVISED: Adds extensive verbose logging for every state transition to
diagnose counter issues. Also makes the state machine more robust by
adding a timeout to the RESETTING state.
"""
import asyncio
import time
from enum import Enum, auto
from typing import Optional, Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config import settings
from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.models.detection import Detection, DetectionDirection

class DetectionState(Enum):
    IDLE = auto()
    ENTERING = auto()
    CONFIRMING_EXIT = auto()
    RESETTING = auto()

class AsyncDetectionService:
    def __init__(
        self,
        gpio_controller: AsyncGPIOController,
        db_session_factory,
        sensor_config,
        camera_manager: AsyncCameraManager,
        on_box_counted: Callable[[], Awaitable[None]]
    ):
        self._gpio = gpio_controller
        self._get_db_session = db_session_factory
        self._config = sensor_config
        self._camera_manager = camera_manager
        self._on_box_counted = on_box_counted
        self._state = DetectionState.IDLE
        self._current_total_count = 0
        self._entry_timestamp: Optional[float] = None
        self._lock = asyncio.Lock()
        self._max_transit_time = 5.0
        self._min_transit_time = 0.1
        self._trigger_delay = settings.CAMERA.TRIGGER_DELAY_MS / 1000.0
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

    async def initialize(self):
        async with self._lock:
            async with self._get_db_session() as session:
                result = await session.execute(select(Detection).order_by(Detection.timestamp.desc()).limit(1))
                last_detection = result.scalar_one_or_none()
                if last_detection: self._current_total_count = last_detection.box_count
                else: self._current_total_count = 0
        print(f"Detection Service: Initialized with total count of {self._current_total_count}.")


    async def _trigger_delayed_capture(self):
        await asyncio.sleep(self._trigger_delay)
        filename = f"event_{int(time.time())}.jpg"
        await self._camera_manager.capture_and_save_image(filename, 'event')


    async def handle_sensor_event(self, event: SensorEvent):
        """The core state machine, now with verbose logging and timeouts."""
        async with self._lock:
            current_time = time.monotonic()
            
            if self._verbose:
                print(f"[State Machine] Current State: {self._state.name}, Event: Sensor {event.sensor_id} -> {event.new_state.name}")

            # --- IDLE STATE ---
            if self._state == DetectionState.IDLE:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    self._state = DetectionState.ENTERING
                    self._entry_timestamp = current_time
                    if self._verbose: print("  -> Transitioning to ENTERING")
                    asyncio.create_task(self._trigger_delayed_capture())

            # --- ENTERING STATE ---
            elif self._state == DetectionState.ENTERING:
                if event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    if self._min_transit_time < (current_time - (self._entry_timestamp or current_time)) < self._max_transit_time:
                        self._state = DetectionState.CONFIRMING_EXIT
                        if self._verbose: print("  -> Transitioning to CONFIRMING_EXIT")
                    else:
                        self._state = DetectionState.IDLE
                        if self._verbose: print(f"  -> Invalid transit time ({current_time - self._entry_timestamp:.2f}s), resetting to IDLE")
                elif self._entry_timestamp and (current_time - self._entry_timestamp) > self._max_transit_time:
                    self._state = DetectionState.IDLE
                    if self._verbose: print("  -> Timed out waiting for exit sensor, resetting to IDLE")

            # --- CONFIRMING_EXIT STATE (COUNTING HAPPENS HERE) ---
            elif self._state == DetectionState.CONFIRMING_EXIT:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.CLEARED:
                    self._current_total_count += 1
                    if self._verbose: print(f"  -> !!!!! BOX COUNTED !!!!! New Total: {self._current_total_count}")
                    await self._log_detection()
                    self._state = DetectionState.RESETTING
                    if self._verbose: print("  -> Transitioning to RESETTING")
                    if self._on_box_counted:
                        await self._on_box_counted()
                elif self._entry_timestamp and (current_time - self._entry_timestamp) > self._max_transit_time:
                    self._state = DetectionState.IDLE
                    if self._verbose: print("  -> Timed out waiting for entry sensor to clear, resetting to IDLE")

            # --- RESETTING STATE (NOW WITH TIMEOUT) ---
            elif self._state == DetectionState.RESETTING:
                if event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.CLEARED:
                    self._state = DetectionState.IDLE
                    self._entry_timestamp = None
                    if self._verbose: print("  -> Sequence complete. Transitioning to IDLE.")
                # --- ROBUSTNESS FIX ---
                elif self._entry_timestamp and (current_time - self._entry_timestamp) > self._max_transit_time:
                    self._state = DetectionState.IDLE
                    self._entry_timestamp = None
                    if self._verbose: print("  -> Timed out waiting for exit sensor to clear, forcing reset to IDLE")

    async def _log_detection(self):
        # We now log the *total* count, not the batch count
        detection_record = Detection(box_count=self._current_total_count, detection_direction=DetectionDirection.FORWARD)
        async with self._get_db_session() as session:
            session.add(detection_record)
            await session.commit()

    async def get_current_total_count(self) -> int:
        async with self._lock:
            return self._current_total_count

    async def reset_counter(self) -> bool:
        # Resetting the total counter should also be persisted.
        async with self._lock:
            self._current_total_count = 0
            self._state = DetectionState.IDLE
            reset_record = Detection(box_count=0, detection_direction=DetectionDirection.RESET)
            async with self._get_db_session() as session:
                session.add(reset_record)
                await session.commit()
            return True