from fastapi import APIRouter, Depends, Request, HTTPException, Path
from typing import Literal
from app.core.gpio_controller import AsyncGPIOController

router = APIRouter()

def get_gpio_controller(request: Request) -> AsyncGPIOController:
    return request.app.state.gpio_controller

@router.post("/pin/{name}/toggle", status_code=200)
async def toggle_pin_by_name(
    gpio: AsyncGPIOController = Depends(get_gpio_controller),
    # This list now includes all controllable pins
    name: Literal["conveyor", "gate", "led_green", "led_red", "buzzer"] = Path(...)
):
    """
    Toggles the state of any configured output pin (Relay, LED, Buzzer).
    Returns the new state ('ON' or 'OFF').
    """
    new_state = await gpio.toggle_pin(name)
    if new_state is None:
        raise HTTPException(status_code=404, detail=f"Pin '{name}' not found.")
    
    return {"pin": name, "new_state": "ON" if new_state else "OFF"}
