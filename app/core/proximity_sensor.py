"""
REVISED: The polling loop now handles read failures (returns of None)
gracefully by resetting the last known state to a safe 'CLEAR' default.
This prevents the UI from getting stuck showing an old 'TRIGGERED' state
when the connection to the sensor module is lost.
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
        self._last_known_corrected_states: Dict[int, bool] = {
            settings.SENSORS.ENTRY_CHANNEL: False,
            settings.SENSORS.EXIT_CHANNEL: False,
        }
        self._module_health: ModuleHealthStatus = ModuleHealthStatus.DISCONNECTED
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

    def get_last_known_corrected_states(self) -> Dict[int, bool]:
        """Returns the CORRECTED state (True means object detected)."""
        return self._last_known_corrected_states

    def get_module_health(self) -> ModuleHealthStatus:
        return self._module_health

    def start(self):
        if self._monitoring_task and not self._monitoring_task.done():
            return
        print(f"Sensor Handler: Starting polling in hardware-locked mode. Polling every {self.polling_interval_sec * 1000}ms.")
        self._monitoring_task = asyncio.create_task(self._poll_sensors())

    async def stop(self):
        if self._monitoring_task: self._monitoring_task.cancel()
        try: await self._monitoring_task
        except asyncio.CancelledError: pass
        await self.io_controller.disconnect()

    async def _poll_sensors(self):
        while True:
            raw_states = await self.io_controller.read_input_channels()
            
            if raw_states is not None:
                if self._module_health != ModuleHealthStatus.CONNECTED:
                    print("Sensor Handler: Re-established connection to IO module.")
                self._module_health = ModuleHealthStatus.CONNECTED
                
                corrected_states = {}
                for sensor_id in self._last_known_corrected_states.keys():
                    raw_state = raw_states.get(sensor_id, True) # Default to True (untriggered) if not present
                    is_triggered = not raw_state
                    corrected_states[sensor_id] = is_triggered

                    if self._last_known_corrected_states.get(sensor_id) is not is_triggered:
                        if self._verbose:
                            print(f"[Sensor Event] ID {sensor_id}: Raw Signal={raw_state} -> Corrected State={'TRIGGERED' if is_triggered else 'CLEARED'}")
                        
                        event = SensorEvent(
                            sensor_id=sensor_id, 
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                
                self._last_known_corrected_states = corrected_states
            else:
                # --- DEFINITIVE FIX for Stale Data ---
                if self._module_health == ModuleHealthStatus.CONNECTED:
                    print("Sensor Handler: Lost connection to IO module. Sensor states will default to CLEAR.")
                
                self._module_health = ModuleHealthStatus.DISCONNECTED
                
                # Reset states to a safe, 'CLEAR' default if any were 'TRIGGERED'
                if any(self._last_known_corrected_states.values()):
                    for sensor_id in self._last_known_corrected_states:
                        self._last_known_corrected_states[sensor_id] = False
                        # Send a CLEAR event to ensure the state machine and UI are reset
                        event = SensorEvent(sensor_id=sensor_id, new_state=SensorState.CLEARED)
                        asyncio.create_task(self.event_callback(event))

            await asyncio.sleep(self.polling_interval_sec)