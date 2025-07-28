"""
FINAL REVISION: Adds a Pydantic field_validator to the SensorSettings
class. This validator handles cases where a variable in the .env file
might be empty (e.g., SENSORS_EXIT_CHANNEL=). It intelligently substitutes
the default value, preventing the int_parsing ValidationError on startup.
"""
from functools import lru_cache
from typing import Literal, Any
from pydantic import Field, field_validator
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
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 30

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

    # --- DEFINITIVE FIX for empty environment variables ---
    @field_validator('ENTRY_CHANNEL', 'EXIT_CHANNEL', mode='before')
    @classmethod
    def handle_empty_string(cls, v: Any, info) -> Any:
        """If the env var is present but empty, use the default value."""
        if v == '':
            # Return the default value for the field being validated
            return cls.model_fields[info.field_name].default
        return v

class OrchestrationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ORCHESTRATION_', case_sensitive=False)
    POST_BATCH_DELAY_SEC: int = 5

class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_', case_sensitive=False)
    VERBOSE_LOGGING: bool = False

# --- This class is the main container for all settings ---
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)
    
    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "4.1.0-Config-Validation-Fix"
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