# box_counter_system/config/__init__.py
"""
Initializes the settings object for global access.
This makes it easy to import the application settings from anywhere
in the project using `from config import settings`.
"""
from .settings import get_settings

settings = get_settings()
