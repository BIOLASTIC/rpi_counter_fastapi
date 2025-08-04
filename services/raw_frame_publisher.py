"""
Raw Frame Publisher Service (BGR888 to JPEG Version)

This service reads raw BGR888 frame data from stdin, encodes it to JPEG,
and publishes it to a Redis channel for the web UI's "RAW" camera feed.
"""
import sys
import cv2
import numpy as np
import redis
import traceback
from pathlib import Path

# Setup project path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_settings

# --- Load Configuration ---
try:
    settings = get_settings()
    FRAME_WIDTH = settings.CAMERA.CAMERA_WIDTH
    FRAME_HEIGHT = settings.CAMERA.CAMERA_HEIGHT
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    OUTPUT_CHANNEL = f"camera:frames:rpi"
except Exception as e:
    print(f"[Raw Publisher] FATAL: Could not load settings. Error: {e}")
    sys.exit(1)

def main():
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.ping()
        print(f"[Raw Publisher] Connected to Redis. Publishing to '{OUTPUT_CHANNEL}'.")
    except Exception as e:
        print(f"[Raw Publisher] FATAL: Could not connect to Redis. Error: {e}")
        return

    while True:
        try:
            # Read a single raw BGR888 frame from the stdin pipeline
            frame_bytes = sys.stdin.buffer.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
            if not frame_bytes:
                print("[Raw Publisher] Input stream finished.")
                break
            
            # Convert raw bytes to a NumPy array for OpenCV
            original_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

            # Encode the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', original_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

            # Publish the JPEG bytes to Redis
            redis_client.publish(OUTPUT_CHANNEL, buffer.tobytes())

        except KeyboardInterrupt:
            break
        except Exception:
            print("[Raw Publisher] --- ERROR during frame publishing ---")
            traceback.print_exc()
            break
            
    print("\n[Raw Publisher] --- Shutting down. ---")

if __name__ == "__main__":
    main()