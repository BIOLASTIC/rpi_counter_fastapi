"""
NEW: Pydantic schemas for API data validation and serialization
for the CameraProfile and ObjectProfile models.

These schemas define the expected request and response bodies for the
profile management API endpoints.
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- CameraProfile Schemas ---

class CameraProfileBase(BaseModel):
    name: str
    exposure: int = 0
    gain: int = 0
    white_balance_temp: int = 0
    brightness: int = 128
    autofocus: bool = True
    description: Optional[str] = None

class CameraProfileCreate(CameraProfileBase):
    pass

class CameraProfileUpdate(CameraProfileBase):
    # All fields are optional for updates
    name: Optional[str] = None
    exposure: Optional[int] = None
    gain: Optional[int] = None
    white_balance_temp: Optional[int] = None
    brightness: Optional[int] = None
    autofocus: Optional[bool] = None

class CameraProfileOut(CameraProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- ObjectProfile Schemas ---

class ObjectProfileBase(BaseModel):
    name: str
    camera_profile_id: int
    sort_offset_ms: int = 0
    description: Optional[str] = None

class ObjectProfileCreate(ObjectProfileBase):
    pass

class ObjectProfileUpdate(ObjectProfileBase):
    name: Optional[str] = None
    camera_profile_id: Optional[int] = None
    sort_offset_ms: Optional[int] = None

class ObjectProfileOut(ObjectProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    # When we output an ObjectProfile, we want to include the full
    # nested CameraProfile object, not just its ID.
    camera_profile: CameraProfileOut