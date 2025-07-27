"""
REVISED: The detection service now uses the configurable sensor channel
mapping instead of hardcoded values.
"""
import asyncio
import time
from enum import Enum, auto
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.gpio_controller import AsyncGPIOController
from app.core.sensor_events import SensorEvent, SensorState
from app.models.detection import Detection, DetectionDirection

class DetectionState(Enum):
    IDLE = auto()
    ENTERING = auto()
    CONFIRMING_EXIT = auto()
    RESETTING = auto()

class AsyncDetectionService:
    # DEFINITIVE FIX: Accept the sensor configuration settings on initialization
    def __init__(self, gpio_controller: AsyncGPIOController, db_session_factory, sensor_config):
        self._gpio = gpio_controller
        self._get_db_session = db_session_factory
        self._config = sensor_config # Store the sensor config
        self._state = DetectionState.IDLE
        self._current_count = 0
        self._entry_timestamp: Optional[float] = None
        self._lock = asyncio.Lock()
        self._max_transit_time = 5.0
        self._min_transit_time = 0.1
        print(f"Detection Service: Initialized. Entry Sensor: Channel {self._config.ENTRY_CHANNEL}, Exit Sensor: Channel {self._config.EXIT_CHANNEL}")

    async def initialize(self):
        """Initializes the service, loading the last count from the database."""
        # ... (this method remains the same)
        async with self._lock:
            async with self._get_db_session() as session:
                result = await session.execute(
                    select(Detection).order_by(Detection.timestamp.desc()).limit(1)
                )
                last_detection = result.scalar_one_or_none()
                if last_detection: self._current_count = last_detection.box_count
                else: self._current_count = 0

    async def handle_sensor_event(self, event: SensorEvent):
        """The core state machine, now using configurable channels."""
        async with self._lock:
            current_time = time.monotonic()
            
            # --- IDLE STATE ---
            if self._state == DetectionState.IDLE:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    self._state = DetectionState.ENTERING
                    self._entry_timestamp = current_time

            # --- ENTERING STATE ---
            elif self._state == DetectionState.ENTERING:
                if event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    transit_time = current_time - (self._entry_timestamp or current_time)
                    if self._min_transit_time < transit_time < self._max_transit_time:
                        self._state = DetectionState.CONFIRMING_EXIT
                    else:
                        self._state = DetectionState.IDLE
                elif self._entry_timestamp and (current_time - self._entry_timestamp) > self._max_transit_time:
                    self._state = DetectionState.IDLE

            # --- CONFIRMING_EXIT STATE ---
            elif self._state == DetectionState.CONFIRMING_EXIT:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.CLEARED:
                    self._current_count += 1
                    await self._log_detection()
                    self._state = DetectionState.RESETTING
                    asyncio.create_task(self._gpio.blink_led("led_green", on_time=0.1, off_time=0.1))

            # --- RESETTING STATE ---
            elif self._state == DetectionState.RESETTING:
                if event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.CLEARED:
                    self._state = DetectionState.IDLE
                    self._entry_timestamp = None

    async def _log_detection(self):
        # ... (this method remains the same)
        detection_record = Detection(box_count=self._current_count, detection_direction=DetectionDirection.FORWARD)
        async with self._get_db_session() as session:
            session.add(detection_record)
            await session.commit()

    async def get_current_count(self) -> int:
        async with self._lock:
            return self._current_count

    async def reset_counter(self) -> bool:
        async with self._lock:
            self._current_count = 0
            self._state = DetectionState.IDLE
        return True
