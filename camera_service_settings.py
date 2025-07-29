"""
NEW STANDALONE configuration file for the camera service.

DEFINITIVE FIX: The main SettingsConfigDict has been updated to be
case-insensitive and to ignore extra fields. This allows this file to
load from the same .env file as the main application without crashing.

NEW: Adds manual camera control settings (SHUTTER_SPEED, ISO, MANUAL_FOCUS).
"""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

nested_config = SettingsConfigDict(case_sensitive=False)

class CameraServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore'
    )

    class CameraSettings(BaseSettings):
        model_config = nested_config
        # Updated Resolution and FPS
        RESOLUTION_WIDTH: int = 1280
        RESOLUTION_HEIGHT: int = 720
        FPS: int = 60
        
        # Existing settings
        JPEG_QUALITY: int = 100

        # --- NEW MANUAL CAMERA CONTROLS ---
        SHUTTER_SPEED: int = Field(0, ge=0)
        ISO: int = Field(0, ge=0)
        MANUAL_FOCUS: float = Field(0.0, ge=0.0)

    class RedisSettings(BaseSettings):
        model_config = nested_config
        HOST: str = 'localhost'
        PORT: int = 6379

    CAMERA: CameraSettings = CameraSettings()
    REDIS: RedisSettings = RedisSettings()


@lru_cache()
def get_camera_service_settings() -> CameraServiceSettings:
    """Creates and caches the settings object."""
    return CameraServiceSettings()

settings = get_camera_service_settings()