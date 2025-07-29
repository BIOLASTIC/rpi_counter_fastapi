"""
Standalone Camera Service for a USB V4L2 Camera.
REVISED: Reads the correct device index from the .env file.
"""
import time
import cv2
import redis
import traceback

from camera_services_config import settings

def main():
    usb_cam_settings = settings.CAMERA_USB
    redis_settings = settings.REDIS

    camera = None
    redis_client = None
    frame_channel = 'camera:frames:usb'

    try:
        print(f"[USB Camera Service] Connecting to Redis at {redis_settings.HOST}:{redis_settings.PORT}...")
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=False)
        redis_client.ping()
        print("[USB Camera Service] Redis connection successful.")

        # This now reads the correct index (0) from your .env file
        device_index = usb_cam_settings.DEVICE_INDEX
        print(f"[USB Camera Service] Attempting to initialize camera at /dev/video{device_index}...")
        camera = cv2.VideoCapture(device_index)
        
        if not camera.isOpened():
            raise RuntimeError(f"Could not open camera at index {device_index}. Check `v4l2-ctl --list-devices` and ensure permissions are correct.")

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, usb_cam_settings.RESOLUTION_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, usb_cam_settings.RESOLUTION_HEIGHT)
        camera.set(cv2.CAP_PROP_FPS, usb_cam_settings.FPS)
        
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
            
            sleep_duration = 1.0 / usb_cam_settings.FPS
            time.sleep(sleep_duration)

    except Exception as e:
        print(f"[USB Camera Service] FATAL ERROR: An unexpected error occurred.")
        print(traceback.format_exc())
    finally:
        if camera and camera.isOpened(): camera.release()
        if redis_client: redis_client.close()
        print("[USB Camera Service] Exited.")

if __name__ == "__main__":
    main()