import asyncio
from enum import Enum, auto
from typing import Optional # +++ Add Optional for the task hint

from app.core.gpio_controller import AsyncGPIOController
from config import settings

class OperatingMode(str, Enum):
    STOPPED = "Stopped"
    RUNNING_BATCH = "Running Batch"
    PAUSED_BETWEEN_BATCHES = "Waiting Between Batches"

class AsyncOrchestrationService:
    def __init__(self, gpio: AsyncGPIOController):
        self._gpio = gpio
        self._mode = OperatingMode.STOPPED
        self._batch_target = 0
        self._current_batch_count = 0
        self._lock = asyncio.Lock()
        self._post_batch_delay = settings.ORCHESTRATION.POST_BATCH_DELAY_SEC
        self._batch_task: Optional[asyncio.Task] = None # Hint changed to Optional

    async def initialize_hardware_state(self):
        """Sets the hardware to the default 'stopped' state on startup."""
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        await self._gpio.set_pin_state("gate", False)
        await self._gpio.set_pin_state("led_red", True)
        await self._gpio.set_pin_state("led_green", False)
        await self._gpio.set_pin_state("conveyor", False)

    # --- NEW: Method to update configuration live ---
    async def update_batch_config(self, size: int, delay: int):
        """Updates the batch configuration parameters live."""
        async with self._lock:
            print(f"Orchestrator: Updating config. New Batch Size: {size}, New Delay: {delay}")
            # The new size will apply to the next batch to start.
            # If a batch is running, its original target is preserved.
            if self._mode != OperatingMode.RUNNING_BATCH:
                self._batch_target = size
            
            self._post_batch_delay = delay
            
    async def start_batch(self, size: int):
        async with self._lock:
            if self._mode == OperatingMode.RUNNING_BATCH:
                print("Orchestrator: Batch already running. Ignoring start command.")
                return

            print(f"Orchestrator: Starting new batch of size {size}.")
            self._batch_target = size
            self._current_batch_count = 0
            self._mode = OperatingMode.RUNNING_BATCH

            await self._gpio.set_pin_state("gate", True)
            await self._gpio.set_pin_state("led_red", False)
            await self._gpio.set_pin_state("led_green", True)
            await self._gpio.set_pin_state("conveyor", True)

    async def stop_process(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED:
                return

            print("Orchestrator: Stopping all operations.")
            self._mode = OperatingMode.STOPPED
            self._batch_target = 0
            self._current_batch_count = 0

            if self._batch_task and not self._batch_task.done():
                self._batch_task.cancel()

            await self.initialize_hardware_state()

    async def on_box_counted(self):
        """Callback to be triggered by DetectionService."""
        async with self._lock:
            if self._mode != OperatingMode.RUNNING_BATCH:
                return

            self._current_batch_count += 1
            print(f"Orchestrator: Batch progress: {self._current_batch_count}/{self._batch_target}")

            if self._current_batch_count >= self._batch_target:
                print("Orchestrator: Batch completed.")
                self._batch_task = asyncio.create_task(self._end_of_batch_sequence())

    async def _end_of_batch_sequence(self):
        """Handles the transition between batches."""
        async with self._lock:
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES
            await self._gpio.set_pin_state("conveyor", False)
            await self._gpio.set_pin_state("led_green", False)
            await self._gpio.set_pin_state("led_red", True)
        
        print(f"Orchestrator: Pausing for {self._post_batch_delay} seconds...")
        await asyncio.sleep(self._post_batch_delay)

        # After delay, start the next batch with the potentially updated target size
        print("Orchestrator: Delay complete, starting next batch.")
        await self.start_batch(self._batch_target)
    
    def get_status(self) -> dict:
        """Returns the current orchestration status for WebSocket updates."""
        return {
            "mode": self._mode.value,
            "batch_target": self._batch_target,
            "batch_progress": self._current_batch_count,
            "post_batch_delay": self._post_batch_delay, # +++ Also send current delay back to UI
        }