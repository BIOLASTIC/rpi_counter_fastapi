"""
Standalone AI Processing Service - FINAL PRODUCTION VERSION (v8)

This version uses a robust message-draining loop to solve the "slow consumer"
problem. When the service starts, it discards any backlog of frames and only
processes the most recent one, preventing the Redis output buffer from
overflowing and causing a disconnect. This is the definitive solution.

ADDED: Redis heartbeat to signal health status to the main application.
CHANGED: Now respects a global 'ai_service:enabled' Redis key to allow for remote toggling.
FIXED: Connects to Redis with decode_responses=False to correctly handle raw binary JPEG data.
NEW: Publishes the name of the last detected object to a Redis key for the UI.
UPDATED: Custom class names for 'OBJ' and 'NO_OBJ' as per the new model.
CORRECTED: Fixed 'TypeError: cannot unpack non-iterable coroutine object' by making the
           CPU-bound 'process_frame' function synchronous ('def') and handling the
           async Redis SET command in the main event loop.
DEBUG-TUNING: Lowered confidence threshold to help diagnose detection issues in poor lighting.
"""
import cv2
import numpy as np
import redis.asyncio as redis
import asyncio
import traceback
import onnxruntime as ort
from redis.exceptions import ConnectionError, TimeoutError
from typing import Optional, Tuple

# --- Configuration ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
INPUT_FRAME_CHANNEL = "camera:frames:usb"
OUTPUT_STREAM_CHANNEL = "ai_stream:frames:usb"
MODEL_PATH = "yolov8n.onnx"

# --- DEBUGGING CHANGE HERE ---
# The original value was 0.5 (50% confidence). By lowering it to 0.2 (20%),
# we can see if the model is trying to detect things but isn't very sure.
# If you see boxes now, it confirms the problem is lighting and/or model training.
CONFIDENCE_THRESHOLD = 0.2

AI_HEALTH_KEY = "ai_service:health_status"
AI_HEALTH_EXPIRY_SEC = 10 
AI_HEARTBEAT_INTERVAL_SEC = 2
AI_ENABLED_KEY = "ai_service:enabled"
AI_LAST_DETECTION_KEY = "ai_service:last_detection"
AI_LAST_DETECTION_EXPIRY_SEC = 5


# --- USER MODEL UPDATE ---
COCO_CLASSES = [
    'NO_OBJ', 
    'OBJ'
]
TARGET_CLASSES = {'OBJ'}


def process_frame_sync(frame_data: bytes, session) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Synchronous, CPU-bound function to process a frame.
    It returns the annotated image buffer and the name of the first detected object.
    """
    model_height, model_width = session.get_inputs()[0].shape[2:]
    np_array = np.frombuffer(frame_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if image is None: return None, None

    original_height, original_width, _ = image.shape
    input_image = cv2.resize(image, (model_width, model_height))
    input_image = input_image.transpose(2, 0, 1)
    input_data = np.expand_dims(input_image, axis=0).astype(np.float32) / 255.0

    outputs = session.run(None, {session.get_inputs()[0].name: input_data})
    output_data = outputs[0][0].T

    detected_label = None
    for row in output_data:
        confidence = row[4:].max()
        if confidence < CONFIDENCE_THRESHOLD: continue
        class_id = int(row[4:].argmax())
        label = COCO_CLASSES[class_id]

        if label in TARGET_CLASSES:
            if detected_label is None:
                detected_label = label
            
            xc, yc, w, h = row[:4]
            x1 = int((xc - w / 2) * original_width / model_width)
            y1 = int((yc - h / 2) * original_height / model_height)
            x2 = int((xc + w / 2) * original_width / model_width)
            y2 = int((yc + h / 2) * original_height / model_height)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return buffer.tobytes(), detected_label


async def main():
    print("--- Starting Standalone AI Processor Service ---")
    try:
        session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        print(f"   ✅ Custom ONNX Model Loaded.")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not load ONNX model: {e}")
        return

    while True:
        redis_client, str_redis_client, exit_reason = None, None, None
        try:
            print("Connecting to Redis...")
            redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", health_check_interval=30, decode_responses=False)
            str_redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", health_check_interval=30, decode_responses=True)
            await redis_client.ping()
            print("✅ Redis connection successful.")
            
            async with redis_client.pubsub() as pubsub:
                await pubsub.subscribe(INPUT_FRAME_CHANNEL)
                print(f"✅ Subscribed to '{INPUT_FRAME_CHANNEL}'. Starting processing loop...")
                
                while True:
                    await asyncio.sleep(0.01)
                    await str_redis_client.set(AI_HEALTH_KEY, "online", ex=AI_HEALTH_EXPIRY_SEC)

                    is_enabled = await str_redis_client.get(AI_ENABLED_KEY)
                    if is_enabled != "true":
                        await asyncio.sleep(1) 
                        continue

                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
                    if not message: continue

                    while True:
                        latest_message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.001)
                        if latest_message is None: break
                        message = latest_message
                    
                    processed_buffer, detected_label = await asyncio.to_thread(
                        process_frame_sync, message['data'], session
                    )

                    if detected_label:
                        await str_redis_client.set(AI_LAST_DETECTION_KEY, detected_label, ex=AI_LAST_DETECTION_EXPIRY_SEC)

                    if processed_buffer:
                        await redis_client.publish(OUTPUT_STREAM_CHANNEL, processed_buffer)

        except (ConnectionError, TimeoutError) as e: exit_reason = e
        except KeyboardInterrupt as e: exit_reason = e; break
        except Exception as e:
            exit_reason = e
            traceback.print_exc()
        finally:
            print(f"❌ Redis connection error: {exit_reason}. Reconnecting in 5 seconds...")
            if redis_client: await redis_client.aclose()
            if str_redis_client: await str_redis_client.aclose()
            if isinstance(exit_reason, KeyboardInterrupt): break
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated manually.")