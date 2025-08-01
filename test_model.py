import cv2
import numpy as np
import time

try:
    from tflite_runtime.interpreter import Interpreter
    print("Successfully imported tflite_runtime.")
except ImportError:
    print("Failed to import tflite_runtime. Trying tensorflow.lite.")
    from tensorflow.lite.python.interpreter import Interpreter

MODEL_PATH = "yolov8n_full_integer_quant.tflite"
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 320

print(f"\n--- TFLite Model Sanity Check ---")

try:
    print(f"1. Loading model from: {MODEL_PATH}")
    interpreter = Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    print("   ✅ Model loaded and tensors allocated successfully.")

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_dtype = input_details[0]['dtype']
    print(f"   - Model expects input type: {input_dtype}")

    print("2. Preparing dummy input data...")
    dummy_input = None
    
    # --- THE FIX IS HERE ---
    if input_dtype == np.int8:
        # 1. Create standard image data (0 to 255)
        dummy_uint8 = np.random.randint(0, 255, size=(1, IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
        # 2. Shift the range from [0, 255] to [-128, 127]
        dummy_input = (dummy_uint8.astype(np.int16) - 128).astype(np.int8)
        print("   - Created uint8 dummy image and converted it to the required int8 format.")
    elif input_dtype == np.float32:
        dummy_input = np.random.randn(1, IMAGE_HEIGHT, IMAGE_WIDTH, 3).astype(np.float32)
        print("   - Created float32 dummy image.")
    else: # Should be uint8
        dummy_input = np.random.randint(0, 255, size=(1, IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
        print("   - Created uint8 dummy image.")

    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    print("   ✅ Input tensor set successfully.")

    print("3. Running inference (invoke)...")
    start_time = time.time()
    interpreter.invoke()
    end_time = time.time()
    print(f"   ✅ Inference completed successfully in { (end_time - start_time) * 1000:.2f} ms.")

    print("4. Getting output tensor...")
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(f"   ✅ Output tensor retrieved successfully. Shape: {output_data.shape}")

    print("\n--- ✅ SANITY CHECK PASSED ---")

except Exception as e:
    print(f"\n--- ❌ SANITY CHECK FAILED ---")
    print(f"A critical error occurred: {e}")
    import traceback
    traceback.print_exc()