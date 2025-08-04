from functools import lru_cache
from typing import Literal, Dict
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Define the absolute path to the .env file
ENV_PATH = Path(__file__).parent.parent / ".env"

# Define a base configuration that ALL settings classes will use
BASE_CONFIG_DICT = {
    'env_file': str(ENV_PATH),
    'extra': 'ignore',
    'case_sensitive': False
}

# --- Nested Settings Classes ---

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='SERVER_')
    # ... (rest of the class is unchanged)
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = Field(..., min_length=32)

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='SECURITY_')
    API_KEY: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='DB_')
    URL: str = "sqlite+aiosqlite:///./data/box_counter.db"
    ECHO: bool = False

class AiHatSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='AI_HAT_')
    MODEL_PATH: str
    CONFIDENCE_THRESHOLD: float

class CameraPipelineSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT)
    CAMERA_WIDTH: int = 1280
    CAMERA_HEIGHT: int = 720
    CAMERA_FRAMERATE: int = 30

class OutputChannelSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='OUTPUTS_')
    # ... (rest of the class is unchanged)
    CONVEYOR: int = 0
    GATE: int = 1
    DIVERTER: int = 2
    LED_GREEN: int = 3
    LED_RED: int = 4
    CAMERA_LIGHT: int = 5
    BUZZER: int = 6

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='MODBUS_')
    # ... (rest of the class is unchanged)
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS_INPUTS: int = 1
    DEVICE_ADDRESS_OUTPUTS: int = 2
    TIMEOUT_SEC: float = 0.5
    POLLING_MS: int = 50

class SensorSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='SENSORS_')
    ENTRY_CHANNEL: int = 1
    EXIT_CHANNEL: int = 3

class OrchestrationSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='ORCHESTRATION_')
    POST_BATCH_DELAY_SEC: int = 5

class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='LOGGING_')
    VERBOSE_LOGGING: bool = False

class ConveyorSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT, env_prefix='CONVEYOR_')
    SPEED_M_PER_SEC: float = 0.5
    CAMERA_TO_SORTER_DISTANCE_M: float = 1.0

class RedisKeys(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT)
    AI_ENABLED_KEY: str = "ai_service:enabled"
    AI_HEALTH_KEY: str = "ai_service:health_status"
    AI_DETECTION_SOURCE_KEY: str = "ai_service:detection_source"
    # --- DEFINITIVE FIX: Add the missing key definition ---
    AI_LAST_DETECTION_RESULT_KEY: str = "ai_service:last_detection_result"


# --- Main AppSettings Container ---
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(**BASE_CONFIG_DICT)
    # ... (rest of the class is unchanged)
    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "12.3.0-Last-Detection-Fix"
    APP_ENV: Literal["development", "production"] = "development"
    AI_DETECTION_SOURCE: Literal['rpi'] = 'rpi'
    CAMERA_CAPTURES_DIR: str = "web/static/captures"
    UI_ANIMATION_TRANSIT_TIME_SEC: int = Field(5, gt=0)
    AI_SERVICE_ENABLED_BY_DEFAULT: bool = True

    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    AI_HAT: AiHatSettings = AiHatSettings()
    CAMERA: CameraPipelineSettings = CameraPipelineSettings()
    OUTPUTS: OutputChannelSettings = OutputChannelSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()
    ORCHESTRATION: OrchestrationSettings = OrchestrationSettings()
    LOGGING: LoggingSettings = LoggingSettings()
    CONVEYOR: ConveyorSettings = ConveyorSettings()
    REDIS_KEYS: RedisKeys = RedisKeys()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()