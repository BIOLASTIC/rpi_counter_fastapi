"""
FINAL REVISION: The SystemService now correctly uses the sensor channel
configuration from the settings file to report the status of the correct
sensors, instead of using hardcoded values.
"""
import asyncio
import psutil
import time
from typing import Optional

from app.core.gpio_controller import AsyncGPIOController, ConveyorStatus
from app.core.camera_manager import AsyncCameraManager
from app.core.proximity_sensor import AsyncProximitySensorHandler
from app.models.system_status import SystemStatus, CameraStatus as DbCameraStatus, GatePosition as DbGatePosition

class AsyncSystemService:
    # DEFINITIVE FIX: Accept the sensor configuration
    def __init__(self, gpio_controller: AsyncGPIOController, camera_manager: AsyncCameraManager, sensor_handler: AsyncProximitySensorHandler, db_session_factory, sensor_config):
        self._gpio = gpio_controller
        self._camera = camera_manager
        self._sensor_handler = sensor_handler
        self._get_db_session = db_session_factory
        self._config = sensor_config # Store the sensor config
        self._monitoring_task: Optional[asyncio.Task] = None
        self._monitoring_interval_sec = 60.0

    def start_monitoring(self):
        if self._monitoring_task is None or self._monitoring_task.done():
            self._monitoring_task = asyncio.create_task(self._monitor_loop())

    def stop_monitoring(self):
        if self._monitoring_task and not self._monitoring_task.done():
            self._monitoring_task.cancel()

    async def _monitor_loop(self):
        try:
            while True:
                await asyncio.sleep(self._monitoring_interval_sec)
        except asyncio.CancelledError:
            pass

    async def get_system_status(self) -> dict:
        """Gathers the current health status from all components."""
        gpio_health, camera_health, conveyor_status, gate_position, gate_relay_status = await asyncio.gather(
            self._gpio.health_check(),
            self._camera.health_check(),
            self._gpio.get_conveyor_status(),
            self._gpio.get_gate_position(),
            self._gpio.get_pin_status("gate")
        )
        
        sensor_states = self._sensor_handler.get_last_known_sensor_states()
        io_module_status = self._sensor_handler.get_module_health()
        
        status_data = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "cpu_temperature": self._get_cpu_temperature(),
            "uptime_seconds": self._get_uptime(),
            "camera_status": camera_health.value,
            "gpio_status": gpio_health.value,
            "conveyor_running": conveyor_status == ConveyorStatus.RUNNING,
            "gate_position": gate_position.value,
            "conveyor_relay_status": "ON" if conveyor_status == ConveyorStatus.RUNNING else "OFF",
            "gate_relay_status": gate_relay_status,
            "io_module_status": io_module_status.value,
            # DEFINITIVE FIX: Use the configured channels instead of hardcoded 1 and 2
            "sensor_1_status": sensor_states.get(self._config.ENTRY_CHANNEL, False),
            "sensor_2_status": sensor_states.get(self._config.EXIT_CHANNEL, False),
        }
        return status_data

    def _get_cpu_temperature(self) -> float:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return float(f.read()) / 1000.0
        except (FileNotFoundError, IOError):
            return 45.5
            
    def _get_uptime(self) -> int:
        return int(time.time() - psutil.boot_time())

    async def emergency_stop(self):
        await self._gpio.emergency_stop()
