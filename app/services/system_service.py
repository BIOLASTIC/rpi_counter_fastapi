"""
REVISED: Now gathers and reports the live status of all 5 GPIO
output devices for the dashboard.
"""
import asyncio
from app.core.gpio_controller import AsyncGPIOController, ConveyorStatus
from app.core.camera_manager import AsyncCameraManager
from app.core.proximity_sensor import AsyncProximitySensorHandler

class AsyncSystemService:
    def __init__(self, gpio_controller: AsyncGPIOController, camera_manager: AsyncCameraManager, sensor_handler: AsyncProximitySensorHandler, db_session_factory, sensor_config):
        self._gpio = gpio_controller
        self._camera = camera_manager
        self._sensor_handler = sensor_handler
        self._config = sensor_config

    async def get_system_status(self) -> dict:
        """Gathers the current health status from all components."""
        # --- DEFINITIVE FIX: Gather status for ALL pins concurrently ---
        (
            gpio_health, camera_health, conveyor_status, gate_position,
            conveyor_relay_status, gate_relay_status,
            led_green_status, led_red_status, buzzer_status
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
        )
        
        sensor_states = self._sensor_handler.get_last_known_sensor_states()
        io_module_status = self._sensor_handler.get_module_health()
        
        return {
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
