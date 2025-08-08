from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime

from .operators import OperatorOut
from .products import ProductOut
from app.models.run_log import RunStatus

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