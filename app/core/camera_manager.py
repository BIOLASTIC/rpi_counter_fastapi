import asyncio
import time
import redis.asyncio as redis
from enum import Enum
from typing import Optional, Dict, Set, List, Tuple
import cv2
import numpy as np
from pathlib import Path

from redis import exceptions as redis_exceptions
from app.services.notification_service import AsyncNotificationService
from config import settings # Import settings to get the base directory

PROJECT_ROOT = Path(__file__).parent.parent.parent

class CameraHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncCameraManager:
    def __init__(
        self,
        notification_service: AsyncNotificationService,
        captures_dir: str,
        redis_client: redis.Redis,
        active_camera_ids: List[str]
    ):
        self.redis_client = redis_client
        self._notification_service = notification_service
        # --- FIX: Store the absolute base path for captures ---
        self._captures_dir_base = PROJECT_ROOT / captures_dir
        self._active_camera_ids = active_camera_ids
        
        self._listener_tasks: Dict[str, asyncio.Task] = {}
        self._health_status: Dict[str, CameraHealthStatus] = {cam_id: CameraHealthStatus.DISCONNECTED for cam_id in self._active_camera_ids}
        self._frame_queues: Dict[str, asyncio.Queue] = {cam_id: asyncio.Queue(maxsize=5) for cam_id in self._active_camera_ids}
        self._stream_listeners: Dict[str, Set[asyncio.Queue]] = {cam_id: set() for cam_id in self._active_camera_ids}
        self._last_event_image_paths: Dict[str, Optional[str]] = {cam_id: None for cam_id in self._active_camera_ids}
        self._stream_lock = asyncio.Lock()

    def start(self):
        for cam_id in self._active_camera_ids:
            if cam_id not in self._listener_tasks or self._listener_tasks[cam_id].done():
                self._listener_tasks[cam_id] = asyncio.create_task(self._redis_listener(cam_id))

    async def stop(self):
        for task in self._listener_tasks.values():
            if task and not task.done():
                task.cancel()

    async def _redis_listener(self, cam_id: str):
        channel_name = f"camera:frames:{cam_id}"
        pubsub = self.redis_client.pubsub()
        while True:
            try:
                await pubsub.subscribe(channel_name)
                print(f"[Camera Manager] Subscribed to Redis channel: {channel_name}")
                while True:
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
                    if message:
                        if self._health_status[cam_id] != CameraHealthStatus.CONNECTED:
                            print(f"[Camera Manager] Re-established frame stream for '{cam_id}'.")
                        self._health_status[cam_id] = CameraHealthStatus.CONNECTED
                        frame_data = message['data']
                        
                        while not self._frame_queues[cam_id].empty():
                            self._frame_queues[cam_id].get_nowait()
                        self._frame_queues[cam_id].put_nowait(frame_data)
                        
                        async with self._stream_lock:
                            listeners = list(self._stream_listeners[cam_id])
                        
                        for queue in listeners:
                            if not queue.full():
                                try: queue.put_nowait(frame_data)
                                except asyncio.QueueFull: pass
                    else:
                        if self._health_status.get(cam_id) == CameraHealthStatus.CONNECTED:
                            await self._notification_service.send_alert("WARNING", f"Camera '{cam_id}' has stopped publishing frames.")
                        self._health_status[cam_id] = CameraHealthStatus.DISCONNECTED
            except redis_exceptions.ConnectionError:
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                print(f"[Camera Manager] Redis connection lost for '{cam_id}'. Retrying in 5 seconds...")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                print(f"[Camera Manager] Listener for '{cam_id}' cancelled.")
                break
            except Exception as e:
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                print(f"[Camera Manager] Unexpected error in '{cam_id}' listener: {e}. Retrying in 10 seconds...")
                await asyncio.sleep(10)
        await pubsub.close()
    
    async def start_stream(self, cam_id: str) -> Optional[asyncio.Queue]:
        if cam_id not in self._active_camera_ids: return None
        q = asyncio.Queue(maxsize=2)
        async with self._stream_lock: self._stream_listeners[cam_id].add(q)
        print(f"[Camera Manager] New stream client connected for '{cam_id}'. Total listeners: {len(self._stream_listeners[cam_id])}")
        return q

    async def stop_stream(self, cam_id: str, queue: asyncio.Queue):
        if cam_id not in self._active_camera_ids: return
        async with self._stream_lock: self._stream_listeners[cam_id].discard(queue)
        print(f"[Camera Manager] Stream client disconnected for '{cam_id}'. Remaining listeners: {len(self._stream_listeners[cam_id])}")
        
    async def capture_and_save_image(self, cam_id: str, filename_prefix: str) -> Tuple[Optional[str], Optional[str], Optional[bytes]]:
        if self._health_status.get(cam_id) != CameraHealthStatus.CONNECTED:
            print(f"CAMERA MANAGER ERROR: Cannot capture image. Camera '{cam_id}' is not connected.")
            return None, None, None
        try:
            jpeg_bytes = await asyncio.wait_for(self._frame_queues[cam_id].get(), timeout=1.0)
            self._frame_queues[cam_id].task_done()
            
            captures_dir = self._captures_dir_base / cam_id
            captures_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{filename_prefix}_{int(time.time())}.jpg"
            full_path = captures_dir / filename

            def save_image_sync():
                try:
                    np_array = np.frombuffer(jpeg_bytes, np.uint8)
                    img_decoded = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                    if img_decoded is None: 
                        print(f"CAMERA MANAGER ERROR: OpenCV failed to decode image buffer for '{filename}'.")
                        return None, None
                    
                    cv2.imwrite(str(full_path), img_decoded)
                    
                    if not full_path.exists():
                        print(f"CAMERA MANAGER ERROR: Failed to save image to disk at '{full_path}'. Check permissions.")
                        return None, None
                    
                    web_path = f"/captures/{cam_id}/{filename}"
                    return web_path, str(full_path)
                except Exception as e:
                    print(f"CAMERA MANAGER ERROR in save_image_sync: {e}")
                    return None, None
            
            web_path, physical_path = await asyncio.to_thread(save_image_sync)
            
            if web_path:
                self._last_event_image_paths[cam_id] = web_path
            
            return web_path, physical_path, jpeg_bytes
            
        except asyncio.TimeoutError:
            print(f"CAMERA MANAGER TIMEOUT: Did not receive frame from '{cam_id}' within 1 second.")
            return None, None, None
        except Exception as e:
            print(f"CAMERA MANAGER ERROR during capture/save for '{cam_id}': {e}")
            return None, None, None
            
    def get_health_status(self, cam_id: str) -> CameraHealthStatus:
        return self._health_status.get(cam_id, CameraHealthStatus.DISCONNECTED)

    def get_all_health_statuses(self) -> Dict[str, str]:
        return {cam_id: status.value for cam_id, status in self._health_status.items()}

    def get_last_event_image_path(self, cam_id: str) -> Optional[str]:
        return self._last_event_image_paths.get(cam_id)