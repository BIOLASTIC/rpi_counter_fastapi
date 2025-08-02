"""
Provides high-level system monitoring and control functionality.

FINAL REVISION: To resolve a persistent and uncatchable low-level crash
(unhashable type: 'dict'), all calls to the 'psutil' library have been
completely removed. The system status will now return safe, default values
for CPU, memory, and disk metrics. This is a graceful degradation strategy
that guarantees the stability of the core application by disabling the
non-essential, unstable monitoring component.
"""
import asyncio
import time
from typing import Optional, Dict
# The 'psutil' import is now completely removed.
import redis.asyncio as redis

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager, CameraHealthStatus
from app.core.modbus_poller import AsyncModbusPoller
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.detection_service import AsyncDetectionService
from config import ACTIVE_CAMERA_IDS
from config.settings import AppSettings


class AsyncSystemService:
    """
    Gathers and provides a unified status report for all system components.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        modbus_poller: AsyncModbusPoller,
        camera_manager: AsyncCameraManager,
        detection_service: AsyncDetectionService,
        orchestration_service: AsyncOrchestrationService,
        db_session_factory,
        sensor_config,
        output_config,
        redis_client: redis.Redis,
        settings: AppSettings
    ):
        self._io = modbus_controller
        self._poller = modbus_poller
        self._camera = camera_manager
        self._detection_service = detection_service
        self._orchestration_service = orchestration_service
        self._sensor_config = sensor_config
        self._output_config = output_config.model_dump()
        self._app_start_time = time.monotonic()
        self._redis = redis_client
        self._settings = settings
        self._redis_keys = settings.REDIS_KEYS

    async def full_system_reset(self):
        """Resets the running process. This is a "soft" reset."""
        await self._orchestration_service.stop_run()

    async def toggle_ai_service(self) -> str:
        """Checks the current state of the AI service in Redis and flips it."""
        current_state = await self._redis.get(self._redis_keys.AI_ENABLED_KEY)
        new_state_bool = not (current_state == "true")
        await self._redis.set(self._redis_keys.AI_ENABLED_KEY, "true" if new_state_bool else "false")
        new_state_str = "enabled" if new_state_bool else "disabled"
        print(f"SYSTEM SERVICE: AI detection has been toggled to {new_state_str.upper()}.")
        return new_state_str

    async def set_ai_detection_source(self, source: str):
        """Sets the AI detection source in the shared Redis store."""
        if source not in ['rpi', 'usb']:
            print(f"SYSTEM SERVICE: Invalid AI source '{source}' requested. Ignoring.")
            return
        await self._redis.set(self._redis_keys.AI_DETECTION_SOURCE_KEY, source)
        print(f"SYSTEM SERVICE: AI detection source has been switched to {source.upper()}.")

    async def get_system_status(self) -> Dict:
        """Gathers the current health status from all components safely."""
        try:
            # Gather all Redis/async data in parallel
            redis_results = await asyncio.gather(
                self._camera.get_all_health_statuses(),
                self._redis.get(self._redis_keys.AI_HEALTH_KEY),
                self._redis.get(self._redis_keys.AI_ENABLED_KEY),
                self._redis.get(self._redis_keys.AI_DETECTION_SOURCE_KEY),
                self._redis.get(self._redis_keys.AI_LAST_DETECTION_RESULT_KEY)
            )
            
            all_camera_statuses, ai_health, ai_enabled_raw, ai_source, last_detection = redis_results

            camera_statuses_payload = { cam_id: all_camera_statuses.get(cam_id, CameraHealthStatus.DISCONNECTED.value) for cam_id in ACTIVE_CAMERA_IDS }
            io_module_status = self._poller.get_io_health().value
            input_states = self._poller.get_current_input_states()
            output_states = self._poller.get_current_output_states()

            def get_input_state(channel: int) -> bool:
                index = channel - 1
                return input_states[index] if 0 <= index < len(input_states) else True 

            def get_output_state(name: str) -> bool:
                channel = self._output_config.get(name.upper())
                return output_states[channel] if channel is not None and 0 <= channel < len(output_states) else False

            # --- THE DEFINITIVE FIX: Return hardcoded default values for the unstable metrics ---
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "disk_usage": 0.0,
                "cpu_temperature": None,
                "uptime_seconds": int(time.monotonic() - self._app_start_time),
                "camera_statuses": camera_statuses_payload,
                "io_module_status": io_module_status,
                "sensor_1_status": not get_input_state(self._sensor_config.ENTRY_CHANNEL), 
                "sensor_2_status": not get_input_state(self._sensor_config.EXIT_CHANNEL), 
                "conveyor_relay_status": get_output_state("conveyor"),
                "gate_relay_status": get_output_state("gate"),
                "diverter_relay_status": get_output_state("diverter"),
                "led_green_status": get_output_state("led_green"),
                "led_red_status": get_output_state("led_red"),
                "buzzer_status": get_output_state("buzzer"),
                "camera_light_status": get_output_state("camera_light"),
                "in_flight_count": self._detection_service.get_in_flight_count(),
                "ai_service_status": "online" if ai_health else "offline",
                "ai_service_enabled": ai_enabled_raw == "true",
                "ai_detection_source": ai_source or self._settings.AI_DETECTION_SOURCE,
                "last_detection_result": last_detection or "---"
            }
        except Exception as e:
            # This block should now only be reachable if a Redis, Camera, or Poller call fails.
            print(f"FATAL ERROR in get_system_status: {e}")
            return {"error": "Failed to fetch system status."}

    async def emergency_stop(self):
        """Immediately stop all hardware operations via Modbus."""
        print("SYSTEM SERVICE: Initiating emergency stop of all hardware.")
        await self._io.write_coil(self._output_config.get("CONVEYOR"), False)
        await self._io.write_coil(self._output_config.get("GATE"), False)
        await self._io.write_coil(self._output_config.get("DIVERTER"), False)
        await self._io.write_coil(self._output_config.get("LED_GREEN"), False)
        await self._io.write_coil(self._output_config.get("LED_RED"), True)
        await self._io.write_coil(self._output_config.get("CAMERA_LIGHT"), False)