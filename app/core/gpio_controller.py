"""
FINAL REVISION: Adds a generic `toggle_pin` method to control all
output devices (relays, LEDs, buzzers) and makes status checking more robust.
"""
import asyncio
from enum import Enum
from typing import Optional, Dict, Any, Set
from gpiozero import DigitalOutputDevice, LED, Buzzer, GPIOZeroError, Device
from gpiozero.pins.lgpio import LGPIOFactory

try:
    factory = LGPIOFactory()
    factory.close = lambda: None
    Device.pin_factory = factory
except Exception:
    Device.pin_factory = None

class ConveyorStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
class GatePosition(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
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
            self._pins["conveyor"] = DigitalOutputDevice(self._config.CONVEYOR_RELAY, active_high=False)
            self._pins["gate"] = DigitalOutputDevice(self._config.GATE_RELAY, active_high=False)
            self._pins["led_green"] = LED(self._config.STATUS_LED_GREEN)
            self._pins["led_red"] = LED(self._config.STATUS_LED_RED)
            self._pins["buzzer"] = Buzzer(self._config.BUZZER)
            self.initialized = True
            return True
        except GPIOZeroError:
            self.health_status = GPIOHealthStatus.ERROR
            return False

    async def shutdown(self):
        for device in self._pins.values():
            try: await asyncio.to_thread(device.close)
            except Exception: pass

    async def get_pin_status(self, name: str) -> bool:
        if name in self._pins:
            return await asyncio.to_thread(getattr, self._pins[name], 'is_active')
        return False
        
    async def get_conveyor_status(self) -> ConveyorStatus:
        is_active = await self.get_pin_status("conveyor")
        return ConveyorStatus.RUNNING if is_active else ConveyorStatus.STOPPED

    async def get_gate_position(self) -> GatePosition:
        is_active = await self.get_pin_status("gate")
        return GatePosition.OPEN if is_active else GatePosition.CLOSED
        
    # --- DEFINITIVE FIX: Generic toggle for ALL output pins ---
    async def toggle_pin(self, name: str) -> Optional[bool]:
        """Toggles any output pin by name and returns its new state."""
        if name not in self._pins:
            return None
        
        device = self._pins[name]
        # Use the standard .toggle() method which exists on all output devices
        await asyncio.to_thread(device.toggle)
        return await self.get_pin_status(name)
