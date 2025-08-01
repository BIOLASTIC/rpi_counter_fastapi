"""
NEW: API endpoints for manually controlling hardware outputs via Modbus.
This replaces the old GPIO control API, preserving the manual toggle feature.
"""
from fastapi import APIRouter, Depends, Request, HTTPException, Path
from typing import Literal

from app.core.modbus_controller import AsyncModbusController

# This is the router for THIS FILE ONLY. It is self-contained.
# It does not know about any other router.
router = APIRouter()

def get_modbus_controller(request: Request) -> AsyncModbusController:
    return request.app.state.modbus_controller

# Define the literal types for valid output names from settings
OutputPinName = Literal["conveyor", "gate", "diverter", "led_green", "led_red", "buzzer", "camera_light"]

@router.post("/toggle/{name}", status_code=200)
async def toggle_output_by_name(
    name: OutputPinName = Path(...),
    io: AsyncModbusController = Depends(get_modbus_controller)
):
    """
    Toggles the state of any configured output coil (Relay, LED, Buzzer).
    Returns the new state ('ON' or 'OFF').
    """
    # When using Path with a Literal, FastAPI passes the string value directly.
    output_name_str = name

    address = io.get_output_address(output_name_str)
    if address is None:
        raise HTTPException(status_code=404, detail=f"Output name '{output_name_str}' not found in configuration.")

    all_coils = await io.read_coils()
    if all_coils is None:
        raise HTTPException(status_code=503, detail="Could not read current coil states from Modbus device.")

    if address >= len(all_coils):
         raise HTTPException(status_code=500, detail=f"Address {address} for '{output_name_str}' is out of bounds for the reported coils.")

    current_state = all_coils[address]
    new_state = not current_state

    success = await io.write_coil(address, new_state)
    if not success:
        raise HTTPException(status_code=503, detail="Failed to write new coil state to Modbus device.")

    return {"output": output_name_str, "new_state": "ON" if new_state else "OFF"}