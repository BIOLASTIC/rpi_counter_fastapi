"""
This file initializes the settings for the main application and derives
the list of active cameras, providing a single source of truth.
"""
from .settings import get_settings

# Create the global settings object for the main app
settings = get_settings()

# Derive the list of active camera IDs from the loaded settings
ACTIVE_CAMERA_IDS = []
# The CAMERA_MODE is read from the .env file by the AppSettings class
if settings.CAMERA_MODE in ['rpi', 'both']:
    ACTIVE_CAMERA_IDS.append('rpi')
if settings.CAMERA_MODE in ['usb', 'both']:
    ACTIVE_CAMERA_IDS.append('usb')

print(f"[Main App Config] Mode: '{settings.CAMERA_MODE}'. Active cameras: {ACTIVE_CAMERA_IDS}")