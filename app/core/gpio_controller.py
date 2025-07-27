"""
REAL HARDWARE IMPLEMENTATION of the Async GPIO Controller.
REVISED: Now explicitly creates and sets the gpiozero pin factory to
prevent race conditions on import. This is the robust, recommended pattern.
"""
import asyncio
from enum import Enum
from typing import Optional, Dict, Any, Set
from gpiozero import DigitalOutputDevice, LED, Buzzer, GPIOZeroError, Device
from gpiozero.pins.lgpio import LGPIOFactory

# --- DEFINITIVE FIX FOR 'GPIO BUSY' and 'NoneType' ERROR ---
# 1. Explicitly create the pin factory we want to use.
# 2. Patch its close method to do nothing, giving our shutdown full control.
# 3. Assign our configured factory to the global Device.pin_factory.
# This entire block runs ONCE when the module is first imported.
try:
    factory = LGPIOFactory()
    factory.close = lambda: None
    Device.pin_factory = factory
    print("GPIO Controller: LGPIOFactory initialized and configured successfully.")
except Exception as e:
    print(f"FATAL GPIO ERROR: Could not initialize LGPIOFactory. Is lgpio daemon running? Error: {e}")
    # Set a dummy factory so the rest of the app can at least import without crashing
    Device.pin_factory = None

class ConveyorStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"

class GatePosition(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    MOVING = "moving"

class GPIOHealthStatus(str, Enum):
    OK = "ok"
    ERROR = "error"

class AsyncGPIOController:
    _instance: Optional['AsyncGPIOController'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        if not hasattr(self, 'initialized'):
            from config import settings
            self._config = settings.GPIO
            self._pins: Dict[str, Any] = {}
            self._conveyor_status = ConveyorStatus.STOPPED
            self._gate_position = GatePosition.CLOSED
            self._blinking_tasks: Dict[str, asyncio.Task] = {}
            self._background_tasks: Set[asyncio.Task] = set()
            self.initialized = False
            self.health_status = GPIOHealthStatus.OK if Device.pin_factory else GPIOHealthStatus.ERROR

    @classmethod
    async def get_instance(cls) -> 'AsyncGPIOController':
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
                await cls._instance.initialize()
        return cls._instance

    async def initialize(self) -> bool:
        if self.initialized: return True
        if not Device.pin_factory:
            print("GPIO Controller: Cannot initialize, pin factory failed to load.")
            return False
        try:
            # Relays are often active-low, meaning they turn ON when the pin is LOW.
            # Set active_high=False if your relay board works this way.
            self._pins["conveyor"] = DigitalOutputDevice(self._config.CONVEYOR_RELAY, active_high=True)
            self._pins["gate"] = DigitalOutputDevice(self._config.GATE_RELAY, active_high=True)
            self._pins["led_green"] = LED(self._config.STATUS_LED_GREEN)
            self._pins["led_red"] = LED(self._config.STATUS_LED_RED)
            self._pins["buzzer"] = Buzzer(self._config.BUZZER)
            self.initialized = True
            print("GPIO Controller: Hardware pins initialized successfully.")
            return True
        except GPIOZeroError as e:
            self.health_status = GPIOHealthStatus.ERROR
            print(f"GPIO Controller: Error initializing devices: {e}")
            return False

    async def shutdown(self) -> None:
        async with self._lock:
            # Task cleanup...
            for task in self._blinking_tasks.values(): task.cancel()
            await asyncio.gather(*self._blinking_tasks.values(), return_exceptions=True)
            if self._background_tasks:
                await asyncio.gather(*self._background_tasks, return_exceptions=True)
            
            # Device cleanup...
            for device in self._pins.values():
                try:
                    await asyncio.to_thread(device.close)
                except Exception as e:
                    print(f"Error closing device: {e}")
        print("GPIO Controller: Shutdown complete.")

    async def get_pin_status(self, name: str) -> bool:
        if name in self._pins:
            return await asyncio.to_thread(getattr, self._pins[name], 'is_active')
        return False

    # ... all other methods (start_conveyor, beep, etc.) remain unchanged ...
    async def _run_blocking_io(self, device_method, *args):
        return await asyncio.to_thread(device_method, *args)
    async def start_conveyor(self):
        await self._run_blocking_io(self._pins["conveyor"].on)
        self._conveyor_status = ConveyorStatus.RUNNING
    async def stop_conveyor(self):
        await self._run_blocking_io(self._pins["conveyor"].off)
        self._conveyor_status = ConveyorStatus.STOPPED
    async def get_conveyor_status(self) -> ConveyorStatus:
        return self._conveyor_status
    async def open_gate(self):
        self._gate_position = GatePosition.MOVING
        await self._run_blocking_io(self._pins["gate"].on)
        await asyncio.sleep(2)
        self._gate_position = GatePosition.OPEN
    async def close_gate(self):
        self._gate_position = GatePosition.MOVING
        await self._run_blocking_io(self._pins["gate"].off)
        await asyncio.sleep(2)
        self._gate_position = GatePosition.CLOSED
    async def get_gate_position(self) -> GatePosition:
        return self._gate_position
    async def set_led_state(self, led_name: str, state: bool):
        await self._stop_blinking(led_name)
        if state: await self._run_blocking_io(self._pins[led_name].on)
        else: await self._run_blocking_io(self._pins[led_name].off)
    async def _blink_task(self, led_name: str, on_time: float, off_time: float):
        device = self._pins[led_name]
        try:
            while True:
                await self._run_blocking_io(device.on)
                await asyncio.sleep(on_time)
                await self._run_blocking_io(device.off)
                await asyncio.sleep(off_time)
        except asyncio.CancelledError:
            await self._run_blocking_io(device.off)
    async def blink_led(self, led_name: str, on_time: float = 0.5, off_time: float = 0.5):
        await self._stop_blinking(led_name)
        task = asyncio.create_task(self._blink_task(led_name, on_time, off_time))
        self._blinking_tasks[led_name] = task
    async def _stop_blinking(self, led_name: str):
        if led_name in self._blinking_tasks:
            task = self._blinking_tasks.pop(led_name)
            if not task.done(): task.cancel()
    async def beep(self, duration: float = 0.1):
        task = asyncio.create_task(self._do_beep(duration))
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
    async def _do_beep(self, duration: float):
        await self._run_blocking_io(self._pins["buzzer"].on)
        await asyncio.sleep(duration)
        await self._run_blocking_io(self._pins["buzzer"].off)
    async def health_check(self) -> GPIOHealthStatus:
        return self.health_status
    async def emergency_stop(self):
        await self.shutdown()
