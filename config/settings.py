"""
FINAL REVISION: Restores the missing TIMEOUT_SEC and POLLING_MS
attributes to the ModbusSettings class. This resolves the final
AttributeError on startup.
"""
import json
from functools import lru_cache
from typing import List, Literal, Tuple, Set

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SERVER_')
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = Field(..., min_length=32)

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SECURITY_')
    API_KEY: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')
    URL: str = "sqlite+aiosqlite:///./data/box_counter.db"
    ECHO: bool = False
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 30

class CameraSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_')
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    BUFFER_SIZE: int = 10
    FPS: int = 30

class GpioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='GPIO_PIN_')
    CONVEYOR_RELAY: int = Field(26, ge=2, le=27)
    GATE_RELAY: int = Field(22, ge=2, le=27)
    STATUS_LED_GREEN: int = Field(27, ge=2, le=27)
    STATUS_LED_RED: int = Field(23, ge=2, le=27)
    BUZZER: int = Field(24, ge=2, le=27)
    @model_validator(mode='after')
    def check_for_pin_conflicts(self) -> 'GpioSettings':
        pins: Set[int] = {
            self.CONVEYOR_RELAY, self.GATE_RELAY,
            self.STATUS_LED_GREEN, self.STATUS_LED_RED, self.BUZZER
        }
        if len(pins) < 5: raise ValueError("GPIO pin conflict detected.")
        return self

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_')
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS: int = 1
    # --- DEFINITIVE FIX: Restored the missing fields ---
    TIMEOUT_SEC: float = 1.0
    POLLING_MS: int = 100

class SensorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SENSOR_')
    ENTRY_CHANNEL: int = Field(1, ge=1)
    EXIT_CHANNEL: int = Field(2, ge=1)

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__', extra='ignore')
    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "1.0.0"
    APP_ENV: Literal["development", "production"] = "development"
    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    CAMERA: CameraSettings = CameraSettings()
    GPIO: GpioSettings = GpioSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
