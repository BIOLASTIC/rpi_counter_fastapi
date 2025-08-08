from datetime import datetime
from sqlalchemy import Integer, String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum

from .database import Base

class OperatorStatus(PyEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[OperatorStatus] = mapped_column(Enum(OperatorStatus), default=OperatorStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def __repr__(self) -> str:
        return f"<Operator(id={self.id}, name='{self.name}')>"