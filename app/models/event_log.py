from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict

from sqlalchemy import Integer, String, Text, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class EventType(PyEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))
    source: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<EventLog(id={self.id}, type={self.event_type}, source='{self.source}')>"
