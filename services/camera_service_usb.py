"""
Standalone Camera Service for a USB V4L2 Camera.
FINAL REVISION: This script is now completely self-contained and includes its
own robust configuration loader to definitively fix the .env loading issue.
"""
import time
import cv2
import redis
import traceback
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

# --- Self-Contained Configuration Loader ---

# Step 1: Define the absolute path to the .env file in the project root
# __file__ is the path to this script (camera_service_usb.py)
# .parent is the 'services' directory
# .parent again is the project root directory
ENV_PATH = Path(__file__).parent.parent / ".env"

class UsbCameraSettings(BaseSettings):
    # This model is now defined directly inside the service script
    model_config = SettingsConfigDict(
        env_prefix='CAMERA_USB_',
        case_sensitive=False,
        env_file=str(ENV_PATH), # Explicitly tell it which .env file to use
        extra='ignore'
    )
    DEVICE_INDEX: int = 0
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)
    EXPOSURE: int = 0
    GAIN: int = 0
    BRIGHTNESS: int = Field(128, ge=0, le=255)
    AUTOFOCUS: bool = True

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='REDIS_',
        case_sensitive=False,
        env_file=str(ENV_PATH),
        extra='ignore'
    )
    HOST: str = 'localhost'
    PORT: int = 6379

@lru_cache()
def load_settings():
    """Loads and caches settings, printing a diagnostic message."""
    if not ENV_PATH.exists():
        print(f"[USB Camera Service] FATAL: .env file not found at expected path: {ENV_PATH}")
    else:
        print(f"[USB Camera Service] Found .env file at: {ENV_PATH}. Loading settings.")
    
    usb_settings = UsbCameraSettings()
    redis_settings = RedisSettings()
    return usb_settings, redis_settings

def main():
    # --- Load Settings and Print Diagnostics ---
    try:
        usb_cam_settings, redis_settings = load_settings()
        
        # Print the loaded settings to confirm they are correct
        print("\n--- Loaded USB Camera Settings ---")
        print(f"  Device Index: {usb_cam_settings.DEVICE_INDEX}")
        print(f"  Exposure:     {usb_cam_settings.EXPOSURE}")
        print(f"  Gain:         {usb_cam_settings.GAIN}")
        print(f"  Brightness:   {usb_cam_settings.BRIGHTNESS}")
        print(f"  Autofocus:    {usb_cam_settings.AUTOFOCUS}")
        print("----------------------------------\n")

    except Exception as e:
        print(f"[USB Camera Service] FATAL: Could not load settings. Error: {e}")
        return

    camera = None
    redis_client = None
    frame_channel = 'camera:frames:usb'

    try:
        print(f"[USB Camera Service] Connecting to Redis at {redis_settings.HOST}:{redis_settings.PORT}...")
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=False)
        redis_client.ping()
        print("[USB Camera Service] Redis connection successful.")

        device_index = usb_cam_settings.DEVICE_INDEX
        print(f"[USB Camera Service] Attempting to initialize camera at /dev/video{device_index}...")
        camera = cv2.VideoCapture(device_index, cv2.CAP_V4L2) 
        
        if not camera.isOpened():
            raise RuntimeError(f"Could not open camera at index {device_index}. Check `v4l2-ctl --list-devices` and ensure permissions are correct.")

        # --- APPLY ALL CAMERA SETTINGS FROM CONFIG ---
        print("[USB Camera Service] Applying base settings...")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, usb_cam_settings.RESOLUTION_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, usb_cam_settings.RESOLUTION_HEIGHT)
        camera.set(cv2.CAP_PROP_FPS, usb_cam_settings.FPS)
        
        print("[USB Camera Service] Applying manual controls...")
        
        camera.set(cv2.CAP_PROP_AUTOFOCUS, 1 if usb_cam_settings.AUTOFOCUS else 0)
        print(f"  -> Applying Autofocus: {'On' if usb_cam_settings.AUTOFOCUS else 'Off'}")

        if usb_cam_settings.GAIN > 0:
            camera.set(cv2.CAP_PROP_GAIN, usb_cam_settings.GAIN)
            print(f"  -> Applying Manual Gain: {usb_cam_settings.GAIN}")
        else:
            print("  -> Using Auto Gain")
            
        camera.set(cv2.CAP_PROP_BRIGHTNESS, usb_cam_settings.BRIGHTNESS)
        print(f"  -> Applying Brightness: {usb_cam_settings.BRIGHTNESS}")
        
        if usb_cam_settings.EXPOSURE != 0:
            # Set to Manual Exposure Mode
            camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 
            camera.set(cv2.CAP_PROP_EXPOSURE, usb_cam_settings.EXPOSURE)
            print(f"  -> Applying Manual Exposure: {usb_cam_settings.EXPOSURE}")
        else:
            # Set to Auto Exposure Mode
            camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) 
            print("  -> Using Auto Exposure")
        
        print(f"[USB Camera Service] Camera at index {device_index} started. Publishing to '{frame_channel}'.")
        time.sleep(1)

        while True:
            ret, frame = camera.read()
            if not ret:
                print(f"[USB Camera Service] Warning: Dropped frame from camera {device_index}. Retrying...")
                time.sleep(0.1)
                continue

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, usb_cam_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())
            
    except Exception as e:
        print(f"[USB Camera Service] FATAL ERROR: An unexpected error occurred.")
        print(traceback.format_exc())
    finally:
        if camera and camera.isOpened(): camera.release()
        if redis_client: redis_client.close()
        print("[USB Camera Service] Exited.")

if __name__ == "__main__":
    main()