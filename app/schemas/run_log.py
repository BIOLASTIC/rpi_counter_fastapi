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
    serial_number: str
    annotated_image_path: Optional[str] = None
    
    # Expose the correct 'details' field from the database model.
    details: Optional[Dict[str, Any]] = None

class RunLogBase(BaseModel):
    batch_code: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    status: RunStatus
    object_profile_snapshot: Optional[Dict[str, Any]] = None

class RunLogOut(RunLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    operator: Optional[OperatorOut] = None
    product: Optional[ProductOut] = None
    
    detected_items_count: int = 0
    duration_seconds: Optional[int] = None

    @field_validator('object_profile_snapshot', mode='before')
    def extract_target_count(cls, v):
        if isinstance(v, dict):
            return v 
        return {}