"""
Service for controlling the high-level orchestration of production runs.

REVISED: Now reads the AI detection source from Redis to ensure it sends
camera profile commands to the correct, dynamically-switched camera service.
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
from config.settings import AppSettings


class OperatingMode(str, Enum):
    """Defines the high-level operational states of the system."""
    STOPPED = "Stopped"
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED_BETWEEN_BATCHES = "Paused (Between Batches)"


class AsyncOrchestrationService:
    """
    The "brain" of the application. Manages the system's operating mode,
    loads production profiles, and commands hardware state changes for runs.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        db_session_factory,
        redis_client: redis.Redis,
        settings: AppSettings
    ):
        self._io = modbus_controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._settings = settings
        self._redis_keys = settings.REDIS_KEYS # Use centralized keys
        self._mode = OperatingMode.STOPPED
        self._lock = asyncio.Lock()
        
        self._active_profile: Optional[ObjectProfile] = None
        self._run_profile_id: Optional[int] = None
        self._run_target_count: int = 0
        self._run_post_batch_delay_sec: int = 5
        self._current_count: int = 0
        
        self._output_map = self._settings.OUTPUTS

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
                asyncio.create_task(self.complete_and_loop_run())


    async def start_run(self, profile_id: int, target_count: int, post_batch_delay_sec: int) -> bool:
        """
        Atomically loads a profile, configures the camera, and starts a production run.
        """
        async with self._lock:
            if self._mode in [OperatingMode.RUNNING, OperatingMode.PAUSED_BETWEEN_BATCHES]:
                return False
            self._run_profile_id = profile_id
            self._run_target_count = target_count
            self._run_post_batch_delay_sec = post_batch_delay_sec
            return await self._execute_start_sequence()
            
    async def _execute_start_sequence(self) -> bool:
        """Internal method to start a batch. Can be called to loop."""
        async with self._get_db_session() as session:
            result = await session.execute(
                select(ObjectProfile)
                .options(selectinload(ObjectProfile.camera_profile))
                .where(ObjectProfile.id == self._run_profile_id)
            )
            profile = result.scalar_one_or_none()

        if not profile or not profile.camera_profile:
            return False

        self._active_profile = profile
        print(f"Orchestrator: Loaded Active Profile -> '{profile.name}' for new batch.")

        # --- DYNAMIC CAMERA COMMAND ---
        cam_profile = self._active_profile.camera_profile
        command = { "action": "apply_settings", "settings": { "autofocus": cam_profile.autofocus, "exposure": cam_profile.exposure, "gain": cam_profile.gain, "white_balance_temp": cam_profile.white_balance_temp, "brightness": cam_profile.brightness } }
        
        # --- REVISED: Get AI source from Redis with a fallback ---
        ai_source_camera = await self._redis.get(self._redis_keys.AI_DETECTION_SOURCE_KEY) or self._settings.AI_DETECTION_SOURCE
        command_channel = f"camera:commands:{ai_source_camera}"
        
        print(f"Orchestrator: Sending profile settings via Redis to '{command_channel}'.")
        await self._redis.publish(command_channel, json.dumps(command))
        
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
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            print(f"Orchestrator: Batch complete. Pausing for {self._run_post_batch_delay_sec} seconds before next batch.")

        await asyncio.sleep(self._run_post_batch_delay_sec)

        async with self._lock:
            if self._mode != OperatingMode.PAUSED_BETWEEN_BATCHES:
                print("Orchestrator: Loop interrupted by a 'Stop' command. Halting continuous run.")
                return

            print("Orchestrator: Pause finished. Looping to next batch...")
            await self._execute_start_sequence()

    async def stop_run(self):
        """
        Stops all operations, unloads profile, and returns hardware to a safe state.
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