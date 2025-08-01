"""
Standalone Camera Service for a USB V4L2 Camera.
FINAL ARCHITECTURE: This service is now a 'dumb' command receiver.

- It NO LONGER reads camera profiles (exposure, gain, etc.) from any file.
- It loads only essential hardware constants (device index, jpeg quality) from .env.
- It starts up with simple 'auto' settings.
- It listens on a Redis channel for commands from the main application, which
  will tell it which settings to apply on the fly.
- ADDED: Verbose logging to diagnose frame publishing issues.
"""
import time
import cv2
import redis
import traceback
import json
import threading
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Constants and Paths ---
ENV_PATH = Path(__file__).parent.parent / ".env"
REDIS_COMMAND_CHANNEL = "camera:commands:usb"
camera = None # Global camera object

# --- Simple Settings Loader for Essential Hardware Config ONLY ---
class UsbHardwareSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='CAMERA_USB_',
        case_sensitive=False,
        env_file=str(ENV_PATH),
        extra='ignore'
    )
    DEVICE_INDEX: int = 0
    JPEG_QUALITY: int = 90

def apply_camera_settings(settings_dict: dict):
    """Applies a dictionary of settings to the global camera object."""
    global camera
    if camera is None or not camera.isOpened():
        print("[USB Camera Service] Error: Cannot apply settings, camera is not available.", flush=True)
        return

    print("\n--- Applying New Camera Settings from Command ---", flush=True)
    
    autofocus = settings_dict.get('autofocus', True)
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 1 if autofocus else 0)
    print(f"  -> Autofocus: {'On' if autofocus else 'Off'}", flush=True)
    
    wb_temp = settings_dict.get('white_balance_temp', 0)
    if wb_temp > 0:
        camera.set(cv2.CAP_PROP_AUTO_WB, 0)
        camera.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, wb_temp)
        print(f"  -> Manual White Balance: {wb_temp}", flush=True)
    else:
        camera.set(cv2.CAP_PROP_AUTO_WB, 1)
        print(f"  -> Auto White Balance", flush=True)
        
    gain = settings_dict.get('gain', 0)
    if gain >= 0: # Gain can be 0
        camera.set(cv2.CAP_PROP_GAIN, gain)
        print(f"  -> Manual Gain: {gain}", flush=True)
    
    brightness = settings_dict.get('brightness', 128)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print(f"  -> Brightness: {brightness}", flush=True)

    exposure = settings_dict.get('exposure', 0)
    if exposure != 0:
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
        print(f"  -> Manual Exposure: {exposure}", flush=True)
    else:
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        print(f"  -> Auto Exposure", flush=True)
    print("-------------------------------------------\n", flush=True)


def command_listener(redis_client: redis.Redis):
    """A thread that listens for commands and applies settings."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_COMMAND_CHANNEL)
    print(f"[Command Listener] Subscribed to '{REDIS_COMMAND_CHANNEL}' for live commands.", flush=True)
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                command = json.loads(message['data'])
                if command.get('action') == 'apply_settings':
                    settings_to_apply = command.get('settings')
                    if isinstance(settings_to_apply, dict):
                        apply_camera_settings(settings_to_apply)
            except Exception as e:
                print(f"[Command Listener] Error processing command: {e}", flush=True)

def main():
    global camera
    hardware_settings = UsbHardwareSettings()
    redis_client = None

    try:
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.ping()
        print("[USB Camera Service] Redis connection successful.", flush=True)

        listener_thread = threading.Thread(target=command_listener, args=(redis_client,), daemon=True)
        listener_thread.start()

        print(f"[USB Camera Service] Opening camera at index {hardware_settings.DEVICE_INDEX}...", flush=True)
        camera = cv2.VideoCapture(hardware_settings.DEVICE_INDEX, cv2.CAP_V4L2)
        if not camera.isOpened():
            raise RuntimeError(f"Could not open camera at index {hardware_settings.DEVICE_INDEX}.")
        print("[USB Camera Service] Camera opened successfully.", flush=True)

        apply_camera_settings({})
        
        frame_channel = 'camera:frames:usb'
        print(f"[USB Camera Service] Starting capture loop. Publishing to '{frame_channel}'.", flush=True)
        time.sleep(1)

        frame_count = 0
        last_log_time = time.time()
        while True:
            ret, frame = camera.read()
            if not ret:
                print("[USB Camera Service] WARNING: camera.read() returned False. Check camera connection.", flush=True)
                time.sleep(1) 
                continue

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, hardware_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())
            frame_count += 1
            
            # Log status every 5 seconds
            current_time = time.time()
            if current_time - last_log_time >= 5.0:
                print(f"[USB Camera Service] Published {frame_count} frames to '{frame_channel}' in the last 5 seconds.", flush=True)
                frame_count = 0
                last_log_time = current_time


    except Exception as e:
        print(f"[USB Camera Service] FATAL ERROR: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
    finally:
        if camera and camera.isOpened(): camera.release()
        if redis_client: redis_client.close()
        print("[USB Camera Service] Exited.", flush=True)

if __name__ == "__main__":
    main()