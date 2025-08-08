from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, Operator
from app.schemas.operators import OperatorCreate, OperatorUpdate, OperatorOut

router = APIRouter()

@router.post("/", status_code=201, response_model=OperatorOut)
async def create_operator(
    operator_in: OperatorCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new operator."""
    result = await db.execute(select(Operator).where(Operator.name == operator_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"An operator with name '{operator_in.name}' already exists.")
    
    new_operator = Operator(**operator_in.model_dump())
    db.add(new_operator)
    await db.commit()
    await db.refresh(new_operator)
    return new_operator

@router.get("/", response_model=List[OperatorOut])
async def get_all_operators(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all operators."""
    result = await db.execute(select(Operator).order_by(Operator.name))
    return result.scalars().all()

@router.get("/{operator_id}", response_model=OperatorOut)
async def get_operator(operator_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single operator by ID."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator

@router.put("/{operator_id}", response_model=OperatorOut)
async def update_operator(
    operator_id: int,
    operator_in: OperatorUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing operator."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    
    update_data = operator_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(operator, key, value)
        
    await db.commit()
    await db.refresh(operator)
    return operator

@router.delete("/{operator_id}", status_code=204)
async def delete_operator(operator_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete an operator."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
        
    await db.delete(operator)
    await db.commit()
    return None