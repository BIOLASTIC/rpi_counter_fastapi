import asyncio
from enum import Enum, auto

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
        self._batch_task: asyncio.Task = None

    async def initialize_hardware_state(self):
        """Sets the hardware to the default 'stopped' state on startup."""
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        await self._gpio.set_pin_state("gate", False)      # Gate Closed
        await self._gpio.set_pin_state("led_red", True)     # Red On
        await self._gpio.set_pin_state("led_green", False)  # Green Off
        await self._gpio.set_pin_state("conveyor", False)   # Conveyor Off

    async def start_batch(self, size: int):
        async with self._lock:
            if self._mode == OperatingMode.RUNNING_BATCH:
                print("Orchestrator: Batch already running. Ignoring start command.")
                return

            print(f"Orchestrator: Starting new batch of size {size}.")
            self._batch_target = size
            self._current_batch_count = 0
            self._mode = OperatingMode.RUNNING_BATCH

            # Set hardware to 'ready' state
            await self._gpio.set_pin_state("gate", True)        # Gate Open
            await self._gpio.set_pin_state("led_red", False)    # Red Off
            await self._gpio.set_pin_state("led_green", True)   # Green On
            await self._gpio.set_pin_state("conveyor", True)    # Conveyor On

    async def stop_process(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED:
                return

            print("Orchestrator: Stopping all operations.")
            self._mode = OperatingMode.STOPPED
            self._batch_target = 0
            self._current_batch_count = 0

            # Cancel any pending batch delay task
            if self._batch_task and not self._batch_task.done():
                self._batch_task.cancel()

            # Set hardware to 'stopped' state
            await self.initialize_hardware_state()

    async def on_box_counted(self):
        """Callback to be triggered by DetectionService."""
        async with self._lock:
            if self._mode != OperatingMode.RUNNING_BATCH:
                return # Ignore counts if we're not in the middle of a batch

            self._current_batch_count += 1
            print(f"Orchestrator: Batch progress: {self._current_batch_count}/{self._batch_target}")

            if self._current_batch_count >= self._batch_target:
                print("Orchestrator: Batch completed.")
                # Start the end-of-batch sequence in the background
                self._batch_task = asyncio.create_task(self._end_of_batch_sequence())

    async def _end_of_batch_sequence(self):
        """Handles the transition between batches."""
        async with self._lock:
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES
            await self._gpio.set_pin_state("conveyor", False) # Stop conveyor first
            await self._gpio.set_pin_state("led_green", False)
            await self._gpio.set_pin_state("led_red", True)
        
        print(f"Orchestrator: Pausing for {self._post_batch_delay} seconds...")
        await asyncio.sleep(self._post_batch_delay)

        # After delay, automatically start the next batch
        print("Orchestrator: Delay complete, starting next batch.")
        await self.start_batch(self._batch_target)
    
    def get_status(self) -> dict:
        """Returns the current orchestration status for WebSocket updates."""
        return {
            "mode": self._mode.value,
            "batch_target": self._batch_target,
            "batch_progress": self._current_batch_count,
        }