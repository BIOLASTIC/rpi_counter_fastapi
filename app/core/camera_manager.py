"""
REVISED: Imports ACTIVE_CAMERA_IDS from the main application's config module.
"""
import asyncio
import time
import redis.asyncio as redis
from enum import Enum
from typing import Optional, Dict, Set
import cv2
import numpy as np
from pathlib import Path

from redis import exceptions as redis_exceptions
from app.services.notification_service import AsyncNotificationService
# --- THE FIX: Import from the main app's centralized config ---
from config import ACTIVE_CAMERA_IDS

class CameraHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncCameraManager:
    # The rest of this file's code is correct from the previous step.
    # No other changes are needed here.
    def __init__(self, notification_service: AsyncNotificationService, captures_dir: str):
        self.redis_client = redis.from_url("redis://localhost")
        self._notification_service = notification_service
        self._captures_dir_base = Path(captures_dir)
        self._listener_tasks: Dict[str, asyncio.Task] = {}
        self._health_status: Dict[str, CameraHealthStatus] = {cam_id: CameraHealthStatus.DISCONNECTED for cam_id in ACTIVE_CAMERA_IDS}
        self._frame_queues: Dict[str, asyncio.Queue] = {cam_id: asyncio.Queue(maxsize=5) for cam_id in ACTIVE_CAMERA_IDS}
        self._stream_listeners: Dict[str, Set[asyncio.Queue]] = {cam_id: set() for cam_id in ACTIVE_CAMERA_IDS}
        self._last_event_image_paths: Dict[str, Optional[str]] = {cam_id: None for cam_id in ACTIVE_CAMERA_IDS}
        self._stream_lock = asyncio.Lock()

    def start(self):
        for cam_id in ACTIVE_CAMERA_IDS:
            if cam_id not in self._listener_tasks or self._listener_tasks[cam_id].done():
                self._listener_tasks[cam_id] = asyncio.create_task(self._redis_listener(cam_id))
                print(f"Camera Manager: Started Redis listener for '{cam_id}'.")

    async def stop(self):
        for task in self._listener_tasks.values():
            if task and not task.done():
                task.cancel()
        await self.redis_client.close()
        print("Camera Manager: Stopped all Redis listeners.")

    async def _redis_listener(self, cam_id: str):
        channel_name = f"camera:frames:{cam_id}"
        while True:
            try:
                async with self.redis_client.pubsub() as pubsub:
                    await pubsub.subscribe(channel_name)
                    print(f"Camera Manager: Subscribed to '{channel_name}' channel.")
                    while True:
                        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
                        if message:
                            self._health_status[cam_id] = CameraHealthStatus.CONNECTED
                            frame_data = message['data']
                            if not self._frame_queues[cam_id].full():
                                self._frame_queues[cam_id].put_nowait(frame_data)
                            async with self._stream_lock:
                                for queue in self._stream_listeners[cam_id]:
                                    if not queue.full():
                                        queue.put_nowait(frame_data)
                        else:
                            if self._health_status.get(cam_id) == CameraHealthStatus.CONNECTED:
                                await self._notification_service.send_alert("WARNING", f"Camera '{cam_id}' has stopped publishing frames.")
                            self._health_status[cam_id] = CameraHealthStatus.DISCONNECTED
            except redis_exceptions.ConnectionError as e:
                if self._health_status.get(cam_id) != CameraHealthStatus.ERROR:
                    error_message = f"Cannot connect to Redis: {e}. Retrying in 10 seconds."
                    print(f"Camera Manager ({cam_id}): {error_message}")
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                print(f"Camera Manager: Redis listener for '{cam_id}' shutting down.")
                break
            except Exception as e:
                print(f"Camera Manager ({cam_id}): Unhandled error in Redis listener: {e}. Retrying in 10s.")
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                await asyncio.sleep(10)
    
    async def start_stream(self, cam_id: str) -> Optional[asyncio.Queue]:
        if cam_id not in ACTIVE_CAMERA_IDS: return None
        q = asyncio.Queue(maxsize=2)
        async with self._stream_lock:
            self._stream_listeners[cam_id].add(q)
        return q

    async def stop_stream(self, cam_id: str, queue: asyncio.Queue):
        if cam_id not in ACTIVE_CAMERA_IDS: return
        async with self._stream_lock:
            self._stream_listeners[cam_id].discard(queue)

    async def capture_and_save_image(self, cam_id: str, filename_prefix: str) -> Optional[str]:
        if self._health_status.get(cam_id) != CameraHealthStatus.CONNECTED or self._frame_queues[cam_id].empty():
            return None
        try:
            jpeg_bytes = await self._frame_queues[cam_id].get()
            self._frame_queues[cam_id].task_done()
            captures_dir = self._captures_dir_base / cam_id
            captures_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{filename_prefix}_{int(time.time())}.jpg"
            full_path = captures_dir / filename
            def save_image_sync():
                np_array = np.frombuffer(jpeg_bytes, np.uint8)
                img_decoded = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                if img_decoded is None: return None
                cv2.imwrite(str(full_path), img_decoded)
                return f"/captures/{cam_id}/{filename}"
            web_path = await asyncio.to_thread(save_image_sync)
            if web_path:
                self._last_event_image_paths[cam_id] = web_path
            return web_path
        except Exception as e:
            print(f"Error saving image for {cam_id}: {e}")
            return None

    def get_health_status(self, cam_id: str) -> CameraHealthStatus:
        return self._health_status.get(cam_id, CameraHealthStatus.DISCONNECTED)

    def get_all_health_statuses(self) -> Dict[str, str]:
        return {cam_id: status.value for cam_id, status in self._health_status.items()}

    def get_last_event_image_path(self, cam_id: str) -> Optional[str]:
        return self._last_event_image_paths.get(cam_id)