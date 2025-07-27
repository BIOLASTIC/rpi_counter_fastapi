"""
FINAL REVISION: The Redis exception import path is now corrected for
redis-py v5.x. This resolves the AttributeError and allows for graceful
handling of connection failures.
"""
import asyncio
import time
import redis.asyncio as redis
from enum import Enum
from typing import Optional, Tuple
from pydantic import BaseModel
import multiprocessing

# --- DEFINITIVE FIX FOR ATTRIBUTE ERROR ---
# Import the exceptions module directly from the top-level 'redis' package.
from redis import exceptions as redis_exceptions

from app.services.notification_service import AsyncNotificationService

# This function remains unchanged, running in the separate camera process.
def camera_process_worker(frame_queue: multiprocessing.Queue, stop_event: multiprocessing.Event, resolution: Tuple[int, int], fps: int):
    camera = None
    try:
        from picamera2 import Picamera2
        print("[Camera Process] Initializing...")
        camera = Picamera2()
        config = camera.create_video_configuration(main={"size": resolution, "format": "RGB888"})
        camera.configure(config)
        camera.start()
        print("[Camera Process] Capture started.")
        time.sleep(1)
        # Pre-flight check
        camera.capture_array()
        print("[Camera Process] Pre-flight check successful. Entering capture loop.")
        while not stop_event.is_set():
            frame = camera.capture_array()
            if not frame_queue.full():
                # In a real system, you would encode this frame (e.g., JPEG) before queuing
                frame_queue.put(frame)
    except Exception as e:
        print(f"[Camera Process] FATAL ERROR: {e}")
    finally:
        if camera and camera.is_open:
            camera.stop()
        print("[Camera Process] Exited cleanly.")

class CameraHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncCameraManager:
    def __init__(self, notification_service: AsyncNotificationService):
        from config import settings
        self._config = settings.CAMERA
        self._notification_service = notification_service
        self._frame_queue = asyncio.Queue(maxsize=5) # Internal async queue
        self._listener_task: Optional[asyncio.Task] = None
        self._health_status = CameraHealthStatus.DISCONNECTED
        self.redis_client = redis.from_url("redis://localhost")

    def start(self):
        if not self._listener_task or self._listener_task.done():
            self._listener_task = asyncio.create_task(self._redis_listener())
            print("Camera Manager: Started Redis listener for frames.")

    async def stop(self):
        if self._listener_task:
            self._listener_task.cancel()
        await self.redis_client.close()
        print("Camera Manager: Stopped Redis listener.")

    async def _redis_listener(self):
        while True:
            try:
                async with self.redis_client.pubsub() as pubsub:
                    await pubsub.subscribe("camera:frames")
                    print("Camera Manager: Subscribed to 'camera:frames' channel.")
                    if self._health_status != CameraHealthStatus.CONNECTED:
                         self._health_status = CameraHealthStatus.DISCONNECTED
                    
                    while True:
                        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
                        if message:
                            self._health_status = CameraHealthStatus.CONNECTED
                            if not self._frame_queue.full():
                               self._frame_queue.put_nowait(message['data'])
                        else:
                            if self._health_status == CameraHealthStatus.CONNECTED:
                                await self._notification_service.send_alert("WARNING", "Camera service has stopped publishing frames.")
                            self._health_status = CameraHealthStatus.DISCONNECTED
            
            # Use the corrected exception path
            except redis_exceptions.ConnectionError as e:
                if self._health_status != CameraHealthStatus.ERROR:
                    error_message = f"Cannot connect to Redis: {e}. Retrying in 10 seconds."
                    print(f"Camera Manager: {error_message}")
                    await self._notification_service.send_alert("CRITICAL", error_message)
                self._health_status = CameraHealthStatus.ERROR
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                print("Camera Manager: Redis listener shutting down.")
                break
            except Exception as e:
                print(f"Camera Manager: Unhandled error in Redis listener: {e}. Retrying in 10s.")
                self._health_status = CameraHealthStatus.ERROR
                await asyncio.sleep(10)

    async def get_frame(self) -> Optional[bytes]:
        try:
            return self._frame_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def health_check(self) -> CameraHealthStatus:
        return self._health_status
