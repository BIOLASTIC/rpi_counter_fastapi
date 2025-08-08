from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, Product, ObjectProfile
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()

@router.post("/", status_code=201, response_model=ProductOut)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new product."""
    result = await db.execute(select(Product).where(Product.name == product_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"A product with name '{product_in.name}' already exists.")
    
    new_product = Product(**product_in.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductOut])
async def get_all_products(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all products."""
    result = await db.execute(select(Product).order_by(Product.name))
    return result.scalars().all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single product by its ID."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing product."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete a product."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.product_id == product_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this product. It is currently in use by one or more object profiles."
        )
        
    await db.delete(product)
    await db.commit()
    return None