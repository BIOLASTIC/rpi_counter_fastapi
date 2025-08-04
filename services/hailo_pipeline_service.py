"""
AI Pipeline Service for the Hailo AI HAT+ (Definitive, Final, Corrected Version)
"""
import sys
import cv2
import numpy as np
import redis
import json
import traceback
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_settings
from hailo_platform import VDevice, HEF, ConfigureParams, HailoStreamInterface, InputVStreamParams, OutputVStreamParams, InferVStreams, FormatType

try:
    settings = get_settings()
    # ... (rest of config loading is the same)
    MODEL_PATH = settings.AI_HAT.MODEL_PATH
    CONFIDENCE_THRESHOLD = settings.AI_HAT.CONFIDENCE_THRESHOLD
    NMS_THRESHOLD = 0.45
    FRAME_WIDTH = settings.CAMERA.CAMERA_WIDTH
    FRAME_HEIGHT = settings.CAMERA.CAMERA_HEIGHT
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    OUTPUT_CHANNEL = "ai_stream:frames:rpi"
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
        # ... (rest of initialization is the same)
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
        
        yuv_frame_size = int(FRAME_WIDTH * FRAME_HEIGHT * 1.5)
        
        with network_group.activate(network_group_params):
            with InferVStreams(network_group, input_vstreams_params, output_vstreams_params) as infer_pipeline:
                while True:
                    try:
                        frame_bytes = sys.stdin.buffer.read(yuv_frame_size)
                        if not frame_bytes: break

                        # Convert raw YUV420 bytes to BGR format for processing
                        yuv_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((int(FRAME_HEIGHT * 1.5), FRAME_WIDTH))
                        bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)
                        
                        # The AI model expects RGB, so we do a final conversion
                        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
                        
                        results = infer_pipeline.infer({input_vstream_info.name: rgb_frame})
                        detections = results[output_vstream_info.name]
                        
                        outputs = np.transpose(np.squeeze(detections))
                        boxes, confidences, class_ids = [], [], []
                        
                        for out in outputs:
                            confidence = out[4]
                            if confidence > CONFIDENCE_THRESHOLD:
                                scores = out[5:]
                                class_id = np.argmax(scores)
                                cx, cy, w, h = out[0], out[1], out[2], out[3]
                                x = int((cx - w / 2) * FRAME_WIDTH)
                                y = int((cy - h / 2) * FRAME_HEIGHT)
                                boxes.append([x, y, int(w * FRAME_WIDTH), int(h * FRAME_HEIGHT)])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                        
                        indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
                        
                        detected_objects = []
                        if len(indices) > 0:
                            for i in indices.flatten():
                                x, y, w, h = boxes[i]
                                label = class_names[class_ids[i]]
                                confidence = confidences[i]
                                detected_objects.append(f"{label} ({confidence:.0%})")
                                cv2.rectangle(bgr_frame, (x, y), (x + w, y + h), (34, 197, 94), 2)
                                cv2.putText(bgr_frame, f"{label} {confidence:.1%}", (x, y - 5), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (34, 197, 94), 2)
                        
                        if detected_objects:
                            redis_client.set(LAST_DETECTION_KEY, ", ".join(detected_objects), ex=20)

                        # Encode the BGR frame for publishing
                        _, buffer = cv2.imencode('.jpg', bgr_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                        redis_client.publish(OUTPUT_CHANNEL, buffer.tobytes())
                        redis_client.set(HEALTH_KEY, "online", ex=10)

                    except KeyboardInterrupt: break
                    except Exception: traceback.print_exc()
    
    print("\n--- AI Pipeline shutting down. ---")

if __name__ == "__main__":
    main()