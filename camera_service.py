"""
Standalone Camera Service.

This script runs in its own process, completely separate from the main web server.
Its only job is to control the camera, capture frames, and publish them to a Redis channel.
If it crashes due to a hardware error, it will not affect the main application.
"""
import time
import cv2
import redis

# --- Configuration ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
FRAME_CHANNEL = 'camera:frames'
RESOLUTION = (640, 480) # Use a smaller resolution for performance
FPS = 15

def main():
    camera = None
    redis_client = None
    try:
        from picamera2 import Picamera2
        print("[Camera Service] Connecting to Redis...")
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.ping()
        print("[Camera Service] Redis connection successful.")

        print("[Camera Service] Initializing camera...")
        camera = Picamera2()
        config = camera.create_video_configuration(main={"size": RESOLUTION, "format": "RGB888"})
        camera.configure(config)
        camera.start()
        print("[Camera Service] Camera started.")
        time.sleep(1) # Allow sensor to stabilize

        while True:
            # This blocking call is fine as it's the only thing this process does.
            frame = camera.capture_array()
            
            # Encode the frame as a JPEG image in memory
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            
            # Publish the binary image data to the Redis channel
            redis_client.publish(FRAME_CHANNEL, buffer.tobytes())
            
            # Optional: slow down the capture rate if needed
            # time.sleep(1 / FPS)

    except Exception as e:
        print(f"[Camera Service] FATAL ERROR: {e}")
        # When an error occurs, the script will simply exit.
        # A process manager like systemd would be configured to restart it.
    finally:
        if camera and camera.is_open:
            camera.stop()
        if redis_client:
            redis_client.close()
        print("[Camera Service] Exited.")

if __name__ == "__main__":
    main()
