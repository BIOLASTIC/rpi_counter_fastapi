"""
This service provides high-level system monitoring and control, including
the full system reset functionality.
"""
import asyncio
import time
from typing import Optional, Dict
from enum import Enum
import psutil

from app.core.gpio_controller import AsyncGPIOController, GPIOHealthStatus
from app.core.camera_manager import AsyncCameraManager, CameraHealthStatus
from app.core.proximity_sensor import AsyncProximitySensorHandler, ModuleHealthStatus
from app.services.detection_service import AsyncDetectionService
from app.services.orchestration_service import AsyncOrchestrationService
from config import ACTIVE_CAMERA_IDS

def _get_rpi_cpu_temp() -> Optional[float]:
    """Safely gets the Raspberry Pi CPU temperature."""
    try:
        temps = psutil.sensors_temperatures()
        return temps.get('cpu_thermal', [None])[0].current if temps else None
    except Exception:
        return None

class AsyncSystemService:
    def __init__(
        self,
        gpio_controller: AsyncGPIOController,
        camera_manager: AsyncCameraManager,
        sensor_handler: AsyncProximitySensorHandler,
        detection_service: AsyncDetectionService,
        orchestration_service: AsyncOrchestrationService,
        db_session_factory,
        sensor_config
    ):
        self._gpio = gpio_controller
        self._camera = camera_manager
        self._sensor_handler = sensor_handler
        self._detection_service = detection_service
        self._orchestration_service = orchestration_service
        self._config = sensor_config
        self._app_start_time = time.monotonic()

    async def full_system_reset(self):
        """Resets all counters and stops all hardware processes."""
        print("SYSTEM SERVICE: Initiating full system reset.")
        await self._orchestration_service.stop_process()
        await self._detection_service.reset_counter()

    async def get_system_status(self) -> Dict:
        """Gathers the current health status from all components safely."""
        try:
            all_camera_statuses = self._camera.get_all_health_statuses()
            camera_statuses_payload = {
                cam_id: all_camera_statuses.get(cam_id, CameraHealthStatus.DISCONNECTED.value)
                for cam_id in ACTIVE_CAMERA_IDS
            }
            results = await asyncio.gather(
                self._gpio.health_check(),
                self._gpio.get_pin_status("conveyor"),
                self._gpio.get_pin_status("gate"),
                self._gpio.get_pin_status("led_green"),
                self._gpio.get_pin_status("led_red"),
                self._gpio.get_pin_status("buzzer"),
                return_exceptions=True
            )
            gpio_health_enum, conveyor_status, gate_status, led_green_status, led_red_status, buzzer_status = [
                res if not isinstance(res, Exception) else None for res in results
            ]
            sensor_states = self._sensor_handler.get_last_known_corrected_states()
            io_module_status_enum = self._sensor_handler.get_module_health()
            gpio_status_str = gpio_health_enum.value if isinstance(gpio_health_enum, Enum) else GPIOHealthStatus.ERROR.value
            io_module_status_str = io_module_status_enum.value if isinstance(io_module_status_enum, Enum) else ModuleHealthStatus.ERROR.value
            return {
                "cpu_usage": psutil.cpu_percent(interval=None),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "cpu_temperature": _get_rpi_cpu_temp(),
                "uptime_seconds": int(time.monotonic() - self._app_start_time),
                "camera_statuses": camera_statuses_payload,
                "gpio_status": gpio_status_str,
                "conveyor_relay_status": conveyor_status,
                "gate_relay_status": gate_status,
                "led_green_status": led_green_status,
                "led_red_status": led_red_status,
                "buzzer_status": buzzer_status,
                "io_module_status": io_module_status_str,
                "sensor_1_status": sensor_states.get(self._config.ENTRY_CHANNEL, False),
                "sensor_2_status": sensor_states.get(self._config.EXIT_CHANNEL, False),
            }
        except Exception as e:
            print(f"FATAL ERROR in get_system_status: {e}")
            return {"error": "Failed to fetch system status."}

    async def emergency_stop(self):
        """Immediately stop all hardware operations. Requires API Key."""
        print("SYSTEM SERVICE: Initiating emergency stop of all hardware.")
        await self._gpio.set_pin_state("conveyor", False)
        await self._gpio.set_pin_state("gate", False)
        await self._gpio.set_pin_state("led_red", True)
        await self._gpio.set_pin_state("led_green", False)