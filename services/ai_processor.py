"""
Standalone AI Processing Service - FINAL, CORRECTED VERSION

This version fixes the Redis "Connection closed by server" error. It replaces
the blocking `pubsub.listen()` generator with a robust, non-blocking
`pubsub.get_message()` loop. This is the definitive, stable architecture.
"""
import cv2
import numpy as np
import time
import redis
import traceback
import onnxruntime as ort

# --- Configuration ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
INPUT_FRAME_CHANNEL = "camera:frames:usb"
OUTPUT_STREAM_CHANNEL = "ai_stream:frames:usb"
MODEL_PATH = "yolov8n.onnx"
CONFIDENCE_THRESHOLD = 0.5
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

def main():
    print("--- Starting Standalone AI Processor Service (ONNX Runtime) ---")
    
    try:
        session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        input_details = session.get_inputs()[0]
        model_height = input_details.shape[2]
        model_width = input_details.shape[3]
        print(f"   ✅ ONNX Model Loaded. Input: {model_width}x{model_height}")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not load ONNX model. Ensure '{MODEL_PATH}' is in the project root.")
        print(f"Error: {e}")
        return

    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(INPUT_FRAME_CHANNEL)
        print(f"✅ Redis connection successful. Subscribed to '{INPUT_FRAME_CHANNEL}'.")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not connect to Redis.")
        print(f"Error: {e}")
        return

    print("\n🚀 AI Processor is running. Waiting for frames...")
    
    # --- THE FINAL BUG FIX IS HERE ---
    # We now use a robust `while True` loop with a non-blocking `get_message()` call.
    # This prevents the Redis connection from timing out during heavy AI processing.
    while True:
        try:
            message = pubsub.get_message()
            if not message:
                time.sleep(0.001)  # Sleep briefly to prevent high CPU usage when idle
                continue

            frame_data = message['data']
            
            # The rest of the logic remains the same
            np_array = np.frombuffer(frame_data, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            if image is None: continue

            original_height, original_width, _ = image.shape
            
            input_image = cv2.resize(image, (model_width, model_height))
            input_image = input_image.transpose(2, 0, 1)
            input_data = np.expand_dims(input_image, axis=0).astype(np.float32) / 255.0

            outputs = session.run(None, {input_details.name: input_data})
            
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
                cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
            redis_client.publish(OUTPUT_STREAM_CHANNEL, buffer.tobytes())

        except KeyboardInterrupt:
            print("\nExiting AI Processor...")
            break
        except Exception as e:
            print(f"- CRITICAL ERROR in AI processing loop: {e}")
            traceback.print_exc()
            time.sleep(2)

if __name__ == "__main__":
    main()