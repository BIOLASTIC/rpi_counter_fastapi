"""
Service for controlling the high-level orchestration of production runs.

FINAL REVISION: This service has been fully refactored to use the new
AsyncModbusController for all hardware interactions, replacing the obsolete
GPIO controller. All original features and logic have been preserved.
- It now controls outputs by writing to Modbus coil addresses.
- It retrieves the mapping of logical names (e.g., 'conveyor') to coil addresses
  from the global settings object.
- ADDED: Logic to track target count for a batch run.
"""
import asyncio
from enum import Enum
from typing import Optional
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import redis.asyncio as redis

from app.core.modbus_controller import AsyncModbusController
from app.models.profiles import ObjectProfile
from config import settings


class OperatingMode(str, Enum):
    """Defines the high-level operational states of the system."""
    STOPPED = "Stopped"
    IDLE = "Idle (Profile Loaded)"
    RUNNING = "Running"
    PAUSED = "Paused"
    COMPLETE = "Complete" # NEW: State for when a batch finishes


class AsyncOrchestrationService:
    """
    The "brain" of the application. Manages the system's operating mode,
    loads production profiles, and commands hardware state changes for runs.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        db_session_factory,
        redis_client: redis.Redis
    ):
        self._io = modbus_controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._mode = OperatingMode.STOPPED
        self._active_profile: Optional[ObjectProfile] = None
        self._current_count = 0
        self._target_count = 0 # NEW: Attribute for batch size
        self._lock = asyncio.Lock()
        self._output_map = settings.OUTPUTS

    async def initialize_hardware_state(self):
        """Sets all Modbus outputs to a safe, default 'off' state."""
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        await self._io.write_coil(self._output_map.GATE, False)
        await self._io.write_coil(self._output_map.DIVERTER, False)
        await self._io.write_coil(self._output_map.CONVEYOR, False)
        await self._io.write_coil(self._output_map.LED_GREEN, False)
        await self._io.write_coil(self._output_map.LED_RED, True)

    async def load_and_set_active_profile(self, profile_id: int) -> bool:
        """Loads a profile from the database and commands the camera."""
        async with self._lock:
            async with self._get_db_session() as session:
                result = await session.execute(
                    select(ObjectProfile)
                    .options(selectinload(ObjectProfile.camera_profile))
                    .where(ObjectProfile.id == profile_id)
                )
                profile = result.scalar_one_or_none()

            if not profile or not profile.camera_profile:
                return False

            self._active_profile = profile
            self._mode = OperatingMode.IDLE
            print(f"Orchestrator: Loaded Active Profile -> '{profile.name}' from DATABASE.")

            cam_profile = self._active_profile.camera_profile
            command = {
                "action": "apply_settings",
                "settings": {
                    "autofocus": cam_profile.autofocus,
                    "exposure": cam_profile.exposure,
                    "gain": cam_profile.gain,
                    "white_balance_temp": cam_profile.white_balance_temp,
                    "brightness": cam_profile.brightness,
                }
            }
            await self._redis.publish("camera:commands:usb", json.dumps(command))
            print(f"Orchestrator: Commanded camera to apply settings for '{cam_profile.name}'.")
            return True

    def get_active_profile(self) -> Optional[ObjectProfile]:
        """Returns the currently loaded ObjectProfile instance."""
        return self._active_profile

    def on_box_processed(self):
        """Callback for the detection service to increment the run counter."""
        if self._mode == OperatingMode.RUNNING:
            self._current_count += 1
            # NEW: Check if the batch is complete
            if self._target_count > 0 and self._current_count >= self._target_count:
                print("Orchestrator: Target count reached. Completing run.")
                asyncio.create_task(self.complete_run())


    async def start_run(self, target_count: int = 0):
        """Starts a production run, commanding hardware to its 'running' state."""
        async with self._lock:
            # A run can only start if a profile is loaded
            if self._mode not in [OperatingMode.IDLE, OperatingMode.PAUSED, OperatingMode.COMPLETE]:
                return

            print(f"Orchestrator: Starting production run. Target: {target_count if target_count > 0 else 'Unlimited'}")
            self._current_count = 0 
            self._target_count = target_count
            self._mode = OperatingMode.RUNNING

            await self._io.write_coil(self._output_map.LED_RED, False)
            await self._io.write_coil(self._output_map.LED_GREEN, True)
            await self._io.write_coil(self._output_map.CONVEYOR, True)
            
    # --- NEW: Method to handle batch completion gracefully ---
    async def complete_run(self):
        """Sequence for when a batch target is met."""
        async with self._lock:
            self._mode = OperatingMode.COMPLETE
            # Stop the conveyor but keep the green light on to show success
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            print("Orchestrator: Run complete. Conveyor stopped.")

    async def stop_run(self):
        """Stops all operations, unloads profile, returns hardware to safe state."""
        async with self._lock:
            if self._mode == OperatingMode.STOPPED:
                return

            print("Orchestrator: Stopping all operations and unloading profile.")
            self._mode = OperatingMode.STOPPED
            self._active_profile = None
            self._current_count = 0
            self._target_count = 0
            await self.initialize_hardware_state()

    def get_status(self) -> dict:
        """Gets the current status of the orchestration service for UI and API polling."""
        profile_name = self._active_profile.name if self._active_profile else "None"
        return {
            "mode": self._mode.value,
            "active_profile": profile_name,
            "run_progress": self._current_count,
            "target_count": self._target_count, # NEW: Send target count
        }