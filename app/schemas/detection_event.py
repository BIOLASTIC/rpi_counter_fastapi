# rpi_counter_fastapi-dev_new/app/schemas/detection_event.py

from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import Optional
import pytz

from app.models.detection_event import QCResult
from config import settings

# --- Timezone Conversion Helper ---
try:
    LOCAL_TZ = pytz.timezone(settings.TIMEZONE)
except pytz.UnknownTimeZoneError:
    LOCAL_TZ = pytz.utc
# ----------------------------------

class DetectionEventBase(BaseModel):
    timestamp: datetime
    image_path: Optional[str] = None
    qc_result: QCResult
    qc_reason: Optional[str] = None

class DetectionEventOut(DetectionEventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    run_log_id: int

    # --- NEW COMPUTED FIELD FOR LOCAL TIME DISPLAY ---
    @computed_field
    @property
    def timestamp_local(self) -> str:
        """Returns a formatted string of the event time in the configured local timezone."""
        if not self.timestamp:
            return ""
        utc_dt = pytz.utc.localize(self.timestamp)
        local_dt = utc_dt.astimezone(LOCAL_TZ)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S')
    # ----------------------------------------------------