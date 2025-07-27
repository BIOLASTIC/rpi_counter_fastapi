from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, Float, Boolean, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class CameraStatus(PyEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class GatePosition(PyEnum):
    OPEN = "open"
    CLOSED = "closed"
    MOVING = "moving"
    ERROR = "error"

class SystemStatus(Base):
    __tablename__ = "system_status_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    cpu_usage: Mapped[float] = mapped_column(Float)
    memory_usage: Mapped[float] = mapped_column(Float)
    disk_usage: Mapped[float] = mapped_column(Float)
    cpu_temperature: Mapped[float] = mapped_column(Float)
    
    camera_status: Mapped[CameraStatus] = mapped_column(Enum(CameraStatus))
    conveyor_running: Mapped[bool] = mapped_column(Boolean)
    gate_position: Mapped[GatePosition] = mapped_column(Enum(GatePosition))
    
    uptime_seconds: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"<SystemStatus(id={self.id}, time={self.timestamp})>"
