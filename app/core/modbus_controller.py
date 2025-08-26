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
                port=self._config.PORT, framer=ModbusRtuFramer,
                baudrate=self._config.BAUDRATE, bytesize=8, parity="N", stopbits=1,
                timeout=self._config.TIMEOUT_SEC,
            )
            self.initialized = True
            self.health_status = ModbusHealthStatus.DISCONNECTED
            self._is_connected = False
            self._output_name_to_address_map = {k.lower(): v for k, v in settings.OUTPUTS.model_dump().items()}
            print("--- Modbus Controller Initialized ---")
            print(f"    Loaded output map: {self._output_name_to_address_map}")

    @classmethod
    async def get_instance(cls) -> 'AsyncModbusController':
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def get_output_address(self, name: str) -> Optional[int]:
        return self._output_name_to_address_map.get(name.lower())

    async def connect(self) -> bool:
        if self._is_connected: return True
        try:
            is_connected = await self.client.connect()
            if is_connected:
                print("Modbus Controller: Successfully connected to serial port.")
                self.health_status = ModbusHealthStatus.OK
                self._is_connected = True
                return True
            else:
                print(f"Modbus Controller: Failed to connect to serial port {self._config.PORT}.")
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
        """Reads discrete inputs. Assumes connection is already established."""
        # --- THIS IS THE FIX: REMOVED connect() and disconnect() calls ---
        if not self._is_connected: return None
        try:
            result = await self.client.read_discrete_inputs(address=0, count=4, slave=self._config.DEVICE_ADDRESS_INPUTS)
            if result.isError(): raise ModbusIOException(f"Modbus error on input read: {result}")
            return result.bits[:4] if result.bits else [True] * 4
        except (ModbusIOException, ConnectionException) as e:
            print(f"Modbus read_digital_inputs failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False  # Mark connection as broken
            return None
        # --- END OF FIX ---

    async def read_coils(self) -> Optional[List[bool]]:
        """Reads coils. Assumes connection is already established."""
        # --- THIS IS THE FIX: REMOVED connect() and disconnect() calls ---
        if not self._is_connected: return None
        try:
            result = await self.client.read_coils(address=0, count=8, slave=self._config.DEVICE_ADDRESS_OUTPUTS)
            if result.isError(): raise ModbusIOException(f"Modbus error on coil read: {result}")
            return result.bits[:8] if result.bits else [False] * 8
        except (ModbusIOException, ConnectionException) as e:
            print(f"Modbus read_coils failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False # Mark connection as broken
            return None
        # --- END OF FIX ---

    async def write_coil(self, address: int, state: bool) -> bool:
        """Writes a single coil. Assumes connection is already established."""
        # --- THIS IS THE FIX: REMOVED connect() and disconnect() calls ---
        if not self._is_connected: return False
        try:
            result = await self.client.write_coil(address=address, value=state, slave=self._config.DEVICE_ADDRESS_OUTPUTS)
            if result.isError(): raise ModbusIOException(f"Modbus error on coil write: {result}")
            return True
        except (ModbusIOException, ConnectionException) as e:
            print(f"Modbus write_coil failed for address {address}: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False # Mark connection as broken
            return False
        # --- END OF FIX ---