from fastapi import APIRouter, Depends, Request, Body
from pydantic import BaseModel, Field

from app.services.orchestration_service import AsyncOrchestrationService

router = APIRouter()

def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    return request.app.state.orchestration_service

class BatchStartRequest(BaseModel):
    size: int = Field(..., gt=0, description="The number of boxes to count in one batch.")

@router.post("/batch/start", status_code=202)
async def start_batch_process(
    payload: BatchStartRequest,
    service: AsyncOrchestrationService = Depends(get_orchestration_service)
):
    """Starts a new batch counting process."""
    await service.start_batch(payload.size)
    return {"message": f"Batch process started with a target size of {payload.size}."}

@router.post("/batch/stop", status_code=202)
async def stop_batch_process(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Stops the current counting process immediately."""
    await service.stop_process()
    return {"message": "Batch process stopped."}

@router.get("/batch/status")
async def get_batch_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Gets the current status of the batch process."""
    return service.get_status()