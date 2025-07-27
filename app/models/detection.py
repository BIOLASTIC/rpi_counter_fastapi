import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict

from sqlalchemy import Integer, String, Boolean, Float, DateTime, Enum, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class DetectionDirection(PyEnum):
    FORWARD = "forward"
    REVERSE = "reverse"
    UNKNOWN = "unknown"

class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String, default=lambda: str(uuid.uuid4()), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    box_count: Mapped[int] = mapped_column(Integer, nullable=False)
    
    sensor_1_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    sensor_2_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    
    processing_time_ms: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    
    detection_direction: Mapped[DetectionDirection] = mapped_column(Enum(DetectionDirection), default=DetectionDirection.UNKNOWN)
    box_dimensions: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Detection(id={self.id}, time={self.timestamp}, count={self.box_count})>"
