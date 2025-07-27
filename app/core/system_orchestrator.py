"""
Conceptual System Orchestrator
In our current design, the FastAPI lifespan manager in `main.py` acts as the
primary orchestrator. This file serves as a conceptual model for how more complex,
multi-service workflows could be managed.
"""
import asyncio

from .gpio_controller import AsyncGPIOController
from .camera_manager import AsyncCameraManager
from app.services.detection_service import AsyncDetectionService
from app.services.notification_service import AsyncNotificationService

class SystemOrchestrator:
    """
    A high-level class to coordinate major system operations.
    """
    def __init__(
        self,
        gpio: AsyncGPIOController,
        camera: AsyncCameraManager,
        detection: AsyncDetectionService,
        notifier: AsyncNotificationService,
    ):
        self.gpio = gpio
        self.camera = camera
        self.detection = detection
        self.notifier = notifier

    async def run_full_diagnostic_sequence(self):
        """
        An example of a complex workflow that involves multiple services.
        """
        print("Orchestrator: Starting full system diagnostic...")
        await self.notifier.send_alert("INFO", "Starting system diagnostics.")
        
        # Step 1: Check hardware
        gpio_health = await self.gpio.health_check()
        camera_health = await self.camera.health_check()
        
        # Step 2: Test hardware functions
        await self.gpio.beep(0.1)
        await self.gpio.blink_led("led_green", 0.1, 0) # Quick flash
        
        # Step 3: Log results
        print(f"Diagnostics complete: GPIO={gpio_health.value}, Camera={camera_health.value}")
        await self.notifier.send_alert("INFO", "Diagnostics complete.", {
            "gpio": gpio_health.value,
            "camera": camera_health.value
        })

    async def perform_safe_shutdown(self):
        """
        An orchestrated shutdown sequence.
        """
        print("Orchestrator: Performing safe shutdown.")
        await self.notifier.send_alert("WARNING", "System is shutting down.")
        await self.gpio.stop_conveyor()
        await self.gpio.close_gate() # Assuming a gate exists
        await self.gpio.shutdown()
        await self.camera.stop_capture()
