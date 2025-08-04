"""
AI Pipeline Service for the Hailo AI HAT+
This service is designed to be run in a Linux pipeline, reading raw frame
data from stdin (e.g., from rpicam-vid) and publishing annotated frames
to Redis for the web UI. This version uses the definitive, correct API
pattern for inference based on official Hailo documentation.
"""
import sys
import cv2
import numpy as np
import redis
import json
import traceback
from pathlib import Path

# Setup project path to import configuration
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_settings
from hailo_platform import VDevice
from hailo_platform.pyhailort.pyhailort import HEF

# --- Load Configuration ---
try:
    settings = get_settings()
    MODEL_PATH = settings.AI_HAT.MODEL_PATH
    CONFIDENCE_THRESHOLD = settings.AI_HAT.CONFIDENCE_THRESHOLD
    FRAME_WIDTH = settings.CAMERA.CAMERA_WIDTH
    FRAME_HEIGHT = settings.CAMERA.CAMERA_HEIGHT
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    OUTPUT_CHANNEL = f"ai_stream:frames:rpi"
    HEALTH_KEY = settings.REDIS_KEYS.AI_HEALTH_KEY
    LAST_DETECTION_KEY = settings.REDIS_KEYS.AI_LAST_DETECTION_RESULT_KEY
except Exception as e:
    print(f"FATAL: Could not load settings. Error: {e}")
    sys.exit(1)

def get_class_names_from_hef(hef: HEF):
    try:
        info = json.loads(hef.get_description())
        return info.get('labels', ['object'])
    except Exception:
        return ['object']

def main():
    if not Path(MODEL_PATH).exists():
        print(f"❌ FATAL ERROR: Model file not found at '{MODEL_PATH}'")
        return

    # --- DEFINITIVE FIX: Restructure the entire main function for the correct lifecycle ---
    try:
        # Step 1: Initialize - Load model and get stream metadata (names, etc.)
        print("--- Initializing Hailo AI Pipeline Service ---")
        hef = HEF(MODEL_PATH)
        input_stream_infos = hef.get_input_stream_infos()
        output_stream_infos = hef.get_output_stream_infos()
        if not input_stream_infos or not output_stream_infos:
            raise RuntimeError("Model HEF file has no stream info.")
        
        input_name, output_name = input_stream_infos[0].name, output_stream_infos[0].name
        model_input_shape = input_stream_infos[0].shape
        class_names = get_class_names_from_hef(hef)
        
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.ping()
        print("--- Initialization complete. Activating hardware... ---")

    except Exception as e:
        print(f"❌ FATAL ERROR during initialization: {e}")
        traceback.print_exc()
        return

    # Step 2: Activate - Use VDevice as the main context manager
    with VDevice() as target:
        # Step 3: Configure - Configure the network on the activated target
        network_group = target.configure(hef)[0]

        # Step 4: Get Live Streams - Get the active stream objects
        input_stream = network_group.get_input_streams()[0]
        output_stream = network_group.get_output_streams()[0]
        
        print("--- Pipeline running. Waiting for frames from stdin... ---")
        
        # Step 5: Infer - Loop and process frames
        while True:
            try:
                frame_bytes = sys.stdin.buffer.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
                if not frame_bytes: break

                original_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
                model_h, model_w, _ = model_input_shape
                resized_frame = cv2.resize(original_frame, (model_w, model_h), interpolation=cv2.INTER_AREA)

                # Write to and read from the live stream objects
                input_stream.write(resized_frame)
                detections = output_stream.read()
                
                detected_objects = []
                for det in detections:
                    confidence = det[4]
                    if confidence < CONFIDENCE_THRESHOLD: continue
                    
                    label = class_names[int(det[5:].argmax())]
                    detected_objects.append(f"{label} ({confidence:.0%})")
                    
                    bbox_x_center, bbox_y_center, bbox_w, bbox_h = det[0], det[1], det[2], det[3]
                    x1 = int((bbox_x_center - bbox_w / 2) * FRAME_WIDTH)
                    y1 = int((bbox_y_center - bbox_h / 2) * FRAME_HEIGHT)
                    x2 = int((bbox_x_center + bbox_w / 2) * FRAME_WIDTH)
                    y2 = int((bbox_y_center + bbox_h / 2) * FRAME_HEIGHT)
                    cv2.rectangle(original_frame, (x1, y1), (x2, y2), (34, 197, 94), 2)
                    cv2.putText(original_frame, f"{label} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (34, 197, 94), 2)
                
                if detected_objects:
                    redis_client.set(LAST_DETECTION_KEY, ", ".join(detected_objects), ex=20)

                _, buffer = cv2.imencode('.jpg', original_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                redis_client.publish(OUTPUT_CHANNEL, buffer.tobytes())
                redis_client.set(HEALTH_KEY, "online", ex=10)

            except KeyboardInterrupt: break
            except Exception: traceback.print_exc()
    
    print("\n--- Pipeline shutting down. ---")

if __name__ == "__main__":
    main()