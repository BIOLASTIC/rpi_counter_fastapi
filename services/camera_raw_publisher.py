#!/usr/bin/env python3
"""
Camera Raw Publisher Service - RAW BGR VERSION
Reads raw BGR frames from FFmpeg and publishes to Redis
"""
import sys
import os
import cv2
import redis
import numpy as np
import time
import signal
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from config.settings import get_settings
except ImportError as e:
    print(f"[Raw Publisher] ERROR: Could not import settings: {e}")
    sys.exit(1)

class RawBGRPublisher:
    """Publisher for raw BGR frames from FFmpeg."""
    
    def __init__(self):
        self.running = True
        self.redis_client = None
        self.frame_count = 0
        self.start_time = time.time()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        print(f"[Raw Publisher] Received signal {signum}, shutting down...")
        self.running = False
        
    def connect_redis(self):
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
            self.redis_client.ping()
            print("[Raw Publisher] Connected to Redis successfully")
            return True
        except Exception as e:
            print(f"[Raw Publisher] Redis connection failed: {e}")
            return False

    def read_raw_bgr_frame(self, width, height):
        """Read raw BGR frame from stdin (from FFmpeg)."""
        try:
            # Raw BGR: width × height × 3 bytes
            frame_size = width * height * 3
            frame_bytes = sys.stdin.buffer.read(frame_size)
            
            if len(frame_bytes) != frame_size:
                if len(frame_bytes) == 0:
                    return None, "EOF"
                return None, f"Incomplete frame: {len(frame_bytes)}/{frame_size}"
            
            # Convert to numpy array (BGR format)
            frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((height, width, 3))
            
            # Add frame counter for verification
            cv2.putText(frame, f"RAW Frame: {self.frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            return frame, "Success"
            
        except Exception as e:
            return None, f"Frame read error: {e}"

    def run(self):
        try:
            settings = get_settings()
            FRAME_WIDTH = settings.CAMERA.CAMERA_WIDTH
            FRAME_HEIGHT = settings.CAMERA.CAMERA_HEIGHT
            JPEG_QUALITY = getattr(settings.CAMERA, 'JPEG_QUALITY', 90)
            
            if not self.connect_redis():
                return 1
            
            print("=" * 60)
            print("[Raw Publisher] RAW BGR Publisher initialized")
            print(f"[Raw Publisher] Frame size: {FRAME_WIDTH}x{FRAME_HEIGHT}")
            print(f"[Raw Publisher] Expected bytes: {FRAME_WIDTH * FRAME_HEIGHT * 3:,}")
            print("[Raw Publisher] Publishing to: camera:frames:rpi")
            print("=" * 60)
            
            while self.running:
                try:
                    # Read raw BGR frame from FFmpeg
                    frame, message = self.read_raw_bgr_frame(FRAME_WIDTH, FRAME_HEIGHT)
                    
                    if frame is None:
                        if "EOF" in message:
                            print("[Raw Publisher] Input stream finished")
                            break
                        else:
                            print(f"[Raw Publisher] {message}")
                            continue
                    
                    self.frame_count += 1
                    
                    # Encode as JPEG
                    success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
                    if not success:
                        print("[Raw Publisher] JPEG encoding failed")
                        continue
                    
                    # Publish to Redis
                    self.redis_client.publish('camera:frames:rpi', buffer.tobytes())
                    
                    # Status updates
                    if self.frame_count % 100 == 0:
                        elapsed = time.time() - self.start_time
                        fps = self.frame_count / elapsed
                        print(f"[Raw Publisher] LIVE VIDEO: {self.frame_count} frames ({fps:.1f} FPS)")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"[Raw Publisher] Processing error: {e}")
                    
        except Exception as e:
            print(f"[Raw Publisher] Fatal error: {e}")
            return 1
        
        print("[Raw Publisher] --- Shutting down ---")
        return 0

def main():
    try:
        publisher = RawBGRPublisher()
        return publisher.run()
    except Exception as e:
        print(f"[Raw Publisher] Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
