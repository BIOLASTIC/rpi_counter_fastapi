"""
REVISED FOR PHASE 3: API endpoints for controlling the high-level
orchestration of production runs. Replaces the old "batch" system.
ADDED: Target count for production runs.
"""
from fastapi import APIRouter, Depends, Request, Body, HTTPException
from pydantic import BaseModel, Field

from app.services.orchestration_service import AsyncOrchestrationService

router = APIRouter()

def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    """Dependency to get the orchestration service instance."""
    return request.app.state.orchestration_service

class SetActiveProfilePayload(BaseModel):
    """Defines the request body for setting an active profile."""
    object_profile_id: int = Field(..., gt=0, description="The ID of the ObjectProfile to activate for the run.")

# --- NEW: Pydantic model for the start run request body ---
class StartRunPayload(BaseModel):
    """Defines the request body for starting a run."""
    target_count: int = Field(0, ge=0, description="The target number of items for this run. 0 means unlimited.")

@router.post("/run/set-profile", status_code=202)
async def set_active_profile(
    payload: SetActiveProfilePayload,
    service: AsyncOrchestrationService = Depends(get_orchestration_service)
):
    """
    Loads an Object Profile from the database, makes it the active profile
    for the system, and commands the camera service to apply the associated
    camera settings. This is the first step before starting a run.
    """
    success = await service.load_and_set_active_profile(payload.object_profile_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"ObjectProfile with ID {payload.object_profile_id} not found."
        )
    return {"message": "Active profile loaded and camera configured successfully."}

@router.post("/run/start", status_code=202)
async def start_production_run(
    payload: StartRunPayload, # MODIFIED: Use the new payload
    service: AsyncOrchestrationService = Depends(get_orchestration_service)
):
    """Starts the conveyor belt if a profile has been loaded."""
    # MODIFIED: Pass the target count to the service
    await service.start_run(target_count=payload.target_count)
    return {"message": "Production run started."}

@router.post("/run/stop", status_code=202)
async def stop_production_run(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Stops the conveyor belt and unloads the active profile."""
    await service.stop_run()
    return {"message": "Production run stopped and profile unloaded."}

@router.get("/run/status")
async def get_run_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Gets the current status of the orchestration service."""
    return service.get_status()