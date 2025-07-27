Of course. Here is the complete and definitive documentation for the Raspberry Pi 5 Box Counter application. This single document covers everything from the project's architecture and folder structure to hardware connections, installation, configuration, and troubleshooting, incorporating all the lessons learned from our development and debugging process.

***

# Project Documentation: Raspberry Pi 5 Box Counter System

## 1. Introduction

This document provides a comprehensive guide to the Raspberry Pi 5 Box Counter System. It is a production-grade, fault-tolerant application designed to count objects on a conveyor belt using proximity sensors and a camera. The system is built on a modern, asynchronous Python stack (FastAPI, SQLAlchemy) and features a resilient multi-service architecture to ensure high availability.

### 1.1. Key Features

-   **High-Performance Backend:** Built on FastAPI for non-blocking, asynchronous I/O, capable of handling real-time hardware events efficiently.
-   **Resilient Multi-Service Architecture:** The camera runs in a completely separate process from the main web application. This provides maximum stability, ensuring that even a catastrophic camera hardware crash will **not** impact the core counting and control functionality.
-   **Real-time Web UI:** A dynamic dashboard provides live updates of the box count, sensor states, and overall system health via WebSockets.
-   **Configurable Hardware Mapping:** All physical connections (GPIO pins, Modbus sensor channels) are defined in a simple `.env` file, allowing for flexible hardware setups without code changes.
-   **Persistent Event Logging:** Critical events, warnings, and hardware errors are automatically logged to a database and are viewable on a dedicated web log page.
-   **Comprehensive Diagnostics:** Includes dedicated web pages for monitoring high-level system status and a detailed live view of all hardware connections and states.
-   **REST API:** A full-featured API allows for programmatic control, monitoring, and integration with other systems.

### 1.2. System Architecture

The system's resilience comes from its decoupled, two-service design that communicates via a Redis message broker.

```
+--------------------------+           +--------------------------+
|    Raspberry Pi 5        |           |    User / Network        |
|                          |           |                          |
|  +--------------------+  |           |  +--------------------+  |
|  |   Camera Service   |  |           |  |   Web Browser      |  |
|  | (camera_service.py)|  |           |  | (Dashboard, etc.)  |  |
|  +--------+-----------+  |           |  +---------+----------+  |
|           |              |           |            ^           |
|  (Hardware Crash Here    |           |            |           |
|   Does NOT Affect App)   |           |  (HTTP / WebSockets)   |
|           |              |           |            |           |
|           v              |           |            v           |
|  +--------+-----------+  |           |  +---------+----------+  |
|  |   Redis Broker     |  | <----------+  |   Main Web App     |  |
|  | (Message Bus)      |  +---------->  | (main.py / Uvicorn)|  |
|  +--------------------+  |           |  +--------------------+  |
|           ^              |           |            |           |
|           |              |           |  (RS485)   | (GPIO)    |
| (Subscribes to Frames)   |           |      v           v     |
|                          |           | +--------+  +--------+ |
|                          |           | | Modbus |  | Relays | |
|                          |           | +--------+  +--------+ |
+--------------------------+           +--------------------------+
```

## 2. Project Structure

This section explains the purpose of each file and folder in the project root.

-   `main.py`: The entry point for the main web application. It creates the FastAPI app and manages the application's startup and shutdown lifecycle.
-   `camera_service.py`: The standalone, independent script for the camera service. It runs in its own process.
-   `.env` / `.env.example`: Configuration files where all hardware pins, sensor channels, and secrets are defined.
-   `requirements.txt`: A list of all required Python packages for the project.
-   `app/`: The main Python package for the web application.
    -   `api/`: Contains the REST API endpoint routers.
    -   `core/`: Contains the low-level classes that directly interface with hardware (`gpio_controller.py`, `camera_manager.py`, `usr8000_client.py`).
    -   `services/`: Contains the higher-level business logic (`detection_service.py`, `system_service.py`).
    -   `models/`: Defines the SQLAlchemy database tables.
    -   `web/`: Contains the routers that serve the HTML web pages.
    -   `websocket/`: Manages the real-time WebSocket connections.
-   `config/`: Manages loading and validating configuration from the `.env` file.
-   `static/`: Contains the CSS and JavaScript files for the web dashboard.
-   `templates/`: Contains the Jinja2 HTML templates for all web pages.
-   `docs/`: Contains all project documentation files (like this one).
-   `tests/`: The `pytest` test suite for validating the application's logic.

## 3. Hardware Setup & Wiring

**Safety Warning:** Always fully power down the Raspberry Pi before connecting or disconnecting any hardware.

### 3.1. Camera Module
-   **Connector:** Use a CSI port on the Raspberry Pi 5.
-   **Cable Orientation:** The ribbon cable's blue tab should face the USB ports on the Pi.
-   **Securing:** Gently pull up the plastic clip, insert the ribbon cable fully, and press the clip down firmly. A loose connection is the #1 cause of camera timeout errors.

### 3.2. USR-IO8000 Modbus Module
-   **Connection:** Connect the module to the Pi via a USB-to-RS485 converter.
-   **Wiring (RS485):**
    -   Connect the `A+` terminal on the converter to the `A` terminal on the IO module.
    -   Connect the `B-` terminal on the converter to the `B` terminal on the IO module.
    -   A swapped A/B connection is the most common cause of Modbus communication timeouts.
-   **Sensor Wiring:** Connect your proximity sensors to the Digital Input (DI) terminals (e.g., `DI1`, `DI4`, etc.).

### 3.3. GPIO Devices
All pin numbers refer to the **BCM numbering scheme**. You can configure these in your `.env` file.

| Device | Default BCM Pin | Notes |
| :--- | :--- | :--- |
| Conveyor Relay | 26 | Set `active_high=False` in `gpio_controller.py` for active-low relays. |
| Gate Relay | 22 | Set `active_high=False` in `gpio_controller.py` for active-low relays. |
| Status LED (Green) | 27 | Standard LED wiring. |
| Status LED (Red) | 23 | Standard LED wiring. |
| Buzzer | 24 | Standard buzzer wiring. |

## 4. Installation & Setup

This guide assumes a fresh installation of Raspberry Pi OS (Bookworm, 64-bit).

### 4.1. System Preparation
1.  **Update OS:** `sudo apt-get update && sudo apt-get upgrade -y`
2.  **Enable Camera:** Run `sudo raspi-config`, go to `3 Interface Options` -> `I1 Legacy Camera`, and select **<No>** to ensure the modern `libcamera` stack is used.
3.  **Set Permissions:** Add your user to the necessary hardware groups. **You must log out and log back in** after running this command.
    ```bash
    sudo usermod -a -G gpio,video $USER
    ```
4.  **Install System Dependencies:**
    ```bash
    sudo apt-get install -y python3-libcamera redis-server python3-venv
    ```

### 4.2. Application Setup
1.  **Get the Code:** Copy the project directory to your Raspberry Pi.
2.  **Navigate to Root:** `cd /path/to/box_counter_system`
3.  **Create Virtual Environment:** The `--system-site-packages` flag is **critical** as it allows the environment to access the `libcamera` library.
    ```bash
    python3 -m venv venv --system-site-packages
    ```
4.  **Activate Environment:**
    ```bash
    source venv/bin/activate
    ```
5.  **Install Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```6.  **Create & Edit Configuration:**
    ```bash
    cp .env.example .env
    nano .env
    ```

## 5. Configuration Reference (`.env` file)

This section details all the variables you can set in your `.env` file.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SERVER_HOST` | IP address for the web server. | `0.0.0.0` |
| `SERVER_PORT` | Port for the web server. | `8000` |
| `SECURITY_API_KEY` | Secret key for protected API endpoints. | `your_secret_api_key_here`|
| `SENSOR_ENTRY_CHANNEL` | **Critical:** The physical channel number (1-8) for the entry sensor. | `1` |
| `SENSOR_EXIT_CHANNEL` | **Critical:** The physical channel number (1-8) for the exit sensor. | `2` |
| `GPIO_PIN_CONVEYOR_RELAY`| BCM pin for the conveyor relay. | `26` |
| `MODBUS_PORT` | The serial port for the RS485 adapter. | `/dev/ttyUSB0` |
| `MODBUS_DEVICE_ADDRESS`| The Modbus slave ID of the IO module. | `1` |
| `DB_URL` | The database connection string. | `sqlite+...`|

## 6. Running the Application

### 6.1. Development Mode
For development, run the two services in two separate terminals. This allows you to see live log output from both.

-   **Terminal 1 (Main Web App):**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env
    ```
-   **Terminal 2 (Camera Service):**
    ```bash
    python camera_service.py
    ```

### 6.2. Production Deployment
For a production environment, you should run the services using `systemd` so they start on boot and restart automatically if they crash.

1.  Create two service files: `sudo nano /etc/systemd/system/box-counter-app.service` and `sudo nano /etc/systemd/system/box-counter-camera.service`.
2.  Use the templates in `docs/deployment.md` to fill them, ensuring you use the correct absolute paths to your project.
3.  Enable and start the services:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable box-counter-app.service box-counter-camera.service
    sudo systemctl start box-counter-app.service box-counter-camera.service
    ```

## 7. Troubleshooting

| Problem | Log Message | Solution |
| :--- | :--- | :--- |
| **Camera Fails to Start** | `Camera frontend has timed out!` | This is a **physical hardware issue**. Power down and securely reseat the camera ribbon cable at both ends. Verify you are using the official 27W power supply. |
| **Web UI is Blank** | No WebSocket messages | The `broadcast_updates` task in `main.py` has likely failed. Check the Uvicorn logs for errors during startup. This is often caused by a service (like `DetectionService`) failing to initialize. |
| **Wrong Sensor Status**| Dashboard shows `CLEARED` but the sensor is on. | The `SENSOR_..._CHANNEL` numbers in your `.env` file do not match your physical wiring. Verify the correct channel number and update your `.env` file. |
| **Port Locked** | `Could not exclusively lock port /dev/ttyUSB0` | Another application (like Node-RED or a previous crashed version of this app) is holding the port open. Stop the other application or reboot the Pi. |
| **No Modbus Response** | `No response received after 3 retries` | Check that the `A` and `B` wires of your RS485 connection are not swapped. Also verify the `MODBUS_DEVICE_ADDRESS` in `.env` matches the hardware. |
| **Cannot Import `libcamera`** | `ModuleNotFoundError: No module named 'libcamera'` | Your virtual environment does not have access to system packages. Recreate it with the `--system-site-packages` flag. See Step 3 of the installation guide. |