"""
NEW STANDALONE configuration file for the camera service.

DEFINITIVE FIX: The main SettingsConfigDict has been updated to be
case-insensitive and to ignore extra fields. This allows this file to
load from the same .env file as the main application without crashing.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# A simple config for the nested classes, as they don't need all the top-level rules.
nested_config = SettingsConfigDict(case_sensitive=False)

class CameraServiceSettings(BaseSettings):
    # This is the main configuration that reads the .env file.
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        case_sensitive=False,  # Allows 'camera__fps' to match 'CAMERA.FPS'
        extra='ignore'         # *** THE CRITICAL FIX *** Ignores variables it doesn't need, like SERVER_HOST.
    )

    # Nested class for Camera settings. Pydantic will look for variables
    # starting with 'CAMERA__' (e.g., CAMERA__RESOLUTION_WIDTH)
    class CameraSettings(BaseSettings):
        model_config = nested_config
        RESOLUTION_WIDTH: int = 640
        RESOLUTION_HEIGHT: int = 480
        FPS: int = 15
        JPEG_QUALITY: int = 85

    # Nested class for Redis settings. Pydantic will look for variables
    # starting with 'REDIS__' (e.g., REDIS__HOST)
    class RedisSettings(BaseSettings):
        model_config = nested_config
        HOST: str = 'localhost'
        PORT: int = 6379

    # These are the only two top-level fields this settings object expects to find.
    CAMERA: CameraSettings = CameraSettings()
    REDIS: RedisSettings = RedisSettings()


@lru_cache()
def get_camera_service_settings() -> CameraServiceSettings:
    """Creates and caches the settings object."""
    return CameraServiceSettings()

# Create a settings object to be imported by the service
settings = get_camera_service_settings()