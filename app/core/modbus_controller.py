"""
NEW: Modbus Hardware Controller
This class is the single source of truth for all Modbus RTU communication.
It handles connections and provides low-level methods to read and write
to the two different USR-IO modules on the RS485 bus.
"""
import asyncio
from enum import Enum
from typing import Optional, List
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.framer import ModbusRtuFramer

from config import settings


class ModbusHealthStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    DISCONNECTED = "disconnected"


class AsyncModbusController:
    _instance: Optional['AsyncModbusController'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._config = settings.MODBUS
            self.client = AsyncModbusSerialClient(
                port=self._config.PORT,
                framer=ModbusRtuFramer,
                baudrate=self._config.BAUDRATE,
                bytesize=8,
                parity="N",
                stopbits=1,
                timeout=self._config.TIMEOUT_SEC,
            )
            self.initialized = True
            self.health_status = ModbusHealthStatus.DISCONNECTED
            self._is_connected = False
            
            # --- THE DEFINITIVE FIX IS HERE ---
            # The API sends lowercase names (e.g., 'camera_light'). The original code created a map
            # with uppercase keys ('CAMERA_LIGHT'), causing the lookup to fail.
            # This comprehension creates the map with lowercase keys to ensure a match.
            self._output_name_to_address_map = {
                k.lower(): v for k, v in settings.OUTPUTS.model_dump().items()
            }
            self._output_address_to_name_map = {v: k for k, v in self._output_name_to_address_map.items()}
            print("--- Modbus Controller Initialized ---")
            print(f"    Loaded output map: {self._output_name_to_address_map}")


    @classmethod
    async def get_instance(cls) -> 'AsyncModbusController':
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def get_output_address(self, name: str) -> Optional[int]:
        # Now, the lookup `name.lower()` will correctly find keys like 'camera_light' in our map.
        return self._output_name_to_address_map.get(name.lower())

    async def connect(self) -> bool:
        if self._is_connected:
            return True
        try:
            is_connected = await self.client.connect()
            if is_connected:
                print("Modbus Controller: Successfully connected to serial port.")
                self.health_status = ModbusHealthStatus.OK
                self._is_connected = True
                return True
            else:
                print("Modbus Controller: Failed to connect to serial port.")
                self.health_status = ModbusHealthStatus.DISCONNECTED
                self._is_connected = False
                return False
        except Exception as e:
            print(f"Modbus Controller: Error during connection attempt: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False
            return False

    async def disconnect(self):
        if self._is_connected:
            self.client.close()
            self._is_connected = False
            self.health_status = ModbusHealthStatus.DISCONNECTED
            print("Modbus Controller: Connection closed.")

    async def read_digital_inputs(self) -> Optional[List[bool]]:
        """Reads the 4 discrete inputs from the USR-IO4040 (Slave ID 1). FC=2, Address=0, Quantity=4."""
        if not await self.connect(): return None
        try:
            result = await self.client.read_discrete_inputs(
                address=0, count=4, slave=self._config.DEVICE_ADDRESS_INPUTS
            )
            if result.isError(): raise ModbusIOException(f"Modbus error on input read: {result}")
            
            # --- THE BUG FIX IS HERE ---
            # The library might return a list shorter than 4. We must pad it.
            # The default state for an NPN sensor input is HIGH (True).
            bits = result.bits
            while len(bits) < 4:
                bits.append(True)
            return bits[:4]
            # --- END OF FIX ---

        except (ConnectionException, ModbusIOException, asyncio.TimeoutError) as e:
            print(f"Modbus read_digital_inputs failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            await self.disconnect()
            return None

    async def read_coils(self) -> Optional[List[bool]]:
        """Reads the 8 relay statuses from the USR-IO8000 (Slave ID 2). FC=1, Address=0, Quantity=8."""
        if not await self.connect(): return None
        try:
            result = await self.client.read_coils(
                address=0, count=8, slave=self._config.DEVICE_ADDRESS_OUTPUTS
            )
            if result.isError(): raise ModbusIOException(f"Modbus error on coil read: {result}")

            # --- APPLYING THE SAME FIX FOR ROBUSTNESS ---
            # The default state for an output coil is OFF (False).
            bits = result.bits
            while len(bits) < 8:
                bits.append(False)
            return bits[:8]
            # --- END OF FIX ---

        except (ConnectionException, ModbusIOException, asyncio.TimeoutError) as e:
            print(f"Modbus read_coils failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            await self.disconnect()
            return None

    async def write_coil(self, address: int, state: bool) -> bool:
        """Writes a single coil (relay) on the USR-IO8000 (Slave ID 2). FC=5."""
        if not await self.connect(): return False
        try:
            result = await self.client.write_coil(
                address=address, value=state, slave=self._config.DEVICE_ADDRESS_OUTPUTS
            )
            if result.isError(): raise ModbusIOException(f"Modbus error on coil write: {result}")
            return True
        except (ConnectionException, ModbusIOException, asyncio.TimeoutError) as e:
            print(f"Modbus write_coil failed for address {address}: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            await self.disconnect()
            return False