"""
Centralized Pydantic v2 settings management for the application.
REVISED: Added a new SensorSettings class for channel mapping.
"""
import json
from functools import lru_cache
from typing import List, Literal, Tuple, Set

from pydantic import Field, field_validator, model_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SERVER_')
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = Field(..., min_length=32)
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000"]
    @field_validator('CORS_ORIGINS', mode='before')
    def assemble_cors_origins(cls, v):
        if isinstance(v, str): return json.loads(v)
        return v

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SECURITY_')
    API_KEY: str
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"

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
    FPS: int = 30
    BUFFER_SIZE: int = 10

class GpioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='GPIO_PIN_')
    CONVEYOR_RELAY: int = 26
    GATE_RELAY: int = 22
    STATUS_LED_GREEN: int = 27
    STATUS_LED_RED: int = 23
    BUZZER: int = 24
    @model_validator(mode='after')
    def check_for_pin_conflicts(self) -> 'GpioSettings':
        pins: Set[int] = {self.CONVEYOR_RELAY, self.GATE_RELAY, self.STATUS_LED_GREEN, self.STATUS_LED_RED, self.BUZZER}
        if len(pins) < 5: raise ValueError("GPIO pin conflict detected.")
        return self

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_')
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS: int = 1
    TIMEOUT_SEC: float = 1.0
    POLLING_MS: int = 100
    @field_validator('BAUDRATE')
    @classmethod
    def baudrate_must_be_standard(cls, v: int) -> int:
        allowed_rates = {4800, 9600, 19200, 38400}
        if v not in allowed_rates:
            raise ValueError(f"Invalid baudrate. Must be one of {allowed_rates}")
        return v

class DetectionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DETECTION_')
    CONFIDENCE_THRESHOLD: float = 0.85
    BOX_MIN_AREA: int = 5000
    BOX_MAX_AREA: int = 50000

# --- NEW SENSOR MAPPING CONFIGURATION ---
class SensorSettings(BaseSettings):
    """Maps physical sensor channels to their logical purpose."""
    model_config = SettingsConfigDict(env_prefix='SENSOR_')
    
    ENTRY_CHANNEL: int = Field(1, ge=1, description="The USR-8000 channel number for the entry sensor.")
    EXIT_CHANNEL: int = Field(2, ge=1, description="The USR-8000 channel number for the exit sensor.")

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
    DETECTION: DetectionSettings = DetectionSettings()
    # Add the new settings object
    SENSORS: SensorSettings = SensorSettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
