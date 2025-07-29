"""
Standalone Camera Service for the Raspberry Pi Camera Module.
REVISED: Now explicitly tells picamera2 which camera number to use (defaulting to 0)
to avoid conflicts with other devices. This refers to the RPi camera index, not the /dev/videoX index.
"""
import time
import cv2
import redis
import traceback

from camera_services_config import settings

def main():
    rpi_cam_settings = settings.CAMERA_RPI
    redis_settings = settings.REDIS
    
    camera = None
    redis_client = None
    frame_channel = 'camera:frames:rpi'

    try:
        from picamera2 import Picamera2
        
        print(f"[RPI Camera Service] Connecting to Redis at {redis_settings.HOST}:{redis_settings.PORT}...")
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=False)
        redis_client.ping()
        print("[RPI Camera Service] Redis connection successful.")

        # This tells picamera2 to use the first available CSI/native camera.
        print("[RPI Camera Service] Initializing camera at hardware index 0 (CSI Port)...")
        camera = Picamera2(camera_num=0) 
        
        print(f"[RPI Camera Service] Configuring with Resolution={rpi_cam_settings.RESOLUTION_WIDTH}x{rpi_cam_settings.RESOLUTION_HEIGHT}, FPS={rpi_cam_settings.FPS}")
        config = camera.create_video_configuration(main={"size": (rpi_cam_settings.RESOLUTION_WIDTH, rpi_cam_settings.RESOLUTION_HEIGHT), "format": "RGB888"}, controls={"FrameRate": rpi_cam_settings.FPS})
        camera.configure(config)

        manual_controls = {}
        if rpi_cam_settings.SHUTTER_SPEED > 0:
            manual_controls['ExposureTime'] = rpi_cam_settings.SHUTTER_SPEED
            manual_controls['AeEnable'] = False
        if rpi_cam_settings.ISO > 0:
            manual_controls['AnalogueGain'] = float(rpi_cam_settings.ISO)
            manual_controls['AeEnable'] = False
        if rpi_cam_settings.MANUAL_FOCUS > 0.0:
            from picamera2 import controls
            manual_controls['AfMode'] = controls.AfModeEnum.Manual
            manual_controls['LensPosition'] = rpi_cam_settings.MANUAL_FOCUS
        
        if manual_controls:
            print(f"[RPI Camera Service] Applying manual controls: {manual_controls}")
            camera.set_controls(manual_controls)
        
        camera.start()
        print(f"[RPI Camera Service] Camera started. Publishing to '{frame_channel}'.")
        time.sleep(2) 

        while True:
            frame = camera.capture_array()
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, rpi_cam_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())

    except Exception as e:
        print(f"[RPI Camera Service] FATAL ERROR: An unexpected error occurred.")
        print(traceback.format_exc())
    finally:
        if camera and camera.is_open: camera.stop()
        if redis_client: redis_client.close()
        print("[RPI Camera Service] Exited.")

if __name__ == "__main__":
    main()