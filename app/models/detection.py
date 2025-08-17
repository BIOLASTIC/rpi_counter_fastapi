# rpi_counter_fastapi-dev2/app/models/detection.py

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .run_log import RunLog

class DetectionEventLog(Base):
    """
    Records a single detection event within a production run.
    This creates a permanent link between a run and its captured images.
    """
    __tablename__ = "detection_event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # --- NEW: Unique identifier for this specific detection event ---
    serial_number: Mapped[str] = mapped_column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    run: Mapped["RunLog"] = relationship(back_populates="detection_events")

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    
    # --- NEW: Path for the annotated image after QC analysis ---
    annotated_image_path: Mapped[str] = mapped_column(String, nullable=True)

    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<DetectionEventLog(id={self.id}, serial_number='{self.serial_number}')>"