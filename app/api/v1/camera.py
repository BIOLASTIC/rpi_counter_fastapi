from fastapi import APIRouter, Depends, Request
from app.core.camera_manager import AsyncCameraManager

router = APIRouter()

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

@router.get("/status")
async def get_camera_status(camera: AsyncCameraManager = Depends(get_camera_manager)):
    """Get camera information and status."""
    return await camera.get_camera_info()
