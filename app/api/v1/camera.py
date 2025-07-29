from fastapi import APIRouter, Depends, Request, Query, HTTPException, Path
from fastapi.responses import StreamingResponse
from app.core.camera_manager import AsyncCameraManager
from config import settings
from pathlib import Path
import asyncio

router = APIRouter()

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

@router.get("/status/{camera_id}")
async def get_camera_status(
    camera_id: str,
    camera: AsyncCameraManager = Depends(get_camera_manager)
):
    status = camera.get_health_status(camera_id)
    return {"camera_id": camera_id, "status": status.value}

@router.get("/stream/{camera_id}")
async def get_camera_stream(
    camera_id: str,
    camera: AsyncCameraManager = Depends(get_camera_manager)
):
    async def frame_generator():
        frame_queue = await camera.start_stream(camera_id)
        if not frame_queue:
            print(f"Attempted to stream invalid camera: {camera_id}")
            return
        try:
            while True:
                frame_bytes = await frame_queue.get()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        finally:
            await camera.stop_stream(camera_id, frame_queue)

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/captures/{camera_id}")
async def get_captured_images(
    camera_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(8, ge=1, le=100)
):
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