"""
This API router handles high-level system endpoints, including status checks,
version info, emergency stops, and the full system reset.
"""
from fastapi import APIRouter, Depends, Request
from app.services.system_service import AsyncSystemService
from app.auth.dependencies import get_api_key, rate_limiter

router = APIRouter()

def get_system_service(request: Request) -> AsyncSystemService:
    return request.app.state.system_service

@router.get("/version")
async def get_version():
    """Returns the current running code version to verify updates."""
    return {"version": "3.1.0-Hardware-Lock"}

@router.get("/status", dependencies=[Depends(rate_limiter)])
async def get_system_status(service: AsyncSystemService = Depends(get_system_service)):
    """Get overall system health status."""
    return await service.get_system_status()

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