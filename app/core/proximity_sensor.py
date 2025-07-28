"""
REVISED: Adds verbose logging to show the raw hardware signal and the
corrected event being generated, aiding in debugging sensor issues.
"""
import asyncio
from typing import Callable, Coroutine, Optional, Dict
from .usr8000_client import AsyncUSRIOController, ModuleHealthStatus
from .sensor_events import SensorState, SensorEvent
from config import settings

AsyncEventCallback = Callable[[SensorEvent], Coroutine[None, None, None]]

class AsyncProximitySensorHandler:
    def __init__(self, io_controller: AsyncUSRIOController, event_callback: AsyncEventCallback):
        self.io_controller = io_controller
        self.event_callback = event_callback
        self.polling_interval_sec = settings.MODBUS.POLLING_MS / 1000.0
        self._monitoring_task: Optional[asyncio.Task] = None
        self._last_known_corrected_states: Dict[int, bool] = {1: False, 2: False}
        self._module_health: ModuleHealthStatus = ModuleHealthStatus.DISCONNECTED
        self._verbose = settings.LOGGING.VERBOSE_LOGGING # Store logging setting

    def get_last_known_corrected_states(self) -> Dict[int, bool]:
        """Returns the CORRECTED state (True means object detected)."""
        return self._last_known_corrected_states

    def get_module_health(self) -> ModuleHealthStatus:
        return self._module_health

    def start(self):
        """Starts the background task for polling sensor states."""
        if self._monitoring_task and not self._monitoring_task.done():
            return
        print(f"Sensor Handler: Starting polling in hardware-locked mode (LOW signal = TRIGGERED). Polling every {self.polling_interval_sec * 1000}ms.")
        self._monitoring_task = asyncio.create_task(self._poll_sensors())

    async def stop(self):
        """Stops the sensor monitoring task."""
        if self._monitoring_task: self._monitoring_task.cancel()
        try: await self._monitoring_task
        except asyncio.CancelledError: pass
        await self.io_controller.disconnect()

    async def _poll_sensors(self):
        while True:
            raw_states = await self.io_controller.read_input_channels()
            if raw_states is not None:
                self._module_health = ModuleHealthStatus.CONNECTED
                
                corrected_states = {}
                for sensor_id, raw_state in raw_states.items():
                    # LOW signal (False) means TRIGGERED
                    is_triggered = not raw_state
                    corrected_states[sensor_id] = is_triggered

                    if self._last_known_corrected_states.get(sensor_id) is not is_triggered:
                        # --- LOGGING FIX ---
                        if self._verbose:
                            print(f"[Sensor Event] ID {sensor_id}: Raw Signal={raw_state} -> Corrected State={'TRIGGERED' if is_triggered else 'CLEARED'}")
                        
                        event = SensorEvent(
                            sensor_id=sensor_id, 
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                
                self._last_known_corrected_states = corrected_states
            else:
                self._module_health = ModuleHealthStatus.DISCONNECTED
            
            await asyncio.sleep(self.polling_interval_sec)