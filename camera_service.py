"""
Standalone Camera Service.

REVISED: Fixes a NameError caused by a typo ('cv-cv2' instead of 'cv2')
in the image encoding line. This was the final bug preventing the service
from running correctly.
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

def main():
    camera = None
    redis_client = None
    try:
        from picamera2 import Picamera2
        print(f"[Camera Service] Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.ping()
        print("[Camera Service] Redis connection successful.")

        print(f"[Camera Service] Initializing camera with resolution {RESOLUTION} @ {FPS} FPS...")
        camera = Picamera2()
        config = camera.create_video_configuration(main={"size": RESOLUTION, "format": "RGB888"})
        camera.configure(config)
        camera.start()
        print("[Camera Service] Camera started. Entering capture loop...")
        time.sleep(1) # Allow sensor to stabilize

        while True:
            frame = camera.capture_array()
            
            # --- DEFINITIVE FIX for the NameError ---
            # The typo 'cv-cv2' has been corrected to 'cv2'
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