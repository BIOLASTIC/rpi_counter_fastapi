# rpi_counter_fastapi-dev_new/app/models/detection_event.py

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from typing import TYPE_CHECKING # <-- Import TYPE_CHECKING

from .database import Base

# --- THIS IS THE FIX (PART 2) ---
if TYPE_CHECKING:
    from .run_log import RunLog
# --- END OF FIX ---


class QCResult(PyEnum):
    PENDING = "Pending"
    PASS = "Pass"
    FAIL = "Fail"

class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    
    qc_result: Mapped[QCResult] = mapped_column(Enum(QCResult), default=QCResult.PENDING)
    qc_reason: Mapped[str] = mapped_column(String, nullable=True)

    run_log: Mapped["RunLog"] = relationship(back_populates="detection_events")

    def __repr__(self) -> str:
        return f"<DetectionEvent(id={self.id}, run_log_id={self.run_log_id}, image_path='{self.image_path}')>"