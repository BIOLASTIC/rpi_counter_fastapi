"""
STANDALONE configuration file for the camera services.
REVISED: Added logic to derive ACTIVE_CAMERA_IDS for the services.
"""
from functools import lru_cache
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# --- THE FIX: Create a robust, absolute path to the .env file ---
# This ensures the .env file is found regardless of where the script is executed.
ENV_PATH = Path(__file__).parent.parent / ".env"

# --- Add a diagnostic print statement ---
if ENV_PATH.exists():
    print(f"[Camera Config] Loading settings from: {ENV_PATH}")
else:
    print(f"[Camera Config] WARNING: .env file not found at {ENV_PATH}. Using default values.")


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
    EXPOSURE: int = 0
    GAIN: int = 0
    # Corrected the default brightness to be within the valid 0-255 range
    BRIGHTNESS: int = Field(128, ge=0, le=255) 
    AUTOFOCUS: bool = True

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_', case_sensitive=False)
    HOST: str = 'localhost'
    PORT: int = 6379

# --- Main Settings Container for Camera Services ---

class CameraServicesSettings(BaseSettings):
    # --- THE FIX: Use the robust, absolute path ---
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), extra='ignore', case_sensitive=False)
    
    CAMERA_MODE: str = 'both'
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