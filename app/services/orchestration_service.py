"""
Service for controlling the high-level orchestration of production runs.

FINAL REVISION: This service has been fully refactored to use the new
AsyncModbusController for all hardware interactions, replacing the obsolete
GPIO controller. All original features and logic have been preserved.
- It now controls outputs by writing to Modbus coil addresses.
- It retrieves the mapping of logical names (e.g., 'conveyor') to coil addresses
  from the global settings object.
- ADDED: Logic to track target count for a batch run.
- ADDED: Logic for a user-defined pause after a run completes.
- REVISED: The start_run method is now atomic, handling profile loading and run start in one transaction.
- REVISED: The system now runs in a continuous loop, starting the next batch automatically after the post-run pause.
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
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED_BETWEEN_BATCHES = "Paused (Between Batches)" # REVISED: New state for clarity
    # REMOVED: The 'COMPLETE' state is no longer a final state, as the system loops.


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
        self._lock = asyncio.Lock()
        
        # --- Run Parameters ---
        # These are stored to allow for continuous looping
        self._active_profile: Optional[ObjectProfile] = None
        self._run_profile_id: Optional[int] = None
        self._run_target_count: int = 0
        self._run_post_batch_delay_sec: int = 5
        self._current_count: int = 0
        
        self._output_map = settings.OUTPUTS

    async def initialize_hardware_state(self):
        """Sets all Modbus outputs to a safe, default 'off' state."""
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        await self._io.write_coil(self._output_map.GATE, False)
        await self._io.write_coil(self._output_map.DIVERTER, False)
        await self._io.write_coil(self._output_map.CONVEYOR, False)
        await self._io.write_coil(self._output_map.LED_GREEN, False)
        await self._io.write_coil(self._output_map.LED_RED, True)

    def get_active_profile(self) -> Optional[ObjectProfile]:
        """Returns the currently loaded ObjectProfile instance."""
        return self._active_profile

    def on_box_processed(self):
        """Callback for the detection service to increment the run counter."""
        if self._mode == OperatingMode.RUNNING:
            self._current_count += 1
            if self._run_target_count > 0 and self._current_count >= self._run_target_count:
                print("Orchestrator: Target count reached. Beginning pause and loop sequence.")
                # This will pause, then re-start the run automatically
                asyncio.create_task(self.complete_and_loop_run())


    async def start_run(self, profile_id: int, target_count: int, post_batch_delay_sec: int) -> bool:
        """
        Atomically loads a profile, configures the camera, and starts a production run.
        This is the single entry point for starting any new run.
        Returns True on success, False on failure (e.g., profile not found).
        """
        async with self._lock:
            # Prevent starting if a run is already in progress
            if self._mode in [OperatingMode.RUNNING, OperatingMode.PAUSED_BETWEEN_BATCHES]:
                print(f"Orchestrator: Ignoring start command, system is already in mode '{self._mode.value}'.")
                return False

            # --- Store run parameters for looping ---
            self._run_profile_id = profile_id
            self._run_target_count = target_count
            self._run_post_batch_delay_sec = post_batch_delay_sec

            # --- Call the internal method to execute the start sequence ---
            return await self._execute_start_sequence()
            
    async def _execute_start_sequence(self) -> bool:
        """Internal method to start a batch. Can be called to loop."""
        # This method assumes it's being called from within a lock.
        
        # --- Step 1: Load the profile from the database ---
        async with self._get_db_session() as session:
            result = await session.execute(
                select(ObjectProfile)
                .options(selectinload(ObjectProfile.camera_profile))
                .where(ObjectProfile.id == self._run_profile_id)
            )
            profile = result.scalar_one_or_none()

        if not profile or not profile.camera_profile:
            print(f"Orchestrator: FAILED to start batch. Profile ID {self._run_profile_id} not found or is invalid.")
            await self.stop_run() # Go to a safe state
            return False

        self._active_profile = profile
        print(f"Orchestrator: Loaded Active Profile -> '{profile.name}' for new batch.")

        # --- Step 2: Command the camera service to apply settings via Redis ---
        cam_profile = self._active_profile.camera_profile
        command = { "action": "apply_settings", "settings": { "autofocus": cam_profile.autofocus, "exposure": cam_profile.exposure, "gain": cam_profile.gain, "white_balance_temp": cam_profile.white_balance_temp, "brightness": cam_profile.brightness } }
        await self._redis.publish("camera:commands:usb", json.dumps(command))
        
        # --- Step 3: Start the hardware and set the operating mode ---
        print(f"Orchestrator: Starting new batch. Target: {self._run_target_count if self._run_target_count > 0 else 'Unlimited'}")
        self._current_count = 0 
        self._mode = OperatingMode.RUNNING

        await self._io.write_coil(self._output_map.LED_RED, False)
        await self._io.write_coil(self._output_map.LED_GREEN, True)
        await self._io.write_coil(self._output_map.CONVEYOR, True)
        return True

    async def complete_and_loop_run(self):
        """
        Sequence for when a batch target is met. Pauses, then starts the next batch.
        """
        # --- Step 1: Pause the system ---
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            print(f"Orchestrator: Batch complete. Pausing for {self._run_post_batch_delay_sec} seconds before next batch.")

        # --- Step 2: Wait for the user-defined duration (outside the lock) ---
        await asyncio.sleep(self._run_post_batch_delay_sec)

        # --- Step 3: Re-acquire lock and start the next batch ---
        async with self._lock:
            # CRITICAL CHECK: If the user hit 'Stop Run' during the pause, the mode will
            # have changed to STOPPED. In this case, we must not start the next batch.
            if self._mode != OperatingMode.PAUSED_BETWEEN_BATCHES:
                print("Orchestrator: Loop interrupted by a 'Stop' command. Halting continuous run.")
                return

            print("Orchestrator: Pause finished. Looping to next batch...")
            await self._execute_start_sequence()

    async def stop_run(self):
        """
        Stops all operations, unloads profile, and returns hardware to a safe state.
        This is the primary method to break the continuous loop.
        """
        async with self._lock:
            if self._mode == OperatingMode.STOPPED:
                return

            print("Orchestrator: STOP command received. Halting all operations and clearing run parameters.")
            self._mode = OperatingMode.STOPPED
            self._active_profile = None
            self._run_profile_id = None
            self._current_count = 0
            self._run_target_count = 0
            await self.initialize_hardware_state()

    def get_status(self) -> dict:
        """Gets the current status of the orchestration service for UI and API polling."""
        profile_name = self._active_profile.name if self._active_profile else "None"
        return {
            "mode": self._mode.value,
            "active_profile": profile_name,
            "run_progress": self._current_count,
            "target_count": self._run_target_count,
            "post_batch_delay_sec": self._run_post_batch_delay_sec,
        }