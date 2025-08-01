"""
Provides high-level system monitoring and control functionality.

FINAL REVISION: This service has been fully refactored to use the new Modbus
hardware services.
- It gets all hardware I/O status from the AsyncModbusPoller.
- It issues commands like emergency stop via the AsyncModbusController.
- The structure of the status payload sent to the frontend is preserved to
  ensure UI compatibility.
- ADDED: Safety checks to prevent IndexError from invalid .env sensor channel config.
- ADDED: In-flight object count from the detection service.
- ADDED: Health check for the standalone AI service via Redis.
"""
import asyncio
import time
from typing import Optional, Dict
import psutil
import redis.asyncio as redis

from app.core.modbus_controller import AsyncModbusController, ModbusHealthStatus
from app.core.camera_manager import AsyncCameraManager, CameraHealthStatus
from app.core.modbus_poller import AsyncModbusPoller
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.detection_service import AsyncDetectionService
from config import ACTIVE_CAMERA_IDS


def _get_rpi_cpu_temp() -> Optional[float]:
    """Safely gets the Raspberry Pi CPU temperature."""
    try:
        temps = psutil.sensors_temperatures()
        return temps.get('cpu_thermal', [None])[0].current if temps else None
    except Exception:
        return None


class AsyncSystemService:
    """
    Gathers and provides a unified status report for all system components.
    Handles high-priority system-wide actions like emergency stop.
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
        redis_client: redis.Redis # <<< THIS IS THE FIX: Added redis_client parameter
    ):
        self._io = modbus_controller
        self._poller = modbus_poller
        self._camera = camera_manager
        self._detection_service = detection_service
        self._orchestration_service = orchestration_service
        self._sensor_config = sensor_config
        self._output_config = output_config.model_dump()
        self._app_start_time = time.monotonic()
        self._redis = redis_client # Store the redis client instance

    async def full_system_reset(self):
        """Resets the running process. This is a "soft" reset."""
        print("SYSTEM SERVICE: Initiating full system reset.")
        await self._orchestration_service.stop_run()

    async def get_system_status(self) -> Dict:
        """Gathers the current health status from all components safely."""
        try:
            all_camera_statuses = self._camera.get_all_health_statuses()
            camera_statuses_payload = {
                cam_id: all_camera_statuses.get(cam_id, CameraHealthStatus.DISCONNECTED.value)
                for cam_id in ACTIVE_CAMERA_IDS
            }
            io_module_status = self._poller.get_io_health().value
            input_states = self._poller.get_current_input_states()
            output_states = self._poller.get_current_output_states()

            def get_input_state(channel: int) -> bool:
                """Safely gets the raw boolean state for a 1-based channel number."""
                index = channel - 1
                if 0 <= index < len(input_states):
                    return input_states[index]
                return True 

            sensor1_raw = get_input_state(self._sensor_config.ENTRY_CHANNEL)
            sensor2_raw = get_input_state(self._sensor_config.EXIT_CHANNEL)

            def get_output_state(name: str) -> bool:
                """Safely get the boolean state for a named output."""
                channel = self._output_config.get(name.upper())
                if channel is not None and 0 <= channel < len(output_states):
                    return output_states[channel]
                return False

            # --- NEW: Check for the AI service's heartbeat in Redis ---
            ai_service_health = await self._redis.get("ai_service:health_status")
            ai_service_status = "online" if ai_service_health else "offline"

            return {
                "cpu_usage": psutil.cpu_percent(interval=None),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "cpu_temperature": _get_rpi_cpu_temp(),
                "uptime_seconds": int(time.monotonic() - self._app_start_time),
                "camera_statuses": camera_statuses_payload,
                "io_module_status": io_module_status,
                "sensor_1_status": not sensor1_raw, 
                "sensor_2_status": not sensor2_raw, 
                "conveyor_relay_status": get_output_state("conveyor"),
                "gate_relay_status": get_output_state("gate"),
                "diverter_relay_status": get_output_state("diverter"),
                "led_green_status": get_output_state("led_green"),
                "led_red_status": get_output_state("led_red"),
                "buzzer_status": get_output_state("buzzer"),
                "in_flight_count": self._detection_service.get_in_flight_count(),
                "ai_service_status": ai_service_status,
            }
        except Exception as e:
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