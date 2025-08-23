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

# --- THIS IS THE FIX: ADD THE SECOND CAMERA LIGHT ---
# Define the literal types for valid output names from settings
OutputPinName = Literal["conveyor", "gate", "diverter", "led_green", "led_red", "buzzer", "camera_light", "camera_light_two"]
# --- END OF FIX ---

@router.post("/toggle/{name}", status_code=200)
async def toggle_output_by_name(
    name: OutputPinName = Path(...),
    io: AsyncModbusController = Depends(get_modbus_controller)
):
    """
    Toggles the state of any configured output coil (Relay, LED, Buzzer).
    Returns the new state ('ON' or 'OFF').
    """
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
    
    # --- THIS IS THE FIX: Invert logic for NC-wired lights ---
    # For the camera lights, the logic is inverted. The UI sends a command to achieve a logical state (e.g., "turn ON").
    # If the light is ON, its relay coil is actually OFF (False). To turn it ON, we need to set the coil to OFF.
    # However, the toggle endpoint is simpler: it just flips the current state. The UI state will be corrected
    # by the `system_service` reporting the correct logical state.
    new_state = not current_state
    # --- END OF FIX ---

    success = await io.write_coil(address, new_state)
    if not success:
        raise HTTPException(status_code=503, detail="Failed to write new coil state to Modbus device.")
        
    # For NC lights, the new logical state is the inverse of the coil's new physical state.
    if name in ["camera_light", "camera_light_two"]:
        final_logical_state = not new_state
    else:
        final_logical_state = new_state

    return {"output": output_name_str, "new_state": "ON" if final_logical_state else "OFF"}