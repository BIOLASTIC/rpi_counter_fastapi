"""
NEW: AI Service for Real-Time Object Detection

FINAL REVISION: This version fixes a critical bug in the coordinate scaling
logic within the drawing function. It also adds more robust error logging.
"""
import asyncio
import redis.asyncio as redis
import cv2
import numpy as np
import time
import traceback

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite.python.interpreter import Interpreter

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

class AIService:
    def __init__(self, camera_id: str, redis_client: redis.Redis):
        self.camera_id = camera_id
        self._redis = redis_client
        self._input_frame_channel = f"camera:frames:{camera_id}"
        self._output_stream_channel = f"ai_stream:frames:{camera_id}"
        self._is_running = False
        self._task: asyncio.Task = None

        try:
            self.interpreter = Interpreter(model_path="yolov8n_full_integer_quant.tflite")
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.model_height = self.input_details[0]['shape'][1]
            self.model_width = self.input_details[0]['shape'][2]
            print(f"[AI Service] TFLite model loaded. Input size: {self.model_width}x{self.model_height}")
        except Exception as e:
            print(f"\n\n[AI Service] FATAL ERROR: Could not load TFLite model 'yolov8n_full_integer_quant.tflite'.")
            print(f"Ensure the file is in the project's root directory. Error: {e}\n\n")
            raise e

    def start(self):
        if not self._is_running:
            print(f"[AI Service - {self.camera_id}] Starting AI processing loop.")
            self._is_running = True
            self._task = asyncio.create_task(self._detection_loop())

    def stop(self):
        if self._is_running:
            print(f"[AI Service - {self.camera_id}] Stopping AI processing loop.")
            self._is_running = False
            if self._task: self._task.cancel()

    def _run_model_and_draw(self, image: np.ndarray) -> np.ndarray:
        """
        Runs the TFLite model on a single frame and draws the results.
        This is a SYNCHRONOUS, CPU-blocking function.
        """
        original_height, original_width, _ = image.shape
        input_image = cv2.resize(image, (self.model_width, self.model_height))
        input_data = np.expand_dims(input_image.astype(np.uint8), axis=0)
        
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        output_data = output_data.T

        for row in output_data:
            confidence = row[4:].max()
            if confidence < 0.4:  # Confidence threshold
                continue

            class_id = int(row[4:].argmax())
            label = COCO_CLASSES[class_id]
            
            if label not in ['bottle', 'cup', 'cell phone', 'book', 'box']: continue

            xc, yc, w, h = row[:4]

            # --- THE BUG FIX IS HERE ---
            # The model's output (xc, yc, w, h) is normalized (values from 0-1).
            # We must scale them by the ORIGINAL image dimensions, not the model dimensions.
            x1 = int((xc - w / 2) * original_width)
            y1 = int((yc - h / 2) * original_height)
            x2 = int((xc + w / 2) * original_width)
            y2 = int((yc + h / 2) * original_height)
            # --- END OF FIX ---
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        return image

    async def _detection_loop(self):
        """The main loop that continuously processes frames."""
        last_frame_data = None
        while self._is_running:
            try:
                frame_data = await self._redis.get(self._input_frame_channel)

                if frame_data and frame_data != last_frame_data:
                    last_frame_data = frame_data
                    
                    np_array = np.frombuffer(frame_data, np.uint8)
                    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                    if image is None:
                        print(f"[AI Service - {self.camera_id}] Warning: Could not decode frame from Redis.")
                        continue

                    loop = asyncio.get_running_loop()
                    processed_image = await loop.run_in_executor(
                        None, self._run_model_and_draw, image
                    )

                    _, buffer = cv2.imencode('.jpg', processed_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    await self._redis.publish(self._output_stream_channel, buffer.tobytes())

                await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                break
            except Exception as e:
                # This new, detailed logging will show us any future errors.
                print(f"[AI Service - {self.camera_id}] CRITICAL ERROR in detection loop: {e}")
                print(traceback.format_exc())
                await asyncio.sleep(1)