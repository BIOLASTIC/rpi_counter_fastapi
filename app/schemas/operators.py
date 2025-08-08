from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.operator import OperatorStatus


class OperatorBase(BaseModel):
    name: str
    status: OperatorStatus = OperatorStatus.ACTIVE

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[OperatorStatus] = None

class OperatorOut(OperatorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime