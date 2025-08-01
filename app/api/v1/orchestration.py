"""
REVISED FOR PHASE 3: API endpoints for controlling the high-level
orchestration of production runs. Replaces the old "batch" system.
ADDED: Target count for production runs.
ADDED: Post-batch delay for pausing between runs.
REVISED: The /run/start endpoint is now the single atomic entry point for starting a new run.
"""
from fastapi import APIRouter, Depends, Request, Body, HTTPException
from pydantic import BaseModel, Field

from app.services.orchestration_service import AsyncOrchestrationService

router = APIRouter()

def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    """Dependency to get the orchestration service instance."""
    return request.app.state.orchestration_service

class StartRunPayload(BaseModel):
    """Defines the request body for starting a run."""
    # MODIFIED: Profile ID is now part of this payload
    object_profile_id: int = Field(..., gt=0, description="The ID of the ObjectProfile to activate for the run.")
    target_count: int = Field(0, ge=0, description="The target number of items for this run. 0 means unlimited.")
    post_batch_delay_sec: int = Field(5, ge=0, description="The time in seconds to pause after the run completes.")

# REMOVED: The /run/set-profile endpoint is no longer needed as the logic is now atomic.

@router.post("/run/start", status_code=202)
async def start_production_run(
    payload: StartRunPayload,
    service: AsyncOrchestrationService = Depends(get_orchestration_service)
):
    """
    Atomically loads the specified profile, configures the camera, and starts the run.
    This is the single endpoint for initiating a production run.
    """
    success = await service.start_run(
        profile_id=payload.object_profile_id,
        target_count=payload.target_count,
        post_batch_delay_sec=payload.post_batch_delay_sec
    )
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to start run. ObjectProfile with ID {payload.object_profile_id} may not exist or the system is in an invalid state to start."
        )
    return {"message": "Production run started successfully."}

@router.post("/run/stop", status_code=202)
async def stop_production_run(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Stops the conveyor belt and unloads the active profile."""
    await service.stop_run()
    return {"message": "Production run stopped and profile unloaded."}

@router.get("/run/status")
async def get_run_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Gets the current status of the orchestration service."""
    return service.get_status()