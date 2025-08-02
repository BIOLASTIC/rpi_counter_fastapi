"""
Standalone AI Processing Service - FINAL PRODUCTION VERSION (v7)

REVISED: This version implements a robust message-draining loop. This is the
definitive fix for the "slow consumer" problem where Redis would disconnect the
service due to its output buffer filling up.

The new logic ensures that only the most recent frame is processed, discarding any
backlog that accumulates while the AI is busy. This keeps the Redis connection
stable and the AI feed responsive.
"""
import cv2
import numpy as np
import redis.asyncio as redis
import asyncio
import traceback
import onnxruntime as ort
from redis.exceptions import ConnectionError, TimeoutError
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

# --- Self-Contained Configuration ---
class AiProcessorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)
    AI_DETECTION_SOURCE: Literal['rpi', 'usb'] = 'usb'

settings = AiProcessorSettings()

# --- Configuration & Constants ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
MODEL_PATH = "yolov8n.onnx"
CONFIDENCE_THRESHOLD = 0.5

# Redis Keys
AI_DETECTION_SOURCE_KEY = "ai_service:detection_source"
AI_HEALTH_KEY = "ai_service:health_status"
AI_ENABLED_KEY = "ai_service:enabled"


COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
    'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]
TARGET_CLASSES = {'bottle', 'cup', 'cell phone', 'book', 'box'}

def process_frame_sync(frame_data: bytes, session, model_width, model_height):
    """Synchronous, CPU-bound function to process a single image frame."""
    np_array = np.frombuffer(frame_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if image is None: return None
    original_height, original_width, _ = image.shape
    input_image = cv2.resize(image, (model_width, model_height))
    input_image = input_image.transpose(2, 0, 1)
    input_data = np.expand_dims(input_image, axis=0).astype(np.float32) / 255.0
    outputs = session.run(None, {session.get_inputs()[0].name: input_data})
    output_data = outputs[0][0].T
    for row in output_data:
        confidence = row[4:].max()
        if confidence < CONFIDENCE_THRESHOLD: continue
        class_id = int(row[4:].argmax())
        label = COCO_CLASSES[class_id]
        if label not in TARGET_CLASSES: continue
        xc, yc, w, h = row[:4]
        x1 = int((xc - w / 2) * original_width / model_width)
        y1 = int((yc - h / 2) * original_height / model_height)
        x2 = int((xc + w / 2) * original_width / model_width)
        y2 = int((yc + h / 2) * original_height / model_height)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return buffer.tobytes()

async def main():
    print("--- Starting Standalone AI Processor Service ---")
    try:
        session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        input_details = session.get_inputs()[0]
        model_height, model_width = input_details.shape[2], input_details.shape[3]
        print(f"   ✅ ONNX Model Loaded. Input: {model_width}x{model_height}")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not load ONNX model: {e}"); return

    while True:
        redis_client = None
        str_redis_client = None
        exit_reason = None
        try:
            print("Connecting to Redis...")
            redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", health_check_interval=30, decode_responses=False)
            str_redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", health_check_interval=30, decode_responses=True)
            await redis_client.ping()
            print("✅ Redis connection successful.")
            
            async with redis_client.pubsub() as pubsub:
                subscribed_source = None
                
                while True:
                    target_source = await str_redis_client.get(AI_DETECTION_SOURCE_KEY) or settings.AI_DETECTION_SOURCE
                    if target_source != subscribed_source:
                        if subscribed_source:
                            await pubsub.unsubscribe(f"camera:frames:{subscribed_source}")
                            print(f"- Unsubscribed from 'camera:frames:{subscribed_source}'")
                        await pubsub.subscribe(f"camera:frames:{target_source}")
                        subscribed_source = target_source
                        print(f"+ Subscribed to 'camera:frames:{subscribed_source}'. Processing...")

                    if await str_redis_client.get(AI_ENABLED_KEY) != "true":
                        await asyncio.sleep(1); continue
                    
                    await str_redis_client.set(AI_HEALTH_KEY, "online", ex=10)

                    # --- THE DEFINITIVE FIX: DRAIN THE QUEUE ---
                    # 1. Wait for the first message to arrive.
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if not message:
                        continue # If no message in 1 sec, just loop to check health/source.

                    # 2. Rapidly consume any other messages that have piled up.
                    # This ensures we only process the most recent frame.
                    while True:
                        latest_msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.001)
                        if latest_msg is None:
                            break # The queue is empty, we have the latest message.
                        message = latest_msg
                    # --- END OF FIX ---
                    
                    processed_buffer = await asyncio.to_thread(
                        process_frame_sync, message['data'], session, model_width, model_height
                    )

                    if processed_buffer:
                        output_channel = f"ai_stream:frames:{subscribed_source}"
                        await redis_client.publish(output_channel, processed_buffer)

        except (ConnectionError, TimeoutError) as e:
            exit_reason = e
            print(f"❌ Redis connection error: {e}. Reconnecting in 5 seconds...")
        except KeyboardInterrupt as e:
            exit_reason = e
            print("\nExiting AI Processor...")
            break
        except Exception as e:
            exit_reason = e
            print(f"❌ CRITICAL ERROR in AI processing loop: {e}")
            traceback.print_exc()
        finally:
            if redis_client: await redis_client.aclose()
            if str_redis_client: await str_redis_client.aclose()
            if isinstance(exit_reason, KeyboardInterrupt):
                break
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated manually.")