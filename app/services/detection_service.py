"""
REVISED: The entire service is overhauled for a robust, two-sensor state machine.
- It now tracks 'entered' and 'exited' counts separately.
- The state machine is more complex to accurately track a box's journey.
- This provides the foundation for the new "digital twin" dashboard.
"""
import asyncio
import time
from enum import Enum, auto
from typing import Optional, Callable, Awaitable, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.models.detection import Detection, DetectionDirection
from config import settings, ACTIVE_CAMERA_IDS

# A more descriptive state machine for tracking box journey
class DetectionState(Enum):
    IDLE = auto()               # System is waiting for a box
    ENTERING = auto()           # Entry sensor triggered, box is entering the belt
    ON_BELT = auto()            # Entry sensor cleared, box is fully on the belt
    EXITING = auto()            # Exit sensor triggered, box is at the end
    # No more WAITING_FOR_CLEAR, the sequence is the state

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
        
        # --- NEW: Separate counters for detailed tracking ---
        self._entered_count = 0
        self._exited_count = 0
        
        self._lock = asyncio.Lock()
        self._max_transit_time = 10.0 # Increased for longer belts
        self._entry_timestamp: Optional[float] = None
        self._trigger_delay = settings.CAMERA_TRIGGER_DELAY_MS / 1000.0
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

    async def initialize(self):
        async with self._lock:
            async with self._get_db_session() as session:
                # We load the last 'exited' count as the source of truth
                result = await session.execute(select(Detection).order_by(Detection.timestamp.desc()).limit(1))
                last_detection = result.scalar_one_or_none()
                if last_detection:
                    self._exited_count = last_detection.box_count
                else:
                    self._exited_count = 0
            # Assume no boxes are on the belt at startup
            self._entered_count = self._exited_count
        print(f"Detection Service: Initialized with Entered={self._entered_count}, Exited={self._exited_count}.")

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

            # --- THE NEW TWO-SENSOR STATE MACHINE LOGIC ---
            if self._state == DetectionState.IDLE:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    self._entry_timestamp = current_time
                    self._entered_count += 1
                    self._state = DetectionState.ENTERING
                    if self._verbose:
                        print(f"  -> Box entering. New Entered Count: {self._entered_count}. Transition to ENTERING.")
                    # Trigger camera capture as soon as the box is seen
                    asyncio.create_task(self._trigger_delayed_capture())

            elif self._state == DetectionState.ENTERING:
                if event.sensor_id == self._config.ENTRY_CHANNEL and event.new_state == SensorState.CLEARED:
                    self._state = DetectionState.ON_BELT
                    if self._verbose:
                        print("  -> Box is fully on the belt. Transition to ON_BELT.")
                elif event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    # This handles very short belts or long objects
                    self._state = DetectionState.EXITING
                    if self._verbose:
                        print("  -> Box reached exit sensor while still on entry sensor. Transition to EXITING.")

            elif self._state == DetectionState.ON_BELT:
                if event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                    self._state = DetectionState.EXITING
                    if self._verbose:
                        print("  -> Box reached exit sensor. Transition to EXITING.")
                # Timeout check: if a box enters but never reaches the exit
                elif self._entry_timestamp and (current_time - self._entry_timestamp) > self._max_transit_time:
                    print("  -> ERROR: Box timed out on belt. Resetting state.")
                    self._state = DetectionState.IDLE
                    self._entry_timestamp = None


            elif self._state == DetectionState.EXITING:
                if event.sensor_id == self._config.EXIT_CHANNEL and event.new_state == SensorState.CLEARED:
                    # !!!!! THIS IS THE COUNTING EVENT !!!!!
                    self._exited_count += 1
                    self._entry_timestamp = None
                    if self._verbose:
                        print(f"  -> !!!!! BOX COUNTED !!!!! New Exited Count: {self._exited_count}. Transition to IDLE.")
                    
                    # Log to DB and notify orchestrator
                    await self._log_detection()
                    if self._on_box_counted:
                        await self._on_box_counted()
                    
                    self._state = DetectionState.IDLE
    
    async def _log_detection(self):
        # We now log the exited_count as the official box_count
        detection_record = Detection(box_count=self._exited_count, detection_direction=DetectionDirection.FORWARD)
        async with self._get_db_session() as session:
            session.add(detection_record)
            await session.commit()

    # --- NEW: Getter for all counts ---
    async def get_counts(self) -> Dict[str, int]:
        """Returns a dictionary of all current counts."""
        async with self._lock:
            return {
                "entered": self._entered_count,
                "exited": self._exited_count,
                "on_belt": self._entered_count - self._exited_count
            }

    async def reset_counter(self) -> bool:
        async with self._lock:
            self._entered_count = 0
            self._exited_count = 0
            self._state = DetectionState.IDLE
            try:
                # The 'box_count' field in the DB represents the total exited/counted items.
                reset_record = Detection(box_count=0, detection_direction=DetectionDirection.UNKNOWN)
                async with self._get_db_session() as session:
                    session.add(reset_record)
                    await session.commit()
                return True
            except Exception as e:
                print(f"Error resetting counter in DB: {e}")
                return False