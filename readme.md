+-------------------------------------------------+
|               Main Web Application              |
|                    (Uvicorn)                    |
|                                                 |
|  +-----------------------+       +------------+ |
|  | Orchestration Service |------>| GPIO Ctrl  | |
|  | (The "Brain")         |       | (Lights)   | |
|  +--------^--------------+       +------------+ |
|           | (Receives "Box Counted" event)      |
|  +--------+--------------+                      |
|  |   Detection Service   |<--------------------+
|  | (Handles State Machine) |(Receives Sensor Events)|
|  +--------^--------------+                      |
|           |                                     |
|  +--------+----------------+                     |
|  | Proximity Sensor Handler|                     |
|  |   (Polls Hardware)      |                     |
|  +--------+----------------+                     |
|           | (Modbus/RS485)                      |
+-----------+-------------------------------------+
            |
+-----------v-------------------------------------+
|              Hardware Layer                     |
|                                                 |
|  +------------+   +------------+   +----------+ |
|  | USR-IO8000 |   |   Relays   |   |  Camera  | |
|  +------------+   +------------+   +----------+ |
+-------------------------------------------------+```

### 4. Hardware Setup & Wiring

**Safety Warning:** Always fully power down the Raspberry Pi and IO Modules before connecting or disconnecting any hardware.

#### 4.1. USR-IO8000 Modbus Module & NPN Proximity Sensors

This system is specifically configured to work with **NPN-type proximity sensors**. The wiring is critical for reliable operation. The USR-IO8000 module has internal pull-up resistors, which simplifies wiring.

**Required Wiring for NPN Sensors:**
-   **VCC (Brown wire):** Connect to your IO Module's power supply (e.g., +12V or +24V).
-   **GND (Blue wire):** Connect to your IO Module's power ground.
-   **Signal (Black wire):** Connect the sensor's signal wire directly to a Digital Input terminal (e.g., `DI1`).

When an object is present, the sensor's light will turn **OFF**, and it will send a `LOW` signal to the IO module. The application is built to interpret this `LOW` signal as `TRIGGERED`.

#### 4.2. GPIO Devices
All pin numbers refer to the **BCM numbering scheme**. You can configure these in your `.env` file.

| Device             | Default BCM Pin |
| ------------------ | --------------- |
| Conveyor Relay     | 26              |
| Gate Relay         | 22              |
| Status LED (Green) | 27              |
| Status LED (Red)   | 23              |
| Buzzer             | 24              |

### 5. Installation & Setup

This guide assumes a fresh installation of Raspberry Pi OS (Bookworm, 64-bit).

1.  **Update OS & Install Dependencies:**
    ```bash
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y python3-libcamera redis-server python3-venv
    ```

2.  **Enable Camera & Set Permissions:**
    -   Run `sudo raspi-config`, go to `3 Interface Options` -> `I1 Legacy Camera`, and select **<No>** to use the modern `libcamera` stack.
    -   Add your user to the necessary hardware groups. **You must log out and log back in** after this.
        ```bash
        sudo usermod -a -G gpio,video,dialout $USER
        ```

3.  **Application Setup:**
    -   Copy the project directory to your Raspberry Pi.
    -   Navigate to the project root: `cd /path/to/box_counter_system`
    -   Create a virtual environment with access to system packages (critical for the camera):
        ```bash
        python3 -m venv venv --system-site-packages
        ```
    -   Activate the environment:
        ```bash
        source venv/bin/activate
        ```
    -   Install Python packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configuration:**
    -   Copy the example environment file: `cp .env.example .env`
    -   Edit the file with your specific hardware settings: `nano .env`

### 6. Configuration Reference (`.env` file)

Your `.env` file should use the `SECTION_VARIABLE` format (e.g., `SERVER_HOST`).

| Variable                            | Description                                                                 | Default      |
| ----------------------------------- | --------------------------------------------------------------------------- | ------------ |
| `APP_ENV`                           | Set to `development` or `production`.                                       | `development`|
| `LOGGING_VERBOSE_LOGGING`           | Set to `true` to see detailed state machine logs in the console.              | `false`      |
| `SERVER_HOST`                       | IP address for the web server to bind to.                                   | `0.0.0.0`    |
| `SERVER_PORT`                       | Port for the web server.                                                    | `8000`       |
| `SERVER_SECRET_KEY`                 | A long, random string for security.                                         | (required)   |
| `SECURITY_API_KEY`                  | A static API key for protected endpoints like Emergency Stop.                 | (required)   |
| `GPIO_PIN_CONVEYOR_RELAY`           | BCM pin number for the conveyor relay.                                      | `26`         |
| `SENSORS_ENTRY_CHANNEL`             | The channel number (1-8) on the IO module for the entry sensor.               | `1`          |
| `SENSORS_EXIT_CHANNEL`              | The channel number (1-8) on the IO module for the exit sensor.                | `2`          |
| `ORCHESTRATION_POST_BATCH_DELAY_SEC`| The time in seconds to pause after a batch completes.                         | `5`          |

### 7. Running the Application

For the system to work, both the main web app and the camera service must be running.

#### Development Mode
Run each service in a separate terminal to see live log output.
-   **Terminal 1 (Main Web App):**
    ```bash
    source venv/bin/activate
    uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env --reload
    ```
-   **Terminal 2 (Camera Service):**
    ```bash
    python camera_service.py
    ```

#### Production Deployment
Use `systemd` to manage the services so they start on boot and restart automatically on failure.
1.  Create two service files: `/etc/systemd/system/box-counter-app.service` and `/etc/systemd/system/box-counter-camera.service`.
2.  Use the templates in `docs/deployment.md` to fill them, ensuring you use the correct absolute paths.
3.  Enable and start the services:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable --now box-counter-app.service box-counter-camera.service
    ```

### 8. Troubleshooting

| Problem                               | Log Message / Symptom                                        | Solution                                                                                                                            |
| ------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Sensors show TRIGGERED when clear** | The UI status is inverted.                                   | The sensor logic is hardcoded for NPN sensors where `Light OFF` = `Object Present`. Check your sensor type and wiring.               |
| **Camera fails to start**             | `Camera frontend has timed out!` or `libcamera` errors.        | This is a **physical hardware issue**. Power down and securely reseat the camera ribbon cable. Verify you enabled the modern camera stack in `raspi-config`. |
| **Cannot start app (ValidationError)**| `Field required`, `Extra inputs not permitted`                 | Your `.env` file format does not match the format in this guide (`SECTION_VARIABLE`). Correct the variable names and restart. |
| **Counter doesn't increase**          | Boxes pass but the count doesn't change.                       | Set `LOGGING_VERBOSE_LOGGING=true` in your `.env` file, restart, and watch the console logs for `[State Machine]` messages to diagnose where the sequence is failing. |
| **UI is not updating**                | The webpage is frozen or buttons do nothing.                 | Perform a **hard refresh** in your browser (Ctrl+F5 or Cmd+Shift+R) to clear any cached old versions of the JavaScript or HTML files. |

---

## Part 2: Knowledge Base for AI Analysis and Development

### Project High-Level Goal
The primary objective is to create a robust, real-time system using a Raspberry Pi to count objects on a conveyor belt in automated batches, control associated hardware (lights, gates, relays), and provide a live monitoring and control interface via a web application.

### Core Technologies
-   **Backend Framework:** FastAPI (Asynchronous)
-   **Database:** SQLAlchemy 2.0 (Async) with SQLite
-   **Real-time Communication:** WebSockets
-   **Inter-Process Communication:** Redis Pub/Sub
-   **Hardware IO:** `gpiozero` for GPIO, `pymodbus` for Modbus RTU (RS485)
-   **Configuration:** Pydantic-settings
-   **Frontend:** Jinja2 templates, vanilla JavaScript (ES6)

### Key Architectural Patterns & Constraints
1.  **Multi-Process Architecture:** The `camera_service.py` runs in a separate process from the main `uvicorn` application. This is a critical design choice for fault tolerance. A failure in the camera hardware or its process must not crash the core counting and control application.
2.  **Service-Oriented Logic:** The application logic is divided into services (`OrchestrationService`, `DetectionService`, `SystemService`). The `OrchestrationService` acts as the central state controller (the "brain").
3.  **Decoupled Communication:**
    -   **Hardware to App:** `AsyncProximitySensorHandler` polls the hardware and emits abstract `SensorEvent` objects. The rest of the application is blind to the hardware specifics.
    -   **App to Frontend:** The backend broadcasts status updates via WebSockets. The frontend listens for these messages and updates the UI reactively. It does not poll for data.
    -   **Detection to Orchestration:** The `DetectionService` uses a callback (`on_box_counted`) to notify the `OrchestrationService` of a successful count. This is a loosely coupled dependency injection pattern.
4.  **Asynchronous Everywhere:** All I/O operations (database, hardware polling, WebSockets) must be asynchronous using `async`/`await` to ensure the application remains responsive to real-time events.
5.  **Hardware Logic Inversion:** The system is hardcoded for a specific hardware behavior: NPN sensors connected to a USR-IO8000 module. For this hardware, a `LOW` (False) signal from the Modbus client means an object is detected. The `AsyncProximitySensorHandler` is responsible for this inversion, translating `False` to a `TRIGGERED` event.

### Service Interaction Map
-   `main.py`: Initializes all services and injects dependencies. Starts the WebSocket broadcast loop.
-   `OrchestrationService`:
    -   Depends on: `AsyncGPIOController`.
    -   Purpose: To control the gate, conveyor, and status LEDs based on the current operating mode (e.g., `RUNNING_BATCH`).
    -   Receives input from: `DetectionService` (via `on_box_counted` callback).
-   `DetectionService`:
    -   Depends on: `AsyncCameraManager`, `on_box_counted` callback.
    -   Purpose: To manage the box detection state machine (`IDLE` -> `ENTERING` -> ...). Triggers the camera and calls the orchestration callback upon a successful count.
    -   Receives input from: `AsyncProximitySensorHandler` (via `handle_sensor_event` method).
-   `AsyncProximitySensorHandler`:
    -   Depends on: `AsyncUSRIOController`, `handle_sensor_event` callback.
    -   Purpose: To poll the Modbus module at high frequency, interpret the raw NPN signal (`False` = Triggered), and emit `SensorEvent` objects.

### Data Flow: Box Counting Sequence
1.  **Hardware:** An object blocks the entry sensor, causing its signal to the USR-IO8000 to go `LOW`.
2.  **`AsyncProximitySensorHandler`:** Polls the IO module, reads the `False` signal, interprets it as `TRIGGERED`, and calls `detection_service.handle_sensor_event` with a `SensorEvent`.
3.  **`DetectionService`:** The state machine transitions from `IDLE` to `ENTERING`. It starts a background task to trigger the camera.
4.  **Hardware:** The object moves and blocks the exit sensor.
5.  **`DetectionService`:** The state machine transitions to `CONFIRMING_EXIT`.
6.  **Hardware:** The object clears the entry sensor.
7.  **`DetectionService`:** The state machine transitions to `RESETTING`. This is the **counting event**. The service increments its internal counter, logs the detection to the database, and calls the `orchestration_service.on_box_counted` callback.
8.  **`OrchestrationService`:** Receives the callback, increments its batch progress, and checks if the batch is complete.
9.  **`main.py` Broadcast Loop:** On its next cycle, it fetches the new total count and the new batch progress and broadcasts them to the UI via a WebSocket message.

### Coding & Development Guidelines
-   **State Management:** All high-level application state (e.g., "is a batch running?") must be managed exclusively by the `OrchestrationService`. Other services should be stateless or manage only their own low-level state.
-   **Logging:** When modifying the state machine in `DetectionService`, add `print` statements prefixed with `[State Machine]` under the `if self._verbose:` block to aid debugging.
-   **Frontend Updates:** If a new piece of data needs to be displayed on the frontend, it must first be added to the payload of a WebSocket message in the `main.py` broadcast loop. Then, the relevant JavaScript file (`dashboard.js`, `status.js`, etc.) can be updated to handle the new data.
-   **API Endpoints:** Business logic must not be placed directly in API endpoint functions. Endpoints should be thin wrappers that call methods on the appropriate service.
-   **Error Handling:** Hardware interaction code (especially in `usr8000_client.py`) must be wrapped in `try...except` blocks to handle `ConnectionException` and `TimeoutError` to prevent crashes and ensure the system can self-heal.