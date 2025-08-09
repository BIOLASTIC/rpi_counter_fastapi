from fastapi import APIRouter, Depends, Request, HTTPException
from app.services.orchestration_service import AsyncOrchestrationService # MODIFIED
from app.services.detection_service import AsyncDetectionService

router = APIRouter()

# MODIFIED: Dependency changed to OrchestrationService
def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    return request.app.state.orchestration_service
    
def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.get("/")
async def get_detection_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)): # MODIFIED
    """Get current detection status and counts."""
    # MODIFIED: Get status from the correct service
    status = service.get_status()
    return {
        "counts": {
            "processed": status["run_progress"],
            "target": status["target_count"]
        },
        "state": status["mode"]
    }

@router.post("/reset", status_code=200)
async def reset_counter(service: AsyncDetectionService = Depends(get_detection_service)):
    """Reset the box counter to zero."""
    # This part of the original code had an error. There is no `reset_counter`
    # on the detection service. We will call the orchestration service stop method
    # which performs a full reset of the counts.
    orchestration_service = get_orchestration_service(service._orchestration)
    await orchestration_service.stop_run()
    return {"message": "Counter and run state reset successfully."}