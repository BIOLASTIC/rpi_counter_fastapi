"""
FINAL REVISION: Corrects the web path generation for saved images
to align with the new, dedicated /captures static mount point.
"""
import asyncio
import time
import redis.asyncio as redis
from enum import Enum
from typing import Optional, Tuple
from pydantic import BaseModel
import multiprocessing
import cv2
import numpy as np
from pathlib import Path

from redis import exceptions as redis_exceptions
from app.services.notification_service import AsyncNotificationService

class CameraHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncCameraManager:
    def __init__(self, notification_service: AsyncNotificationService):
        from config import settings
        self._config = settings.CAMERA
        self._notification_service = notification_service
        self._frame_queue = asyncio.Queue(maxsize=5)
        self._listener_task: Optional[asyncio.Task] = None
        self._health_status = CameraHealthStatus.DISCONNECTED
        self.redis_client = redis.from_url("redis://localhost")
        
        self._captures_dir = Path(self._config.CAPTURES_DIR)
        self._last_event_image_path: Optional[str] = None
        self._last_surveillance_image_path: Optional[str] = None

    def start(self):
        if not self._listener_task or self._listener_task.done():
            self._listener_task = asyncio.create_task(self._redis_listener())
            print("Camera Manager: Started Redis listener for frames.")

    async def stop(self):
        if self._listener_task: self._listener_task.cancel()
        await self.redis_client.close()
        print("Camera Manager: Stopped Redis listener.")

    async def _redis_listener(self):
        # ... (this method is unchanged)
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

    async def capture_and_save_image(self, filename: str, image_type: str) -> Optional[str]:
        """
        Grabs the latest frame from the queue, saves it, and returns the web-accessible path.
        """
        if self._health_status != CameraHealthStatus.CONNECTED or self._frame_queue.empty():
            return None
        
        try:
            jpeg_bytes = await self._frame_queue.get()
            self._frame_queue.task_done()

            def save_image_sync():
                np_array = np.frombuffer(jpeg_bytes, np.uint8)
                img_decoded = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                if img_decoded is None: return None
                
                full_path = self._captures_dir / filename
                cv2.imwrite(str(full_path), img_decoded)
                
                # --- DEFINITIVE FIX ---
                # Generate a path that matches the new mount point in main.py
                return f"/captures/{filename}"

            web_path = await asyncio.to_thread(save_image_sync)

            if web_path:
                if image_type == 'event':
                    self._last_event_image_path = web_path
                elif image_type == 'surveillance':
                    self._last_surveillance_image_path = web_path
            return web_path
            
        except Exception as e:
            print(f"Error saving image {filename}: {e}")
            return None

    async def health_check(self) -> CameraHealthStatus:
        return self._health_status

    def get_last_event_image_path(self) -> Optional[str]:
        return self._last_event_image_path
        
    def get_last_surveillance_image_path(self) -> Optional[str]:
        return self._last_surveillance_image_path