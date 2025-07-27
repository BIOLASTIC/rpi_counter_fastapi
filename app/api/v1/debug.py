"""
Debug endpoints for testing purposes.
This router should only be mounted in a 'development' environment.
"""
from fastapi import APIRouter, Depends, Request, HTTPException, Body
from app.services.detection_service import AsyncDetectionService
from app.core.sensor_events import SensorEvent, SensorState

router = APIRouter()

def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.post("/sensor-event")
async def trigger_sensor_event(
    service: AsyncDetectionService = Depends(get_detection_service),
    sensor_id: int = Body(..., embed=True),
    new_state: SensorState = Body(..., embed=True)
):
    """
    Manually triggers a sensor event to test the detection state machine.
    This provides a 'backdoor' for end-to-end testing without physical hardware.
    
    Example Body:
    {
        "sensor_id": 1,
        "new_state": "triggered"
    }
    """
    print(f"DEBUG: Manually triggering event: Sensor {sensor_id} -> {new_state.name}")
    event = SensorEvent(sensor_id=sensor_id, new_state=new_state)
    await service.handle_sensor_event(event)
    return {"message": "Debug sensor event triggered successfully.", "new_state": service._state.name}
