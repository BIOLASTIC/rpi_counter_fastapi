"""
Standalone AI Processing Service - FINAL PRODUCTION VERSION (v9)

REVISED: This version now separates the result generation from the image
annotation. It determines the textual result ("bottle", "No Object", etc.)
and publishes this string to a dedicated Redis key. This allows the main
application to broadcast the text result to the UI in real-time.
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
AI_LAST_DETECTION_RESULT_KEY = "ai_service:last_detection_result" # Use new key

# Your custom class list
CUSTOM_CLASSES = [ 'bottle', 'book', 'cup' ] # Example
TARGET_CLASSES = {'bottle', 'book', 'cup'} # Example


def process_frame_sync(frame_data: bytes, session, model_width, model_height):
    """
    Synchronous, CPU-bound function to process a single image frame.
    
    REVISED: Now returns a tuple: (annotated_image_bytes, detection_result_text)
    """
    np_array = np.frombuffer(frame_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if image is None: 
        return None, "Error decoding image"
    
    original_height, original_width, _ = image.shape
    input_image = cv2.resize(image, (model_width, model_height))
    input_image = input_image.transpose(2, 0, 1)
    input_data = np.expand_dims(input_image, axis=0).astype(np.float32) / 255.0
    
    outputs = session.run(None, {session.get_inputs()[0].name: input_data})
    output_data = outputs[0][0].T

    # --- NEW: Logic to find the best detection and its text ---
    best_detection_text = "No Object"
    highest_confidence = 0.0
    detections = []

    for row in output_data:
        confidence = row[4:].max()
        if confidence > CONFIDENCE_THRESHOLD:
            class_id = int(row[4:].argmax())
            label = CUSTOM_CLASSES[class_id]
            if label in TARGET_CLASSES:
                detections.append((confidence, label, row[:4]))
                if confidence > highest_confidence:
                    highest_confidence = confidence
                    best_detection_text = label

    # --- Draw boxes and text on the image ---
    if not detections:
        # If no objects were detected, write "No Object" on the image
        cv2.putText(image, "No Object", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    else:
        # Otherwise, draw all valid detections
        for conf, label, box_data in detections:
            xc, yc, w, h = box_data
            x1 = int((xc - w / 2) * original_width / model_width)
            y1 = int((yc - h / 2) * original_height / model_height)
            x2 = int((xc + w / 2) * original_width / model_width)
            y2 = int((yc + h / 2) * original_height / model_height)
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    
    # Return both the image and the textual result
    return buffer.tobytes(), best_detection_text

async def main():
    print("--- Starting Standalone AI Processor Service (CUSTOM MODEL) ---")
    try:
        session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        input_details = session.get_inputs()[0]
        model_height, model_width = input_details.shape[2], input_details.shape[3]
        print(f"   ✅ Custom ONNX Model Loaded. Input: {model_width}x{model_height}")
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
                        await str_redis_client.set(AI_LAST_DETECTION_RESULT_KEY, "AI Disabled") # Set status when disabled
                        await asyncio.sleep(1); continue
                    
                    await str_redis_client.set(AI_HEALTH_KEY, "online", ex=10)

                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if not message: continue
                    while True:
                        latest_msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.001)
                        if latest_msg is None: break
                        message = latest_msg
                    
                    # --- REVISED: Get both results from the function ---
                    processed_buffer, detection_text = await asyncio.to_thread(
                        process_frame_sync, message['data'], session, model_width, model_height
                    )

                    if processed_buffer:
                        # Publish the image stream as before
                        output_channel = f"ai_stream:frames:{subscribed_source}"
                        await redis_client.publish(output_channel, processed_buffer)
                        
                        # --- NEW: Publish the text result to its dedicated key ---
                        await str_redis_client.set(AI_LAST_DETECTION_RESULT_KEY, detection_text)

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