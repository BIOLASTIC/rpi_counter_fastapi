"""
This API router handles high-level system endpoints, including status checks,
version info, emergency stops, and the full system reset.
"""
from fastapi import APIRouter, Depends, Request, Body
from pydantic import BaseModel, Field
from typing import Literal
from app.services.system_service import AsyncSystemService
from app.auth.dependencies import get_api_key, rate_limiter

router = APIRouter()

def get_system_service(request: Request) -> AsyncSystemService:
    return request.app.state.system_service

# --- NEW: Pydantic model for the switch source payload ---
class AiSourcePayload(BaseModel):
    source: Literal['rpi', 'usb'] = Field(..., description="The camera source to use for AI detection.")

@router.get("/version")
async def get_version():
    """Returns the current running code version to verify updates."""
    return {"version": "9.0.0-Dynamic-AI-Switch"}

@router.get("/status", dependencies=[Depends(rate_limiter)])
async def get_system_status(service: AsyncSystemService = Depends(get_system_service)):
    """Get overall system health status."""
    return await service.get_system_status()

@router.post("/ai/toggle", status_code=200)
async def toggle_ai_service(service: AsyncSystemService = Depends(get_system_service)):
    """
    Toggles the AI detection service on or off.
    Returns the new state ('enabled' or 'disabled').
    """
    new_state = await service.toggle_ai_service()
    return {"message": f"AI service is now {new_state}.", "new_state": new_state}

# --- NEW: Endpoint to switch the AI camera source ---
@router.post("/ai/source", status_code=200)
async def set_ai_source(
    payload: AiSourcePayload,
    service: AsyncSystemService = Depends(get_system_service)
):
    """
    Sets the camera source ('rpi' or 'usb') for AI detection processing.
    """
    await service.set_ai_detection_source(payload.source)
    return {"message": f"AI detection source switched to {payload.source.upper()}."}


@router.post("/reset-all", status_code=200)
async def reset_all_state(service: AsyncSystemService = Depends(get_system_service)):
    """Resets all counters and stops all hardware. A full system state reset."""
    await service.full_system_reset()
    return {"message": "System state has been fully reset."}

@router.post("/emergency-stop", status_code=200, dependencies=[Depends(get_api_key)])
async def emergency_stop(service: AsyncSystemService = Depends(get_system_service)):
    """Immediately stop all hardware operations. Requires API Key."""
    await service.emergency_stop()
    return {"message": "Emergency stop sequence initiated."}