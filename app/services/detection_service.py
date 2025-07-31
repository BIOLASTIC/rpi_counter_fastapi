"""
REVISED FOR PHASE 2: This service now manages the entire detection and
sorting workflow based on the active profile.

- It tracks individual objects on the conveyor using a queue.
- It triggers a (mock) AI quality control check for each object.
- It calculates the precise time required for a failed object to travel
  from the camera to the sorting mechanism.
- It uses a non-blocking, timed background task to activate the
  physical sorting relay at the exact right moment.
"""
import asyncio
import time
import uuid
import random
from enum import Enum, auto
from collections import deque

from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
# Import the orchestrator to check the system's run state and get the active profile
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from config import settings

class AsyncDetectionService:
    def __init__(
        self,
        gpio_controller: AsyncGPIOController,
        camera_manager: AsyncCameraManager,
        orchestration_service: AsyncOrchestrationService,
        conveyor_settings
    ):
        """
        Initializes the detection service.

        Args:
            gpio_controller: The instance for controlling GPIO hardware.
            camera_manager: The instance for managing camera operations.
            orchestration_service: The instance for managing the overall system state.
            conveyor_settings: The configuration object with physical conveyor dimensions.
        """
        self._gpio = gpio_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._conveyor_config = conveyor_settings
        self._lock = asyncio.Lock()
        self._verbose = settings.LOGGING.VERBOSE_LOGGING
        
        # A deque is a highly efficient queue for adding and removing items from both ends.
        self._in_flight_objects = deque()
        
        # Calculate the fixed time it takes for an object to travel from the camera to the sorter.
        # This is a critical value for our timed sorting.
        self._base_travel_time_sec = 0.0
        if self._conveyor_config.SPEED_M_PER_SEC > 0:
            self._base_travel_time_sec = self._conveyor_config.CAMERA_TO_SORTER_DISTANCE_M / self._conveyor_config.SPEED_M_PER_SEC
        
        print(f"Detection Service: Calculated base travel time of {self._base_travel_time_sec:.2f} seconds.")

    async def _mock_ai_qc_check(self, image_path: str) -> str:
        """
        A placeholder for the real AI quality control API call.
        This simulates network latency and a random PASS/FAIL result.
        """
        if self._verbose:
            print(f"AI STUB: Checking quality of image '{image_path}'...")
        
        await asyncio.sleep(random.uniform(0.3, 0.8)) # Simulate network and processing time
        result = random.choice(["PASS", "PASS", "PASS", "FAIL"]) # Skewed to pass more often
        
        if self._verbose:
            print(f"AI STUB: Result for '{image_path}' is -> {result}")
        return result

    async def _trigger_sorter_after_delay(self, sleep_duration: float):
        """
        Waits for the calculated time, then pulses the diverter relay.
        This runs as a separate, non-blocking background task.
        """
        if self._verbose:
            print(f"SORTER: FAILED product detected. Waiting {sleep_duration:.2f} seconds to activate diverter.")
        
        await asyncio.sleep(sleep_duration)
        
        print("SORTER: ACTIVATING DIVERTER RELAY!")
        await self._gpio.set_pin_state("diverter", True)
        # Hold the diverter arm out for a short duration to ensure the object is cleared.
        await asyncio.sleep(0.5) 
        await self._gpio.set_pin_state("diverter", False)

    async def _run_qc_for_box(self, box_id: str, image_path: str):
        """
        The main background task for processing a single box. It calls the AI
        and, if necessary, initiates the timed sorting task.
        """
        active_profile = self._orchestration.get_active_profile()
        if not active_profile:
            print(f"DETECTION ERROR: QC check started for box {box_id}, but no active profile is loaded. Aborting.")
            return

        qc_result = await self._mock_ai_qc_check(image_path)
        
        if qc_result == "FAIL":
            # Calculate the precise time to wait before activating the sorter.
            # This accounts for both the physical travel time and any per-object adjustments.
            sort_offset_sec = active_profile.sort_offset_ms / 1000.0
            total_wait_time = self._base_travel_time_sec + sort_offset_sec
            
            # Start the final background task that will wait and then handle the physical sorting.
            # This is "fire-and-forget"; the main logic moves on immediately.
            asyncio.create_task(self._trigger_sorter_after_delay(total_wait_time))
        # If the result is "PASS", we simply do nothing. The box continues to the exit.

    async def handle_sensor_event(self, event: SensorEvent):
        """
        The entry point for all sensor events. This is the primary state
        machine for the detection process.
        """
        # Lock to ensure events are processed one at a time.
        async with self._lock:
            # IMPORTANT: Only process events if the system is actively running.
            # This prevents accidental triggers when the system is stopped or idle.
            if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value:
                return

            # A new box has been detected by the first sensor.
            if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                box_id = str(uuid.uuid4())
                self._in_flight_objects.append(box_id)
                
                if self._verbose:
                    print(f"DETECTION: New box entered with ID {box_id}. In-flight count: {len(self._in_flight_objects)}")

                # Trigger the camera to capture an image for this specific box.
                image_path = await self._camera_manager.capture_and_save_image('usb', f'qc_{box_id}')
                
                if image_path:
                    # If an image was successfully captured, start the background QC process.
                    asyncio.create_task(self._run_qc_for_box(box_id, image_path))
                else:
                    print(f"DETECTION WARNING: Failed to capture image for box {box_id}. Cannot perform QC check.")

            # A box has reached the end of the conveyor.
            elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                # We assume boxes exit in the same First-In, First-Out (FIFO) order they entered.
                if self._in_flight_objects:
                    exiting_box_id = self._in_flight_objects.popleft()
                    # Notify the orchestrator that a box has been fully processed.
                    self._orchestration.on_box_processed()
                    if self._verbose:
                        print(f"DETECTION: Box {exiting_box_id} confirmed at exit. In-flight count: {len(self._in_flight_objects)}")
                else:
                    # This can happen if the exit sensor is triggered erroneously.
                    print("DETECTION WARNING: Exit sensor triggered, but no objects were tracked in-flight.")