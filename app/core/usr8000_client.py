"""
FINAL REVISION: The Modbus client has been rewritten to be more robust
and self-healing. It now ensures a connection before every read and handles
ConnectionExceptions and Timeouts gracefully, which was the root cause
of the "stuck" sensor state problem.
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
        # --- DIAGNOSTIC LOGGING ---
        print("--- USR-IO Modbus Client Initialized with a Read Address of 0 ---")

    async def connect(self) -> bool:
        if self._is_connected:
            return True
        try:
            # The 'await' is crucial here for the async client
            is_connected = await self.client.connect()
            if is_connected:
                self._is_connected = True
                return True
            else:
                self._is_connected = False
                return False
        except Exception as e:
            print(f"USR-8000 Real Client: Error during connection attempt: {e}")
            self._is_connected = False
            return False

    async def disconnect(self) -> None:
        """Closes the Modbus connection."""
        if self._is_connected:
            self.client.close()
            self._is_connected = False

    async def read_input_channels(self) -> Optional[Dict[int, bool]]:
        """
        Reads all discrete input channels from the hardware. This method
        is now designed to be self-healing and robust against connection drops.
        """
        # --- DEFINITIVE FIX: Ensure connection before every read ---
        if not await self.connect():
            # If we can't even connect, fail immediately.
            return None
        
        try:
            # --- THE CRITICAL CHANGE: Trying address 0 as a final test ---
            # Some devices use 0-based indexing for the protocol despite 1-based documentation.
            result = await self.client.read_discrete_inputs(
                address=0, count=self._config.QUANTITY, slave=self._config.DEVICE_ADDRESS
            )

            if result.isError():
                print(f"USR-8000 Real Client: Modbus read error: {result}")
                # An error suggests the connection might be bad, so disconnect.
                await self.disconnect()
                return None
            
            # This is a list of booleans.
            bits = result.bits[:self._config.QUANTITY]
            return {i + 1: bits[i] for i in range(len(bits))}

        except ConnectionException as e:
            print(f"USR-8000 Real Client: Connection lost during read: {e}. Will attempt to reconnect on next poll.")
            await self.disconnect() # Force a full reconnect next time
            return None
        except asyncio.TimeoutError:
            print("USR-8000 Real Client: Read timed out. Check wiring and device status.")
            await self.disconnect() # Force a full reconnect next time
            return None
        except Exception as e:
            print(f"USR-8000 Real Client: Unhandled error during read: {e}")
            await self.disconnect() # Force a full reconnect next time
            return None

    async def get_module_status(self) -> ModuleHealthStatus:
        if self._is_connected:
            return ModuleHealthStatus.CONNECTED
        return ModuleHealthStatus.DISCONNECTED