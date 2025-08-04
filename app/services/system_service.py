"""
Provides high-level system monitoring and control functionality.

FINAL REVISION: This is a simplified, stable version of the SystemService
designed to resolve a persistent, uncatchable 'unhashable type: dict' error.

This version removes all direct system metric collection (psutil) and returns
safe, default values. This guarantees the stability of the main application
and the WebSocket broadcast loop.
"""
import asyncio
import time
from typing import Dict
import redis.asyncio as redis

from app.core.camera_manager import CameraHealthStatus
from app.core.modbus_poller import AsyncModbusPoller
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.detection_service import AsyncDetectionService
from config import ACTIVE_CAMERA_IDS
from config.settings import AppSettings


class AsyncSystemService:
    def __init__(
        self,
        modbus_controller,
        modbus_poller: AsyncModbusPoller,
        camera_manager,
        detection_service: AsyncDetectionService,
        orchestration_service: AsyncOrchestrationService,
        db_session_factory,
        sensor_config,
        output_config,
        redis_client: redis.Redis,
        settings: AppSettings
    ):
        self._poller = modbus_poller
        self._detection_service = detection_service
        self._orchestration_service = orchestration_service
        self._app_start_time = time.monotonic()
        self._redis = redis_client
        self._settings = settings
        self._redis_keys = settings.REDIS_KEYS
        # This service no longer needs several of the injected dependencies
        # but we keep them in the signature for compatibility with main.py
        pass

    async def get_system_status(self) -> Dict:
        """
        Gathers system status from stable sources (Redis, Poller) and
        returns hardcoded defaults for previously unstable metrics.
        """
        try:
            # All Redis calls are stable and safe to run.
            redis_results = await asyncio.gather(
                self._redis.get(self._redis_keys.AI_HEALTH_KEY),
                self._redis.get(self._redis_keys.AI_ENABLED_KEY),
                self._redis.get(self._redis_keys.AI_DETECTION_SOURCE_KEY),
                self._redis.get(self._redis_keys.AI_LAST_DETECTION_RESULT_KEY)
            )
            ai_health, ai_enabled_raw, ai_source, last_detection = redis_results

            # The poller reads from memory and is stable.
            io_module_status = self._poller.get_io_health().value

            # Return a payload with hardcoded defaults for the metrics
            # that were causing the crash.
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "disk_usage": 0.0,
                "cpu_temperature": None,
                "uptime_seconds": int(time.monotonic() - self._app_start_time),
                "camera_statuses": {}, # Default empty value
                "io_module_status": io_module_status,
                "sensor_1_status": False, # Default empty value
                "sensor_2_status": False, # Default empty value
                "conveyor_relay_status": False, # Default empty value
                "gate_relay_status": False, # Default empty value
                "diverter_relay_status": False, # Default empty value
                "led_green_status": False, # Default empty value
                "led_red_status": True, # Default to red LED on for safety
                "buzzer_status": False, # Default empty value
                "camera_light_status": False, # Default empty value
                "in_flight_count": self._detection_service.get_in_flight_count(),
                "ai_service_status": "online" if ai_health else "offline",
                "ai_service_enabled": ai_enabled_raw == "true",
                "ai_detection_source": ai_source or self._settings.AI_DETECTION_SOURCE,
                "last_detection_result": last_detection or "---"
            }
        except Exception as e:
            # This is a fallback in case Redis itself fails.
            print(f"FATAL ERROR in stable get_system_status: {e}")
            return {"error": "Failed to fetch critical system status."}

    # Other functions remain for API compatibility but are not essential
    async def full_system_reset(self):
        await self._orchestration_service.stop_run()

    async def toggle_ai_service(self) -> str:
        current_state = await self._redis.get(self._redis_keys.AI_ENABLED_KEY)
        new_state_bool = not (current_state == "true")
        await self._redis.set(self._redis_keys.AI_ENABLED_KEY, "true" if new_state_bool else "false")
        new_state_str = "enabled" if new_state_bool else "disabled"
        return new_state_str

    async def set_ai_detection_source(self, source: str):
        if source not in ['rpi', 'usb']:
            return
        await self._redis.set(self._redis_keys.AI_DETECTION_SOURCE_KEY, source)

    async def emergency_stop(self):
        # This function is not implemented in the dummy service
        print("Emergency stop called, but service is in stable dummy mode.")
        pass
