from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column # Correctly import Mapped
from enum import Enum as PyEnum

from .database import Base

class ProductStatus(PyEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # --- THIS IS THE FIX ---
    # Changed 'Mpped' to the correct 'Mapped'
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    # -----------------------
    description: Mapped[str] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    ai_model_path: Mapped[str] = mapped_column(String(255), nullable=True, default="yolov8n.pt")
    min_sensor_block_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    max_sensor_block_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}')>"