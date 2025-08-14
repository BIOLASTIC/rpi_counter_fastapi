# rpi_counter_fastapi-dev2/app/schemas/products.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.product import ProductStatus

class ProductBase(BaseModel):
    name: str
    
    # --- NEW FIELDS ---
    category: Optional[str] = None
    size: Optional[str] = None
    # --- END OF NEW FIELDS ---
    
    description: Optional[str] = None
    version: str = "1.0.0"
    status: ProductStatus = ProductStatus.ACTIVE
    ai_model_path: Optional[str] = "yolov8n.pt"
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    
    # --- NEW FIELDS ---
    category: Optional[str] = None
    size: Optional[str] = None
    # --- END OF NEW FIELDS ---

    description: Optional[str] = None
    version: Optional[str] = None
    status: Optional[ProductStatus] = None
    ai_model_path: Optional[str] = None
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int