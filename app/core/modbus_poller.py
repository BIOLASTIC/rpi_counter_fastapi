"""
REVISED: Now acts as the Modbus Poller Service.
- It continuously polls BOTH the input and output modules.
- It maintains a complete, up-to-date state of all hardware I/O.
- It detects changes in inputs and fires sensor events.
- It correctly inverts the NPN sensor signal (LOW signal = TRIGGERED).

DEFINITIVE FIX: The poller now uses the injected sensor configuration to determine
which physical channels to monitor, instead of hardcoding a 1-to-1 mapping. This
makes the SENSORS_ENTRY_CHANNEL and SENSORS_EXIT_CHANNEL settings work correctly.
"""
import asyncio
from typing import Callable, Coroutine, Optional, List
from .modbus_controller import AsyncModbusController, ModbusHealthStatus
from .sensor_events import SensorState, SensorEvent
from config import settings

AsyncEventCallback = Callable[[SensorEvent], Coroutine[None, None, None]]

class AsyncModbusPoller:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        event_callback: AsyncEventCallback,
        sensor_config  # <-- ADDED: Inject the sensor settings object
    ):
        self.modbus_controller = modbus_controller
        self.event_callback = event_callback
        # --- ADDED: Store the sensor configuration ---
        self._sensor_config = sensor_config
        self.polling_interval_sec = settings.MODBUS.POLLING_MS / 1000.0
        self._monitoring_task: Optional[asyncio.Task] = None
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

        # Initialize all states to True (cleared for NPN sensors)
        self._input_channels: List[bool] = [True] * 4
        self._output_channels: List[bool] = [False] * 8
        self._last_known_entry_state: bool = True
        self._last_known_exit_state: bool = True
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
        print(f"   -> Monitoring Entry Sensor on Channel: {self._sensor_config.ENTRY_CHANNEL}")
        print(f"   -> Monitoring Exit Sensor on Channel:  {self._sensor_config.EXIT_CHANNEL}")
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

            if raw_inputs is not None:
                if self._health_status != ModbusHealthStatus.OK:
                    print("Modbus Poller: Re-established connection to IO modules.")
                self._health_status = ModbusHealthStatus.OK
                self._input_channels = raw_inputs
                
                # Update output channels if read was successful
                if raw_outputs is not None:
                    self._output_channels = raw_outputs

                # --- THE REWRITTEN LOGIC ---
                # Convert 1-based config channels to 0-based list indices
                entry_idx = self._sensor_config.ENTRY_CHANNEL - 1
                exit_idx = self._sensor_config.EXIT_CHANNEL - 1

                # Check Entry Sensor state if index is valid
                if 0 <= entry_idx < len(self._input_channels):
                    current_entry_state = self._input_channels[entry_idx]
                    if current_entry_state != self._last_known_entry_state:
                        is_triggered = not current_entry_state  # NPN Logic Inversion
                        if self._verbose:
                            print(f"[Sensor Event] Entry Sensor (Channel {entry_idx + 1}): Raw={current_entry_state} -> {'TRIGGERED' if is_triggered else 'CLEARED'}")
                        event = SensorEvent(
                            sensor_id=self._sensor_config.ENTRY_CHANNEL,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                        self._last_known_entry_state = current_entry_state

                # Check Exit Sensor state if index is valid
                if 0 <= exit_idx < len(self._input_channels):
                    current_exit_state = self._input_channels[exit_idx]
                    if current_exit_state != self._last_known_exit_state:
                        is_triggered = not current_exit_state  # NPN Logic Inversion
                        if self._verbose:
                            print(f"[Sensor Event] Exit Sensor (Channel {exit_idx + 1}): Raw={current_exit_state} -> {'TRIGGERED' if is_triggered else 'CLEARED'}")
                        event = SensorEvent(
                            sensor_id=self._sensor_config.EXIT_CHANNEL,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                        self._last_known_exit_state = current_exit_state
                # --- END OF REWRITTEN LOGIC ---
                
            else:
                if self._health_status == ModbusHealthStatus.OK:
                    print("Modbus Poller: Lost connection to IO modules.")
                self._health_status = self.modbus_controller.health_status
                
                # If connection is lost, force sensors to a 'cleared' state
                if not self._last_known_entry_state:
                    self._last_known_entry_state = True
                    event = SensorEvent(sensor_id=self._sensor_config.ENTRY_CHANNEL, new_state=SensorState.CLEARED)
                    asyncio.create_task(self.event_callback(event))

                if not self._last_known_exit_state:
                    self._last_known_exit_state = True
                    event = SensorEvent(sensor_id=self._sensor_config.EXIT_CHANNEL, new_state=SensorState.CLEARED)
                    asyncio.create_task(self.event_callback(event))

            await asyncio.sleep(self.polling_interval_sec)