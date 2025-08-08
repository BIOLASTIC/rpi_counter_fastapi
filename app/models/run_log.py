from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict
from sqlalchemy import Integer, String, DateTime, Enum, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
# These imports are needed for the relationships
from .operator import Operator
from .product import Product


class RunStatus(PyEnum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ABORTED = "Aborted by User"

class RunLog(Base):
    __tablename__ = "run_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    batch_code: Mapped[str] = mapped_column(String(100), index=True)
    start_timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    end_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.RUNNING)
    
    object_profile_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    operator: Mapped["Operator"] = relationship()
    product: Mapped["Product"] = relationship()

    def __repr__(self) -> str:
        return f"<RunLog(id={self.id}, batch_code='{self.batch_code}', status='{self.status.name}')>"