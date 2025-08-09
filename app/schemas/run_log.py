from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict, List # Import List
from datetime import datetime

from .operators import OperatorOut
from .products import ProductOut
from app.models.run_log import RunStatus

# NEW: Pydantic schema for a detection event log
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

class RunLogOut(RunLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    operator: Optional[OperatorOut] = None
    product: Optional[ProductOut] = None
    # We can optionally include the events here in the future
    # detection_events: List[DetectionEventLogOut] = []