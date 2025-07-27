"""
REVISED: Renamed start_monitoring to start() for consistency.
"""
import asyncio
from typing import Callable, Coroutine, Optional, Dict
from .usr8000_client import AsyncUSRIOController, ModuleHealthStatus
from .sensor_events import SensorState, SensorEvent

AsyncEventCallback = Callable[[SensorEvent], Coroutine[None, None, None]]

class AsyncProximitySensorHandler:
    def __init__(self, io_controller: AsyncUSRIOController, event_callback: AsyncEventCallback):
        from config import settings
        self.io_controller = io_controller
        self.event_callback = event_callback
        self.polling_interval_sec = settings.MODBUS.POLLING_MS / 1000.0
        self._monitoring_task: Optional[asyncio.Task] = None
        self._last_known_states: Dict[int, bool] = {1: False, 2: False}
        self._module_health: ModuleHealthStatus = ModuleHealthStatus.DISCONNECTED

    def get_last_known_sensor_states(self) -> Dict[int, bool]:
        return self._last_known_states

    def get_module_health(self) -> ModuleHealthStatus:
        return self._module_health

    def start(self):
        """Starts the background task for polling sensor states."""
        if self._monitoring_task and not self._monitoring_task.done():
            return
        print("Sensor Handler: Starting proximity sensor polling...")
        self._monitoring_task = asyncio.create_task(self._poll_sensors())

    async def stop(self):
        """Stops the sensor monitoring task."""
        if self._monitoring_task and not self._monitoring_task.done():
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        await self.io_controller.disconnect()

    async def _poll_sensors(self):
        while True:
            current_states = await self.io_controller.read_input_channels()
            if current_states is not None:
                self._module_health = ModuleHealthStatus.CONNECTED
                for sensor_id, state in current_states.items():
                    if self._last_known_states.get(sensor_id) is not state:
                        event = SensorEvent(sensor_id=sensor_id, new_state=SensorState.TRIGGERED if state else SensorState.CLEARED)
                        asyncio.create_task(self.event_callback(event))
                self._last_known_states = current_states
            else:
                self._module_health = ModuleHealthStatus.DISCONNECTED
            await asyncio.sleep(self.polling_interval_sec)
