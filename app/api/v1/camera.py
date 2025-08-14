# rpi_counter_fastapi-dev2/app/api/v1/camera.py

import os
import io
import zipfile
from datetime import datetime as dt_datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query, HTTPException, Path, Body
from fastapi.responses import StreamingResponse
import asyncio
import redis.asyncio as redis
from pydantic import BaseModel
import json

from app.core.camera_manager import AsyncCameraManager
from config import settings, ACTIVE_CAMERA_IDS
from pathlib import Path

router = APIRouter()
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis_client

class CameraPreviewSettings(BaseModel):
    exposure: Optional[int] = None
    gain: Optional[int] = None
    white_balance_temp: Optional[int] = None
    brightness: Optional[int] = None
    autofocus: Optional[bool] = None

@router.get("/status/{camera_id}")
async def get_camera_status(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    status = camera.get_health_status(camera_id)
    return {"camera_id": camera_id, "status": status.value}

@router.get("/stream/{camera_id}")
async def get_camera_stream(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    """Provides the live MJPEG stream for a given camera."""
    async def frame_generator():
        frame_queue = await camera.start_stream(camera_id)
        if not frame_queue:
            print(f"API ERROR: start_stream() for '{camera_id}' returned None. Cannot start stream.")
            return

        print(f"API INFO: Client connected to stream for '{camera_id}'. Waiting for the first frame...")
        try:
            # Wait for the first frame with a timeout
            first_frame = await asyncio.wait_for(frame_queue.get(), timeout=7.0)
            print(f"API INFO: First frame received for '{camera_id}'. Starting stream.")
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + first_frame + b'\r\n')

            # Continue with the rest of the frames
            while True:
                frame_bytes = await frame_queue.get()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except asyncio.TimeoutError:
            print(f"API WARNING: Timed out after 7s waiting for the first frame from camera '{camera_id}'. Closing stream. Is the camera service running and publishing to Redis?")
        except asyncio.CancelledError:
            print(f"API INFO: Client disconnected from '{camera_id}' stream.")
        except Exception as e:
            print(f"API ERROR: An unexpected error occurred in the frame generator for '{camera_id}': {e}")
        finally:
            print(f"API INFO: Cleaning up stream resources for '{camera_id}'.")
            await camera.stop_stream(camera_id, frame_queue)

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
    
@router.post("/preview_settings/{camera_id}", status_code=202)
async def apply_preview_settings(
    camera_id: str,
    settings_payload: CameraPreviewSettings,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    if camera_id not in ACTIVE_CAMERA_IDS:
        raise HTTPException(status_code=404, detail=f"Camera '{camera_id}' is not active or does not exist.")

    command = {
        "action": "apply_settings",
        "settings": settings_payload.model_dump(exclude_none=True)
    }
    
    command_bytes = json.dumps(command).encode('utf-8')
    channel = f"camera:commands:{camera_id}"
    await redis_client.publish(channel, command_bytes)
    
    return {"message": f"Preview settings applied to camera '{camera_id}'.", "settings": command["settings"]}

@router.get("/captures/{camera_id}")
async def get_captured_images(camera_id: str, page: int = Query(1, ge=1), page_size: int = Query(8, ge=1, le=100)):
    captures_dir = Path(settings.CAMERA_CAPTURES_DIR) / camera_id
    if not captures_dir.exists():
        return {"images": [], "has_more": False}
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

class ZipRequestPayload(BaseModel):
    camera_id: str
    start_date: date
    end_date: date

def create_zip_in_memory_sync(camera_id: str, start_date: date, end_date: date) -> io.BytesIO:
    captures_dir = PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR / camera_id
    if not captures_dir.is_dir():
        return None
    start_ts = dt_datetime.combine(start_date, dt_datetime.min.time()).timestamp()
    end_ts = dt_datetime.combine(end_date, dt_datetime.max.time()).timestamp()
    files_to_zip = [f for f in captures_dir.glob("*.jpg") if start_ts <= f.stat().st_mtime <= end_ts]
    zip_buffer = io.BytesIO()
    if not files_to_zip:
        return zip_buffer
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            zipf.write(file_path, arcname=file_path.name)
    zip_buffer.seek(0)
    return zip_buffer

@router.post("/captures/download-zip")
async def download_captures_as_zip(payload: ZipRequestPayload = Body(...)):
    zip_buffer = await asyncio.to_thread(
        create_zip_in_memory_sync, payload.camera_id, payload.start_date, payload.end_date
    )
    if zip_buffer is None:
        raise HTTPException(status_code=404, detail=f"Capture directory for camera '{payload.camera_id}' not found.")
    if not zip_buffer.getbuffer().nbytes > 0:
        raise HTTPException(status_code=404, detail="No images found in the specified date range.")
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=captures_{payload.camera_id}_{payload.start_date}_to_{payload.end_date}.zip"}
    )

@router.get("/ai_stream/{camera_id}")
async def get_ai_stream(camera_id: str, redis_client: redis.Redis = Depends(get_redis_client)):
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
    return StreamingResponse(ai_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")