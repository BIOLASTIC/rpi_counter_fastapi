"""
Standalone AI Processing Service - FINAL PRODUCTION VERSION (v3)

This version uses a robust message-draining loop to solve the "slow consumer"
problem. When the service starts, it discards any backlog of frames and only
processes the most recent one, preventing the Redis output buffer from
overflowing and causing a disconnect. This is the definitive solution.

ADDED: Redis heartbeat to signal health status to the main application.
"""
import cv2
import numpy as np
import redis.asyncio as redis
import asyncio
import traceback
import onnxruntime as ort
from redis.exceptions import ConnectionError, TimeoutError

# --- Configuration ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
INPUT_FRAME_CHANNEL = "camera:frames:usb"
OUTPUT_STREAM_CHANNEL = "ai_stream:frames:usb"
MODEL_PATH = "yolov8n.onnx"
CONFIDENCE_THRESHOLD = 0.5
# --- NEW: Redis health/heartbeat configuration ---
AI_HEALTH_KEY = "ai_service:health_status"
AI_HEALTH_EXPIRY_SEC = 10 # The service is considered offline if no heartbeat for 10s
AI_HEARTBEAT_INTERVAL_SEC = 2 # Send a heartbeat every 2 seconds

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

def process_frame_sync(frame_data, session, model_width, model_height):
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
    print("--- Starting Standalone AI Processor Service (PRODUCTION v3) ---")
    try:
        session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        input_details = session.get_inputs()[0]
        model_height, model_width = input_details.shape[2], input_details.shape[3]
        print(f"   ✅ ONNX Model Loaded. Input: {model_width}x{model_height}")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not load ONNX model: {e}")
        return

    while True:
        redis_client = None
        exit_reason = None
        try:
            print("Connecting to Redis...")
            redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", health_check_interval=30)
            await redis_client.ping()
            print("✅ Redis connection successful.")
            
            async with redis_client.pubsub() as pubsub:
                await pubsub.subscribe(INPUT_FRAME_CHANNEL)
                print(f"✅ Subscribed to '{INPUT_FRAME_CHANNEL}'. Starting processing loop...")
                
                last_heartbeat_time = 0
                while True:
                    # --- NEW: Send heartbeat periodically ---
                    current_time = asyncio.get_event_loop().time()
                    if current_time - last_heartbeat_time > AI_HEARTBEAT_INTERVAL_SEC:
                        await redis_client.set(AI_HEALTH_KEY, "online", ex=AI_HEALTH_EXPIRY_SEC)
                        last_heartbeat_time = current_time

                    # Wait for a message with a timeout to allow the loop to run for heartbeats
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if not message:
                        continue # Loop to send next heartbeat

                    # THE FIX: Drain the queue to get the most recent frame
                    while True:
                        latest_message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.001)
                        if latest_message is None:
                            break
                        message = latest_message
                    
                    # Process the single, most-recent frame in a separate thread
                    processed_buffer = await asyncio.to_thread(
                        process_frame_sync, message['data'], session, model_width, model_height
                    )

                    if processed_buffer:
                        await redis_client.publish(OUTPUT_STREAM_CHANNEL, processed_buffer)

        except (ConnectionError, TimeoutError) as e:
            exit_reason = e
            print(f"❌ Redis connection error: {e}. Reconnecting in 5 seconds...")
        except KeyboardInterrupt as e:
            exit_reason = e
            print("\nExiting AI Processor...")
            break
        except Exception as e:
            exit_reason = e
            print(f"- CRITICAL ERROR in AI processing loop: {e}")
            traceback.print_exc()
        finally:
            if redis_client: await redis_client.aclose()
            if isinstance(exit_reason, KeyboardInterrupt): break
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated manually.")