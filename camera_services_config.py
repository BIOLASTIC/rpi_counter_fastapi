"""
STANDALONE configuration file for the camera services.
REVISED: Added logic to derive ACTIVE_CAMERA_IDS for the services.
"""
from functools import lru_cache
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Reusable Base Classes ---

class BaseCameraSettings(BaseSettings):
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RpiCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_RPI_', case_sensitive=False)
    SHUTTER_SPEED: int = Field(0, ge=0)
    ISO: int = Field(0, ge=0)
    MANUAL_FOCUS: float = Field(0.0, ge=0.0)

class UsbCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_USB_', case_sensitive=False)
    DEVICE_INDEX: int = 0

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_', case_sensitive=False)
    HOST: str = 'localhost'
    PORT: int = 6379

# --- Main Settings Container for Camera Services ---

class CameraServicesSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)
    CAMERA_MODE: str = 'both' # Load the camera mode from .env
    CAMERA_RPI: RpiCameraSettings = RpiCameraSettings()
    CAMERA_USB: UsbCameraSettings = UsbCameraSettings()
    REDIS: RedisSettings = RedisSettings()

@lru_cache()
def get_camera_services_settings() -> CameraServicesSettings:
    return CameraServicesSettings()

# Create a single settings object to be imported by the services
settings = get_camera_services_settings()

# --- Derive the list of active camera IDs for the services ---
ACTIVE_CAMERA_IDS = []
if settings.CAMERA_MODE in ['rpi', 'both']:
    ACTIVE_CAMERA_IDS.append('rpi')
if settings.CAMERA_MODE in ['usb', 'both']:
    ACTIVE_CAMERA_IDS.append('usb')