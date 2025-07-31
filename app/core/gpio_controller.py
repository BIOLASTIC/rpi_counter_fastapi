"""
FINAL REVISION: A non-blocking `blink_led` method has been implemented to fix the
AttributeError in the notification service. It correctly manages background
blinking tasks using asyncio.
"""
import asyncio
from enum import Enum
from typing import Optional, Dict, Any

from gpiozero import DigitalOutputDevice, LED, Buzzer, GPIOZeroError, Device
from gpiozero.pins.lgpio import LGPIOFactory

try:
    factory = LGPIOFactory()
    Device.pin_factory = factory
except Exception:
    Device.pin_factory = None

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
            self.initialized = False
            self.health_status = GPIOHealthStatus.OK if Device.pin_factory else GPIOHealthStatus.ERROR
            self._blink_tasks: Dict[str, asyncio.Task] = {}

    @classmethod
    async def get_instance(cls) -> 'AsyncGPIOController':
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
                await cls._instance.initialize()
        return cls._instance

    async def initialize(self) -> bool:
        if self.initialized: return True
        if not Device.pin_factory: return False
        try:
            self._pins["conveyor"] = DigitalOutputDevice(self._config.PIN_CONVEYOR_RELAY, active_high=False)
            self._pins["gate"] = DigitalOutputDevice(self._config.PIN_GATE_RELAY, active_high=False)
            # --- NEW: Initialize the diverter relay pin ---
            self._pins["diverter"] = DigitalOutputDevice(self._config.PIN_DIVERTER_RELAY, active_high=False)
            self._pins["led_green"] = LED(self._config.PIN_STATUS_LED_GREEN)
            self._pins["led_red"] = LED(self._config.PIN_STATUS_LED_RED)
            self._pins["buzzer"] = Buzzer(self._config.PIN_BUZZER)
            self.initialized = True
            return True
        except GPIOZeroError as e:
            print(f"GPIO Initialization failed: {e}")
            self.health_status = GPIOHealthStatus.ERROR
            return False

    async def shutdown(self):
        for task in self._blink_tasks.values():
            if task and not task.done():
                task.cancel()
        for name in self._pins:
            await self.set_pin_state(name, False)
        for device in self._pins.values():
            try:
                await asyncio.to_thread(device.close)
            except Exception:
                pass

    async def get_pin_status(self, name: str) -> bool:
        if name in self._pins:
            return await asyncio.to_thread(getattr, self._pins[name], 'is_active')
        return False

    async def toggle_pin(self, name: str) -> Optional[bool]:
        # --- NEW: Add 'diverter' to the list of toggleable pins ---
        if name in self._pins:
            if name in self._blink_tasks and not self._blink_tasks[name].done():
                self._blink_tasks[name].cancel()
            await asyncio.to_thread(self._pins[name].toggle)
            return await self.get_pin_status(name)
        return None

    async def set_pin_state(self, name: str, state: bool) -> Optional[bool]:
        if name in self._pins:
            if name in self._blink_tasks and not self._blink_tasks[name].done():
                self._blink_tasks[name].cancel()
            action = self._pins[name].on if state else self._pins[name].off
            await asyncio.to_thread(action)
            return await self.get_pin_status(name)
        return None

    async def blink_led(self, name: str, on_time: float = 0.5, off_time: float = 0.5, n: int = 1):
        """Blinks an LED in the background without blocking."""
        if name not in self._pins or not isinstance(self._pins[name], LED):
            print(f"Warning: Cannot blink non-LED pin '{name}'")
            return

        if name in self._blink_tasks and not self._blink_tasks[name].done():
            self._blink_tasks[name].cancel()

        async def _blinker():
            device = self._pins[name]
            loop_count = n if n is not None else float('inf')
            count = 0
            try:
                while count < loop_count:
                    device.on()
                    await asyncio.sleep(on_time)
                    device.off()
                    await asyncio.sleep(off_time)
                    if n is not None:
                        count += 1
            except asyncio.CancelledError:
                device.off()
            finally:
                device.off()

        self._blink_tasks[name] = asyncio.create_task(_blinker())

    async def health_check(self) -> GPIOHealthStatus:
        if not Device.pin_factory or not self.initialized:
            self.health_status = GPIOHealthStatus.ERROR
            return self.health_status
        try:
            await asyncio.to_thread(getattr, self._pins["led_green"], 'is_active')
            self.health_status = GPIOHealthStatus.OK
        except (GPIOZeroError, AttributeError, KeyError):
            self.health_status = GPIOHealthStatus.ERROR
        return self.health_status