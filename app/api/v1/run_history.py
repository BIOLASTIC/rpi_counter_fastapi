import io
import zipfile
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Path as FastApiPath
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, RunLog, DetectionEventLog
from app.schemas.run_log import RunLogOut, DetectionEventLogOut
from config import settings

router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

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

@router.get("/{run_id}/detections", response_model=List[DetectionEventLogOut])
async def get_run_detection_events(
    run_id: int = FastApiPath(..., description="The ID of the run log"),
    db: AsyncSession = Depends(get_async_session)
):
    """Retrieve all detection events (including image paths) for a single run."""
    result = await db.execute(
        select(DetectionEventLog)
        .where(DetectionEventLog.run_log_id == run_id)
        .order_by(DetectionEventLog.timestamp.asc())
    )
    return result.scalars().all()

def create_zip_from_paths_sync(image_web_paths: List[str]) -> io.BytesIO:
    """Synchronously creates a ZIP archive from a list of web paths."""
    captures_base_dir = PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR
    
    files_to_zip = []
    for web_path in image_web_paths:
        if not web_path: continue
        relative_path = web_path.lstrip('/').lstrip('captures').lstrip('/')
        full_path = captures_base_dir / relative_path
        if full_path.exists():
            files_to_zip.append(full_path)

    zip_buffer = io.BytesIO()
    if not files_to_zip:
        return zip_buffer

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            zipf.write(file_path, arcname=file_path.name)
    
    zip_buffer.seek(0)
    return zip_buffer

@router.get("/{run_id}/download-images")
async def download_run_images_zip(
    run_id: int = FastApiPath(..., description="The ID of the run log to download images from"),
    db: AsyncSession = Depends(get_async_session)
):
    """Downloads all captured images for a specific run as a single ZIP file."""
    run_log = await db.get(RunLog, run_id)
    if not run_log:
        raise HTTPException(status_code=404, detail="Run not found.")

    result = await db.execute(
        select(DetectionEventLog.image_path)
        .where(DetectionEventLog.run_log_id == run_id)
    )
    image_paths = result.scalars().all()

    if not any(image_paths):
        raise HTTPException(status_code=404, detail="No images were logged for this run.")

    zip_buffer = await asyncio.to_thread(create_zip_from_paths_sync, image_paths)
    
    if not zip_buffer.getbuffer().nbytes > 0:
         raise HTTPException(status_code=404, detail="Images for this run were logged, but the files could not be found on disk.")

    filename = f"run_{run_id}_{run_log.batch_code}_images.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )