"""
Manages the detection and counting workflow.

REVISED: All AI-related Quality Control (QC) and automated sorting logic
has been removed. The service now only manages the state machine for counting
objects and captures a diagnostic image when an object enters.

DEFINITIVE FIX: The __init__ method now correctly omits the 'settings'
and 'redis_client' arguments, which are no longer used by this service.
"""
import asyncio
import uuid
from collections import deque

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from config import ACTIVE_CAMERA_IDS, settings

class AsyncDetectionService:
    """
    Manages the box detection state machine and triggers camera captures.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        camera_manager: AsyncCameraManager,
        orchestration_service: AsyncOrchestrationService,
        conveyor_settings
    ):
        """
        Initializes the detection service.
        """
        self._io = modbus_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._conveyor_config = conveyor_settings
        self._lock = asyncio.Lock()
        self._verbose = settings.LOGGING.VERBOSE_LOGGING
        self._output_map = settings.OUTPUTS

        self._in_flight_objects = deque()
        self._base_travel_time_sec = 0.0
        if self._conveyor_config.SPEED_M_PER_SEC > 0:
            self._base_travel_time_sec = self._conveyor_config.CAMERA_TO_SORTER_DISTANCE_M / self._conveyor_config.SPEED_M_PER_SEC

        print(f"Detection Service: Calculated base travel time of {self._base_travel_time_sec:.2f} seconds.")

    def get_in_flight_count(self) -> int:
        """Returns the number of objects currently tracked on the conveyor."""
        return len(self._in_flight_objects)

    async def handle_sensor_event(self, event: SensorEvent):
        """
        The entry point for all sensor events from the Modbus Poller.
        This is the primary state machine for the detection process.
        """
        async with self._lock:
            if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value:
                return

            # A new box has been detected by the first sensor.
            if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL and event.new_state == SensorState.TRIGGERED:
                box_id = str(uuid.uuid4())
                self._in_flight_objects.append(box_id)

                if self._verbose:
                    print(f"DETECTION: New box entered with ID {box_id}. In-flight count: {len(self._in_flight_objects)}")

                delay_ms = settings.CAMERA_TRIGGER_DELAY_MS
                if delay_ms > 0:
                    await asyncio.sleep(delay_ms / 1000.0)

                # Use the first configured camera as the event camera.
                if ACTIVE_CAMERA_IDS:
                    event_camera_id = ACTIVE_CAMERA_IDS[0]
                    if self._verbose:
                        print(f"DETECTION: Triggering diagnostic capture from '{event_camera_id}'.")
                    
                    await self._camera_manager.capture_and_save_image(
                        event_camera_id, 
                        f'event_{box_id}'
                    )
                else:
                    print(f"DETECTION WARNING: No active cameras configured. Cannot capture image.")

            # A box has reached the end of the conveyor.
            elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                if self._in_flight_objects:
                    exiting_box_id = self._in_flight_objects.popleft()
                    self._orchestration.on_box_processed()
                    if self._verbose:
                        print(f"DETECTION: Box {exiting_box_id} confirmed at exit. In-flight count: {len(self._in_flight_objects)}")
                else:
                    print("DETECTION WARNING: Exit sensor triggered, but no objects were tracked in-flight.")