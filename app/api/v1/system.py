from fastapi import APIRouter, Depends, Request
from app.services.system_service import AsyncSystemService
from app.auth.dependencies import get_api_key, rate_limiter

router = APIRouter()

def get_system_service(request: Request) -> AsyncSystemService:
    return request.app.state.system_service

# This endpoint is public and rate-limited
@router.get("/status", dependencies=[Depends(rate_limiter)])
async def get_system_status(service: AsyncSystemService = Depends(get_system_service)):
    """Get overall system health status."""
    return await service.get_system_status()

# This endpoint is protected by an API key
@router.post("/emergency-stop", status_code=200, dependencies=[Depends(get_api_key)])
async def emergency_stop(service: AsyncSystemService = Depends(get_system_service)):
    """Immediately stop all hardware operations. Requires API Key."""
    await service.emergency_stop()
    return {"message": "Emergency stop sequence initiated."}
