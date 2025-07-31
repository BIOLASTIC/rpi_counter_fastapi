import asyncio
from enum import Enum, auto
from typing import Optional
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.gpio_controller import AsyncGPIOController
from app.models.profiles import ObjectProfile
import redis.asyncio as redis

class OperatingMode(str, Enum):
    STOPPED = "Stopped"
    IDLE = "Idle (Profile Loaded)"
    RUNNING = "Running"
    PAUSED = "Paused"

class AsyncOrchestrationService:
    def __init__(
        self,
        gpio: AsyncGPIOController,
        db_session_factory,
        redis_client: redis.Redis
    ):
        self._gpio = gpio
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._mode = OperatingMode.STOPPED
        self._active_profile: Optional[ObjectProfile] = None
        self._current_count = 0
        self._lock = asyncio.Lock()

    async def initialize_hardware_state(self):
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        await self._gpio.set_pin_state("gate", False)
        await self._gpio.set_pin_state("diverter", False)
        await self._gpio.set_pin_state("led_red", True)
        await self._gpio.set_pin_state("led_green", False)
        await self._gpio.set_pin_state("conveyor", False)

    async def load_and_set_active_profile(self, profile_id: int) -> bool:
        """
        Loads a profile from the DATABASE and commands the camera service via Redis.
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
        return self._active_profile
    
    def on_box_processed(self):
        """Callback for the detection service to increment the run counter."""
        if self._mode == OperatingMode.RUNNING:
            self._current_count += 1

    async def start_run(self):
        async with self._lock:
            if self._mode not in [OperatingMode.IDLE, OperatingMode.PAUSED]:
                return

            print("Orchestrator: Starting production run.")
            self._current_count = 0 # Reset count at the start of a run
            self._mode = OperatingMode.RUNNING
            await self._gpio.set_pin_state("led_red", False)
            await self._gpio.set_pin_state("led_green", True)
            await self._gpio.set_pin_state("conveyor", True)

    async def stop_run(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED:
                return

            print("Orchestrator: Stopping all operations and unloading profile.")
            self._mode = OperatingMode.STOPPED
            self._active_profile = None
            self._current_count = 0
            await self.initialize_hardware_state()

    def get_status(self) -> dict:
        profile_name = self._active_profile.name if self._active_profile else "None"
        return {
            "mode": self._mode.value,
            "active_profile": profile_name,
            "run_progress": self._current_count,
        }