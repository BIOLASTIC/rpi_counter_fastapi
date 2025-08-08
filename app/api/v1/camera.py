import os
import io
import zipfile
from datetime import datetime as dt_datetime, date
from fastapi import APIRouter, Depends, Request, Query, HTTPException, Path, Body
from fastapi.responses import StreamingResponse
from app.core.camera_manager import AsyncCameraManager
from config import settings
from pathlib import Path
import asyncio
import redis.asyncio as redis
from pydantic import BaseModel

router = APIRouter()

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

@router.get("/status/{camera_id}")
async def get_camera_status(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    status = camera.get_health_status(camera_id)
    return {"camera_id": camera_id, "status": status.value}

@router.get("/stream/{camera_id}")
async def get_camera_stream(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    async def frame_generator():
        frame_queue = await camera.start_stream(camera_id)
        if not frame_queue: return
        try:
            while True:
                frame_bytes = await frame_queue.get()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        finally:
            await camera.stop_stream(camera_id, frame_queue)
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/captures/{camera_id}")
async def get_captured_images(
    camera_id: str, page: int = Query(1, ge=1), page_size: int = Query(8, ge=1, le=100)
):
    captures_dir = Path(settings.CAMERA_CAPTURES_DIR) / camera_id
    if not captures_dir.exists(): return {"images": [], "has_more": False}
    try:
        image_files = sorted([p for p in captures_dir.glob("*.jpg")], key=lambda p: p.stat().st_mtime, reverse=True)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_files = image_files[start_index:end_index]
        has_more = len(image_files) > end_index
        web_paths = [f"/captures/{camera_id}/{p.name}" for p in paginated_files]
        return {"images": web_paths, "has_more": has_more}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- PHASE 5: New endpoint to download images as a ZIP archive ---
class ZipRequestPayload(BaseModel):
    camera_id: str
    start_date: date
    end_date: date

@router.post("/captures/download-zip")
async def download_captures_as_zip(payload: ZipRequestPayload = Body(...)):
    """
    Creates a ZIP archive of captured images from a specific camera within a date range.
    """
    captures_dir = Path(settings.CAMERA_CAPTURES_DIR) / payload.camera_id
    if not captures_dir.exists() or not captures_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"Capture directory for camera '{payload.camera_id}' not found.")

    start_ts = dt_datetime.combine(payload.start_date, dt_datetime.min.time()).timestamp()
    end_ts = dt_datetime.combine(payload.end_date, dt_datetime.max.time()).timestamp()

    files_to_zip = []
    for f in captures_dir.glob("*.jpg"):
        try:
            mtime = f.stat().st_mtime
            if start_ts <= mtime <= end_ts:
                files_to_zip.append(f)
        except FileNotFoundError:
            continue
    
    if not files_to_zip:
        raise HTTPException(status_code=404, detail="No images found in the specified date range.")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            zipf.write(file_path, arcname=file_path.name)
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=captures_{payload.camera_id}_{payload.start_date}_to_{payload.end_date}.zip"}
    )


@router.get("/ai_stream/{camera_id}")
async def get_ai_stream(camera_id: str):
    redis_client = redis.from_url("redis://localhost")
    async def ai_frame_generator():
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"ai_stream:frames:{camera_id}")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10.0)
                if message and message.get("type") == "message":
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + message['data'] + b'\r\n')
        finally:
            await pubsub.close()
            await redis_client.close()
    return StreamingResponse(ai_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")