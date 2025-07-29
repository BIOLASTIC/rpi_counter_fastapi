"""
Standalone Camera Service for the Raspberry Pi Camera Module.
FINAL REVISION: This script is now completely self-contained.
- It no longer uses an external config file.
- It defines its own Pydantic settings model to load ONLY the variables it needs
  directly from the .env file. This is the definitive fix for the AttributeError.
"""
import time
import cv2
import redis
import traceback
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Self-Contained Configuration ---
class RpiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_prefix='CAMERA_RPI_', case_sensitive=False, extra='ignore')
    
    # This is the critical field that was failing before.
    ID: str
    
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)
    SHUTTER_SPEED: int = Field(0, ge=0)
    ISO: int = Field(0, ge=0)
    MANUAL_FOCUS: float = Field(0.0, ge=0.0)

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_prefix='REDIS_', case_sensitive=False, extra='ignore')
    HOST: str = 'localhost'
    PORT: int = 6379

def main():
    try:
        # Load settings at the very top. If this fails, the script will exit with a clear error.
        rpi_cam_settings = RpiSettings()
        redis_settings = RedisSettings()
        
        camera_id = rpi_cam_settings.ID
        if not camera_id:
            print("[RPI Camera Service] FATAL ERROR: The CAMERA_RPI_ID is not set in your .env file!")
            print("[RPI Camera Service] Please run `libcamera-hello --list-cameras`, copy the ID, and set it in your .env file.")
            return

        camera = None
        redis_client = None
        frame_channel = 'camera:frames:rpi'

        from picamera2 import Picamera2
        
        print(f"[RPI Camera Service] Connecting to Redis at {redis_settings.HOST}:{redis_settings.PORT}...")
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=False)
        redis_client.ping()
        print("[RPI Camera Service] Redis connection successful.")

        print(f"[RPI Camera Service] Initializing camera with specific ID: {camera_id}")
        camera = Picamera2(camera_id) 
        
        print(f"[RPI Camera Service] Configuring with Resolution={rpi_cam_settings.RESOLUTION_WIDTH}x{rpi_cam_settings.RESOLUTION_HEIGHT}")
        config = camera.create_video_configuration(
            main={"size": (rpi_cam_settings.RESOLUTION_WIDTH, rpi_cam_settings.RESOLUTION_HEIGHT), "format": "RGB888"}
        )
        camera.configure(config)

        controls_to_set = {"FrameRate": rpi_cam_settings.FPS}
        if rpi_cam_settings.SHUTTER_SPEED > 0:
            controls_to_set['ExposureTime'] = rpi_cam_settings.SHUTTER_SPEED
            controls_to_set['AeEnable'] = False
        if rpi_cam_settings.ISO > 0:
            controls_to_set['AnalogueGain'] = float(rpi_cam_settings.ISO)
            controls_to_set['AeEnable'] = False
        if rpi_cam_settings.MANUAL_FOCUS > 0.0:
            from picamera2 import controls
            controls_to_set['AfMode'] = controls.AfModeEnum.Manual
            controls_to_set['LensPosition'] = rpi_cam_settings.MANUAL_FOCUS
        
        print(f"[RPI Camera Service] Applying controls: {controls_to_set}")
        camera.set_controls(controls_to_set)
        
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
        if 'camera' in locals() and camera and camera.is_open:
            camera.stop()
        if 'redis_client' in locals() and redis_client:
            redis_client.close()
        print("[RPI Camera Service] Exited.")

if __name__ == "__main__":
    main()