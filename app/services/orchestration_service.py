"""
Service for controlling the high-level orchestration of production runs.

FINAL REVISION: This service has been fully refactored to use the new
AsyncModbusController for all hardware interactions, replacing the obsolete
GPIO controller. All original features and logic have been preserved.
- It now controls outputs by writing to Modbus coil addresses.
- It retrieves the mapping of logical names (e.g., 'conveyor') to coil addresses
  from the global settings object.
"""
import asyncio
from enum import Enum
from typing import Optional
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import redis.asyncio as redis

# MODIFIED: Import the new Modbus controller and global settings
from app.core.modbus_controller import AsyncModbusController
from app.models.profiles import ObjectProfile
from config import settings


class OperatingMode(str, Enum):
    """Defines the high-level operational states of the system."""
    STOPPED = "Stopped"
    IDLE = "Idle (Profile Loaded)"
    RUNNING = "Running"
    PAUSED = "Paused"


class AsyncOrchestrationService:
    """
    The "brain" of the application. Manages the system's operating mode,
    loads production profiles, and commands hardware state changes for runs.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,  # MODIFIED: Dependency changed from GPIO to Modbus
        db_session_factory,
        redis_client: redis.Redis
    ):
        """
        Initializes the orchestration service.

        Args:
            modbus_controller: The instance for controlling hardware via Modbus.
            db_session_factory: The factory for creating database sessions.
            redis_client: The client for communicating with Redis.
        """
        self._io = modbus_controller  # MODIFIED: Internal variable now refers to the Modbus IO controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._mode = OperatingMode.STOPPED
        self._active_profile: Optional[ObjectProfile] = None
        self._current_count = 0
        self._lock = asyncio.Lock()
        # NEW: Store the output-to-coil-address mapping from settings
        self._output_map = settings.OUTPUTS

    async def initialize_hardware_state(self):
        """
        Sets all Modbus outputs to a safe, default 'off' state.
        This is a critical safety feature for application startup.
        FEATURE PRESERVED.
        """
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        # MODIFIED: Use write_coil with mapped addresses instead of GPIO calls
        await self._io.write_coil(self._output_map.GATE, False)
        await self._io.write_coil(self._output_map.DIVERTER, False)
        await self._io.write_coil(self._output_map.CONVEYOR, False)
        await self._io.write_coil(self._output_map.LED_GREEN, False)
        # Turn on the red 'stopped' LED to indicate the system is halted.
        await self._io.write_coil(self._output_map.LED_RED, True)

    async def load_and_set_active_profile(self, profile_id: int) -> bool:
        """
        Loads a profile from the database and commands the camera service via Redis
        to apply the associated camera settings.
        FEATURE PRESERVED. This method's logic did not need to change.
        """
        async with self._lock:
            async with self._get_db_session() as session:
                # Use selectinload to efficiently fetch the ObjectProfile AND its related CameraProfile
                result = await session.execute(
                    select(ObjectProfile)
                    .options(selectinload(ObjectProfile.camera_profile))
                    .where(ObjectProfile.id == profile_id)
                )
                profile = result.scalar_one_or_none()

            if not profile or not profile.camera_profile:
                print(f"Orchestrator Error: Profile with ID {profile_id} or its linked camera profile not found.")
                return False

            self._active_profile = profile
            self._mode = OperatingMode.IDLE
            print(f"Orchestrator: Loaded Active Profile -> '{profile.name}' from DATABASE.")

            # Construct the command using the data from the linked camera profile
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
            # Publish the specific settings to the camera service
            await self._redis.publish("camera:commands:usb", json.dumps(command))
            print(f"Orchestrator: Commanded camera to apply settings for '{cam_profile.name}'.")
            return True

    def get_active_profile(self) -> Optional[ObjectProfile]:
        """
        Returns the currently loaded ObjectProfile instance.
        FEATURE PRESERVED.
        """
        return self._active_profile

    def on_box_processed(self):
        """
        Callback for the detection service to increment the run counter.
        FEATURE PRESERVED.
        """
        if self._mode == OperatingMode.RUNNING:
            self._current_count += 1

    async def start_run(self):
        """
        Starts a production run, commanding hardware to its 'running' state.
        FEATURE PRESERVED.
        """
        async with self._lock:
            if self._mode not in [OperatingMode.IDLE, OperatingMode.PAUSED]:
                return

            print("Orchestrator: Starting production run.")
            self._current_count = 0 # Reset count at the start of a run
            self._mode = OperatingMode.RUNNING

            # MODIFIED: Use write_coil to set the 'running' hardware state
            await self._io.write_coil(self._output_map.LED_RED, False)
            await self._io.write_coil(self._output_map.LED_GREEN, True)
            await self._io.write_coil(self._output_map.CONVEYOR, True)

    async def stop_run(self):
        """
        Stops all operations, unloads the profile, and returns hardware to its safe 'stopped' state.
        FEATURE PRESERVED.
        """
        async with self._lock:
            if self._mode == OperatingMode.STOPPED:
                return

            print("Orchestrator: Stopping all operations and unloading profile.")
            self._mode = OperatingMode.STOPPED
            self._active_profile = None
            self._current_count = 0
            # MODIFIED: Call the dedicated method to return hardware to a safe state
            await self.initialize_hardware_state()

    def get_status(self) -> dict:
        """
        Gets the current status of the orchestration service for UI and API polling.
        FEATURE PRESERVED.
        """
        profile_name = self._active_profile.name if self._active_profile else "None"
        return {
            "mode": self._mode.value,
            "active_profile": profile_name,
            "run_progress": self._current_count,
        }