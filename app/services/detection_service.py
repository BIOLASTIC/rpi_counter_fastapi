"""
REVISED: Imports ACTIVE_CAMERA_IDS from the main application's config module.
"""
import asyncio
import time
from enum import Enum, auto
from typing import Optional, Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.models.detection import Detection, DetectionDirection
# --- THE FIX: Import from the main app's centralized config ---
from config import settings, ACTIVE_CAMERA_IDS

class DetectionState(Enum):
    # ... The rest of the file is correct from the previous step ...
    IDLE = auto()
    WAITING_FOR_CLEAR = auto()

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
        self._trigger_delay = settings.CAMERA_TRIGGER_DELAY_MS / 1000.0
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
        for cam_id in ACTIVE_CAMERA_IDS:
            asyncio.create_task(
                self._camera_manager.capture_and_save_image(cam_id, 'event')
            )

    async def handle_sensor_event(self, event: SensorEvent):
        async with self._lock:
            current_time = time.monotonic()
            if self._verbose:
                print(f"[State Machine] Current State: {self._state.name}, Event: Sensor {event.sensor_id} -> {event.new_state.name}")
            if self._state == DetectionState.IDLE:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    self._entry_timestamp = current_time
                    self._current_total_count += 1
                    if self._verbose: print(f"  -> !!!!! BOX COUNTED !!!!! New Total: {self._current_total_count}")
                    await self._log_detection()
                    if self._on_box_counted:
                        await self._on_box_counted()
                    asyncio.create_task(self._trigger_delayed_capture())
                    self._state = DetectionState.WAITING_FOR_CLEAR
                    if self._verbose: print("  -> Transitioning to WAITING_FOR_CLEAR")
            elif self._state == DetectionState.WAITING_FOR_CLEAR:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.CLEARED:
                    self._state = DetectionState.IDLE
                    self._entry_timestamp = None
                    if self._verbose: print("  -> Sequence complete. Transitioning to IDLE.")
                elif self._entry_timestamp and (current_time - self._entry_timestamp) > self._max_transit_time:
                    self._state = DetectionState.IDLE
                    self._entry_timestamp = None
                    if self._verbose: print("  -> Timed out waiting for entry sensor to clear, forcing reset to IDLE")

    async def _log_detection(self):
        detection_record = Detection(box_count=self._current_total_count, detection_direction=DetectionDirection.FORWARD)
        async with self._get_db_session() as session:
            session.add(detection_record)
            await session.commit()

    async def get_current_total_count(self) -> int:
        async with self._lock:
            return self._current_total_count

    async def reset_counter(self) -> bool:
        async with self._lock:
            self._current_total_count = 0
            self._state = DetectionState.IDLE
            try:
                reset_record = Detection(box_count=0, detection_direction=DetectionDirection.UNKNOWN)
                async with self._get_db_session() as session:
                    session.add(reset_record)
                    await session.commit()
                return True
            except Exception as e:
                print(f"Error resetting counter in DB: {e}")
                return False