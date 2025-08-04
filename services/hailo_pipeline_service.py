"""
AI Pipeline Service for the Hailo AI HAT+ (Definitive, Final Version)

This service reads raw frame data from stdin, performs inference, and uses
OpenCV's DNN module for robust Non-Maximum Suppression (NMS) to correctly
process the YOLOv8 output. It publishes the final, annotated frames to Redis.
"""
import sys
import cv2
import numpy as np
import redis
import json
import traceback
from pathlib import Path

# Setup project path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_settings
from hailo_platform import VDevice, HEF, ConfigureParams, HailoStreamInterface, InputVStreamParams, OutputVStreamParams, InferVStreams, FormatType

# --- Load Configuration ---
try:
    settings = get_settings()
    MODEL_PATH = settings.AI_HAT.MODEL_PATH
    CONFIDENCE_THRESHOLD = settings.AI_HAT.CONFIDENCE_THRESHOLD
    NMS_THRESHOLD = 0.45 # Standard NMS threshold
    FRAME_WIDTH = settings.CAMERA.CAMERA_WIDTH
    FRAME_HEIGHT = settings.CAMERA.CAMERA_HEIGHT
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    OUTPUT_CHANNEL = "ai_stream:frames:rpi" # AI feed has its own channel
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

    try:
        print("--- Initializing Hailo AI Pipeline Service ---")
        hef = HEF(MODEL_PATH)
        input_vstream_info = hef.get_input_vstream_infos()[0]
        output_vstream_info = hef.get_output_vstream_infos()[0]
        model_input_shape = input_vstream_info.shape
        class_names = get_class_names_from_hef(hef)
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.ping()
        print("--- Initialization complete. Activating hardware... ---")

    except Exception as e:
        print(f"❌ FATAL ERROR during initialization: {e}")
        traceback.print_exc()
        return

    with VDevice() as target:
        configure_params = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
        network_group = target.configure(hef, configure_params)[0]
        
        input_vstreams_params = InputVStreamParams.make_from_network_group(network_group, quantized=True, format_type=FormatType.UINT8)
        output_vstreams_params = OutputVStreamParams.make_from_network_group(network_group, quantized=False, format_type=FormatType.FLOAT32)
        network_group_params = network_group.create_params()
        
        print("--- AI Pipeline running. Waiting for frames from stdin... ---")
        
        with network_group.activate(network_group_params):
            with InferVStreams(network_group, input_vstreams_params, output_vstreams_params) as infer_pipeline:
                while True:
                    try:
                        frame_bytes = sys.stdin.buffer.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
                        if not frame_bytes: break

                        original_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
                        
                        # --- Run Inference ---
                        results = infer_pipeline.infer({input_vstream_info.name: original_frame})
                        detections = results[output_vstream_info.name]
                        
                        # --- Post-Processing with OpenCV NMS ---
                        # Transpose the output from (1, 84, 8400) to (8400, 84)
                        outputs = np.transpose(np.squeeze(detections))
                        
                        boxes = []
                        confidences = []
                        class_ids = []
                        
                        for out in outputs:
                            confidence = out[4]
                            if confidence > CONFIDENCE_THRESHOLD:
                                scores = out[5:]
                                class_id = np.argmax(scores)
                                
                                # Bbox is center_x, center_y, width, height
                                cx, cy, w, h = out[0], out[1], out[2], out[3]
                                x = int((cx - w / 2) * FRAME_WIDTH)
                                y = int((cy - h / 2) * FRAME_HEIGHT)
                                boxes.append([x, y, int(w * FRAME_WIDTH), int(h * FRAME_HEIGHT)])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                        
                        # Apply Non-Maximum Suppression
                        indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
                        
                        detected_objects = []
                        if len(indices) > 0:
                            for i in indices.flatten():
                                x, y, w, h = boxes[i]
                                label = class_names[class_ids[i]]
                                confidence = confidences[i]
                                
                                detected_objects.append(f"{label} ({confidence:.0%})")
                                cv2.rectangle(original_frame, (x, y), (x + w, y + h), (34, 197, 94), 2)
                                cv2.putText(original_frame, f"{label} {confidence:.1%}", (x, y - 5), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (34, 197, 94), 2)
                        
                        # Publish results to Redis
                        if detected_objects:
                            redis_client.set(LAST_DETECTION_KEY, ", ".join(detected_objects), ex=20)

                        _, buffer = cv2.imencode('.jpg', original_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                        redis_client.publish(OUTPUT_CHANNEL, buffer.tobytes())
                        redis_client.set(HEALTH_KEY, "online", ex=10)

                    except KeyboardInterrupt: break
                    except Exception:
                        print("--- ERROR during frame processing ---")
                        traceback.print_exc()
    
    print("\n--- AI Pipeline shutting down. ---")

if __name__ == "__main__":
    main()