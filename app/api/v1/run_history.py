from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, RunLog
from app.schemas.run_log import RunLogOut # We will create this schema next

router = APIRouter()

@router.get("/", response_model=List[RunLogOut])
async def get_run_history(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None, description="ISO 8601 format: YYYY-MM-DDTHH:MM:SS"),
    end_date: Optional[datetime] = Query(None, description="ISO 8601 format: YYYY-MM-DDTHH:MM:SS"),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
    batch_code: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Retrieve historical run logs with filtering and pagination.
    """
    query = (
        select(RunLog)
        .options(selectinload(RunLog.operator), selectinload(RunLog.product))
        .order_by(RunLog.start_timestamp.desc())
    )

    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)
    if operator_id:
        query = query.where(RunLog.operator_id == operator_id)
    if product_id:
        query = query.where(RunLog.product_id == product_id)
    if batch_code:
        query = query.where(RunLog.batch_code.ilike(f"%{batch_code}%"))

    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()