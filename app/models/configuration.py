from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class ConfigDataType(PyEnum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    JSON = "json"

class Configuration(Base):
    __tablename__ = "configurations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    namespace: Mapped[str] = mapped_column(String(100), index=True)
    key: Mapped[str] = mapped_column(String(100), index=True)
    value: Mapped[str] = mapped_column(Text)
    data_type: Mapped[ConfigDataType] = mapped_column(Enum(ConfigDataType))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    requires_restart: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    updated_by: Mapped[str] = mapped_column(String(100), default="system")

    def __repr__(self) -> str:
        return f"<Configuration(namespace='{self.namespace}', key='{self.key}')>"
