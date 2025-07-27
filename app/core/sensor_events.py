"""
Phase 2.2: Event Handling System for Sensors
Defines the data structures for sensor events using Pydantic for validation
and Enums for clear state representation.
"""
import time
from enum import Enum
from pydantic import BaseModel, Field

class SensorState(str, Enum):
    """Represents the state of a single sensor."""
    TRIGGERED = "triggered" # Object detected
    CLEARED = "cleared"   # No object detected

class SensorEvent(BaseModel):
    """Data model for a sensor state change event."""
    sensor_id: int
    new_state: SensorState
    timestamp: float = Field(default_factory=time.monotonic)
