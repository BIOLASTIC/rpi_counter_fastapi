"""
REVISED: Now acts as the Modbus Poller Service.
- It continuously polls BOTH the input and output modules.
- It maintains a complete, up-to-date state of all hardware I/O.
- It detects changes in inputs and fires sensor events.
- It correctly inverts the NPN sensor signal (LOW signal = TRIGGERED).
"""
import asyncio
from typing import Callable, Coroutine, Optional, List
from .modbus_controller import AsyncModbusController, ModbusHealthStatus
from .sensor_events import SensorState, SensorEvent
from config import settings

AsyncEventCallback = Callable[[SensorEvent], Coroutine[None, None, None]]

class AsyncModbusPoller:
    def __init__(self, modbus_controller: AsyncModbusController, event_callback: AsyncEventCallback):
        self.modbus_controller = modbus_controller
        self.event_callback = event_callback
        self.polling_interval_sec = settings.MODBUS.POLLING_MS / 1000.0
        self._monitoring_task: Optional[asyncio.Task] = None
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

        self._input_channels: List[bool] = [False] * 4
        self._output_channels: List[bool] = [False] * 8
        self._last_known_input_states: List[bool] = [False] * 4
        self._health_status: ModbusHealthStatus = ModbusHealthStatus.DISCONNECTED

    def get_io_health(self) -> ModbusHealthStatus:
        return self._health_status

    def get_current_input_states(self) -> List[bool]:
        return self._input_channels

    def get_current_output_states(self) -> List[bool]:
        return self._output_channels

    def start(self):
        if self._monitoring_task and not self._monitoring_task.done():
            return
        print(f"Modbus Poller: Starting polling every {self.polling_interval_sec * 1000}ms.")
        self._monitoring_task = asyncio.create_task(self._poll_hardware())

    async def stop(self):
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass

    async def _poll_hardware(self):
        while True:
            raw_inputs = await self.modbus_controller.read_digital_inputs()
            raw_outputs = await self.modbus_controller.read_coils()

            if raw_inputs is not None and raw_outputs is not None:
                if self._health_status != ModbusHealthStatus.OK:
                    print("Modbus Poller: Re-established connection to IO modules.")
                self._health_status = ModbusHealthStatus.OK
                self._input_channels = raw_inputs
                self._output_channels = raw_outputs

                for i, current_state in enumerate(self._input_channels):
                    if current_state != self._last_known_input_states[i]:
                        sensor_id = i + 1
                        is_triggered = not current_state  # NPN Logic Inversion

                        if self._verbose:
                            print(f"[Sensor Event] ID {sensor_id}: Raw Signal={current_state} -> State={'TRIGGERED' if is_triggered else 'CLEARED'}")

                        event = SensorEvent(
                            sensor_id=sensor_id,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))

                self._last_known_input_states = list(self._input_channels)
            else:
                if self._health_status == ModbusHealthStatus.OK:
                    print("Modbus Poller: Lost connection to IO modules.")
                self._health_status = self.modbus_controller.health_status
                if any(s is False for s in self._last_known_input_states):
                    for i in range(len(self._last_known_input_states)):
                        self._last_known_input_states[i] = True
                        event = SensorEvent(sensor_id=i+1, new_state=SensorState.CLEARED)
                        asyncio.create_task(self.event_callback(event))

            await asyncio.sleep(self.polling_interval_sec)