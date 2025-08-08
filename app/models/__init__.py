# box_counter_system/app/models/__init__.py
"""
Makes key database components available for easy import.
This pattern simplifies imports for sessions, the base model class,
and all defined ORM models.
"""
from .database import Base, get_async_session, engine
from .detection import Detection
from .system_status import SystemStatus
from .event_log import EventLog
from .configuration import Configuration
from .profiles import CameraProfile, ObjectProfile
from .product import Product, ProductStatus
from .operator import Operator, OperatorStatus
from .run_log import RunLog, RunStatus


__all__ = [
    "Base",
    "get_async_session",
    "engine",
    "Detection",
    "SystemStatus",
    "EventLog",
    "Configuration",
    "CameraProfile",
    "ObjectProfile",
    "Product",
    "ProductStatus",
    "Operator",
    "OperatorStatus",
    "RunLog",
    "RunStatus",
]