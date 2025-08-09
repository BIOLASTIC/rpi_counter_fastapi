import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
# This import is needed for the relationship
from .run_log import RunLog

class DetectionEventLog(Base):
    """
    Records a single detection event within a production run.
    This creates a permanent link between a run and its captured images.
    """
    __tablename__ = "detection_event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign key to the run this detection belongs to
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    
    # The run this event belongs to
    run: Mapped["RunLog"] = relationship(back_populates="detection_events")

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<DetectionEventLog(id={self.id}, run_id={self.run_log_id}, image='{self.image_path}')>"