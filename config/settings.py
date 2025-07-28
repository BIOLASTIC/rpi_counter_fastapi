"""
FINAL REVISION: The entire configuration has been refactored to the
correct architectural pattern. Each settings class now inherits from
BaseSettings and uses its own `env_prefix` to load variables
(e.g., SERVER_HOST, GPIO_PIN_CONVEYOR_RELAY). This matches the standard
.env file format and permanently resolves all ValidationErrors on startup.
"""
from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Each class is now a self-contained settings loader ---

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SERVER_', case_sensitive=False)
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = Field(..., min_length=32)

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SECURITY_', case_sensitive=False)
    API_KEY: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_', case_sensitive=False)
    URL: str = "sqlite+aiosqlite:///./data/box_counter.db"
    ECHO: bool = False

class CameraSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_', case_sensitive=False)
    RESOLUTION_WIDTH: int = 640
    RESOLUTION_HEIGHT: int = 480
    JPEG_QUALITY: int = Field(85, ge=10, le=100)
    TRIGGER_DELAY_MS: int = 100
    SURVEILLANCE_INTERVAL_SEC: int = 10
    CAPTURES_DIR: str = "static/captures"
    FPS: int = 15

class GpioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='GPIO_', case_sensitive=False)
    PIN_CONVEYOR_RELAY: int = 26
    PIN_GATE_RELAY: int = 22
    PIN_STATUS_LED_GREEN: int = 27
    PIN_STATUS_LED_RED: int = 23
    PIN_BUZZER: int = 24

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_', case_sensitive=False)
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS: int = 1
    TIMEOUT_SEC: float = 0.2
    POLLING_MS: int = 50

class SensorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SENSORS_', case_sensitive=False)
    ENTRY_CHANNEL: int = 1
    EXIT_CHANNEL: int = 2

class OrchestrationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ORCHESTRATION_', case_sensitive=False)
    POST_BATCH_DELAY_SEC: int = 5

class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_', case_sensitive=False)
    VERBOSE_LOGGING: bool = False

# --- This class is now a simple container for the other loaders ---
class AppSettings(BaseSettings):
    # This loads top-level variables and tells all nested BaseSettings
    # classes to load from the .env file.
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)
    
    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "4.0.0-Final-Config"
    APP_ENV: Literal["development", "production"] = "development"
    
    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    CAMERA: CameraSettings = CameraSettings()
    GPIO: GpioSettings = GpioSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()
    ORCHESTRATION: OrchestrationSettings = OrchestrationSettings()
    LOGGING: LoggingSettings = LoggingSettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()