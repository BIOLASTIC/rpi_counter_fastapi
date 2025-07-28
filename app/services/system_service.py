"""
REVISED: The get_system_status method now fetches the *corrected* sensor
states from the handler, ensuring the UI display logic is always correct
regardless of the sensor type (NO or NC).
"""
import asyncio
import time
from typing import Optional
import psutil

from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.proximity_sensor import AsyncProximitySensorHandler

def _get_rpi_cpu_temp() -> Optional[float]:
    try:
        temps = psutil.sensors_temperatures()
        if 'cpu_thermal' in temps:
            return temps['cpu_thermal'][0].current
    except Exception:
        pass
    return None

class AsyncSystemService:
    def __init__(self, gpio_controller: AsyncGPIOController, camera_manager: AsyncCameraManager, sensor_handler: AsyncProximitySensorHandler, db_session_factory, sensor_config):
        self._gpio = gpio_controller
        self._camera = camera_manager
        self._sensor_handler = sensor_handler
        self._config = sensor_config
        self._app_start_time = time.monotonic()

    async def get_system_status(self) -> dict:
        """Gathers the current health status from all components."""
        (
            gpio_health, camera_health, conveyor_status, gate_position,
            conveyor_relay_status, gate_relay_status,
            led_green_status, led_red_status, buzzer_status,
            cpu_usage, mem_info, disk_info, cpu_temp
        ) = await asyncio.gather(
            self._gpio.health_check(),
            self._camera.health_check(),
            self._gpio.get_conveyor_status(),
            self._gpio.get_gate_position(),
            self._gpio.get_pin_status("conveyor"),
            self._gpio.get_pin_status("gate"),
            self._gpio.get_pin_status("led_green"),
            self._gpio.get_pin_status("led_red"),
            self._gpio.get_pin_status("buzzer"),
            asyncio.to_thread(psutil.cpu_percent, interval=None),
            asyncio.to_thread(psutil.virtual_memory),
            asyncio.to_thread(psutil.disk_usage, '/'),
            asyncio.to_thread(_get_rpi_cpu_temp)
        )
        
        # --- DEFINITIVE FIX: Get the CORRECTED states for UI display ---
        sensor_states = self._sensor_handler.get_last_known_corrected_states()
        io_module_status = self._sensor_handler.get_module_health()
        uptime_seconds = int(time.monotonic() - self._app_start_time)
        
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": mem_info.percent,
            "disk_usage": disk_info.percent,
            "cpu_temperature": cpu_temp,
            "uptime_seconds": uptime_seconds,
            "camera_status": camera_health.value,
            "gpio_status": gpio_health.value,
            "conveyor_relay_status": conveyor_relay_status,
            "gate_relay_status": gate_relay_status,
            "led_green_status": led_green_status,
            "led_red_status": led_red_status,
            "buzzer_status": buzzer_status,
            "io_module_status": io_module_status.value,
            "sensor_1_status": sensor_states.get(self._config.ENTRY_CHANNEL, False),
            "sensor_2_status": sensor_states.get(self._config.EXIT_CHANNEL, False),
        }