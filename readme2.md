
### 2. Hardware Setup & Wiring

**Safety Warning:** Always fully power down the Raspberry Pi and the 12V/24V power supply before connecting or disconnecting any hardware.

#### 2.1. Core Components
*   **Raspberry Pi 5**
*   **USB to RS485 Converter**
*   **USR-IO4040:** For sensor inputs (set to Modbus Slave ID **1**).
*   **USR-IO8000:** For relay outputs (set to Modbus Slave ID **2**).
*   **12V or 24V DC Power Supply:** To power the Modbus modules, sensors, and relay coils.
*   **5V Logic-Level Relay Modules:** One or more modules that accept a 5V signal on their `IN` pins.
*   **NPN Proximity Sensors**
*   **USB Camera**

#### 2.2. RS485 Bus & Power Wiring
1.  **Power:** Provide 12V/24V DC power to both the USR-IO4040 and USR-IO8000 modules.
2.  **RS485 Bus (Daisy-Chain):**
    *   Connect the RPi's USB to the RS485 converter.
    *   Connect the converter's `A+` and `B-` to the `A` and `B` terminals on the USR-IO4040 (ID 1).
    *   Connect the `A` and `B` terminals from the USR-IO4040 to the `A` and `B` terminals on the USR-IO8000 (ID 2).

#### 2.3. Sensor Wiring (to USR-IO4040)
*   **Power Sensor:** Connect the sensor's Brown (`+V`) and Blue (`GND`) wires to your 12V/24V power supply.
*   **Connect Signal:** Connect the sensor's Black (Signal) wire directly to a Digital Input terminal (e.g., `DI1`, `DI2`).

#### 2.4. Output Wiring: USR-IO8000 to 5V Relay Modules (Safe, Isolated Method)
This method uses the USR-IO8000's internal relays to safely switch the 5V logic signal required by your relay modules. This protects your high-power devices and your control hardware.

**Step 1: Power the 5V Relay Module from the Raspberry Pi**
| From Component | From Terminal | To Component | To Terminal |
| :--- | :--- | :--- | :--- |
| Raspberry Pi | `5V` | 5V Relay Module | `VCC` |
| Raspberry Pi | `GND` | 5V Relay Module | `GND` |

**Step 2: Connect the USR-IO8000 to the Relay Module's `IN` Pins**
This circuit uses the USR-IO8000 as a dry switch for the Pi's 5V signal. Repeat this pattern for each relay you want to control.
| Logical Device | From Pi `5V` Wire -> | USR-IO8000 Terminals | -> To Relay Module Pin |
| :--- | :--- | :--- | :--- |
| Conveyor | Pi `5V` | `COM1` -> `NO1` | `IN1` |
| Gate | Pi `5V` | `COM2` -> `NO2` | `IN2` |
| Diverter | Pi `5V` | `COM3` -> `NO3` | `IN3` |
| Green LED | Pi `5V` | `COM4` -> `NO4` | `IN4` |

**Step 3: Connect High-Power Devices to the Relay Module's Contacts**
The blue screw terminals on your 5V relay module switch the actual high-power load.
| From High-Power Source | -> To Relay Contact | -> To Device (e.g., Motor) | -> Back to High-Power Source |
| :--- | :--- | :--- | :--- |
| `+` / `Line` | `COM` terminal | `Power In` terminal | `-` / `Neutral` |
| (Switched by Relay) | `NO` terminal | | |

### 3. Installation & Setup

1.  **Update OS & Install Dependencies:**
    ```bash
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y redis-server python3-venv
    ```

2.  **Enable Camera & Set Permissions:**
    *   Run `sudo raspi-config` and ensure the legacy camera stack is **disabled**.
    *   Add your user to the necessary hardware groups. **You must log out and log back in**.
        ```bash
        sudo usermod -a -G video,dialout $USER
        ```

3.  **Application Setup:**
    *   Navigate to the project root.
    *   Create and activate a virtual environment:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   Install Python packages from `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```
    *   **Install AI Libraries:**
        ```bash
        pip install ultralytics tflite-runtime opencv-python-headless
        ```

4.  **Download and Convert AI Model:**
    *   Run this command to download the YOLOv8n model:
        ```bash
        yolo
        ```
    *   Run this command to convert it to the required TFLite format:
        ```bash
        yolo export model=yolov8n.pt format=tflite int8
        ```
    *   Move the resulting file (`yolov8n_export/yolov8n_full_integer_quant.tflite`) to the root of your project directory.

5.  **Configuration:**
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit the file with your specific hardware settings: `nano .env`

### 4. Configuration Reference (`.env` file)

| Section | Variable | Description | Default |
| :--- | :--- | :--- | :--- |
| **MODBUS** | `MODBUS_PORT` | The serial port for your RS485 adapter. | `/dev/ttyUSB0`|
| | `MODBUS_DEVICE_ADDRESS_INPUTS` | Slave ID of the USR-IO4040. | `1` |
| | `MODBUS_DEVICE_ADDRESS_OUTPUTS` | Slave ID of the USR-IO8000. | `2` |
| **SENSORS**| `SENSORS_ENTRY_CHANNEL` | **1-based** channel number for the entry sensor. | `1` |
| | `SENSORS_EXIT_CHANNEL` | **1-based** channel number for the exit sensor. | `2` |
| **OUTPUTS**| `OUTPUTS_CONVEYOR` | **0-based** coil address for the conveyor relay. | `0` |
| | `OUTPUTS_GATE` | **0-based** coil address for the gate relay. | `1` |
| | `OUTPUTS_...` | ...and so on for other outputs. | |

### 5. Running the Application

For the system to work, the main web app and the camera service must be running.

#### Development Mode
Run each service in a separate terminal to see live log output.
*   **Terminal 1 (Main App & AI Service):**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env --reload
    ```
*   **Terminal 2 (USB Camera Service):**
    ```bash
    python services/camera_service_usb.py
    ```

#### Production Deployment
Use `systemd` to manage the services so they start on boot. Update your service files to run `main:app` and `camera_service_usb.py`.

### 6. Troubleshooting

| Problem | Symptom | Solution |
| :--- | :--- | :--- |
| **One sensor not working** | The UI status for one sensor is stuck. | The issue is likely physical. Perform the "Swap Test": swap the sensor signal wires on the USR-IO4040 terminals (`DI1`, `DI2`). If the problem moves to the other sensor in the UI, the sensor/cable is bad. If the problem stays on the same UI element, the USR-IO4040 port is bad. |
| **Blurry AI Images** | Objects in the captured images are smeared. | This is **Motion Blur**. You need to **add more physical light** to the scene and use the Profile Management UI to set a faster **shutter speed** (e.g., `Exposure = -8`). |
| **Dark AI Images** | Images are sharp but too dark to see. | This is the result of a fast shutter speed. You must **add more physical light**. You can also increase the `Gain` setting in the camera profile, but too much gain will make the image noisy. |
| **AI Feed is slow** | The video in the AI feed is not 30 FPS. | This is expected. The Pi's CPU can only process ~8-12 FPS. For real-time 30+ FPS, you must add a **Google Coral USB Accelerator**. The TFLite model is already prepared for this upgrade. |

### 7. Knowledge Base for AI Analysis

#### Core Technologies
*   **Backend Framework:** FastAPI (Asynchronous)
*   **Real-time Communication:** WebSockets & Redis Pub/Sub
*   **Hardware IO:** `pymodbus` for Modbus RTU (RS485)
*   **AI Framework:** **TensorFlow Lite (TFLite)**, chosen for its efficiency and direct compatibility with Google Coral accelerators.

#### Key Architectural Patterns
1.  **Decoupled AI Processing:** The `AIService` runs as an independent `asyncio` task. It reads the latest frame from Redis, processes it (slowly), and publishes the result to a new Redis channel. This ensures the high-speed camera capture and live video stream are **never blocked** by slow AI inference.
2.  **Modbus Abstraction:** All hardware interaction is funneled through the `AsyncModbusController`. High-level services like `OrchestrationService` simply command "turn on conveyor"; they do not need to know about Slave IDs or coil addresses.
3.  **Hardware State Caching:** The `AsyncModbusPoller` constantly polls the hardware in the background and keeps the latest state in memory. This means status requests from the UI (`system_service`) are instant and do not need to wait for a slow hardware query.

#### Data Flow: Live AI Video Stream
1.  **Capture (30 FPS):** `camera_service_usb.py` captures a frame and publishes it to the `camera:frames:usb` Redis channel.
2.  **Raw Stream (30 FPS):** The `/api/v1/camera/stream/usb` endpoint in `camera.py` immediately reads from that channel and sends the raw JPEG to the browser's left-hand video feed.
3.  **AI Processing (~8 FPS):** The `AIService` in `main.py` grabs the latest frame from the same `camera:frames:usb` channel.
4.  **Inference (Slow):** The `AIService` runs the YOLOv8 TFLite model on the frame. This is the slow step (~100ms).
5.  **Annotate & Publish:** The `AIService` draws the resulting bounding boxes onto the image and publishes the *new*, annotated JPEG to a different Redis channel: `ai_stream:frames:usb`.
6.  **AI Stream (~8 FPS):** The `/api/v1/ai_stream/usb` endpoint reads from this second channel and sends the annotated JPEG to the browser's right-hand video feed.

#### Future Upgrade Path: Google Coral
Because you are using a **quantized TFLite model**, upgrading is simple:
1.  Purchase a Google Coral USB Accelerator.
2.  Install the Edge TPU compiler (`sudo apt-get install edgetpu-compiler`).
3.  Compile your existing model: `edgetpu_compiler yolov8n_full_integer_quant.tflite`. This creates `..._edgetpu.tflite`.
4.  Update your `ai_service.py` to load the new `_edgetpu.tflite` model and add `{'edgetpu.dll': 'libedgetpu.so.1'}` as a delegate to the TFLite Interpreter. Your AI framerate will jump from ~8 FPS to over 60 FPS.