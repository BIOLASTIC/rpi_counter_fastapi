# rpi_counter_fastapi-dev2/app/schemas/run_log.py

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Any, Dict, List
from datetime import datetime

from .operators import OperatorOut
from .products import ProductOut
from app.models.run_log import RunStatus

class DetectionEventLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime
    image_path: Optional[str] = None

class RunLogBase(BaseModel):
    batch_code: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    status: RunStatus
    object_profile_snapshot: Optional[Dict[str, Any]] = None

# --- THIS IS THE FIX ---
# The RunLogOut schema is updated to include the new fields that the API is trying to add.
class RunLogOut(RunLogBase):
    """
    Represents a single, detailed entry in the run history report.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    operator: Optional[OperatorOut] = None
    product: Optional[ProductOut] = None
    
    # --- NEW FIELDS FOR DETAILED REPORTING ---
    # These fields were missing, causing the ValueError. They are now correctly defined.
    detected_items_count: int = 0
    duration_seconds: Optional[int] = None
    # --- END NEW FIELDS ---

    # This validator handles the case where object_profile_snapshot might be None
    # and extracts the target_count safely.
    @field_validator('object_profile_snapshot', mode='before')
    def extract_target_count(cls, v):
        if isinstance(v, dict):
            # The original snapshot from the DB is preserved
            return v 
        return {}