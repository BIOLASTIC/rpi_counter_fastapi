# rpi_counter_fastapi-dev2/app/schemas/products.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.product import ProductStatus

class ProductBase(BaseModel):
    name: str
    
    category: Optional[str] = None
    size: Optional[str] = None
    
    description: Optional[str] = None
    version: str = "1.0.0"
    status: ProductStatus = ProductStatus.ACTIVE
    ai_model_path: Optional[str] = "yolov8n.pt"
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

    # --- NEW FIELDS FOR DYNAMIC QC ---
    verify_category: bool = False
    verify_size: bool = False
    verify_defects: bool = False
    verify_ticks: bool = False
    # --- END OF NEW FIELDS ---

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    
    category: Optional[str] = None
    size: Optional[str] = None

    description: Optional[str] = None
    version: Optional[str] = None
    status: Optional[ProductStatus] = None
    ai_model_path: Optional[str] = None
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

    # --- NEW FIELDS FOR DYNAMIC QC ---
    verify_category: Optional[bool] = None
    verify_size: Optional[bool] = None
    verify_defects: Optional[bool] = None
    verify_ticks: Optional[bool] = None
    # --- END OF NEW FIELDS ---

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int