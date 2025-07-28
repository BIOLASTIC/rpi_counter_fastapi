from fastapi import APIRouter, Depends, Request, Query
from app.core.camera_manager import AsyncCameraManager
from config import settings
from pathlib import Path
from typing import List

router = APIRouter()

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

@router.get("/status")
async def get_camera_status(camera: AsyncCameraManager = Depends(get_camera_manager)):
    """Get camera information and status."""
    return await camera.get_camera_info()

# --- NEW: Endpoint to list captured images for the gallery ---
@router.get("/captures")
async def get_captured_images(
    page: int = Query(1, ge=1),
    page_size: int = Query(8, ge=1, le=100) # Load 8 images (4 per column) at a time
):
    """
    Get a paginated list of captured images, sorted from newest to oldest.
    This supports the lazy-loading gallery.
    """
    captures_dir = Path(settings.CAMERA.CAPTURES_DIR)
    if not captures_dir.exists():
        return {"images": [], "has_more": False}

    try:
        # Get all .jpg files and sort by modification time (newest first)
        image_files = sorted(
            [p for p in captures_dir.glob("*.jpg")],
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        # Paginate the results
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        paginated_files = image_files[start_index:end_index]
        has_more = len(image_files) > end_index

        # Return web-accessible paths
        web_paths = [f"/{p.parent.name}/{p.name}" for p in paginated_files]

        return {"images": web_paths, "has_more": has_more}

    except Exception as e:
        # Log the error and return an empty list
        print(f"Error reading capture directory: {e}")
        return {"images": [], "has_more": False}