from fastapi import APIRouter, Depends, Request, Path
from app.core.gpio_controller import AsyncGPIOController

router = APIRouter()

def get_gpio_controller(request: Request) -> AsyncGPIOController:
    return request.app.state.gpio_controller

@router.get("/status")
async def get_gpio_status(gpio: AsyncGPIOController = Depends(get_gpio_controller)):
    """Get the status of all configured GPIO devices."""
    return {
        "conveyor": await gpio.get_conveyor_status(),
        "gate": await gpio.get_gate_position(),
    }

@router.post("/conveyor/{action}")
async def control_conveyor(action: str = Path(..., description="'start' or 'stop'"), gpio: AsyncGPIOController = Depends(get_gpio_controller)):
    if action == "start":
        await gpio.start_conveyor()
        return {"message": "Conveyor started."}
    elif action == "stop":
        await gpio.stop_conveyor()
        return {"message": "Conveyor stopped."}
    return {"error": "Invalid action."}
