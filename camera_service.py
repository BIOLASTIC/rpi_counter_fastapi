"""
Standalone Camera Service.

REVISED: Reads manual camera control settings (shutter speed, ISO, focus)
from the configuration and applies them to the Picamera2 object on startup.
"""
import time
import cv2
import redis

# --- Import the dedicated settings for this service ---
from camera_service_settings import settings

# --- Configuration is now loaded from the settings object ---
REDIS_HOST = settings.REDIS.HOST
REDIS_PORT = settings.REDIS.PORT
FRAME_CHANNEL = 'camera:frames'
RESOLUTION = (settings.CAMERA.RESOLUTION_WIDTH, settings.CAMERA.RESOLUTION_HEIGHT)
FPS = settings.CAMERA.FPS
JPEG_QUALITY = settings.CAMERA.JPEG_QUALITY

# --- NEW: Load manual control settings ---
SHUTTER_SPEED = settings.CAMERA.SHUTTER_SPEED
ISO = settings.CAMERA.ISO
MANUAL_FOCUS = settings.CAMERA.MANUAL_FOCUS

def main():
    camera = None
    redis_client = None
    try:
        from picamera2 import Picamera2, controls
        
        print(f"[Camera Service] Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.ping()
        print("[Camera Service] Redis connection successful.")

        print(f"[Camera Service] Initializing camera with resolution {RESOLUTION} @ {FPS} FPS...")
        camera = Picamera2()
        config = camera.create_video_configuration(main={"size": RESOLUTION, "format": "RGB888"})
        camera.configure(config)

        # --- NEW: Apply manual controls ---
        manual_controls = {}
        # A value of 0 for any of these settings implies 'auto'
        if SHUTTER_SPEED > 0:
            manual_controls['ExposureTime'] = SHUTTER_SPEED
            manual_controls['AeEnable'] = False # Auto Exposure must be disabled for manual shutter
            print(f"[Camera Service] Setting manual shutter speed: {SHUTTER_SPEED}µs")
        else:
            print("[Camera Service] Using auto shutter speed.")

        if ISO > 0:
            # AnalogueGain is the picamera2 term for ISO
            manual_controls['AnalogueGain'] = float(ISO)
            manual_controls['AeEnable'] = False # Auto Exposure must be disabled for manual ISO
            print(f"[Camera Service] Setting manual ISO (AnalogueGain): {ISO}")
        else:
            print("[Camera Service] Using auto ISO.")

        if MANUAL_FOCUS > 0.0:
            # LensPosition is the control for manual focus, where the value is the reciprocal of the distance in meters.
            manual_controls['AfMode'] = controls.AfModeEnum.Manual
            manual_controls['LensPosition'] = MANUAL_FOCUS
            print(f"[Camera Service] Setting manual focus (LensPosition): {MANUAL_FOCUS}")
        else:
            print("[Camera Service] Using auto focus.")
            
        if manual_controls:
            print("[Camera Service] Applying manual controls...")
            camera.set_controls(manual_controls)
        
        camera.start()
        print("[Camera Service] Camera started. Entering capture loop...")
        # Allow 2 seconds for camera sensor and manual controls to stabilize
        time.sleep(2) 

        while True:
            frame = camera.capture_array()
            
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            
            # Publish the binary image data to the Redis channel
            redis_client.publish(FRAME_CHANNEL, buffer.tobytes())

    except ImportError:
        print("[Camera Service] FATAL ERROR: picamera2 library not found. Cannot run camera service.")
    except redis.exceptions.ConnectionError as e:
        print(f"[Camera Service] FATAL ERROR: Could not connect to Redis. Is the Redis server running? Error: {e}")
    except Exception as e:
        print(f"[Camera Service] FATAL ERROR: {e}")
    finally:
        if camera and camera.is_open:
            camera.stop()
        if redis_client:
            redis_client.close()
        print("[Camera Service] Exited.")

if __name__ == "__main__":
    main()