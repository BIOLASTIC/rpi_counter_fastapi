# rpi_counter_fastapi-apinaudio/app/schemas/run_log.py

from pydantic import BaseModel, ConfigDict, field_validator, computed_field
from typing import Optional, Any, Dict, List
from datetime import datetime
import pytz

from .operators import OperatorOut
from .products import ProductOut
from app.models.run_log import RunStatus
from config import settings

# --- THIS IS THE FIX: TIMEZONE CONVERSION LOGIC ---
try:
    LOCAL_TZ = pytz.timezone(settings.TIMEZONE)
except pytz.UnknownTimeZoneError:
    # Fallback to UTC if the timezone in .env is invalid
    LOCAL_TZ = pytz.utc
# --- END OF FIX ---

class DetectionEventLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime
    image_path: Optional[str] = None
    serial_number: str
    annotated_image_path: Optional[str] = None
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

    # --- NEW COMPUTED FIELD FOR LOCAL TIME DISPLAY ---
    @computed_field
    @property
    def start_timestamp_local(self) -> str:
        """Returns a formatted string of the start time in the configured local timezone."""
        if not self.start_timestamp:
            return "N/A"
        # Assume DB time is naive UTC, localize it, then convert
        utc_dt = pytz.utc.localize(self.start_timestamp)
        local_dt = utc_dt.astimezone(LOCAL_TZ)
        return local_dt.strftime('%d/%m/%Y, %H:%M:%S')

    @field_validator('object_profile_snapshot', mode='before')
    def extract_target_count(cls, v):
        if isinstance(v, dict):
            return v 
        return {}