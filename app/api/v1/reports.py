from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

# --- THIS IS THE FIX ---
# The import is changed to the correct 'DetectionEventLog' model.
from app.models import get_async_session, RunLog, RunStatus, DetectionEventLog
# ---------------------

router = APIRouter()

@router.get("/summary")
async def get_production_summary(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None, description="Start date for the report query (ISO 8601)"),
    end_date: Optional[datetime] = Query(None, description="End date for the report query (ISO 8601)"),
):
    """
    Generates a high-level production summary report for a given date range.
    This calculates total runs, their statuses, and the total number of items detected.
    """
    # Base query to select RunLogs. We use selectinload to efficiently fetch
    # all related detection events in a single follow-up query, preventing the N+1 problem.
    query = select(RunLog).options(selectinload(RunLog.detection_events))

    # Apply date filters if provided
    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)

    result = await db.execute(query)
    runs = result.scalars().all()

    # Calculate statistics from the fetched runs
    total_runs = len(runs)
    total_detections = sum(len(run.detection_events) for run in runs)
    completed_runs = sum(1 for run in runs if run.status == RunStatus.COMPLETED)
    failed_runs = sum(1 for run in runs if run.status == RunStatus.FAILED)
    aborted_runs = sum(1 for run in runs if run.status == RunStatus.ABORTED)

    # Return a structured summary response
    return {
        "query_parameters": {
            "start_date": start_date.isoformat() if start_date else "Not specified",
            "end_date": end_date.isoformat() if end_date else "Not specified",
        },
        "summary": {
            "total_runs_in_period": total_runs,
            "completed_runs": completed_runs,
            "failed_runs": failed_runs,
            "aborted_runs": aborted_runs,
            "total_items_detected": total_detections,
        }
    }