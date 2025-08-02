"""
Manages the detection and sorting workflow based on the active profile.

FINAL REVISION: Implements the CAMERA_TRIGGER_DELAY_MS functionality. The service
now correctly pauses for the specified duration after the entry sensor is
triggered and before the camera capture is initiated.
"""
import asyncio
import time
import uuid
import random
from collections import deque
import redis.asyncio as redis

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from config.settings import AppSettings


class AsyncDetectionService:
    """
    Manages the box detection state machine, triggers camera captures,
    and initiates the sorting process for objects on the conveyor.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        camera_manager: AsyncCameraManager,
        orchestration_service: AsyncOrchestrationService,
        conveyor_settings,
        redis_client: redis.Redis,
        settings: AppSettings
    ):
        """
        Initializes the detection service.
        """
        self._io = modbus_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._conveyor_config = conveyor_settings
        self._redis = redis_client
        self._settings = settings
        self._redis_keys = self._settings.REDIS_KEYS
        self._lock = asyncio.Lock()
        self._verbose = self._settings.LOGGING.VERBOSE_LOGGING
        self._output_map = self._settings.OUTPUTS

        self._in_flight_objects = deque()
        self._base_travel_time_sec = 0.0
        if self._conveyor_config.SPEED_M_PER_SEC > 0:
            self._base_travel_time_sec = self._conveyor_config.CAMERA_TO_SORTER_DISTANCE_M / self._conveyor_config.SPEED_M_PER_SEC

        print(f"Detection Service: Calculated base travel time of {self._base_travel_time_sec:.2f} seconds.")

    def get_in_flight_count(self) -> int:
        """Returns the number of objects currently tracked on the conveyor."""
        return len(self._in_flight_objects)

    async def _mock_ai_qc_check(self, image_path: str) -> str:
        """A placeholder for a real AI quality control API call."""
        if self._verbose:
            print(f"AI STUB: Checking quality of image '{image_path}'...")
        await asyncio.sleep(random.uniform(0.3, 0.8))
        result = random.choice(["PASS", "PASS", "PASS", "FAIL"])
        if self._verbose:
            print(f"AI STUB: Result for '{image_path}' is -> {result}")
        return result

    async def _trigger_sorter_after_delay(self, sleep_duration: float):
        """Waits for the calculated time, then pulses the diverter relay via Modbus."""
        if self._verbose:
            print(f"SORTER: FAILED product detected. Waiting {sleep_duration:.2f} seconds to activate diverter.")
        await asyncio.sleep(sleep_duration)
        print("SORTER: ACTIVATING DIVERTER RELAY!")
        await self._io.write_coil(self._output_map.DIVERTER, True)
        await asyncio.sleep(0.5)
        await self._io.write_coil(self._output_map.DIVERTER, False)

    async def _run_qc_for_box(self, box_id: str, image_path: str):
        """Main background task for processing a single box. Calls AI and triggers sorting."""
        active_profile = self._orchestration.get_active_profile()
        if not active_profile:
            print(f"DETECTION ERROR: QC check started for box {box_id}, but no active profile is loaded. Aborting.")
            return

        qc_result = await self._mock_ai_qc_check(image_path)

        if qc_result == "FAIL":
            sort_offset_sec = active_profile.sort_offset_ms / 1000.0
            total_wait_time = self._base_travel_time_sec + sort_offset_sec
            asyncio.create_task(self._trigger_sorter_after_delay(total_wait_time))

    async def handle_sensor_event(self, event: SensorEvent):
        """
        The entry point for all sensor events from the Modbus Poller.
        This is the primary state machine for the detection process.
        """
        async with self._lock:
            if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value:
                return

            # A new box has been detected by the first sensor.
            if event.sensor_id == self._settings.SENSORS.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                box_id = str(uuid.uuid4())
                self._in_flight_objects.append(box_id)

                if self._verbose:
                    print(f"DETECTION: New box entered with ID {box_id}. In-flight count: {len(self._in_flight_objects)}")

                # --- THE DEFINITIVE FIX: Implement the camera trigger delay ---
                # 1. Get the delay in milliseconds from the settings.
                delay_ms = self._settings.CAMERA_TRIGGER_DELAY_MS
                
                if delay_ms > 0:
                    # 2. Convert to seconds for asyncio.sleep().
                    delay_sec = delay_ms / 1000.0
                    if self._verbose:
                        print(f"DETECTION: Waiting for camera trigger delay of {delay_ms}ms...")
                    # 3. Wait for the specified duration.
                    await asyncio.sleep(delay_sec)
                # --- END OF FIX ---

                # Get the current AI source from Redis, with a fallback to the default config.
                active_ai_camera = await self._redis.get(self._redis_keys.AI_DETECTION_SOURCE_KEY) or self._settings.AI_DETECTION_SOURCE
                
                if self._verbose:
                    print(f"DETECTION: Active AI camera is '{active_ai_camera}'. Triggering capture.")

                # Use the retrieved source to capture the image.
                image_path = await self._camera_manager.capture_and_save_image(
                    active_ai_camera, 
                    f'qc_{box_id}'
                )

                if image_path:
                    asyncio.create_task(self._run_qc_for_box(box_id, image_path))
                else:
                    print(f"DETECTION WARNING: Failed to capture image for box {box_id}. Cannot perform QC check.")

            # A box has reached the end of the conveyor.
            elif event.sensor_id == self._settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                if self._in_flight_objects:
                    exiting_box_id = self._in_flight_objects.popleft()
                    self._orchestration.on_box_processed()
                    if self._verbose:
                        print(f"DETECTION: Box {exiting_box_id} confirmed at exit. In-flight count: {len(self._in_flight_objects)}")
                else:
                    print("DETECTION WARNING: Exit sensor triggered, but no objects were tracked in-flight.")