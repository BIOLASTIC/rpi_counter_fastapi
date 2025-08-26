# rpi_counter_fastapi/config/settings.py

from functools import lru_cache
from typing import Literal, Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Nested Settings Classes for Core Components ---

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SERVER_', case_sensitive=False)
    HOST: str = "0.0.0.0"
    PORT: int = 8000

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SECURITY_', case_sensitive=False)
    API_KEY: str = "your_secret_api_key_here"
    JWT_SECRET_KEY: str = Field("a_very_secret_key_that_is_at_least_32_chars_long", min_length=32)
    JWT_ALGORITHM: str = "HS256"

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_', case_sensitive=False)
    URL: str = "sqlite+aiosqlite:///./data/box_counter.db"
    ECHO: bool = False
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 30

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_', case_sensitive=False)
    HOST: str = "localhost"
    PORT: int = 6379

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

class AiApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AI_API_', case_sensitive=False)
    BASE_URL: str = "http://192.168.88.97:3001"
    # --- FIX: Changed QC_MODEL_ID to a list to support multiple models ---
    QC_MODEL_IDS: List[str] = ["yolo11m_qc", "yolo11m_categories"]

class LlmApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LLM_API_', case_sensitive=False)
    BASE_URL: str = "http://192.168.88.81:8000"

class TtsApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TTS_API_', case_sensitive=False)
    BASE_URL: str = "http://localhost:5003"

class OutputChannelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OUTPUTS_', case_sensitive=False)
    CONVEYOR: int = 0
    GATE: int = 1
    DIVERTER: int = 2
    LED_GREEN: int = 3
    LED_RED: int = 4
    CAMERA_LIGHT: int = 5
    BUZZER: int = 6
    CAMERA_LIGHT_TWO: int = 7

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_', case_sensitive=False)
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS_INPUTS: int = 1
    DEVICE_ADDRESS_OUTPUTS: int = 2
    TIMEOUT_SEC: float = 0.5
    POLLING_MS: int = 50

class SensorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SENSORS_', case_sensitive=False)
    ENTRY_CHANNEL: int = 1
    EXIT_CHANNEL: int = 3

class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_', case_sensitive=False)
    VERBOSE_LOGGING: bool = False

class BuzzerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BUZZER_', case_sensitive=False)
    MISMATCH_MS: int = Field(500, description="Buzzer duration in ms for a product size mismatch.")
    MANUAL_TOGGLE_MS: int = Field(200, description="Buzzer duration in ms for a manual toggle from the UI.")
    LOOP_COMPLETE_MS: int = Field(1000, description="Buzzer duration in ms when a batch loop completes.")
    EXIT_SENSOR_MS: int = Field(150, description="Buzzer duration in ms when the exit sensor is triggered.")

class ConveyorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CONVEYOR_', case_sensitive=False)
    SPEED_M_PER_SEC: float = 0.5
    CAMERA_TO_SORTER_DISTANCE_M: float = 1.0
    CONVEYOR_AUTO_STOP_DELAY_SEC: int = Field(2, description="How many seconds the conveyor runs after the last box of a batch is counted before stopping.")
    MAX_TRANSIT_TIME_SEC: float = Field(15.0, gt=0, description="Max time for a product to travel from entry to exit before a failure is triggered.")

class AiStrategySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AI_STRATEGY_', case_sensitive=False)
    YOLO_ENABLED: bool = Field(True, description="Enable/disable the primary YOLO QC analysis.")
    LLM_ENABLED: bool = Field(True, description="Enable/disable all LLM-based summarization features.")
    TTS_ENABLED: bool = Field(True, description="Enable/disable all Text-to-Speech audio feedback.")
    LANGUAGE: str = Field("english", description="LLM Language (full name, e.g., 'english', 'bengali').")
    TTS_LANGUAGE: str = Field("en", description="TTS Language (short code, e.g., 'en', 'bn').")
    REALTIME_TTS_ENGINE: Literal["mac", "xtts", "parler"] = Field("mac", description="TTS engine for instant, per-item feedback.")
    ALERT_ON_PASS: bool = Field(False, description="Enable audio alert for every accepted item.")
    ALERT_ON_REJECT: bool = Field(True, description="Enable audio alert for every rejected item.")
    PASS_TEMPLATE: str = Field("Item {count} accepted.", description="Text template for accepted items.")
    REJECT_TEMPLATE: str = Field("Item {count} rejected. Reason: {defects}.", description="Text template for rejected items.")
    LLM_ITEM_ANALYSIS_ENABLED: bool = Field(True, description="Enable background LLM analysis for each item.")
    LLM_ITEM_WORD_COUNT: int = Field(25, description="Target word count for the per-item LLM summary.")
    SUMMARY_TTS_ENGINE: Literal["parler", "xtts", "mac"] = Field("parler", description="High-quality TTS engine for the end-of-batch summary.")
    SUMMARY_LLM_MODEL: Literal["realtime", "high_quality"] = Field("high_quality", description="LLM model for generating the batch summary.")
    LLM_SUMMARY_WORD_COUNT: int = Field(75, description="Target word count for the detailed batch report.")
    TTS_SUMMARY_CHUNK_COUNT: int = Field(4, ge=1, le=10, description="Number of chunks to split the LLM summary into for pipelined TTS playback.")
    BATCH_COMPLETE_TEMPLATE: str = Field(
        "Batch {batch_id} for {product_name} complete. Total Items: {total_items}, Rejects: {reject_count}.",
        description="Text spoken immediately after a batch finishes."
    )
    NEXT_BATCH_TEMPLATE: str = Field(
        "Next run starting in {countdown}.",
        description="Text spoken before the next batch starts."
    )
    LLM_PROMPT_TEMPLATE: str = Field(
        "You are a helpful assistant on a factory floor. Summarize the following production batch results "
        "with an encouraging but honest tone for the operator. The top defect was {top_defect}. "
        "Batch details: {batch_data}",
        description="The master instruction given to the LLM for batch summarization."
    )

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)
    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "12.0.0-HybridAI"
    APP_ENV: Literal["development", "production"] = "development"
    TIMEZONE: str = "UTC"
    CAMERA_MODE: Literal['rpi', 'usb', 'both', 'none'] = 'both'
    CAMERA_TRIGGER_DELAY_MS: int = 100
    CAMERA_CAPTURES_DIR: str = "web/static/captures"
    UI_ANIMATION_TRANSIT_TIME_SEC: int = Field(5, gt=0)
    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    REDIS: RedisSettings = RedisSettings()
    CAMERA_RPI: RpiCameraSettings = RpiCameraSettings()
    CAMERA_USB: UsbCameraSettings = UsbCameraSettings()
    AI_API: AiApiSettings = AiApiSettings()
    LLM_API: LlmApiSettings = LlmApiSettings()
    TTS_API: TtsApiSettings = TtsApiSettings()
    OUTPUTS: OutputChannelSettings = OutputChannelSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()
    LOGGING: LoggingSettings = LoggingSettings()
    CONVEYOR: ConveyorSettings = ConveyorSettings()
    BUZZER: BuzzerSettings = BuzzerSettings()
    AI_STRATEGY: AiStrategySettings = AiStrategySettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()