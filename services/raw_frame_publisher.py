"""
Raw Frame Publisher Service (YUV420 to JPEG Version)
"""
import sys
import cv2
import numpy as np
import redis
import traceback
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_settings

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

    # For YUV420, the frame size is 1.5 times the width * height
    yuv_frame_size = int(FRAME_WIDTH * FRAME_HEIGHT * 1.5)
    
    while True:
        try:
            frame_bytes = sys.stdin.buffer.read(yuv_frame_size)
            if not frame_bytes: break
            
            # Create a 1D numpy array and then reshape to the correct YUV dimensions
            yuv_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((int(FRAME_HEIGHT * 1.5), FRAME_WIDTH))

            # Convert from YUV I420 format to BGR for JPEG encoding
            bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)
            
            _, buffer = cv2.imencode('.jpg', bgr_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            redis_client.publish(OUTPUT_CHANNEL, buffer.tobytes())

        except KeyboardInterrupt: break
        except Exception:
            traceback.print_exc()
            break
            
    print("\n[Raw Publisher] --- Shutting down. ---")

if __name__ == "__main__":
    main()