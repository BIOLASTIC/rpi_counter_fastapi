"""
NEW: Database models for storing dynamic camera and object profiles.
This allows for on-the-fly management of "recipes" for different
production runs.
"""
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class CameraProfile(Base):
    """
    Stores a complete set of hardware settings for a camera.
    This can be reused across multiple object profiles.
    """
    __tablename__ = "camera_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Camera hardware settings
    exposure: Mapped[int] = mapped_column(Integer, default=0)
    gain: Mapped[int] = mapped_column(Integer, default=0)
    white_balance_temp: Mapped[int] = mapped_column(Integer, default=0)
    brightness: Mapped[int] = mapped_column(Integer, default=128)
    autofocus: Mapped[bool] = mapped_column(Boolean, default=True)
    
    description: Mapped[Optional[str]] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"<CameraProfile(id={self.id}, name='{self.name}')>"


class ObjectProfile(Base):
    """
    The master "recipe" for a production run. It defines an object's
    name, its sorting logic, and links to a specific camera profile.
    """
    __tablename__ = "object_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Foreign key to link to a camera hardware configuration
    camera_profile_id: Mapped[int] = mapped_column(ForeignKey("camera_profiles.id"))
    
    # Sorting logic for this specific object
    sort_offset_ms: Mapped[int] = mapped_column(Integer, default=0, comment="Time adjustment in ms for sorting (+/- from base travel time)")
    
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # SQLAlchemy relationship to easily access the linked CameraProfile object
    camera_profile: Mapped["CameraProfile"] = relationship()

    def __repr__(self) -> str:
        return f"<ObjectProfile(id={self.id}, name='{self.name}')>"