from fastapi import APIRouter, Depends, Request, HTTPException
from app.services.detection_service import AsyncDetectionService

router = APIRouter()

def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.get("/")
async def get_detection_status(service: AsyncDetectionService = Depends(get_detection_service)):
    """Get current detection status and counts."""
    # --- FIX: Call the new get_counts() method ---
    counts = await service.get_counts()
    return {
        "counts": counts,
        "state": service._state.name
    }

@router.post("/reset", status_code=200)
async def reset_counter(service: AsyncDetectionService = Depends(get_detection_service)):
    """Reset the box counter to zero."""
    success = await service.reset_counter()
    if success:
        return {"message": "Counter reset successfully."}
    raise HTTPException(status_code=500, detail="Failed to reset counter.")