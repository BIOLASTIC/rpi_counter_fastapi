#!/usr/bin/env python3
"""
Video Streaming Service for FastAPI - BROWSER COMPATIBLE VERSION
Subscribes to Redis camera feeds and streams to browser via MJPEG
"""
import redis
import asyncio
import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import time

class VideoStreamer:
    """Handles video streaming from Redis to browser."""
    
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
        
    async def generate_mjpeg_stream(self, channel_name, default_message="NO SIGNAL"):
        """
        Generate MJPEG stream from Redis channel.
        Creates proper multipart boundaries for browser compatibility.
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel_name)
        
        # Create a default "no signal" frame
        default_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(default_frame, default_message, (200, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        _, default_jpeg = cv2.imencode('.jpg', default_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        default_bytes = default_jpeg.tobytes()
        
        last_frame_time = time.time()
        
        try:
            while True:
                try:
                    # Check for new message with timeout
                    message = pubsub.get_message(timeout=0.1)
                    
                    if message and message['type'] == 'message':
                        frame_data = message['data']
                        if frame_data and len(frame_data) > 1000:  # Valid JPEG frame
                            # Yield MJPEG frame with proper boundaries
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n'
                                   b'Content-Length: ' + str(len(frame_data)).encode() + b'\r\n\r\n' +
                                   frame_data + b'\r\n')
                            last_frame_time = time.time()
                        else:
                            # Invalid frame data, use default
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n'
                                   b'Content-Length: ' + str(len(default_bytes)).encode() + b'\r\n\r\n' +
                                   default_bytes + b'\r\n')
                    else:
                        # No new message, check if we should send default frame
                        if time.time() - last_frame_time > 2.0:  # No frame for 2 seconds
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n'
                                   b'Content-Length: ' + str(len(default_bytes)).encode() + b'\r\n\r\n' +
                                   default_bytes + b'\r\n')
                            last_frame_time = time.time()
                    
                    # Small delay to prevent CPU spinning
                    await asyncio.sleep(0.033)  # ~30 FPS max
                    
                except Exception as e:
                    print(f"[Video Streamer] Stream error for {channel_name}: {e}")
                    # Send default frame on error
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n'
                           b'Content-Length: ' + str(len(default_bytes)).encode() + b'\r\n\r\n' +
                           default_bytes + b'\r\n')
                    await asyncio.sleep(1)
                    
        except Exception as e:
            print(f"[Video Streamer] Fatal error for {channel_name}: {e}")
        finally:
            pubsub.close()

# Global video streamer instance
video_streamer = VideoStreamer()
