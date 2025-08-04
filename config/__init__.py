"""
This file initializes the settings for the main application and defines
the list of active cameras, providing a single source of truth for the UI.

UPDATED for AI HAT Pipeline Architecture: The concept of a selectable
'CAMERA_MODE' is obsolete. The system now has a single, fixed camera
source provided by the `rpicam-vid` pipeline, which we identify as 'rpi'.
"""
from .settings import get_settings

# Create the global settings object for the main app
settings = get_settings()

# In the new architecture, there is only one active camera source,
# which is the stream coming from the AI HAT pipeline. We statically
# define this as 'rpi' so that the web interface (e.g., the navbar)
# can correctly render links for it.
ACTIVE_CAMERA_IDS = ['rpi']

print(f"[Main App Config] Architecture: AI HAT Pipeline. Active camera source: {ACTIVE_CAMERA_IDS}")