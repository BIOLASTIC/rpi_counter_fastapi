from fastapi import APIRouter, Depends, Request, HTTPException, Path
from typing import Literal
from app.core.gpio_controller import AsyncGPIOController

router = APIRouter()

def get_gpio_controller(request: Request) -> AsyncGPIOController:
    return request.app.state.gpio_controller

@router.post("/pin/{name}/toggle", status_code=200)
async def toggle_pin_by_name(
    gpio: AsyncGPIOController = Depends(get_gpio_controller),
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

@router.post("/pin/{name}/on", status_code=200)
async def turn_pin_on(
    gpio: AsyncGPIOController = Depends(get_gpio_controller),
    name: Literal["conveyor", "gate"] = Path(...)
):
    """Explicitly turns a pin ON."""
    new_state = await gpio.set_pin_state(name, True)
    if new_state is None:
        raise HTTPException(status_code=404, detail=f"Pin '{name}' not found.")
    return {"pin": name, "new_state": "ON"}

@router.post("/pin/{name}/off", status_code=200)
async def turn_pin_off(
    gpio: AsyncGPIOController = Depends(get_gpio_controller),
    name: Literal["conveyor", "gate"] = Path(...)
):
    """Explicitly turns a pin OFF."""
    new_state = await gpio.set_pin_state(name, False)
    if new_state is None:
        raise HTTPException(status_code=404, detail=f"Pin '{name}' not found.")
    return {"pin": name, "new_state": "OFF"}

# --- DEFINITIVE FIX: Add backward-compatible /start and /stop endpoints ---
@router.post("/conveyor/start", status_code=200, tags=["Legacy"])
async def start_conveyor(gpio: AsyncGPIOController = Depends(get_gpio_controller)):
    """Starts the conveyor. (Alias for /pin/conveyor/on)"""
    await gpio.set_pin_state("conveyor", True)
    return {"message": "Conveyor started."}

@router.post("/conveyor/stop", status_code=200, tags=["Legacy"])
async def stop_conveyor(gpio: AsyncGPIOController = Depends(get_gpio_controller)):
    """Stops the conveyor. (Alias for /pin/conveyor/off)"""
    await gpio.set_pin_state("conveyor", False)
    return {"message": "Conveyor stopped."}