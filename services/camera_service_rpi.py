"""
Standalone Camera Service for the Raspberry Pi Camera Module.
FINAL REVISION: This script is now completely self-contained and robust.

- It now checks if the connected camera supports autofocus before attempting
  to set autofocus controls, fixing the AttributeError for fixed-focus cameras
  like the imx219. This makes the script compatible with multiple camera models.
- It correctly finds the numerical index of the camera based on the ID string.
- It continues to listen to the Redis command channel for on-the-fly profile updates.
"""
import time
import cv2
import redis
import traceback
import json
import threading
from pathlib import Path
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Global Camera Object ---
camera = None

# --- Robust Path and Configuration ---
ENV_PATH = Path(__file__).parent.parent / ".env"

class RpiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_prefix='CAMERA_RPI_', case_sensitive=False, extra='ignore')
    ID: str
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_prefix='REDIS_', case_sensitive=False, extra='ignore')
    HOST: str = 'localhost'
    PORT: int = 6379

REDIS_COMMAND_CHANNEL = "camera:commands:rpi"

def apply_camera_settings(settings_dict: dict):
    """Applies a dictionary of settings to the global picamera2 object."""
    global camera
    if camera is None:
        print("[RPI Camera Service] Error: Cannot apply settings, camera is not available.", flush=True)
        return

    print("\n--- Applying New RPi Camera Settings from Command ---", flush=True)
    from picamera2 import controls
    
    controls_to_set = {}
    
    # --- DEFINITIVE FIX: Check if the camera supports Autofocus before setting it ---
    if 'autofocus' in settings_dict:
        # Check the list of available controls for this specific camera model.
        if 'AfMode' in camera.camera_controls:
            af_mode = controls.AfMode.Continuous if settings_dict['autofocus'] else controls.AfMode.Manual
            controls_to_set['AfMode'] = af_mode
            print(f"  -> AF Mode: {af_mode.name}", flush=True)
        else:
            # If the control doesn't exist, inform the user and skip it.
            print("  -> AF Mode: Not supported by this camera model (imx219). Skipping.", flush=True)

    if 'white_balance_temp' in settings_dict:
        controls_to_set['AwbEnable'] = settings_dict['white_balance_temp'] == 0
        print(f"  -> AWB Enable: {controls_to_set['AwbEnable']}", flush=True)
    
    use_auto_exposure = True
    if 'gain' in settings_dict and settings_dict['gain'] > 0:
        controls_to_set['AnalogueGain'] = float(settings_dict['gain'])
        use_auto_exposure = False
        print(f"  -> Manual AnalogueGain: {controls_to_set['AnalogueGain']}", flush=True)
        
    if 'exposure' in settings_dict and settings_dict['exposure'] > 0:
        controls_to_set['ExposureTime'] = settings_dict['exposure']
        use_auto_exposure = False
        print(f"  -> Manual ExposureTime (µs): {controls_to_set['ExposureTime']}", flush=True)

    controls_to_set['AeEnable'] = use_auto_exposure
    print(f"  -> Auto Exposure Enable: {use_auto_exposure}", flush=True)

    if 'brightness' in settings_dict:
        scaled_brightness = (settings_dict['brightness'] / 255.0) * 2.0 - 1.0
        controls_to_set['Brightness'] = scaled_brightness
        print(f"  -> Brightness: {scaled_brightness:.2f}", flush=True)

    if controls_to_set:
        camera.set_controls(controls_to_set)
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
    try:
        rpi_cam_settings = RpiSettings()
        redis_settings = RedisSettings()
    except ValidationError as e:
        if any(err.get('type') == 'missing' and err.get('loc') == ('ID',) for err in e.errors()):
            print("\n" + "="*60, "\n--- CONFIGURATION ERROR ---")
            print("FATAL: The 'CAMERA_RPI_ID' is missing from your .env file.")
            print("\nTo fix this: run 'libcamera-hello --list-cameras', copy the ID,")
            print(f"and add it to your .env file at: {ENV_PATH}")
            print("\n   CAMERA_RPI_ID='your_camera_id_here'\n" + "="*60 + "\n")
            return
        else:
            raise

    redis_client = None
    try:
        from picamera2 import Picamera2
        
        target_camera_id = rpi_cam_settings.ID
        all_cameras_info = Picamera2.global_camera_info()
        if not all_cameras_info:
            print("FATAL ERROR: No cameras found by the libcamera system. Check hardware connection.")
            return

        camera_index = None
        for i, info in enumerate(all_cameras_info):
            if info['Id'] == target_camera_id:
                camera_index = i
                break
        
        if camera_index is None:
            print("\n" + "="*70, "\n--- CAMERA NOT FOUND ERROR ---")
            print(f"FATAL: The camera ID '{target_camera_id}' from your .env file was NOT FOUND.")
            print("\nAvailable cameras are:")
            for i, info in enumerate(all_cameras_info):
                print(f"  - Index {i}: {info['Id']} ({info['Model']})")
            print("\nPlease ensure the correct ID is copied into your .env file.", "\n" + "="*70 + "\n")
            return
        
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=True)
        redis_client.ping()
        print("[RPI Camera Service] Redis connection successful.", flush=True)

        listener_thread = threading.Thread(target=command_listener, args=(redis_client,), daemon=True)
        listener_thread.start()

        print(f"[RPI Camera Service] Initializing camera at index {camera_index} (ID: {target_camera_id})", flush=True)
        camera = Picamera2(camera_index)
        
        config = camera.create_video_configuration(
            main={"size": (rpi_cam_settings.RESOLUTION_WIDTH, rpi_cam_settings.RESOLUTION_HEIGHT), "format": "RGB888"}
        )
        camera.configure(config)
        camera.set_controls({"FrameRate": rpi_cam_settings.FPS})
        
        # This will now run without crashing, as it will intelligently skip the
        # unsupported autofocus setting.
        apply_camera_settings({'autofocus': True, 'white_balance_temp': 0})
        
        camera.start()
        frame_channel = 'camera:frames:rpi'
        print(f"[RPI Camera Service] Camera started. Publishing to '{frame_channel}'.", flush=True)
        time.sleep(2) 

        while True:
            frame = camera.capture_array()
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, rpi_cam_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())

    except ImportError:
        print("[RPI Camera Service] FATAL ERROR: The 'picamera2' library is not installed.", flush=True)
    except Exception as e:
        print(f"[RPI Camera Service] FATAL ERROR: An unexpected error occurred.", flush=True)
        print(traceback.format_exc(), flush=True)
    finally:
        if 'camera' in locals() and camera and camera.is_open:
            camera.stop()
        if 'redis_client' in locals() and redis_client:
            redis_client.close()
        print("[RPI Camera Service] Exited.", flush=True)

if __name__ == "__main__":
    main()