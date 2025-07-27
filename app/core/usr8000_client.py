"""
FINAL REVISION: The Modbus client now correctly reads all 8 discrete
inputs and maps them to their proper channel numbers (1-8). This resolves
the bug where the app was blind to the status of higher-numbered channels.
"""
import asyncio
from enum import Enum
from typing import Dict, Optional

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException
from pymodbus.framer import ModbusRtuFramer

class ModuleHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncUSRIOController:
    """Real asynchronous client for the USR-8000 IO Controller."""
    def __init__(self):
        from config import settings
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
        self._is_connected = False
        print(f"USR-8000 Real Client: Initialized for port {self._config.PORT}")

    async def connect(self) -> bool:
        if self._is_connected:
            return True
        print("USR-8000 Real Client: Attempting to connect...")
        try:
            is_connected = await self.client.connect()
            if is_connected:
                self._is_connected = True
                print("USR-8000 Real Client: Connection successful.")
                return True
            else:
                print("USR-8000 Real Client: Connection failed.")
                return False
        except Exception as e:
            print(f"USR-8000 Real Client: Error during connection: {e}")
            return False

    async def disconnect(self) -> None:
        """Closes the Modbus connection."""
        if self._is_connected:
            self.client.close()
            self._is_connected = False

    async def read_input_channels(self) -> Optional[Dict[int, bool]]:
        """Reads all 8 discrete input channels from the hardware."""
        if not self._is_connected:
            if not await self.connect():
                return None
        
        try:
            # --- DEFINITIVE FIX FOR SENSOR READING ---
            # Read all 8 inputs starting from address 0.
            # This matches the screenshot and the hardware manual.
            result = await self.client.read_discrete_inputs(
                address=0, count=8, slave=self._config.DEVICE_ADDRESS
            )

            if result.isError():
                print(f"USR-8000 Real Client: Modbus read error: {result}")
                return None
            
            # Create a dictionary mapping the channel number (1-8) to its boolean state.
            # result.bits is a list where index 0 is Input 1, index 1 is Input 2, etc.
            return {i + 1: result.bits[i] for i in range(len(result.bits))}

        except ConnectionException as e:
            print(f"USR-8000 Real Client: Connection lost during read: {e}")
            self._is_connected = False
            return None
        except asyncio.TimeoutError:
            print("USR-8000 Real Client: Read timed out. Check wiring and device status.")
            return None
        except Exception as e:
            print(f"USR-8000 Real Client: Unhandled error during read: {e}")
            return None

    async def get_module_status(self) -> ModuleHealthStatus:
        if self._is_connected:
            return ModuleHealthStatus.CONNECTED
        return ModuleHealthStatus.DISCONNECTED
