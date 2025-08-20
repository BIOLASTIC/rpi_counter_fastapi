# rpi_counter_fastapi-apintrigation/app/models/__init__.py

"""
Makes key database components available for easy import.
This pattern simplifies imports for sessions, the base model class,
and all defined ORM models.
"""
from .database import Base, get_async_session, engine
from .detection import DetectionEventLog
from .system_status import SystemStatus
from .event_log import EventLog
# --- THIS IS THE FIX ---
# We now import and expose ConfigDataType alongside Configuration.
from .configuration import Configuration, ConfigDataType
# --- END OF FIX ---
from .profiles import CameraProfile, ObjectProfile
from .product import Product, ProductStatus
from .operator import Operator, OperatorStatus
from .run_log import RunLog, RunStatus


__all__ = [
    "Base",
    "get_async_session",
    "engine",
    "DetectionEventLog",
    "SystemStatus",
    "EventLog",
    "Configuration",
    "ConfigDataType", # <-- ADD THIS LINE
    "CameraProfile",
    "ObjectProfile",
    "Product",
    "ProductStatus",
    "Operator",
    "OperatorStatus",
    "RunLog",
    "RunStatus",
]