"""
REVISED: Added the missing `ID` field to the RpiCameraSettings class to ensure
consistency with the standalone camera service configuration.
"""
from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Nested Settings Classes ---

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

class BaseCameraSettings(BaseSettings):
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RpiCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_RPI_', case_sensitive=False)
    ID: str = ""
    SHUTTER_SPEED: int = Field(0, ge=0)
    ISO: int = Field(0, ge=0)
    MANUAL_FOCUS: float = Field(0.0, ge=0.0)

class UsbCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_USB_', case_sensitive=False)
    DEVICE_INDEX: int = 0
    EXPOSURE: int = 0
    GAIN: int = 0
    BRIGHTNESS: int = Field(128, ge=0, le=255)
    AUTOFOCUS: bool = True
    WHITE_BALANCE_TEMP: int = 0

class GpioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='GPIO_', case_sensitive=False)
    PIN_CONVEYOR_RELAY: int = 26
    PIN_GATE_RELAY: int = 22
    PIN_STATUS_LED_GREEN: int = 27
    PIN_STATUS_LED_RED: int = 23
    PIN_BUZZER: int = 24
    # --- NEW: GPIO Pin for the sorting mechanism ---
    PIN_DIVERTER_RELAY: int = 19

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_', case_sensitive=False)
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS: int = 1
    START_ADDRESS: int = 1
    TIMEOUT_SEC: float = 0.2
    POLLING_MS: int = 50
    QUANTITY: int = 4

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

class ConveyorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CONVEYOR_', case_sensitive=False)
    SPEED_M_PER_SEC: float = 0.5
    CAMERA_TO_SORTER_DISTANCE_M: float = 1.2

# --- Main AppSettings Container ---

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)

    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "5.1.0-Profiles-Integration"
    APP_ENV: Literal["development", "production"] = "development"
    CAMERA_MODE: Literal['rpi', 'usb', 'both', 'none'] = 'both'
    CAMERA_TRIGGER_DELAY_MS: int = 100
    CAMERA_CAPTURES_DIR: str = "web/static/captures"
    UI_ANIMATION_TRANSIT_TIME_SEC: int = Field(5, gt=0)


    # Nested configuration objects
    CAMERA_RPI: RpiCameraSettings = RpiCameraSettings()
    CAMERA_USB: UsbCameraSettings = UsbCameraSettings()
    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    GPIO: GpioSettings = GpioSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()
    ORCHESTRATION: OrchestrationSettings = OrchestrationSettings()
    LOGGING: LoggingSettings = LoggingSettings()
    CONVEYOR: ConveyorSettings = ConveyorSettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()