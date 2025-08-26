# File Structure

- rpi_counter_fastapi/
    - requirements.txt
    - readme2.md
    - safety_instructions.md
    - start_main_app.sh
    - createstructure.py
    - .lgd-nfy0
    - readme.md
    - start_camera_services.sh
    - hailort.log
    - llmttd.md
    - check_db_data.py
    - structurefiles.md
    - pytest.ini
    - .env
    - .gitignore
    - .env.example
    - pyproject.toml
    - main.py
    - data/
        - box_counter.db
        - box_counter_26_aug_25.db
        - box_counter.db.bkp
        - box_counter.db.bkp3
        - box_counter.db.2
    - docs/
        - manuals/
            - operator_manual.md
            - ai_features.md
            - ai_labelling.md
    - app/
        - __init__.py
        - websocket/
            - __init__.py
            - connection_manager.py
            - router.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - connection_manager.cpython-311.pyc
                - router.cpython-311.pyc
        - api/
            - v1/
                - __init__.py
                - operators.py
                - reports.py
                - system.py
                - ai_strategy.py
                - camera.py
                - analytics.py
                - profiles.py
                - products.py
                - outputs.py
                - debug.py
                - detection.py
                - run_history.py
                - orchestration.py
                - auth/
                    - __init__.py
                    - security.py
                    - dependencies.py
                    - jwt_handler.py
                    - __pycache__/
                        - __init__.cpython-311.pyc
                        - dependencies.cpython-311.pyc
                - __pycache__/
                    - debug.cpython-311.pyc
                    - audio.cpython-311.pyc
                    - run_history.cpython-311.pyc
                    - __init__.cpython-311.pyc
                    - detection.cpython-311.pyc
                    - reports.cpython-311.pyc
                    - operators.cpython-311.pyc
                    - system.cpython-311.pyc
                    - camera.cpython-311.pyc
                    - ai_strategy.cpython-311.pyc
                    - analytics.cpython-311.pyc
                    - profiles.cpython-311.pyc
                    - products.cpython-311.pyc
                    - outputs.cpython-311.pyc
                    - orchestration.cpython-311.pyc
        - auth/
        - middleware/
            - metrics_middleware.py
            - __pycache__/
                - metrics_middleware.cpython-311.pyc
        - core/
            - __init__.py
            - modbus_poller.py
            - camera_manager.py
            - modbus_controller.py
            - system_orchestrator.py
            - sensor_events.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - camera_manager.cpython-311.pyc
                - modbus_controller.cpython-311.pyc
                - modbus_poller.cpython-311.pyc
                - sensor_events.cpython-311.pyc
        - utils/
            - __init__.py
            - tokenizer.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - tokenizer.cpython-311.pyc
        - __pycache__/
            - __init__.cpython-311.pyc
        - web/
            - __init__.py
            - router.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - router.cpython-311.pyc
        - services/
            - __init__.py
            - detection_service.py
            - llm_service.py
            - tts_service.py
            - notification_service.py
            - system_service.py
            - orchestration_service.py
            - audio_service.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - llm_service.cpython-311.pyc
                - audio_service.cpython-311.pyc
                - system_service.cpython-311.pyc
                - detection_service.cpython-311.pyc
                - orchestration_service.cpython-311.pyc
                - tts_service.cpython-311.pyc
                - notification_service.cpython-311.pyc
        - models/
            - __init__.py
            - product.py
            - run_log.py
            - event_log.py
            - profiles.py
            - system_status.py
            - detection.py
            - detection_event.py
            - configuration.py
            - database.py
            - operator.py
            - __pycache__/
                - product.cpython-311.pyc
                - operator.cpython-311.pyc
                - database.cpython-311.pyc
                - __init__.cpython-311.pyc
                - detection.cpython-311.pyc
                - detection_event.cpython-311.pyc
                - run_log.cpython-311.pyc
                - configuration.cpython-311.pyc
                - profiles.cpython-311.pyc
                - event_log.cpython-311.pyc
                - system_status.cpython-311.pyc
        - schemas/
            - operators.py
            - run_log.py
            - reports.py
            - profiles.py
            - products.py
            - detection_event.py
            - __pycache__/
                - detection_event.cpython-311.pyc
                - reports.cpython-311.pyc
                - run_log.cpython-311.pyc
                - operators.cpython-311.pyc
                - profiles.cpython-311.pyc
                - products.cpython-311.pyc
    - __pycache__/
        - main.cpython-311.pyc
    - scripts/
        - load_test.py
        - setup_database.sh
        - system_test.py
        - backup.sh
        - install.sh
        - create_service.sh
        - setup_pi5.sh
        - benchmark.py
        - install_dependencies.sh
    - web/
        - static/
            - css/
                - dashboard_v3.css
                - dashboard.css
            - js/
                - operators.js
                - reports.js
                - dashboard.js
                - status.js
                - audio_settings.js
                - hardware.js
                - run_history.js
                - analytics.js
                - gallery_usb.js
                - dashboard_v3.js
                - gallery.js
                - products.js
                - connections.js
                - ai_strategy.js
                - profiles.js
                - qc_testing.js
                - gallery_rpi.js
            - captures/
                - rpi/
                    - event_5fe3c143-2334-4e2d-acff-a32bed6112f2_1755511297.jpg
                    - event_1d5422f5-1210-4556-b950-e4f24007b7ef_1755688146.jpg
                    - event_009d5628-7e11-4388-acd5-7014ac8f5f64_1755598806.jpg
                    - event_7354a6e1-f306-457d-b8ec-bd76958618d1_1755090487.jpg
                    - event_08409048-cbe7-4505-b395-794f4bb4c013_1755594398.jpg
                    - event_019f42bf-8cf9-48d0-bd4a-940c8b7954c9_1755604298.jpg
                    - event_46ac1310-d769-421d-abe8-723d71b103c0_1755602201.jpg

                    - qc_41ece90f-63f4-43d2-a0d6-c29a7f295f9c_1753993265.jpg
                    - qc_7bc00100-ea19-4f0a-9992-85f4c929dcde_1754082814.jpg
                    - qc_7cf35d9e-816c-4d3f-97eb-2157860e8359_1754089048.jpg
                    - qc_ff988d77-d092-428e-a10d-685b06f068a3_1753988876.jpg
                    - qc_c5c1da21-84f2-48ba-b5ca-cdee954c84a7_1753994132.jpg
                    - qc_d1d59b3a-2cc9-4583-82c0-e9c465306106_1754153390.jpg
                    - qc_3a038140-a18a-4b60-9927-c293be7ba681_1754088981.jpg
                    - qc_3c3015ec-8315-4225-ba47-1c4e3665b1e1_1754081302.jpg
                    - qc_ba17c683-4d97-4f26-801d-6ae0716058b4_1754089037.jpg
                    - qc_6f9fb896-b58c-4ed1-b9b1-e3fed190bd58_1753988854.jpg
                    - qc_52323ef9-53ec-4de6-82ea-1dda38a848fd_1753992471.jpg
                    - qc_a6ec9ba7-edd7-4a48-bd9a-6e5979102a75_1754057396.jpg
                    - qc_fe24bbc4-6f5a-480e-ad14-1fb70a6bbc39_1754153501.jpg
                    - qc_130e4dd3-3e20-4a4e-9d92-3acd6334b69b_1753992908.jpg
                    - qc_dc8e1005-4927-44b7-828c-d464ecaaee38_1754091157.jpg
                    - qc_fca2c711-5d5b-4b4f-a4f1-2a349a11cde5_1753989008.jpg
                    - qc_1e926c0e-0470-4d6f-bcf3-65fd75cf3c98_1754049274.jpg
                    - qc_d801ba8f-9944-4933-85b6-12224d437048_1754064310.jpg
            - images/
                - placeholder.jpg
        - templates/
            - index.html
            - gallery_rpi.html
            - status.html
            - live_view.html
            - reports.html
            - operators.html
            - live_view_rpi.html
            - analytics.html
            - audio_settings.html
            - logs.html
            - profiles.html
            - gallery.html
            - connections.html
            - gallery_usb.html
            - live_view_usb.html
            - api.html
            - products.html
            - help.html
            - qc_testing.html
            - hardware.html
            - dashboard.html
            - run_history.html
            - base.html
            - ai_strategy.html
    - audio_files/
        - cat_bl_carry_bags.mp3
        - qc_accept.mp3
        - product_stall_detected.mp3
        - qc_reject_distortion.mp3
        - cat_bb_carry_bags.mp3
        - qc_light_low_light.mp3
        - tts_cache/
            - startup_complete.wav
            - PASS_TEMPLATE.wav
            - LLM_PROMPT_TEMPLATE.wav
            - REJECT_TEMPLATE.wav
            - BATCH_COMPLETE_TEMPLATE.wav
            - NEXT_BATCH_TEMPLATE.wav
    - config/
        - __init__.py
        - settings.py
        - __pycache__/
            - __init__.cpython-311.pyc
            - settings.cpython-311.pyc
    - services/
        - camera_service_rpi.py
        - camera_service_usb.py
    - tests/
        - test_api.py
        - conftest.py
        - test_models.py
        - test_services.py

# Python Files Content

---

### `createstructure.py`

```python
import os

def generate_file_structure_md(root_dir='.', output_file='structurefiles.md'):
    """
    Generates a Markdown file with the directory structure and content of Python files.

    Args:
        root_dir (str): The root directory to start from. Defaults to the current directory.
        output_file (str): The name of the output Markdown file. Defaults to 'structurefiles.md'.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # First, write the file structure
            f.write("# File Structure\n\n")
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # To ignore hidden directories like .git, .idea, etc. and venv folders
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 'venv' not in d]
                
                # Normalize path to handle both Windows and Unix-like systems
                normalized_dirpath = os.path.normpath(dirpath)
                level = normalized_dirpath.replace(root_dir, '').count(os.sep)
                
                # Indent based on the directory level
                indent = ' ' * 4 * (level)
                
                # To handle the root directory properly
                if dirpath == root_dir:
                    f.write(f"- {os.path.basename(root_dir)}/\n")
                else:
                    f.write(f"{indent}- {os.path.basename(dirpath)}/\n")
                
                sub_indent = ' ' * 4 * (level + 1)
                for filename in filenames:
                    f.write(f"{sub_indent}- {filename}\n")

            # Then, write the content of each Python file
            f.write("\n# Python Files Content\n")
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Again, ignore hidden directories and venv
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 'venv' not in d]

                for filename in filenames:
                    if filename.endswith('.py'):
                        file_path = os.path.join(dirpath, filename)
                        # Use a relative path for cleaner output
                        relative_path = os.path.relpath(file_path, root_dir)
                        
                        f.write(f"\n---\n\n")
                        f.write(f"### `{relative_path}`\n\n")
                        f.write("```python\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as py_file:
                                content = py_file.read()
                                # Prevent empty file content from breaking markdown
                                if not content.strip():
                                    f.write("# This file is empty.\n")
                                else:
                                    f.write(content)
                        except Exception as e:
                            f.write(f"# Error reading file: {e}")
                        f.write("\n```\n")
        
        print(f"Successfully generated '{output_file}' in the current directory.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    # Run the function in the current directory where the script is executed
    current_directory = os.getcwd()
    generate_file_structure_md(current_directory)
```

---

### `check_db_data.py`

```python
# check_db_data.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.future import select

# We need to import the settings and models from your application
from config import settings
from app.models import RunLog, DetectionEventLog, Base

# Use the exact same database URL as your main application
DATABASE_URL = settings.DATABASE.URL

# Set up the database connection
engine = create_async_engine(DATABASE_URL)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def check_data():
    """
    Connects to the database and prints the contents of the RunLog
    and DetectionEventLog tables.
    """
    print(f"--- Connecting to database: {DATABASE_URL} ---")
    
    async with AsyncSessionFactory() as session:
        # Check the RunLog table
        print("\n--- Checking 'run_logs' Table ---")
        run_log_query = select(RunLog).order_by(RunLog.start_timestamp.desc())
        run_log_result = await session.execute(run_log_query)
        all_runs = run_log_result.scalars().all()

        if not all_runs:
            print("RESULT: The 'run_logs' table is EMPTY.")
        else:
            print(f"RESULT: Found {len(all_runs)} records in 'run_logs' table:")
            for run in all_runs:
                print(
                    f"  - ID: {run.id}, "
                    f"Batch: {run.batch_code}, "
                    f"Status: {run.status.name}, "
                    f"Start: {run.start_timestamp.isoformat()}, "
                    f"End: {run.end_timestamp.isoformat() if run.end_timestamp else 'N/A'}"
                )

        # Check the DetectionEventLog table
        print("\n--- Checking 'detection_event_logs' Table ---")
        detection_log_query = select(DetectionEventLog).order_by(DetectionEventLog.timestamp.desc())
        detection_log_result = await session.execute(detection_log_query)
        all_detections = detection_log_result.scalars().all()

        if not all_detections:
            print("RESULT: The 'detection_event_logs' table is EMPTY.")
        else:
            print(f"RESULT: Found {len(all_detections)} records in 'detection_event_logs' table:")
            for detection in all_detections:
                print(
                    f"  - ID: {detection.id}, "
                    f"Run ID: {detection.run_log_id}, "
                    f"Timestamp: {detection.timestamp.isoformat()}, "
                    f"Image: {detection.image_path}"
                )

    await engine.dispose()
    print("\n--- Check complete ---")

if __name__ == "__main__":
    asyncio.run(check_data())
```

---

### `main.py`

```python
import asyncio
from contextlib import asynccontextmanager
import json
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import redis.asyncio as redis

# --- Core Application Imports ---
PROJECT_ROOT = Path(__file__).parent
from config import settings, ACTIVE_CAMERA_IDS
from app.models.database import engine, Base, AsyncSessionFactory

# --- Routers ---
from app.api.v1 import api_router as api_v1_router
from app.api.v1 import ai_strategy as ai_strategy_router
from app.web.router import router as web_router
from app.websocket.router import router as websocket_router
if settings.APP_ENV == "development":
    from app.api.v1 import debug as debug_router

# --- Middleware & Managers ---
from app.middleware.metrics_middleware import MetricsMiddleware
from app.websocket.connection_manager import manager as websocket_manager

# --- Core Hardware & System Components ---
from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.modbus_poller import AsyncModbusPoller

# --- Application Services ---
from app.services.detection_service import AsyncDetectionService
from app.services.system_service import AsyncSystemService
from app.services.notification_service import AsyncNotificationService
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.audio_service import AsyncAudioService, TTS_CACHE_DIR
from app.services.llm_service import LlmApiService
from app.services.tts_service import TtsApiService


class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"--- Application starting up in {settings.APP_ENV} mode... ---")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified.")
    
    app.state.redis_client = redis.from_url(f"redis://{settings.REDIS.HOST}:{settings.REDIS.PORT}")

    # Instantiate services
    app.state.llm_service = LlmApiService()
    app.state.tts_service = TtsApiService()
    app.state.audio_service = AsyncAudioService(db_session_factory=AsyncSessionFactory, tts_service=app.state.tts_service)
    app.state.modbus_controller = await AsyncModbusController.get_instance()
    
    # --- THIS IS THE FIX (Part 1): Connect to Modbus on startup ---
    await app.state.modbus_controller.connect()
    # --- END OF FIX ---

    app.state.orchestration_service = AsyncOrchestrationService(
        modbus_controller=app.state.modbus_controller, db_session_factory=AsyncSessionFactory,
        redis_client=app.state.redis_client, app_settings=settings,
        audio_service=app.state.audio_service, llm_service=app.state.llm_service
    )
    app.state.notification_service = AsyncNotificationService(db_session_factory=AsyncSessionFactory)
    app.state.camera_manager = AsyncCameraManager(
        notification_service=app.state.notification_service, captures_dir=settings.CAMERA_CAPTURES_DIR,
        redis_client=app.state.redis_client, active_camera_ids=ACTIVE_CAMERA_IDS
    )
    app.state.detection_service = AsyncDetectionService(
        modbus_controller=app.state.modbus_controller, camera_manager=app.state.camera_manager,
        orchestration_service=app.state.orchestration_service, redis_client=app.state.redis_client,
        conveyor_settings=settings.CONVEYOR, db_session_factory=AsyncSessionFactory,
        active_camera_ids=ACTIVE_CAMERA_IDS, audio_service=app.state.audio_service,
        llm_service=app.state.llm_service
    )
    app.state.modbus_poller = AsyncModbusPoller(
        modbus_controller=app.state.modbus_controller,
        event_callback=app.state.detection_service.handle_sensor_event,
        sensor_config=settings.SENSORS
    )
    app.state.system_service = AsyncSystemService(
        modbus_controller=app.state.modbus_controller, modbus_poller=app.state.modbus_poller,
        camera_manager=app.state.camera_manager, detection_service=app.state.detection_service,
        orchestration_service=app.state.orchestration_service, llm_service=app.state.llm_service,
        tts_service=app.state.tts_service, settings=settings
    )
    
    app.state.orchestration_service.set_detection_service(app.state.detection_service)

    startup_audio_path = TTS_CACHE_DIR / "startup_complete.wav"
    if not startup_audio_path.exists():
        print("First run detected: Pre-generating startup audio...")
        await app.state.audio_service.pre_generate_and_cache_alert("startup_complete", "System startup complete.")
    
    await app.state.orchestration_service.initialize_hardware_state()
    app.state.active_camera_ids = ACTIVE_CAMERA_IDS

    app.state.notification_service.start()
    app.state.modbus_poller.start()
    app.state.camera_manager.start()
    app.state.orchestration_service.start_background_tasks()

    async def broadcast_updates():
        while True:
            try:
                system_status = await app.state.system_service.get_system_status()
                orchestration_status = app.state.orchestration_service.get_status()
                full_status_payload = { "system": system_status, "orchestration": orchestration_status }
                await websocket_manager.broadcast_json({"type": "full_status", "data": full_status_payload})
                await asyncio.sleep(0.5)
            except asyncio.CancelledError: break
            except Exception as e:
                print(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    async def qc_image_broadcaster():
        pubsub = app.state.redis_client.pubsub()
        await pubsub.subscribe("qc_annotated_image:new")
        print("QC Image Broadcaster: Subscribed to Redis channel.")
        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=None)
                if message and message.get("type") == "message":
                    payload_str = message['data'].decode('utf-8')
                    image_data = json.loads(payload_str)
                    payload = {"type": "qc_update", "data": image_data}
                    await websocket_manager.broadcast_json(payload)
            except asyncio.CancelledError: break
            except Exception as e:
                print(f"Error in QC Image Broadcaster loop: {e}")
                await asyncio.sleep(5)

    app.state.broadcast_task = asyncio.create_task(broadcast_updates())
    app.state.qc_broadcast_task = asyncio.create_task(qc_image_broadcaster())
    
    await app.state.notification_service.send_alert("INFO", "Application startup complete.")
    await app.state.audio_service.play_event_from_cache("startup_complete")
    print("--- Application startup complete. Server is online. ---")

    yield

    # --- Shutdown Sequence ---
    print("--- Application shutting down... ---")
    if 'broadcast_task' in app.state and app.state.broadcast_task: app.state.broadcast_task.cancel()
    if 'qc_broadcast_task' in app.state and app.state.qc_broadcast_task: app.state.qc_broadcast_task.cancel()
    
    app.state.orchestration_service.stop_background_tasks()
    await app.state.modbus_poller.stop()
    app.state.notification_service.stop()
    await app.state.camera_manager.stop()
    await app.state.modbus_controller.disconnect()
    await app.state.redis_client.close()
    await engine.dispose()
    print("--- Application shutdown complete. ---")

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.mount("/static", NoCacheStaticFiles(directory=PROJECT_ROOT / "web/static"), name="static")
    app.mount("/captures", NoCacheStaticFiles(directory=PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR), name="captures")
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(ai_strategy_router.router, prefix="/api/v1/ai-strategy", tags=["AI & Audio Strategy"])
    app.include_router(web_router)
    app.include_router(websocket_router)
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
    app.state.templates = Jinja2Templates(directory=str(PROJECT_ROOT / "web/templates"))
    return app

app = create_app()
```

---

### `app/__init__.py`

```python
# This file is empty.

```

---

### `app/websocket/__init__.py`

```python
# This file is empty.

```

---

### `app/websocket/connection_manager.py`

```python
"""
Manages all active WebSocket connections.
This file is already correct, but provided for completeness.
"""
import asyncio
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts a new websocket connection and adds it to the active list."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a websocket connection from the active list."""
        self.active_connections.remove(websocket)

    async def broadcast_json(self, data: dict):
        """Broadcasts a JSON message to all connected clients concurrently."""
        if not self.active_connections:
            return

        # Create a list of tasks for sending messages
        tasks = [conn.send_json(data) for conn in self.active_connections]
        
        # gather waits for all tasks to complete. return_exceptions=True prevents
        # one failed send from crashing the entire broadcast loop.
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Optional: Log any errors that occurred during broadcast
        for result in results:
            if isinstance(result, Exception):
                print(f"Error broadcasting websocket message: {result}")

# A single, shared instance for the entire application
manager = ConnectionManager()
```

---

### `app/websocket/router.py`

```python
"""
Defines the WebSocket endpoint.
REVISED: The entire connection lifecycle is now wrapped in a single
try/finally block. This is a more robust pattern that guarantees
the disconnect logic is always called, even if an error occurs
immediately after connection. This resolves the handshake error.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # The fix is to handle the connection and disconnection in a try/finally block.
    await manager.connect(websocket)
    try:
        # This loop keeps the connection open.
        # It waits for the client to send a message (which we don't use)
        # or for the connection to be closed by the client or server.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # This block is executed when the client's browser closes the connection.
        print("A client disconnected cleanly.")
    except Exception as e:
        # This can catch other unexpected errors.
        print(f"An unexpected error occurred in the websocket connection: {e}")
    finally:
        # This block is GUARANTEED to run, whether the disconnect was
        # clean or caused by an error. This prevents stale connections.
        manager.disconnect(websocket)
        print("Connection resources cleaned up.")
```

---

### `app/api/v1/__init__.py`

```python
from fastapi import APIRouter

# Import the MODULES where the routers are defined.
from . import system
from . import detection
from . import outputs
from . import camera
from . import profiles
from . import orchestration
from . import products
from . import operators
from . import run_history
from . import reports
from . import analytics
from . import ai_strategy

# Create the main router for the v1 API.
api_router = APIRouter()

# Include the `router` OBJECT from each of the imported modules.
api_router.include_router(system.router, prefix="/system", tags=["System & Monitoring"])
api_router.include_router(detection.router, prefix="/detection", tags=["Box Detection"])
api_router.include_router(outputs.router, prefix="/outputs", tags=["Hardware Control"])
api_router.include_router(camera.router, prefix="/camera", tags=["Camera"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profile Management"])
api_router.include_router(orchestration.router, prefix="/orchestration", tags=["Run Orchestration"])
api_router.include_router(products.router, prefix="/products", tags=["Product Master"])
api_router.include_router(operators.router, prefix="/operators", tags=["Operator Master"])
api_router.include_router(run_history.router, prefix="/run-history", tags=["Run History"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(ai_strategy.router, prefix="/ai-strategy", tags=["AI & Audio Strategy"])
```

---

### `app/api/v1/operators.py`

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, Operator
from app.schemas.operators import OperatorCreate, OperatorUpdate, OperatorOut

router = APIRouter()

@router.post("/", status_code=201, response_model=OperatorOut)
async def create_operator(
    operator_in: OperatorCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new operator."""
    result = await db.execute(select(Operator).where(Operator.name == operator_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"An operator with name '{operator_in.name}' already exists.")
    
    new_operator = Operator(**operator_in.model_dump())
    db.add(new_operator)
    await db.commit()
    await db.refresh(new_operator)
    return new_operator

@router.get("/", response_model=List[OperatorOut])
async def get_all_operators(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all operators."""
    result = await db.execute(select(Operator).order_by(Operator.name))
    return result.scalars().all()

@router.get("/{operator_id}", response_model=OperatorOut)
async def get_operator(operator_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single operator by ID."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator

@router.put("/{operator_id}", response_model=OperatorOut)
async def update_operator(
    operator_id: int,
    operator_in: OperatorUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing operator."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    
    update_data = operator_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(operator, key, value)
        
    await db.commit()
    await db.refresh(operator)
    return operator

@router.delete("/{operator_id}", status_code=204)
async def delete_operator(operator_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete an operator."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
        
    await db.delete(operator)
    await db.commit()
    return None
```

---

### `app/api/v1/reports.py`

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

# --- THIS IS THE FIX ---
# The import is changed to the correct 'DetectionEventLog' model.
from app.models import get_async_session, RunLog, RunStatus, DetectionEventLog
# ---------------------

router = APIRouter()

@router.get("/summary")
async def get_production_summary(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None, description="Start date for the report query (ISO 8601)"),
    end_date: Optional[datetime] = Query(None, description="End date for the report query (ISO 8601)"),
):
    """
    Generates a high-level production summary report for a given date range.
    This calculates total runs, their statuses, and the total number of items detected.
    """
    # Base query to select RunLogs. We use selectinload to efficiently fetch
    # all related detection events in a single follow-up query, preventing the N+1 problem.
    query = select(RunLog).options(selectinload(RunLog.detection_events))

    # Apply date filters if provided
    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)

    result = await db.execute(query)
    runs = result.scalars().all()

    # Calculate statistics from the fetched runs
    total_runs = len(runs)
    total_detections = sum(len(run.detection_events) for run in runs)
    completed_runs = sum(1 for run in runs if run.status == RunStatus.COMPLETED)
    failed_runs = sum(1 for run in runs if run.status == RunStatus.FAILED)
    aborted_runs = sum(1 for run in runs if run.status == RunStatus.ABORTED)

    # Return a structured summary response
    return {
        "query_parameters": {
            "start_date": start_date.isoformat() if start_date else "Not specified",
            "end_date": end_date.isoformat() if end_date else "Not specified",
        },
        "summary": {
            "total_runs_in_period": total_runs,
            "completed_runs": completed_runs,
            "failed_runs": failed_runs,
            "aborted_runs": aborted_runs,
            "total_items_detected": total_detections,
        }
    }
```

---

### `app/api/v1/system.py`

```python
"""
This API router handles high-level system endpoints, including status checks,
version info, emergency stops, and the full system reset.

DEFINITIVE FIX: Removed all obsolete AI-related endpoints (/ai/source, /ai/toggle)
and their associated Pydantic models and dependencies.
"""
from fastapi import APIRouter, Depends, Request
from app.services.system_service import AsyncSystemService
# --- THIS IS THE FIX ---
# The import path is corrected to match your project's directory structure.
from app.api.v1.auth.dependencies import get_api_key, rate_limiter
# -----------------------
from config import settings # Import settings for version

router = APIRouter()

def get_system_service(request: Request) -> AsyncSystemService:
    return request.app.state.system_service

@router.get("/version")
async def get_version():
    """Returns the current running code version to verify updates."""
    return {"version": settings.PROJECT_VERSION}

@router.get("/status", dependencies=[Depends(rate_limiter)])
async def get_system_status(service: AsyncSystemService = Depends(get_system_service)):
    """Get overall system health status."""
    return await service.get_system_status()

@router.post("/reset-all", status_code=200)
async def reset_all_state(service: AsyncSystemService = Depends(get_system_service)):
    """Resets all counters and stops all hardware. A full system state reset."""
    await service.full_system_reset()
    return {"message": "System state has been fully reset."}

@router.post("/emergency-stop", status_code=200, dependencies=[Depends(get_api_key)])
async def emergency_stop(service: AsyncSystemService = Depends(get_system_service)):
    """Immediately stop all hardware operations. Requires API Key."""
    await service.emergency_stop()
    return {"message": "Emergency stop sequence initiated."}
```

---

### `app/api/v1/ai_strategy.py`

```python
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Configuration, ConfigDataType, get_async_session
from sqlalchemy.future import select
from sqlalchemy import delete
import asyncio
import logging

from config import settings
from app.services.audio_service import AsyncAudioService
from app.services.llm_service import LlmApiService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_audio_service(request: Request) -> AsyncAudioService: return request.app.state.audio_service
def get_llm_service(request: Request) -> LlmApiService: return request.app.state.llm_service

def _get_summary_from_llm_response(llm_response: Dict[str, Any]) -> str | None:
    try:
        return llm_response['analysis']['plain_text_summary']
    except (KeyError, TypeError):
        return None

# --- THIS IS THE FIX (Part 1): A single, complete dictionary for all tests ---
def _get_full_test_data() -> Dict[str, Any]:
    """Provides a comprehensive dictionary with all possible keys for template formatting."""
    return {
        "count": 123,
        "defects": "Test Defect",
        "batch_id": "TEST-001",
        "product_name": "Test Product",
        "total_items": 1000,
        "reject_count": 50,
        "countdown": 3,
        "qc_status": "REJECT",
        "type": "TEST_TYPE",
        "size": "Medium",
        "wait_time": 30,
        "top_defect": "Cosmetic Blemish"
    }
# --- END OF FIX ---

@router.get("/", response_model=Dict[str, Any])
async def get_ai_strategy(db: AsyncSession = Depends(get_async_session)):
    strategy = {}
    try:
        result = await db.execute(select(Configuration).where(Configuration.namespace == "ai_strategy"))
        for item in result.scalars().all():
            try:
                if item.data_type == ConfigDataType.BOOL: strategy[item.key] = item.value.lower() in ['true', '1', 't']
                elif item.data_type == ConfigDataType.INT: strategy[item.key] = int(item.value)
                elif item.data_type == ConfigDataType.FLOAT: strategy[item.key] = float(item.value)
                else: strategy[item.key] = item.value
            except (ValueError, TypeError): continue
        default_strategy = settings.AI_STRATEGY.model_dump()
        for key, value in default_strategy.items():
            if key not in strategy: strategy[key] = value
        return strategy
    except Exception: return settings.AI_STRATEGY.model_dump()

@router.post("/", status_code=200)
async def save_ai_strategy(strategy: Dict[str, Any], db: AsyncSession = Depends(get_async_session), audio_service: AsyncAudioService = Depends(get_audio_service)):
    if not strategy: raise HTTPException(status_code=400, detail="No strategy data provided")
    try:
        async with db.begin():
            await db.execute(delete(Configuration).where(Configuration.namespace == "ai_strategy"))
            default_strategy = settings.AI_STRATEGY.model_dump()
            template_keys = []
            for key, value in strategy.items():
                default_value = default_strategy.get(key)
                data_type = ConfigDataType.STRING
                if isinstance(default_value, bool): data_type = ConfigDataType.BOOL
                elif isinstance(default_value, int): data_type = ConfigDataType.INT
                elif isinstance(default_value, float): data_type = ConfigDataType.FLOAT
                db.add(Configuration(namespace="ai_strategy", key=key, value=str(value), data_type=data_type))
                if key.endswith("_TEMPLATE") and isinstance(value, str) and value.strip():
                    template_keys.append((key, value))
        if hasattr(audio_service, '_config_cache'): audio_service._config_cache.clear()
        for key, value in template_keys:
            asyncio.create_task(audio_service.pre_generate_and_cache_alert(key, value))
        return {"message": "AI & Audio strategy saved successfully."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save settings: {str(e)}")

@router.post("/test-audio")
async def test_audio_template(payload: Dict[str, str], audio_service: AsyncAudioService = Depends(get_audio_service)):
    template_key, text = payload.get("template_key"), payload.get("text")
    engine_override, tts_language = payload.get("engine"), payload.get("tts_language")
    
    # --- THIS IS THE FIX (Part 2): Correct Error Handling and Complete Test Data ---
    try:
        if not all([template_key, text, engine_override, tts_language]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        formatted_text = text.format(**_get_full_test_data())
        audio_bytes = await audio_service._tts_service.synthesize_speech(text=formatted_text, model=engine_override, language=tts_language)

        if not audio_bytes:
            raise HTTPException(status_code=500, detail="TTS service returned empty audio data")
        
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise # Re-raise FastAPI's exceptions directly
    except Exception as e:
        # Catches other errors like the KeyError
        raise HTTPException(status_code=500, detail=f"Failed to generate test audio: {str(e)}")
    # --- END OF FIX ---

@router.post("/test-item-pipeline", status_code=200)
async def test_item_pipeline(request: Request, llm_service: LlmApiService = Depends(get_llm_service), audio_service: AsyncAudioService = Depends(get_audio_service)):
    try:
        payload = await request.json()
        engine_override, llm_language, tts_language = payload.get("engine"), payload.get("llm_language"), payload.get("tts_language")
        if not all([engine_override, llm_language, tts_language]):
            raise HTTPException(status_code=400, detail="Missing required fields in pipeline test.")
        
        test_item_data = {"qc_summary": {"overall_status": "REJECTED_COSMETIC_BLEMISH"}}
        word_count = payload.get("word_count", settings.AI_STRATEGY.LLM_ITEM_WORD_COUNT)
        
        llm_response = await llm_service.analyze_item(item_data=test_item_data, language=llm_language, word_count=word_count)
        summary_text = _get_summary_from_llm_response(llm_response)
        
        if not summary_text: raise HTTPException(status_code=400, detail="LLM service failed to generate a valid item summary.")
        
        audio_bytes = await audio_service._tts_service.synthesize_speech(text=summary_text, model=engine_override, language=tts_language)
        
        if not audio_bytes: raise HTTPException(status_code=500, detail="TTS service failed to synthesize audio.")
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

@router.post("/test-summary-pipeline", status_code=200)
async def test_summary_pipeline(request: Request, llm_service: LlmApiService = Depends(get_llm_service), audio_service: AsyncAudioService = Depends(get_audio_service)):
    try:
        payload = await request.json()
        engine_override, llm_language, tts_language = payload.get("engine"), payload.get("llm_language"), payload.get("tts_language")
        if not all([engine_override, llm_language, tts_language]):
            raise HTTPException(status_code=400, detail="Missing required fields in pipeline test.")

        test_batch_data = [{"qc_summary": {"overall_status": "ACCEPTED"}}, {"qc_summary": {"overall_status": "REJECTED_MINOR_DEFECT"}}]
        word_count = payload.get("word_count", settings.AI_STRATEGY.LLM_SUMMARY_WORD_COUNT)
        model_pref = payload.get("model_preference", settings.AI_STRATEGY.SUMMARY_LLM_MODEL)
        
        llm_response = await llm_service.summarize_batch(batch_data=test_batch_data, language=llm_language, word_count=word_count, model_preference=model_pref)
        summary_text = _get_summary_from_llm_response(llm_response)
        
        if not summary_text: raise HTTPException(status_code=400, detail="LLM Service returned an invalid summary.")

        audio_bytes = await audio_service.generate_pipelined_summary_audio(summary_text, tts_language=tts_language, engine_override=engine_override)

        if not audio_bytes: raise HTTPException(status_code=500, detail="TTS service failed to generate summary audio.")
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### `app/api/v1/camera.py`

```python
# rpi_counter_fastapi-dev2/app/api/v1/camera.py

import os
import io
import zipfile
from datetime import datetime as dt_datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query, HTTPException, Path, Body
from fastapi.responses import StreamingResponse
import asyncio
import redis.asyncio as redis
from pydantic import BaseModel
import json

from app.core.camera_manager import AsyncCameraManager
from config import settings, ACTIVE_CAMERA_IDS
from pathlib import Path

router = APIRouter()
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis_client

class CameraPreviewSettings(BaseModel):
    exposure: Optional[int] = None
    gain: Optional[int] = None
    white_balance_temp: Optional[int] = None
    brightness: Optional[int] = None
    autofocus: Optional[bool] = None

@router.get("/status/{camera_id}")
async def get_camera_status(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    status = camera.get_health_status(camera_id)
    return {"camera_id": camera_id, "status": status.value}

@router.get("/stream/{camera_id}")
async def get_camera_stream(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    """Provides the live MJPEG stream for a given camera."""
    async def frame_generator():
        frame_queue = await camera.start_stream(camera_id)
        if not frame_queue:
            print(f"API ERROR: start_stream() for '{camera_id}' returned None. Cannot start stream.")
            return

        print(f"API INFO: Client connected to stream for '{camera_id}'. Waiting for the first frame...")
        try:
            # Wait for the first frame with a timeout
            first_frame = await asyncio.wait_for(frame_queue.get(), timeout=7.0)
            print(f"API INFO: First frame received for '{camera_id}'. Starting stream.")
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + first_frame + b'\r\n')

            # Continue with the rest of the frames
            while True:
                frame_bytes = await frame_queue.get()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except asyncio.TimeoutError:
            print(f"API WARNING: Timed out after 7s waiting for the first frame from camera '{camera_id}'. Closing stream. Is the camera service running and publishing to Redis?")
        except asyncio.CancelledError:
            print(f"API INFO: Client disconnected from '{camera_id}' stream.")
        except Exception as e:
            print(f"API ERROR: An unexpected error occurred in the frame generator for '{camera_id}': {e}")
        finally:
            print(f"API INFO: Cleaning up stream resources for '{camera_id}'.")
            await camera.stop_stream(camera_id, frame_queue)

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
    
@router.post("/preview_settings/{camera_id}", status_code=202)
async def apply_preview_settings(
    camera_id: str,
    settings_payload: CameraPreviewSettings,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    if camera_id not in ACTIVE_CAMERA_IDS:
        raise HTTPException(status_code=404, detail=f"Camera '{camera_id}' is not active or does not exist.")

    command = {
        "action": "apply_settings",
        "settings": settings_payload.model_dump(exclude_none=True)
    }
    
    command_bytes = json.dumps(command).encode('utf-8')
    channel = f"camera:commands:{camera_id}"
    await redis_client.publish(channel, command_bytes)
    
    return {"message": f"Preview settings applied to camera '{camera_id}'.", "settings": command["settings"]}

@router.get("/captures/{camera_id}")
async def get_captured_images(camera_id: str, page: int = Query(1, ge=1), page_size: int = Query(8, ge=1, le=100)):
    captures_dir = Path(settings.CAMERA_CAPTURES_DIR) / camera_id
    if not captures_dir.exists():
        return {"images": [], "has_more": False}
    try:
        image_files = sorted([p for p in captures_dir.glob("*.jpg")], key=lambda p: p.stat().st_mtime, reverse=True)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_files = image_files[start_index:end_index]
        has_more = len(image_files) > end_index
        web_paths = [f"/captures/{camera_id}/{p.name}" for p in paginated_files]
        return {"images": web_paths, "has_more": has_more}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ZipRequestPayload(BaseModel):
    camera_id: str
    start_date: date
    end_date: date

def create_zip_in_memory_sync(camera_id: str, start_date: date, end_date: date) -> io.BytesIO:
    captures_dir = PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR / camera_id
    if not captures_dir.is_dir():
        return None
    start_ts = dt_datetime.combine(start_date, dt_datetime.min.time()).timestamp()
    end_ts = dt_datetime.combine(end_date, dt_datetime.max.time()).timestamp()
    files_to_zip = [f for f in captures_dir.glob("*.jpg") if start_ts <= f.stat().st_mtime <= end_ts]
    zip_buffer = io.BytesIO()
    if not files_to_zip:
        return zip_buffer
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            zipf.write(file_path, arcname=file_path.name)
    zip_buffer.seek(0)
    return zip_buffer

@router.post("/captures/download-zip")
async def download_captures_as_zip(payload: ZipRequestPayload = Body(...)):
    zip_buffer = await asyncio.to_thread(
        create_zip_in_memory_sync, payload.camera_id, payload.start_date, payload.end_date
    )
    if zip_buffer is None:
        raise HTTPException(status_code=404, detail=f"Capture directory for camera '{payload.camera_id}' not found.")
    if not zip_buffer.getbuffer().nbytes > 0:
        raise HTTPException(status_code=404, detail="No images found in the specified date range.")
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=captures_{payload.camera_id}_{payload.start_date}_to_{payload.end_date}.zip"}
    )

@router.get("/ai_stream/{camera_id}")
async def get_ai_stream(camera_id: str, redis_client: redis.Redis = Depends(get_redis_client)):
    async def ai_frame_generator():
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"ai_stream:frames:{camera_id}")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10.0)
                if message and message.get("type") == "message":
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + message['data'] + b'\r\n')
        finally:
            await pubsub.close()
    return StreamingResponse(ai_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
```

---

### `app/api/v1/analytics.py`

```python
# rpi_counter_fastapi-apinaudio/app/api/v1/analytics.py

import asyncio
from fastapi import APIRouter, Depends, Query, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timedelta, time
import json
import io
import csv
import httpx
from pathlib import Path

from app.models import get_async_session, RunLog, DetectionEventLog, Product, Operator, RunStatus
from config import settings

router = APIRouter()

@router.post("/qc-test/upload")
async def handle_qc_test_upload(
    image: UploadFile = File(...),
    models: List[str] = Form(...)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    image_bytes = await image.read()
    
    async with httpx.AsyncClient(base_url=settings.AI_API.BASE_URL, timeout=20.0) as client:
        tasks = []
        for model_id in models:
            files = {"image": (image.filename, image_bytes, image.content_type)}
            data = {"model_id": model_id, "serial_no": "MANUAL_TEST"}
            task = client.post("/predict", files=files, data=data)
            tasks.append(task)
        
        try:
            responses = await asyncio.gather(*tasks)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Could not connect to the AI service: {e}")

    results = {}
    for response in responses:
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AI service returned an error: {response.text}"
            )
        data = response.json()
        model_id = data.get("model_id")
        results[model_id] = data

    return results

@router.get("/summary")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
):
    """
    Generates a comprehensive analytics report for a given date range with optional filters.
    """
    # --- THIS IS THE DEFINITIVE FIX ---
    # The incoming datetime objects are timezone-aware. The database stores them
    # as naive UTC. We must convert the incoming filters to naive UTC before querying.
    if start_date and start_date.tzinfo:
        start_date = start_date.replace(tzinfo=None)
    if end_date and end_date.tzinfo:
        end_date = end_date.replace(tzinfo=None)
    # --- END OF FIX ---

    query = select(RunLog).options(
        selectinload(RunLog.detection_events).selectinload(DetectionEventLog.run).selectinload(RunLog.product),
        selectinload(RunLog.product),
        selectinload(RunLog.operator)
    ).order_by(RunLog.start_timestamp.asc())

    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)
    if operator_id:
        query = query.where(RunLog.operator_id == operator_id)
    if product_id:
        query = query.where(RunLog.product_id == product_id)

    result = await db.execute(query)
    runs_in_period = result.scalars().unique().all()
    
    # This diagnostic print will now show the correct number of runs found.
    print(f"[Analytics API] Found {len(runs_in_period)} runs matching the query criteria.")
    
    detections_in_period = [event for run in runs_in_period for event in run.detection_events]
    
    total_runs = len(runs_in_period)
    completed_runs = sum(1 for r in runs_in_period if r.status == RunStatus.COMPLETED)
    failed_runs = sum(1 for r in runs_in_period if r.status == RunStatus.FAILED)
    aborted_runs = sum(1 for r in runs_in_period if r.status == RunStatus.ABORTED)
    total_items = len(detections_in_period)

    total_run_time_seconds = sum(
        (r.end_timestamp - r.start_timestamp).total_seconds() 
        for r in runs_in_period if r.end_timestamp and r.start_timestamp
    )
    
    availability = 0.0
    planned_downtime_sec = 0.0
    unplanned_downtime_sec = 0.0
    daily_trends = {}
    
    if start_date and end_date:
        total_period_seconds = (end_date - start_date).total_seconds()
        if total_period_seconds > 0:
            availability = (total_run_time_seconds / total_period_seconds) * 100
        
        for i in range(len(runs_in_period) - 1):
            current_run, next_run = runs_in_period[i], runs_in_period[i+1]
            if current_run.end_timestamp and next_run.start_timestamp:
                gap = (next_run.start_timestamp - current_run.end_timestamp).total_seconds()
                if gap > 0:
                    if current_run.status == RunStatus.COMPLETED:
                        planned_downtime_sec += gap
                    else:
                        unplanned_downtime_sec += gap
        
        try:
            delta = end_date.date() - start_date.date()
            for i in range(delta.days + 1):
                day = start_date.date() + timedelta(days=i)
                daily_trends[day.isoformat()] = {"items": 0, "pass": 0, "fail": 0, "pass_rate": 0}
        except Exception:
            pass

    performance = (total_items / (total_run_time_seconds / 3600)) if total_run_time_seconds > 0 else 0

    for det in detections_in_period:
        day_str = det.timestamp.date().isoformat()
        if day_str in daily_trends:
            daily_trends[day_str]["items"] += 1
            if det.details:
                qc_summary = det.details.get("qc_summary", {})
                if qc_summary.get("overall_status") == "ACCEPT":
                    daily_trends[day_str]["pass"] += 1
                elif "REJECT" in qc_summary.get("overall_status", ""):
                    daily_trends[day_str]["fail"] += 1

    for day, data in daily_trends.items():
        total_qc = data["pass"] + data["fail"]
        if total_qc > 0:
            daily_trends[day]["pass_rate"] = (data["pass"] / total_qc) * 100

    hourly_counts = {f"{h:02d}": 0 for h in range(24)}
    for detection in detections_in_period:
        hour = detection.timestamp.strftime('%H')
        hourly_counts[hour] += 1

    product_counts = {}
    for run in runs_in_period:
        if run.product:
            product_name = run.product.name
            product_counts[product_name] = product_counts.get(product_name, 0) + len(run.detection_events)
    
    top_products = sorted(product_counts.items(), key=lambda item: item[1], reverse=True)[:5]

    qc_pass, qc_fail, defect_counts = 0, 0, {}
    for detection in detections_in_period:
        if detection.details:
            qc_summary = detection.details.get("qc_summary", {})
            if qc_summary.get("overall_status") == "ACCEPT":
                qc_pass += 1
            elif "REJECT" in qc_summary.get("overall_status", ""):
                qc_fail += 1
            
            defects_summary = detection.details.get("defects_summary", {})
            for defect_type, count in defects_summary.get("defect_counts", {}).items():
                defect_counts[defect_type] = defect_counts.get(defect_type, 0) + count

    top_defects = sorted(defect_counts.items(), key=lambda item: item[1], reverse=True)[:5]
    
    return {
        "kpis": {
            "total_runs": total_runs, "completed_runs": completed_runs, "failed_runs": failed_runs,
            "aborted_runs": aborted_runs, "total_items_detected": total_items,
            "quality_pass_rate": (qc_pass / (qc_pass + qc_fail)) * 100 if (qc_pass + qc_fail) > 0 else 0,
        },
        "oee_lite": {
            "availability": availability,
            "performance_items_per_hour": performance,
        },
        "downtime": {
            "planned_changeover_hours": planned_downtime_sec / 3600,
            "unplanned_downtime_hours": unplanned_downtime_sec / 3600,
        },
        "daily_trends": daily_trends,
        "hourly_throughput": hourly_counts,
        "product_counts": product_counts,
        "top_5_products": top_products,
        "quality_control": { "pass_count": qc_pass, "fail_count": qc_fail, "top_5_defects": top_defects }
    }


@router.get("/export-csv")
async def export_analytics_csv(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
):
    if start_date and start_date.tzinfo:
        start_date = start_date.replace(tzinfo=None)
    if end_date and end_date.tzinfo:
        end_date = end_date.replace(tzinfo=None)

    query = (
        select(DetectionEventLog)
        .join(RunLog)
        .options(
            selectinload(DetectionEventLog.run).selectinload(RunLog.product),
            selectinload(DetectionEventLog.run).selectinload(RunLog.operator)
        )
        .order_by(DetectionEventLog.timestamp.desc())
    )
    if start_date: query = query.where(RunLog.start_timestamp >= start_date)
    if end_date: query = query.where(RunLog.start_timestamp <= end_date)
    if operator_id: query = query.where(RunLog.operator_id == operator_id)
    if product_id: query = query.where(RunLog.product_id == product_id)
    
    results = await db.execute(query)
    detections = results.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "DetectionTimestamp", "SerialNumber", "RunID", "BatchCode", "Operator", "Product",
        "QC_Status", "DetectedCategory", "DetectedSize", "DefectCount", "ImagePath"
    ])
    
    for det in detections:
        qc_summary = det.details.get("qc_summary", {}) if det.details else {}
        category_summary = det.details.get("category_summary", {}) if det.details else {}
        size_summary = det.details.get("size_summary", {}) if det.details else {}
        defects_summary = det.details.get("defects_summary", {}) if det.details else {}

        writer.writerow([
            det.timestamp.isoformat(), det.serial_number, det.run.id, det.run.batch_code,
            det.run.operator.name if det.run.operator else "N/A",
            det.run.product.name if det.run.product else "N/A",
            qc_summary.get("overall_status", "N/A"),
            category_summary.get("detected_type", "N/A"),
            size_summary.get("detected_size", "N/A"),
            defects_summary.get("total_defects", 0),
            det.image_path
        ])

    output.seek(0)
    
    filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

---

### `app/api/v1/profiles.py`

```python
"""
NEW: API endpoints for managing Camera and Object profiles.

This provides the full CRUD (Create, Read, Update, Delete) functionality
required for a UI to manage production "recipes" dynamically without
restarting the application.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, CameraProfile, ObjectProfile, Product
from app.schemas.profiles import (
    CameraProfileCreate, CameraProfileUpdate, CameraProfileOut,
    ObjectProfileCreate, ObjectProfileUpdate, ObjectProfileOut
)

router = APIRouter()

# --- Camera Profile Endpoints ---

@router.post("/camera", status_code=201, response_model=CameraProfileOut)
async def create_camera_profile(
    profile_in: CameraProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new camera profile."""
    # Check if a profile with the same name already exists
    result = await db.execute(select(CameraProfile).where(CameraProfile.name == profile_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"A camera profile with the name '{profile_in.name}' already exists."
        )
    
    new_profile = CameraProfile(**profile_in.model_dump())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile

@router.get("/camera", response_model=List[CameraProfileOut])
async def get_all_camera_profiles(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all camera profiles."""
    result = await db.execute(select(CameraProfile).order_by(CameraProfile.name))
    return result.scalars().all()

@router.get("/camera/{profile_id}", response_model=CameraProfileOut)
async def get_camera_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single camera profile by its ID."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    return profile

@router.put("/camera/{profile_id}", response_model=CameraProfileOut)
async def update_camera_profile(
    profile_id: int,
    profile_in: CameraProfileUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing camera profile."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    
    update_data = profile_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
        
    await db.commit()
    await db.refresh(profile)
    return profile

@router.delete("/camera/{profile_id}", status_code=204)
async def delete_camera_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete a camera profile."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    
    # Check if any ObjectProfile is using this CameraProfile
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.camera_profile_id == profile_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this camera profile. It is currently in use by one or more object profiles."
        )

    await db.delete(profile)
    await db.commit()
    return None

# --- Object Profile Endpoints ---

@router.post("/object", status_code=201, response_model=ObjectProfileOut)
async def create_object_profile(
    profile_in: ObjectProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new object profile."""
    # Check if an object profile with the same name already exists
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.name == profile_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"An object profile with the name '{profile_in.name}' already exists."
        )
    
    # --- PHASE 1: Validate that the product_id exists if provided ---
    if profile_in.product_id:
        product = await db.get(Product, profile_in.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {profile_in.product_id} not found.")

    new_profile = ObjectProfile(**profile_in.model_dump())
    db.add(new_profile)
    await db.commit()
    # We need to load the relationships to return them in the response
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == new_profile.id)
    )
    return result.scalar_one()


@router.get("/object", response_model=List[ObjectProfileOut])
async def get_all_object_profiles(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all object profiles, including their linked camera and product profiles."""
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .order_by(ObjectProfile.name)
    )
    return result.scalars().all()

@router.get("/object/{profile_id}", response_model=ObjectProfileOut)
async def get_object_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single object profile by ID."""
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
    return profile

@router.put("/object/{profile_id}", response_model=ObjectProfileOut)
async def update_object_profile(
    profile_id: int,
    profile_in: ObjectProfileUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing object profile."""
    # Use selectinload to fetch the profile and its related camera_profile in one go
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
        
    update_data = profile_in.model_dump(exclude_unset=True)

    # --- PHASE 1: Validate that the product_id exists if provided ---
    if "product_id" in update_data and update_data["product_id"]:
         product = await db.get(Product, update_data["product_id"])
         if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {update_data['product_id']} not found.")

    for key, value in update_data.items():
        setattr(profile, key, value)
        
    await db.commit()
    # Refresh to ensure all data, including relationships, is up to date
    await db.refresh(profile, attribute_names=['product']) # Eagerly refresh the product relationship
    await db.refresh(profile)
    return profile

@router.delete("/object/{profile_id}", status_code=204)
async def delete_object_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete an object profile."""
    profile = await db.get(ObjectProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
        
    await db.delete(profile)
    await db.commit()
    return None
```

---

### `app/api/v1/products.py`

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, Product, ObjectProfile
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()

@router.post("/", status_code=201, response_model=ProductOut)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new product."""
    result = await db.execute(select(Product).where(Product.name == product_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"A product with name '{product_in.name}' already exists.")
    
    new_product = Product(**product_in.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductOut])
async def get_all_products(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all products."""
    result = await db.execute(select(Product).order_by(Product.name))
    return result.scalars().all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single product by its ID."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing product."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete a product."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.product_id == product_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this product. It is currently in use by one or more object profiles."
        )
        
    await db.delete(product)
    await db.commit()
    return None
```

---

### `app/api/v1/outputs.py`

```python
"""
NEW: API endpoints for manually controlling hardware outputs via Modbus.
This replaces the old GPIO control API, preserving the manual toggle feature.
"""
from fastapi import APIRouter, Depends, Request, HTTPException, Path
from typing import Literal

from app.core.modbus_controller import AsyncModbusController

# This is the router for THIS FILE ONLY. It is self-contained.
# It does not know about any other router.
router = APIRouter()

def get_modbus_controller(request: Request) -> AsyncModbusController:
    return request.app.state.modbus_controller

# --- THIS IS THE FIX: ADD THE SECOND CAMERA LIGHT ---
# Define the literal types for valid output names from settings
OutputPinName = Literal["conveyor", "gate", "diverter", "led_green", "led_red", "buzzer", "camera_light", "camera_light_two"]
# --- END OF FIX ---

@router.post("/toggle/{name}", status_code=200)
async def toggle_output_by_name(
    name: OutputPinName = Path(...),
    io: AsyncModbusController = Depends(get_modbus_controller)
):
    """
    Toggles the state of any configured output coil (Relay, LED, Buzzer).
    Returns the new state ('ON' or 'OFF').
    """
    output_name_str = name

    address = io.get_output_address(output_name_str)
    if address is None:
        raise HTTPException(status_code=404, detail=f"Output name '{output_name_str}' not found in configuration.")

    all_coils = await io.read_coils()
    if all_coils is None:
        raise HTTPException(status_code=503, detail="Could not read current coil states from Modbus device.")

    if address >= len(all_coils):
         raise HTTPException(status_code=500, detail=f"Address {address} for '{output_name_str}' is out of bounds for the reported coils.")

    current_state = all_coils[address]
    
    # --- THIS IS THE FIX: Invert logic for NC-wired lights ---
    # For the camera lights, the logic is inverted. The UI sends a command to achieve a logical state (e.g., "turn ON").
    # If the light is ON, its relay coil is actually OFF (False). To turn it ON, we need to set the coil to OFF.
    # However, the toggle endpoint is simpler: it just flips the current state. The UI state will be corrected
    # by the `system_service` reporting the correct logical state.
    new_state = not current_state
    # --- END OF FIX ---

    success = await io.write_coil(address, new_state)
    if not success:
        raise HTTPException(status_code=503, detail="Failed to write new coil state to Modbus device.")
        
    # For NC lights, the new logical state is the inverse of the coil's new physical state.
    if name in ["camera_light", "camera_light_two"]:
        final_logical_state = not new_state
    else:
        final_logical_state = new_state

    return {"output": output_name_str, "new_state": "ON" if final_logical_state else "OFF"}
```

---

### `app/api/v1/debug.py`

```python
"""
Debug endpoints for testing purposes.
This router should only be mounted in a 'development' environment.
"""
from fastapi import APIRouter, Depends, Request, HTTPException, Body
from app.services.detection_service import AsyncDetectionService
from app.core.sensor_events import SensorEvent, SensorState

router = APIRouter()

def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.post("/sensor-event")
async def trigger_sensor_event(
    service: AsyncDetectionService = Depends(get_detection_service),
    sensor_id: int = Body(..., embed=True),
    new_state: SensorState = Body(..., embed=True)
):
    """
    Manually triggers a sensor event to test the detection state machine.
    This provides a 'backdoor' for end-to-end testing without physical hardware.
    
    Example Body:
    {
        "sensor_id": 1,
        "new_state": "triggered"
    }
    """
    print(f"DEBUG: Manually triggering event: Sensor {sensor_id} -> {new_state.name}")
    event = SensorEvent(sensor_id=sensor_id, new_state=new_state)
    await service.handle_sensor_event(event)
    return {"message": "Debug sensor event triggered successfully.", "new_state": service._state.name}

```

---

### `app/api/v1/detection.py`

```python
from fastapi import APIRouter, Depends, Request, HTTPException
from app.services.orchestration_service import AsyncOrchestrationService # MODIFIED
from app.services.detection_service import AsyncDetectionService

router = APIRouter()

# MODIFIED: Dependency changed to OrchestrationService
def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    return request.app.state.orchestration_service
    
def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.get("/")
async def get_detection_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)): # MODIFIED
    """Get current detection status and counts."""
    # MODIFIED: Get status from the correct service
    status = service.get_status()
    return {
        "counts": {
            "processed": status["run_progress"],
            "target": status["target_count"]
        },
        "state": status["mode"]
    }

@router.post("/reset", status_code=200)
async def reset_counter(service: AsyncDetectionService = Depends(get_detection_service)):
    """Reset the box counter to zero."""
    # This part of the original code had an error. There is no `reset_counter`
    # on the detection service. We will call the orchestration service stop method
    # which performs a full reset of the counts.
    orchestration_service = get_orchestration_service(service._orchestration)
    await orchestration_service.stop_run()
    return {"message": "Counter and run state reset successfully."}
```

---

### `app/api/v1/run_history.py`

```python
# rpi_counter_fastapi-dev2/app/api/v1/run_history.py

import io
import zipfile
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Path as FastApiPath
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
import asyncio

from app.models import get_async_session, RunLog, DetectionEventLog
from app.schemas.run_log import RunLogOut, DetectionEventLogOut
from config import settings

router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

@router.get("/", response_model=List[RunLogOut])
async def get_run_history(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None, description="ISO 8601 format: YYYY-MM-DDTHH:MM:SS"),
    end_date: Optional[datetime] = Query(None, description="ISO 8601 format: YYYY-MM-DDTHH:MM:SS"),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
    batch_code: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Retrieve historical run logs with detailed, aggregated data for reporting.
    """
    # Base query now efficiently counts detection events at the database level
    # to prevent loading all events into memory, which is crucial for performance.
    query = (
        select(
            RunLog,
            func.count(DetectionEventLog.id).label("detection_count")
        )
        .outerjoin(DetectionEventLog, RunLog.id == DetectionEventLog.run_log_id)
        .options(
            selectinload(RunLog.operator), 
            selectinload(RunLog.product)
        )
        .group_by(RunLog.id) # Group by the RunLog to count events per run
        .order_by(RunLog.start_timestamp.desc())
    )

    # Apply filters based on query parameters
    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)
    if operator_id:
        query = query.where(RunLog.operator_id == operator_id)
    if product_id:
        query = query.where(RunLog.product_id == product_id)
    if batch_code:
        query = query.where(RunLog.batch_code.ilike(f"%{batch_code}%"))

    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    
    # Manually construct the detailed response objects to include calculated fields
    detailed_runs = []
    for run_log, detection_count in result.all():
        duration = None
        if run_log.start_timestamp and run_log.end_timestamp:
            duration = int((run_log.end_timestamp - run_log.start_timestamp).total_seconds())

        # Use the Pydantic model to validate and structure the base data from the ORM object
        run_out = RunLogOut.model_validate(run_log)
        
        # Add the newly calculated/aggregated fields to the response object
        run_out.detected_items_count = detection_count
        run_out.duration_seconds = duration
        
        detailed_runs.append(run_out)
        
    return detailed_runs

@router.get("/{run_id}/detections", response_model=List[DetectionEventLogOut])
async def get_run_detection_events(
    run_id: int = FastApiPath(..., description="The ID of the run log"),
    db: AsyncSession = Depends(get_async_session)
):
    """Retrieve all detection events (including image paths) for a single run."""
    result = await db.execute(
        select(DetectionEventLog)
        .where(DetectionEventLog.run_log_id == run_id)
        .order_by(DetectionEventLog.timestamp.asc())
    )
    return result.scalars().all()

def create_zip_from_paths_sync(image_web_paths: List[str]) -> io.BytesIO:
    """Synchronously creates a ZIP archive from a list of web paths."""
    captures_base_dir = PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR
    
    files_to_zip = []
    for web_path in image_web_paths:
        if not web_path: continue
        # Convert web path (/captures/cam_id/file.jpg) to a full system path
        relative_path = web_path.lstrip('/').lstrip('captures').lstrip('/')
        full_path = captures_base_dir / relative_path
        if full_path.exists():
            files_to_zip.append(full_path)

    zip_buffer = io.BytesIO()
    if not files_to_zip:
        return zip_buffer

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            # Add file to zip using its name, not the full path
            zipf.write(file_path, arcname=file_path.name)
    
    zip_buffer.seek(0)
    return zip_buffer

@router.get("/{run_id}/download-images")
async def download_run_images_zip(
    run_id: int = FastApiPath(..., description="The ID of the run log to download images from"),
    db: AsyncSession = Depends(get_async_session)
):
    """Downloads all captured images for a specific run as a single ZIP file."""
    run_log = await db.get(RunLog, run_id)
    if not run_log:
        raise HTTPException(status_code=404, detail="Run not found.")

    # Get all image paths associated with this run
    result = await db.execute(
        select(DetectionEventLog.image_path)
        .where(DetectionEventLog.run_log_id == run_id)
    )
    image_paths = result.scalars().all()

    if not any(image_paths):
        raise HTTPException(status_code=404, detail="No images were logged for this run.")
    
    # Run the blocking ZIP creation in a separate thread to avoid blocking the server
    zip_buffer = await asyncio.to_thread(create_zip_from_paths_sync, image_paths)
    
    if not zip_buffer.getbuffer().nbytes > 0:
         raise HTTPException(status_code=404, detail="Images for this run were logged, but the files could not be found on disk.")

    filename = f"run_{run_id}_{run_log.batch_code}_images.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

---

### `app/api/v1/orchestration.py`

```python
"""
REVISED FOR PHASE 3: API endpoints for controlling the high-level
orchestration of production runs. Replaces the old "batch" system.
ADDED: Target count for production runs.
ADDED: Post-batch delay for pausing between runs.
REVISED: The /run/start endpoint is now the single atomic entry point for starting a new run.
PHASE 3: Payload updated to include batch_code and operator_id.
PHASE 4: Added endpoint to acknowledge alarms.
"""
from fastapi import APIRouter, Depends, Request, Body, HTTPException
from pydantic import BaseModel, Field

from app.services.orchestration_service import AsyncOrchestrationService

router = APIRouter()

def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    """Dependency to get the orchestration service instance."""
    return request.app.state.orchestration_service

class StartRunPayload(BaseModel):
    """Defines the request body for starting a run."""
    object_profile_id: int = Field(..., gt=0, description="The ID of the ObjectProfile to activate for the run.")
    target_count: int = Field(0, ge=0, description="The target number of items for this run. 0 means unlimited.")
    post_batch_delay_sec: int = Field(5, ge=0, description="The time in seconds to pause after the run completes.")
    batch_code: str = Field(..., min_length=1, description="The unique code for this production batch.")
    operator_id: int = Field(..., gt=0, description="The ID of the operator running the batch.")


@router.post("/run/start", status_code=202)
async def start_production_run(
    payload: StartRunPayload,
    service: AsyncOrchestrationService = Depends(get_orchestration_service)
):
    """
    Atomically loads the specified profile, logs the run, configures the camera, and starts the run.
    This is the single endpoint for initiating a production run.
    """
    success = await service.start_run(
        profile_id=payload.object_profile_id,
        target_count=payload.target_count,
        post_batch_delay_sec=payload.post_batch_delay_sec,
        batch_code=payload.batch_code,
        operator_id=payload.operator_id
    )
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to start run. ObjectProfile with ID {payload.object_profile_id} may not exist, the operator ID may be invalid, or the system is in an invalid state to start."
        )
    return {"message": "Production run started successfully."}

@router.post("/run/stop", status_code=202)
async def stop_production_run(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Stops the conveyor belt and unloads the active profile."""
    await service.stop_run()
    return {"message": "Production run stopped and profile unloaded."}

@router.get("/run/status")
async def get_run_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Gets the current status of the orchestration service."""
    return service.get_status()

# --- PHASE 4: New endpoint to acknowledge alarms ---
@router.post("/run/acknowledge-alarm", status_code=200)
async def acknowledge_run_alarm(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Acknowledges and clears the current active alarm."""
    await service.acknowledge_alarm()
    return {"message": "Alarm acknowledged successfully."}
```

---

### `app/api/v1/auth/__init__.py`

```python
# This file is empty.

```

---

### `app/api/v1/auth/security.py`

```python
"""
Security-related utility functions, such as password hashing.
"""
from passlib.context import CryptContext

# Use bcrypt for password hashing, a standard and secure choice.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

```

---

### `app/api/v1/auth/dependencies.py`

```python
"""
FastAPI dependencies for handling security aspects like API key auth and rate limiting.
"""
import time
from typing import Dict, List
from fastapi import Request, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

# --- API Key Authentication ---
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    """
    Dependency that verifies the X-API-Key header against the configured API_KEY.
    """
    if api_key == settings.SECURITY.API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

# --- Simple In-Memory Rate Limiting ---
rate_limit_db: Dict[str, List[float]] = {}
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_TIMEFRAME = 60

async def rate_limiter(request: Request):
    """
    Dependency that provides simple IP-based rate limiting.
    """
    client_ip = request.client.host
    current_time = time.monotonic()

    if client_ip not in rate_limit_db:
        rate_limit_db[client_ip] = []

    rate_limit_db[client_ip] = [
        t for t in rate_limit_db[client_ip] if t > current_time - RATE_LIMIT_TIMEFRAME
    ]

    if len(rate_limit_db[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Limit is {RATE_LIMIT_REQUESTS} per {RATE_LIMIT_TIMEFRAME} seconds.",
        )
    
    rate_limit_db[client_ip].append(current_time)
```

---

### `app/api/v1/auth/jwt_handler.py`

```python
"""
Functions for creating, encoding, and decoding JSON Web Tokens (JWTs).
"""
import time
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from config import settings

SECRET_KEY = settings.SECURITY.JWT_SECRET_KEY
ALGORITHM = settings.SECURITY.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes a JWT access token, returning the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # This could be due to an expired signature or invalid token
        return None

```

---

### `app/middleware/metrics_middleware.py`

```python
"""
FastAPI middleware to calculate and report request processing time.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.monotonic()
        response = await call_next(request)
        process_time = time.monotonic() - start_time
        response.headers["X-Process-Time-Seconds"] = str(process_time)
        print(f"Request {request.method} {request.url.path} processed in {process_time:.4f} seconds")
        return response

```

---

### `app/core/__init__.py`

```python
# This file is empty.

```

---

### `app/core/modbus_poller.py`

```python
"""
REVISED: Now acts as the Modbus Poller Service.
- It continuously polls BOTH the input and output modules.
- It maintains a complete, up-to-date state of all hardware I/O.
- It detects changes in inputs and fires sensor events.
- It correctly inverts the NPN sensor signal (LOW signal = TRIGGERED).

DEFINITIVE FIX: The poller now uses the injected sensor configuration to determine
which physical channels to monitor, instead of hardcoding a 1-to-1 mapping. This
makes the SENSORS_ENTRY_CHANNEL and SENSORS_EXIT_CHANNEL settings work correctly.
"""
import asyncio
from typing import Callable, Coroutine, Optional, List
from .modbus_controller import AsyncModbusController, ModbusHealthStatus
from .sensor_events import SensorState, SensorEvent
from config import settings

AsyncEventCallback = Callable[[SensorEvent], Coroutine[None, None, None]]

class AsyncModbusPoller:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        event_callback: AsyncEventCallback,
        sensor_config  # <-- ADDED: Inject the sensor settings object
    ):
        self.modbus_controller = modbus_controller
        self.event_callback = event_callback
        # --- ADDED: Store the sensor configuration ---
        self._sensor_config = sensor_config
        self.polling_interval_sec = settings.MODBUS.POLLING_MS / 1000.0
        self._monitoring_task: Optional[asyncio.Task] = None
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

        # Initialize all states to True (cleared for NPN sensors)
        self._input_channels: List[bool] = [True] * 4
        self._output_channels: List[bool] = [False] * 8
        self._last_known_entry_state: bool = True
        self._last_known_exit_state: bool = True
        self._health_status: ModbusHealthStatus = ModbusHealthStatus.DISCONNECTED

    def get_io_health(self) -> ModbusHealthStatus:
        return self._health_status

    def get_current_input_states(self) -> List[bool]:
        return self._input_channels

    def get_current_output_states(self) -> List[bool]:
        return self._output_channels

    def start(self):
        if self._monitoring_task and not self._monitoring_task.done():
            return
        print(f"Modbus Poller: Starting polling every {self.polling_interval_sec * 1000}ms.")
        print(f"   -> Monitoring Entry Sensor on Channel: {self._sensor_config.ENTRY_CHANNEL}")
        print(f"   -> Monitoring Exit Sensor on Channel:  {self._sensor_config.EXIT_CHANNEL}")
        self._monitoring_task = asyncio.create_task(self._poll_hardware())

    async def stop(self):
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass

    async def _poll_hardware(self):
        while True:
            raw_inputs = await self.modbus_controller.read_digital_inputs()
            raw_outputs = await self.modbus_controller.read_coils()

            if raw_inputs is not None:
                if self._health_status != ModbusHealthStatus.OK:
                    print("Modbus Poller: Re-established connection to IO modules.")
                self._health_status = ModbusHealthStatus.OK
                self._input_channels = raw_inputs
                
                # Update output channels if read was successful
                if raw_outputs is not None:
                    self._output_channels = raw_outputs

                # --- THE REWRITTEN LOGIC ---
                # Convert 1-based config channels to 0-based list indices
                entry_idx = self._sensor_config.ENTRY_CHANNEL - 1
                exit_idx = self._sensor_config.EXIT_CHANNEL - 1

                # Check Entry Sensor state if index is valid
                if 0 <= entry_idx < len(self._input_channels):
                    current_entry_state = self._input_channels[entry_idx]
                    if current_entry_state != self._last_known_entry_state:
                        is_triggered = not current_entry_state  # NPN Logic Inversion
                        if self._verbose:
                            print(f"[Sensor Event] Entry Sensor (Channel {entry_idx + 1}): Raw={current_entry_state} -> {'TRIGGERED' if is_triggered else 'CLEARED'}")
                        event = SensorEvent(
                            sensor_id=self._sensor_config.ENTRY_CHANNEL,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                        self._last_known_entry_state = current_entry_state

                # Check Exit Sensor state if index is valid
                if 0 <= exit_idx < len(self._input_channels):
                    current_exit_state = self._input_channels[exit_idx]
                    if current_exit_state != self._last_known_exit_state:
                        is_triggered = not current_exit_state  # NPN Logic Inversion
                        if self._verbose:
                            print(f"[Sensor Event] Exit Sensor (Channel {exit_idx + 1}): Raw={current_exit_state} -> {'TRIGGERED' if is_triggered else 'CLEARED'}")
                        event = SensorEvent(
                            sensor_id=self._sensor_config.EXIT_CHANNEL,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                        self._last_known_exit_state = current_exit_state
                # --- END OF REWRITTEN LOGIC ---
                
            else:
                if self._health_status == ModbusHealthStatus.OK:
                    print("Modbus Poller: Lost connection to IO modules.")
                self._health_status = self.modbus_controller.health_status
                
                # If connection is lost, force sensors to a 'cleared' state
                if not self._last_known_entry_state:
                    self._last_known_entry_state = True
                    event = SensorEvent(sensor_id=self._sensor_config.ENTRY_CHANNEL, new_state=SensorState.CLEARED)
                    asyncio.create_task(self.event_callback(event))

                if not self._last_known_exit_state:
                    self._last_known_exit_state = True
                    event = SensorEvent(sensor_id=self._sensor_config.EXIT_CHANNEL, new_state=SensorState.CLEARED)
                    asyncio.create_task(self.event_callback(event))

            await asyncio.sleep(self.polling_interval_sec)
```

---

### `app/core/camera_manager.py`

```python
# rpi_counter_fastapi-dev2/app/core/camera_manager.py

"""
REVISED: The `capture_and_save_image` method is now more robust.
- It now actively waits for up to 1 second for a new frame to arrive.
FIXED: The Redis listener is re-architected for better connection resilience,
which is critical for the stability of the live camera stream.
"""
import asyncio
import time
import redis.asyncio as redis
from enum import Enum
from typing import Optional, Dict, Set, List
import cv2
import numpy as np
from pathlib import Path

from redis import exceptions as redis_exceptions
from app.services.notification_service import AsyncNotificationService

class CameraHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncCameraManager:
    def __init__(
        self,
        notification_service: AsyncNotificationService,
        captures_dir: str,
        redis_client: redis.Redis,
        active_camera_ids: List[str]
    ):
        self.redis_client = redis_client
        self._notification_service = notification_service
        self._captures_dir_base = Path(captures_dir)
        self._active_camera_ids = active_camera_ids
        
        self._listener_tasks: Dict[str, asyncio.Task] = {}
        self._health_status: Dict[str, CameraHealthStatus] = {cam_id: CameraHealthStatus.DISCONNECTED for cam_id in self._active_camera_ids}
        self._frame_queues: Dict[str, asyncio.Queue] = {cam_id: asyncio.Queue(maxsize=5) for cam_id in self._active_camera_ids}
        self._stream_listeners: Dict[str, Set[asyncio.Queue]] = {cam_id: set() for cam_id in self._active_camera_ids}
        self._last_event_image_paths: Dict[str, Optional[str]] = {cam_id: None for cam_id in self._active_camera_ids}
        self._stream_lock = asyncio.Lock()

    def start(self):
        for cam_id in self._active_camera_ids:
            if cam_id not in self._listener_tasks or self._listener_tasks[cam_id].done():
                self._listener_tasks[cam_id] = asyncio.create_task(self._redis_listener(cam_id))

    async def stop(self):
        for task in self._listener_tasks.values():
            if task and not task.done():
                task.cancel()

    # --- THIS IS THE FIX ---
    # This listener logic is re-written to be more robust for a service that must
    # run forever and survive Redis connection drops.
    async def _redis_listener(self, cam_id: str):
        channel_name = f"camera:frames:{cam_id}"
        pubsub = self.redis_client.pubsub()

        async def listen_for_messages():
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
                if message:
                    if self._health_status[cam_id] != CameraHealthStatus.CONNECTED:
                        print(f"[Camera Manager] Re-established frame stream for '{cam_id}'.")
                    self._health_status[cam_id] = CameraHealthStatus.CONNECTED
                    frame_data = message['data']
                    
                    # Distribute frame to single-shot capture queue
                    while not self._frame_queues[cam_id].empty():
                        self._frame_queues[cam_id].get_nowait()
                    self._frame_queues[cam_id].put_nowait(frame_data)
                    
                    # Distribute frame to all active stream listeners (e.g., dashboard clients)
                    async with self._stream_lock:
                        # Make a copy of the set to prevent issues if it's modified while iterating
                        listeners = list(self._stream_listeners[cam_id])
                    
                    for queue in listeners:
                        if not queue.full():
                            try:
                                queue.put_nowait(frame_data)
                            except asyncio.QueueFull:
                                pass # It's okay if a slow client misses a frame
                else:
                    # Timeout occurred
                    if self._health_status.get(cam_id) == CameraHealthStatus.CONNECTED:
                        await self._notification_service.send_alert("WARNING", f"Camera '{cam_id}' has stopped publishing frames.")
                    self._health_status[cam_id] = CameraHealthStatus.DISCONNECTED
        
        # Main reconnection loop
        while True:
            try:
                await pubsub.subscribe(channel_name)
                print(f"[Camera Manager] Subscribed to Redis channel: {channel_name}")
                await listen_for_messages()
            except redis_exceptions.ConnectionError:
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                print(f"[Camera Manager] Redis connection lost for '{cam_id}'. Retrying in 5 seconds...")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                print(f"[Camera Manager] Listener for '{cam_id}' cancelled.")
                break
            except Exception as e:
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                print(f"[Camera Manager] Unexpected error in '{cam_id}' listener: {e}. Retrying in 10 seconds...")
                await asyncio.sleep(10)
        
        # Cleanup
        await pubsub.close()
    
    async def start_stream(self, cam_id: str) -> Optional[asyncio.Queue]:
        if cam_id not in self._active_camera_ids:
            return None
        q = asyncio.Queue(maxsize=2)
        async with self._stream_lock:
            self._stream_listeners[cam_id].add(q)
        print(f"[Camera Manager] New stream client connected for '{cam_id}'. Total listeners: {len(self._stream_listeners[cam_id])}")
        return q

    async def stop_stream(self, cam_id: str, queue: asyncio.Queue):
        if cam_id not in self._active_camera_ids: return
        async with self._stream_lock:
            self._stream_listeners[cam_id].discard(queue)
        print(f"[Camera Manager] Stream client disconnected for '{cam_id}'. Remaining listeners: {len(self._stream_listeners[cam_id])}")
        
    # ... (rest of the file is unchanged)
    async def capture_and_save_image(self, cam_id: str, filename_prefix: str) -> Optional[str]:
        if self._health_status.get(cam_id) != CameraHealthStatus.CONNECTED: return None
        try:
            jpeg_bytes = await asyncio.wait_for(self._frame_queues[cam_id].get(), timeout=1.0)
            self._frame_queues[cam_id].task_done()
            captures_dir = self._captures_dir_base / cam_id
            captures_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{filename_prefix}_{int(time.time())}.jpg"
            full_path = captures_dir / filename
            def save_image_sync():
                np_array = np.frombuffer(jpeg_bytes, np.uint8)
                img_decoded = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                if img_decoded is None: return None
                cv2.imwrite(str(full_path), img_decoded)
                return f"/captures/{cam_id}/{filename}"
            web_path = await asyncio.to_thread(save_image_sync)
            if web_path: self._last_event_image_paths[cam_id] = web_path
            return web_path
        except asyncio.TimeoutError: return None
        except Exception: return None

    def get_health_status(self, cam_id: str) -> CameraHealthStatus:
        return self._health_status.get(cam_id, CameraHealthStatus.DISCONNECTED)

    def get_all_health_statuses(self) -> Dict[str, str]:
        return {cam_id: status.value for cam_id, status in self._health_status.items()}

    def get_last_event_image_path(self, cam_id: str) -> Optional[str]:
        return self._last_event_image_paths.get(cam_id)
```

---

### `app/core/modbus_controller.py`

```python
import asyncio
from enum import Enum
from typing import Optional, List
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.framer import ModbusRtuFramer

from config import settings

class ModbusHealthStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    DISCONNECTED = "disconnected"

class AsyncModbusController:
    _instance: Optional['AsyncModbusController'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._config = settings.MODBUS
            self.client = AsyncModbusSerialClient(
                port=self._config.PORT, framer=ModbusRtuFramer,
                baudrate=self._config.BAUDRATE, bytesize=8, parity="N", stopbits=1,
                timeout=self._config.TIMEOUT_SEC,
            )
            self.initialized = True
            self.health_status = ModbusHealthStatus.DISCONNECTED
            self._is_connected = False
            self._output_name_to_address_map = {k.lower(): v for k, v in settings.OUTPUTS.model_dump().items()}
            print("--- Modbus Controller Initialized ---")
            print(f"    Loaded output map: {self._output_name_to_address_map}")

    @classmethod
    async def get_instance(cls) -> 'AsyncModbusController':
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def get_output_address(self, name: str) -> Optional[int]:
        return self._output_name_to_address_map.get(name.lower())

    async def connect(self) -> bool:
        if self._is_connected: return True
        try:
            is_connected = await self.client.connect()
            if is_connected:
                print("Modbus Controller: Successfully connected to serial port.")
                self.health_status = ModbusHealthStatus.OK
                self._is_connected = True
                return True
            else:
                print(f"Modbus Controller: Failed to connect to serial port {self._config.PORT}.")
                self.health_status = ModbusHealthStatus.DISCONNECTED
                self._is_connected = False
                return False
        except Exception as e:
            print(f"Modbus Controller: Error during connection attempt: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False
            return False

    async def disconnect(self):
        if self._is_connected:
            self.client.close()
            self._is_connected = False
            self.health_status = ModbusHealthStatus.DISCONNECTED
            print("Modbus Controller: Connection closed.")

    async def read_digital_inputs(self) -> Optional[List[bool]]:
        """Reads discrete inputs. Assumes connection is already established."""
        # --- THIS IS THE FIX: REMOVED connect() and disconnect() calls ---
        if not self._is_connected: return None
        try:
            result = await self.client.read_discrete_inputs(address=0, count=4, slave=self._config.DEVICE_ADDRESS_INPUTS)
            if result.isError(): raise ModbusIOException(f"Modbus error on input read: {result}")
            return result.bits[:4] if result.bits else [True] * 4
        except (ModbusIOException, ConnectionException) as e:
            print(f"Modbus read_digital_inputs failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False  # Mark connection as broken
            return None
        # --- END OF FIX ---

    async def read_coils(self) -> Optional[List[bool]]:
        """Reads coils. Assumes connection is already established."""
        # --- THIS IS THE FIX: REMOVED connect() and disconnect() calls ---
        if not self._is_connected: return None
        try:
            result = await self.client.read_coils(address=0, count=8, slave=self._config.DEVICE_ADDRESS_OUTPUTS)
            if result.isError(): raise ModbusIOException(f"Modbus error on coil read: {result}")
            return result.bits[:8] if result.bits else [False] * 8
        except (ModbusIOException, ConnectionException) as e:
            print(f"Modbus read_coils failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False # Mark connection as broken
            return None
        # --- END OF FIX ---

    async def write_coil(self, address: int, state: bool) -> bool:
        """Writes a single coil. Assumes connection is already established."""
        # --- THIS IS THE FIX: REMOVED connect() and disconnect() calls ---
        if not self._is_connected: return False
        try:
            result = await self.client.write_coil(address=address, value=state, slave=self._config.DEVICE_ADDRESS_OUTPUTS)
            if result.isError(): raise ModbusIOException(f"Modbus error on coil write: {result}")
            return True
        except (ModbusIOException, ConnectionException) as e:
            print(f"Modbus write_coil failed for address {address}: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False # Mark connection as broken
            return False
        # --- END OF FIX ---
```

---

### `app/core/system_orchestrator.py`

```python
"""
Conceptual System Orchestrator
In our current design, the FastAPI lifespan manager in `main.py` acts as the
primary orchestrator. This file serves as a conceptual model for how more complex,
multi-service workflows could be managed.
"""
import asyncio

from .gpio_controller import AsyncGPIOController
from .camera_manager import AsyncCameraManager
from app.services.detection_service import AsyncDetectionService
from app.services.notification_service import AsyncNotificationService

class SystemOrchestrator:
    """
    A high-level class to coordinate major system operations.
    """
    def __init__(
        self,
        gpio: AsyncGPIOController,
        camera: AsyncCameraManager,
        detection: AsyncDetectionService,
        notifier: AsyncNotificationService,
    ):
        self.gpio = gpio
        self.camera = camera
        self.detection = detection
        self.notifier = notifier

    async def run_full_diagnostic_sequence(self):
        """
        An example of a complex workflow that involves multiple services.
        """
        print("Orchestrator: Starting full system diagnostic...")
        await self.notifier.send_alert("INFO", "Starting system diagnostics.")
        
        # Step 1: Check hardware
        gpio_health = await self.gpio.health_check()
        camera_health = await self.camera.health_check()
        
        # Step 2: Test hardware functions
        await self.gpio.beep(0.1)
        await self.gpio.blink_led("led_green", 0.1, 0) # Quick flash
        
        # Step 3: Log results
        print(f"Diagnostics complete: GPIO={gpio_health.value}, Camera={camera_health.value}")
        await self.notifier.send_alert("INFO", "Diagnostics complete.", {
            "gpio": gpio_health.value,
            "camera": camera_health.value
        })

    async def perform_safe_shutdown(self):
        """
        An orchestrated shutdown sequence.
        """
        print("Orchestrator: Performing safe shutdown.")
        await self.notifier.send_alert("WARNING", "System is shutting down.")
        await self.gpio.stop_conveyor()
        await self.gpio.close_gate() # Assuming a gate exists
        await self.gpio.shutdown()
        await self.camera.stop_capture()

```

---

### `app/core/sensor_events.py`

```python
"""
Phase 2.2: Event Handling System for Sensors
Defines the data structures for sensor events using Pydantic for validation
and Enums for clear state representation.
"""
import time
from enum import Enum
from pydantic import BaseModel, Field

class SensorState(str, Enum):
    """Represents the state of a single sensor."""
    TRIGGERED = "triggered" # Object detected
    CLEARED = "cleared"   # No object detected

class SensorEvent(BaseModel):
    """Data model for a sensor state change event."""
    sensor_id: int
    new_state: SensorState
    timestamp: float = Field(default_factory=time.monotonic)

```

---

### `app/utils/__init__.py`

```python
# This file is empty.

```

---

### `app/utils/tokenizer.py`

```python
import tiktoken
from typing import List

# This encoding is a good general-purpose choice for modern models and multiple languages.
enc = tiktoken.get_encoding("cl100k_base")

def chunk_text_by_tokens(text: str, tokens_per_chunk: int) -> List[str]:
    """
    Splits a text string into a list of smaller strings, with each chunk
    containing approximately the specified number of tokens.

    Args:
        text: The input text to be split.
        tokens_per_chunk: The target number of tokens for each chunk.

    Returns:
        A list of text chunks.
    """
    if not text or tokens_per_chunk <= 0:
        return []

    # Encode the entire text into a list of token integers
    tokens = enc.encode(text)
    
    chunks = []
    # Iterate through the token list, creating slices of the desired size
    for i in range(0, len(tokens), tokens_per_chunk):
        chunk_tokens = tokens[i:i + tokens_per_chunk]
        # Decode the token slice back into a readable string
        chunks.append(enc.decode(chunk_tokens))
        
    return chunks
```

---

### `app/web/__init__.py`

```python
# This file is empty.

```

---

### `app/web/router.py`

```python
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path
import markdown2 
import json

from app.models import get_async_session, EventLog, ObjectProfile
from config import settings, ACTIVE_CAMERA_IDS

router = APIRouter(tags=["Web Dashboard"])
PROJECT_ROOT = Path(__file__).parent.parent.parent

def NoCacheTemplateResponse(request: Request, name: str, context: dict):
    templates = request.app.state.templates
    context['active_camera_ids'] = ACTIVE_CAMERA_IDS
    context['camera_profiles'] = getattr(request.app.state, 'camera_profiles', [])
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return templates.TemplateResponse(name, context, headers=headers)

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ObjectProfile).order_by(ObjectProfile.name))
    object_profiles = result.scalars().all()
    context = {"request": request, "object_profiles": object_profiles, "animation_time": settings.UI_ANIMATION_TRANSIT_TIME_SEC}
    return NoCacheTemplateResponse(request, "dashboard.html", context)

@router.get("/management/recipes", response_class=HTMLResponse)
async def read_profiles_page(request: Request):
    return NoCacheTemplateResponse(request, "profiles.html", {"request": request})

@router.get("/management/products", response_class=HTMLResponse)
async def read_products_page(request: Request):
    return NoCacheTemplateResponse(request, "products.html", {"request": request})

@router.get("/management/operators", response_class=HTMLResponse)
async def read_operators_page(request: Request):
    return NoCacheTemplateResponse(request, "operators.html", {"request": request})

@router.get("/settings/ai-strategy", response_class=HTMLResponse)
async def read_ai_strategy_page(request: Request):
    """Serves the AI & Audio Strategy settings page."""
    context = {"request": request}
    return NoCacheTemplateResponse(request, "ai_strategy.html", context)

@router.get("/status", response_class=HTMLResponse)
async def read_status_page(request: Request):
    return NoCacheTemplateResponse(request, "status.html", {"request": request})

@router.get("/hardware", response_class=HTMLResponse)
async def read_hardware_page(request: Request):
    return NoCacheTemplateResponse(request, "hardware.html", {"request": request, "config": settings})
    
@router.get("/run-history", response_class=HTMLResponse)
async def read_run_history_page(request: Request):
    return NoCacheTemplateResponse(request, "run_history.html", {"request": request})

@router.get("/qc-testing", response_class=HTMLResponse)
async def read_qc_testing_page(request: Request):
    return NoCacheTemplateResponse(request, "qc_testing.html", {"request": request})

@router.get("/help/{page_name}", response_class=HTMLResponse)
async def read_help_page(request: Request, page_name: str):
    if ".." in page_name or "/" in page_name:
        raise HTTPException(status_code=404, detail="Help page not found.")
    file_path = PROJECT_ROOT / "docs" / "manuals" / f"{page_name}.md"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Help page not found.")
    markdown_text = file_path.read_text()
    html_content = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "admonitions"])
    title = page_name.replace("_", " ").capitalize()
    context = {"request": request, "title": title, "content": html_content}
    return NoCacheTemplateResponse(request, "help.html", context)

@router.get("/connections", response_class=HTMLResponse)
async def read_connections_page(request: Request):
    return NoCacheTemplateResponse(request, "connections.html", {"request": request, "config": settings})

if 'rpi' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/rpi", response_class=HTMLResponse)
    async def read_live_view_rpi(request: Request):
        return NoCacheTemplateResponse(request, "live_view_rpi.html", {"request": request})
    @router.get("/gallery/rpi", response_class=HTMLResponse)
    async def read_gallery_rpi(request: Request):
        context = {"request": request, "camera_id": "rpi", "camera_name": "RPi"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

if 'usb' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/usb", response_class=HTMLResponse)
    async def read_live_view_usb(request: Request):
        return NoCacheTemplateResponse(request, "live_view_usb.html", {"request": request})
    @router.get("/gallery/usb", response_class=HTMLResponse)
    async def read_gallery_usb(request: Request):
        context = {"request": request, "camera_id": "usb", "camera_name": "USB"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

@router.get("/logs", response_class=HTMLResponse)
async def read_logs_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(EventLog).order_by(EventLog.timestamp.desc()).limit(100))
    logs = result.scalars().all()
    context = {"request": request, "logs": logs}
    return NoCacheTemplateResponse(request, "logs.html", context)

@router.get("/api-docs", response_class=HTMLResponse)
async def read_api_docs_page(request: Request):
    openapi_schema = request.app.openapi()
    context = {"request": request, "api_title": openapi_schema.get("info", {}).get("title", "API"), "api_version": openapi_schema.get("info", {}).get("version", ""), "api_paths": openapi_schema.get("paths", {})}
    return NoCacheTemplateResponse(request, "api.html", context)

@router.get("/analytics", response_class=HTMLResponse)
async def read_analytics_page(request: Request):
    return NoCacheTemplateResponse(request, "analytics.html", {"request": request})
```

---

### `app/services/__init__.py`

```python
# This file is empty.

```

---

### `app/services/detection_service.py`

```python
import asyncio
import uuid
import json
from collections import deque
from typing import Dict, Deque, List, Optional, Any
import httpx
import cv2
import numpy as np
from pathlib import Path
import redis.asyncio as redis
from sqlalchemy.orm.attributes import flag_modified

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from app.models.detection import DetectionEventLog
from config import settings
from app.services.audio_service import AsyncAudioService
from app.services.llm_service import LlmApiService

PROJECT_ROOT = Path(__file__).parent.parent.parent

class QcApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=20.0)

    async def predict(self, image_path: str, serial_number: str, model_id: str) -> Optional[Dict[str, Any]]:
        try:
            with open(image_path, "rb") as f:
                files = {"image": (Path(image_path).name, f.read(), "image/jpeg")}
                data = {"model_id": model_id, "serial_no": serial_number}
                response = await self.client.post("/predict", files=files, data=data)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"ERROR during AI API call for {model_id}: {e}")
            return None

class AsyncDetectionService:
    def __init__(self, modbus_controller: AsyncModbusController, camera_manager: AsyncCameraManager, orchestration_service: AsyncOrchestrationService, redis_client: redis.Redis, conveyor_settings, db_session_factory, active_camera_ids: List[str], audio_service: AsyncAudioService, llm_service: LlmApiService):
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._redis = redis_client
        self._conveyor_config = conveyor_settings
        self._get_db_session = db_session_factory
        self._active_camera_ids = active_camera_ids
        self._audio_service = audio_service
        self._llm_service = llm_service
        self._qc_api_service = QcApiService(base_url=settings.AI_API.BASE_URL)
        self._in_flight_objects: Deque[str] = deque()
        self._stalled_product_timers: Dict[str, asyncio.TimerHandle] = {}
        self._entry_sensor_is_blocked = False

    def get_in_flight_count(self) -> int:
        return len(self._in_flight_objects)

    async def reset_state(self):
        self._in_flight_objects.clear()
        for timer in self._stalled_product_timers.values(): timer.cancel()
        self._stalled_product_timers.clear()
        self._entry_sensor_is_blocked = False

    async def _handle_stalled_product(self, serial_number: str):
        self._stalled_product_timers.pop(serial_number, None)
        if serial_number in self._in_flight_objects:
            self._in_flight_objects.remove(serial_number)
            await self._orchestration.trigger_run_failure(f"Stalled product detected: {serial_number}")
    
    def _annotate_image_from_results(self, image_path: str, api_response: Optional[Dict[str, Any]]) -> str:
        try:
            image = cv2.imread(image_path)
            if image is None or api_response is None: return image_path
            original_path = Path(image_path)
            annotated_dir = original_path.parent / "annotated"
            annotated_dir.mkdir(exist_ok=True)

            detections = api_response.get("detections", [])
            for detection in detections:
                box_points = detection.get("box", [])
                if box_points and len(box_points) == 4:
                    contour = np.array([[int(p['x']), int(p['y'])] for p in box_points], np.int32)
                    cv2.polylines(image, [contour], True, (36, 255, 12), 2)
                    label = f"{detection.get('class_name', 'N/A')} ({detection.get('confidence', 0):.2f})"
                    cv2.putText(image, label, (contour[0][0], contour[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

            save_path = str(annotated_dir / original_path.name)
            cv2.imwrite(save_path, image)
            relative_path = Path(save_path).relative_to(PROJECT_ROOT / "web")
            return f"/{relative_path.as_posix()}"
        except Exception as e:
            print(f"FATAL ERROR during image annotation: {e}")
            return image_path

    async def _run_qc_and_update_db(self, detection_log_id: int, serial_number: str, web_image_path: str):
        if not await self._audio_service._get_config("YOLO_ENABLED", settings.AI_STRATEGY.YOLO_ENABLED): return

        full_image_path = str(PROJECT_ROOT / "web" / web_image_path.lstrip('/'))
        
        api_response = await self._qc_api_service.predict(full_image_path, serial_number, settings.AI_API.QC_MODEL_ID)
        
        analysis_summary = {"overall_status": "REJECT", "reject_reason": "No valid objects detected.", "primary_detection": None}

        if api_response and api_response.get("detections"):
            detections = sorted(api_response.get("detections", []), key=lambda d: d.get('confidence', 0), reverse=True)
            primary = detections[0]
            analysis_summary["primary_detection"] = {"type": primary.get("class_name", "Unknown"), "confidence": round(primary.get("confidence", 0), 4)}
            analysis_summary["overall_status"] = "ACCEPT"
            analysis_summary["reject_reason"] = None
        
        await self._orchestration.on_item_inspected(
            qc_status=analysis_summary["overall_status"],
            defects=analysis_summary["reject_reason"],
            type=analysis_summary["primary_detection"]["type"] if analysis_summary["primary_detection"] else "Unknown",
            count=self._orchestration.get_status().get('run_progress', 0)
        )
        
        annotated_path = self._annotate_image_from_results(full_image_path, api_response)
        
        async with self._get_db_session() as session:
            log_entry = await session.get(DetectionEventLog, detection_log_id)
            if log_entry:
                log_entry.annotated_image_path = annotated_path
                log_entry.details = analysis_summary
                flag_modified(log_entry, "details")
                await session.commit()
        
        await self._redis.publish("qc_annotated_image:new", json.dumps({
            "annotated_path": annotated_path, "results": analysis_summary
        }))

    async def handle_sensor_event(self, event: SensorEvent):
        if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value: return

        if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL:
            if event.new_state == SensorState.TRIGGERED and not self._entry_sensor_is_blocked:
                self._entry_sensor_is_blocked = True
                serial_number = str(uuid.uuid4())
                self._in_flight_objects.append(serial_number)
                
                loop = asyncio.get_running_loop()
                timer = loop.call_later(self._conveyor_config.MAX_TRANSIT_TIME_SEC, 
                                        lambda: asyncio.create_task(self._handle_stalled_product(serial_number)))
                self._stalled_product_timers[serial_number] = timer
                
                await self._orchestration.on_item_detected(serial_number)
                
                if settings.CAMERA_TRIGGER_DELAY_MS > 0: await asyncio.sleep(settings.CAMERA_TRIGGER_DELAY_MS / 1000.0)
                
                image_path = None
                if self._active_camera_ids:
                    image_path = await self._camera_manager.capture_and_save_image(self._active_camera_ids[0], f'event_{serial_number}')
                
                active_run_id = self._orchestration.get_active_run_id()
                if active_run_id and image_path:
                    async with self._get_db_session() as session:
                        new_event = DetectionEventLog(run_log_id=active_run_id, image_path=image_path, serial_number=serial_number)
                        session.add(new_event); await session.commit(); await session.refresh(new_event)
                        asyncio.create_task(self._run_qc_and_update_db(new_event.id, serial_number, image_path))

            elif event.new_state == SensorState.CLEARED:
                self._entry_sensor_is_blocked = False

        elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
            if self._in_flight_objects:
                serial = self._in_flight_objects.popleft()
                if serial in self._stalled_product_timers:
                    self._stalled_product_timers.pop(serial).cancel()
                await self._orchestration.on_exit_sensor_triggered()
```

---

### `app/services/llm_service.py`

```python
import httpx
import json
import re
from typing import Optional, Any, Dict, List

from config import settings

class LlmApiService:
    """A client to interact with the external LLM Summarization API."""
    def __init__(self):
        self.base_url = settings.LLM_API.BASE_URL
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    def _parse_llm_response(self, response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        FIXED: Robustly parses multiple possible JSON response structures from the LLM API.
        """
        if not response_data:
            return None
        
        # --- THIS IS THE FINAL FIX ---
        # CASE 1: The response is already in the simple, direct format.
        if 'analysis' in response_data and isinstance(response_data.get('analysis'), dict):
            print("LLM Service INFO: Parsed simple/direct LLM response format.")
            return response_data

        # CASE 2: The response is the complex format with embedded JSON.
        try:
            text_content = response_data['choices'][0]['text']
            cleaned_text = re.sub(r'```json\s*|\s*```', '', text_content).strip()
            parsed_json = json.loads(cleaned_text)
            
            # The parsed content might be the final object, or it might be nested
            if 'analysis' in parsed_json:
                 print("LLM Service INFO: Parsed complex/embedded LLM response format.")
                 return parsed_json
            else:
                 # Handle cases where the embedded text IS the analysis object
                 print("LLM Service INFO: Parsed complex/embedded LLM response (direct content).")
                 return {"analysis": parsed_json}

        except (KeyError, IndexError, json.JSONDecodeError, TypeError) as e:
            print(f"LLM Service CRITICAL ERROR: Failed to parse any known LLM response format. Error: {e}. Raw data: {response_data}")
            return None
        # --- END OF FIX ---

    async def analyze_item(
        self,
        item_data: Dict[str, Any],
        language: str,
        word_count: int,
        model_preference: str = "realtime"
    ) -> Optional[Dict[str, Any]]:
        """Generates a summary for a single QC item."""
        if not settings.AI_STRATEGY.LLM_ENABLED: return None

        payload = {
            "item_data": item_data, "language": language, "word_count": word_count,
            "max_tokens": int(word_count * 3.5), "model_preference": model_preference
        }
        try:
            response = await self.client.post("/item_analysis", json=payload)
            response.raise_for_status()
            return self._parse_llm_response(response.json())
        except httpx.RequestError as e:
            print(f"LLM Service ERROR: Could not connect to LLM API at {e.request.url}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"LLM Service ERROR: API returned status {e.response.status_code}. Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"LLM Service ERROR: An unexpected error occurred during item analysis: {e}")
            return None

    async def summarize_batch(
        self,
        batch_data: List[Dict[str, Any]],
        language: str,
        word_count: int,
        model_preference: str = "high_quality"
    ) -> Optional[Dict[str, Any]]:
        """Generates a summary for an entire batch of items."""
        if not settings.AI_STRATEGY.LLM_ENABLED: return None

        payload = {
            "batch_data": batch_data, "language": language, "word_count": word_count,
            "max_tokens": int(word_count * 2.5), "model_preference": model_preference
        }
        try:
            response = await self.client.post("/batch_summary", json=payload)
            response.raise_for_status()
            return self._parse_llm_response(response.json())
        except Exception as e:
            print(f"LLM Service ERROR: An unexpected error occurred during batch summary: {e}")
            return None

    async def health_check(self) -> bool:
        """Performs a simple health check on the LLM API."""
        if not settings.AI_STRATEGY.LLM_ENABLED: return False
        try:
            response = await self.client.get("/health", timeout=2.0)
            return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False
```

---

### `app/services/tts_service.py`

```python
import httpx
from typing import Optional
from config import settings

class TtsApiService:
    """A client to interact with the external Text-to-Speech API."""
    def __init__(self):
        self.base_url = settings.TTS_API.BASE_URL
        # --- DEFINITIVE FIX: Increased timeout to handle slow AI models ---
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=90.0)

    async def synthesize_speech(
        self,
        text: str,
        model: str,
        language: Optional[str] = None,
        speaker: Optional[str] = None,
        emotion: Optional[str] = None,
        desc: Optional[str] = None
    ) -> Optional[bytes]:
        if not settings.AI_STRATEGY.TTS_ENABLED:
            return None 

        payload = {"text": text, "model": model}

        if model == "xtts":
            if language:
                payload["language"] = language
            if speaker:
                payload["speaker"] = speaker
        
        elif model == "parler":
            if desc:
                payload["desc"] = desc
        
        elif model == "mac":
            if language:
                payload["language"] = language
            if language == "en":
                payload["emotion"] = emotion or "neutral"

        try:
            response = await self.client.post("/tts", json=payload)
            response.raise_for_status()
            
            if response.content and len(response.content) > 1024:
                 return response.content
            else:
                print(f"TTS Service WARNING: Received 200 OK but audio content was empty. Silent failure in TTS engine likely.")
                return None

        except httpx.RequestError as e:
            print(f"TTS Service ERROR: Could not connect to TTS API at {e.request.url}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"TTS Service ERROR: API returned status {e.response.status_code}. Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"TTS Service ERROR: An unexpected error occurred during synthesis: {e}")
            return None

    async def health_check(self) -> bool:
        if not settings.AI_STRATEGY.TTS_ENABLED:
            return False
        try:
            response = await self.client.get("/health", timeout=2.0)
            return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False

```

---

### `app/services/notification_service.py`

```python
"""
REVISED: The notification service is now simplified and has no direct hardware control.
- The `gpio_controller` dependency has been completely removed.
- Its only responsibilities are printing alerts and logging them to the database.
"""
import asyncio
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel

# Removed the obsolete import for AsyncGPIOController
from app.models.event_log import EventLog, EventType

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class Alert(BaseModel):
    level: AlertLevel
    message: str
    details: Optional[Dict[str, Any]] = None

class AsyncNotificationService:
    # --- THE FIX IS HERE ---
    # The `gpio_controller` argument has been removed from the __init__ method.
    def __init__(self, db_session_factory):
        # The self._gpio attribute has been removed.
        self._get_db_session = db_session_factory
        self._queue = asyncio.Queue(maxsize=100)
        self._worker_task: Optional[asyncio.Task] = None

    def start(self):
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._notification_worker())

    def stop(self):
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()

    async def send_alert(self, level: str, message: str, details: Optional[dict] = None):
        try:
            alert_level = AlertLevel(level.lower())
            alert = Alert(level=alert_level, message=message, details=details)
            self._queue.put_nowait(alert)
        except asyncio.QueueFull:
            print("Notification Service Warning: Alert queue is full. Dropping oldest alert.")
            await self._queue.get()
            await self._queue.put(alert)

    async def _notification_worker(self):
        while True:
            try:
                alert: Alert = await self._queue.get()
                # 1. Print to console
                print(f"Notification: [{alert.level.name}] {alert.message}")

                # 2. Persist the log to the database
                await self._log_event_to_db(alert)

                # --- The physical notification logic (blinking LEDs) has been removed ---
                # This is because this service no longer controls hardware.
                # The OrchestrationService is now responsible for status lights.

                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in notification worker: {e}")

    async def _log_event_to_db(self, alert: Alert):
        try:
            async with self._get_db_session() as session:
                log_entry = EventLog(
                    event_type=EventType(alert.level.value),
                    source="SYSTEM", # Could be enhanced to be more specific
                    message=alert.message,
                    details=alert.details
                )
                session.add(log_entry)
                await session.commit()
        except Exception as e:
            print(f"Failed to log event to database: {e}")
```

---

### `app/services/system_service.py`

```python
import time
from typing import Dict, Optional
import psutil
import asyncio

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager, CameraHealthStatus
from app.core.modbus_poller import AsyncModbusPoller
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.detection_service import AsyncDetectionService
from app.services.llm_service import LlmApiService
from app.services.tts_service import TtsApiService
from config import ACTIVE_CAMERA_IDS
from config.settings import AppSettings

def _get_rpi_cpu_temp() -> Optional[float]:
    """Safely gets the Raspberry Pi CPU temperature."""
    try:
        temps = psutil.sensors_temperatures()
        return temps.get('cpu_thermal', [None])[0].current if temps else None
    except Exception:
        return None

class AsyncSystemService:
    """
    Gathers and provides a unified status report for all system components,
    including the health and enabled status of external AI services.
    """
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        modbus_poller: AsyncModbusPoller,
        camera_manager: AsyncCameraManager,
        detection_service: AsyncDetectionService,
        orchestration_service: AsyncOrchestrationService,
        llm_service: LlmApiService,
        tts_service: TtsApiService,
        settings: AppSettings
    ):
        self._io = modbus_controller
        self._poller = modbus_poller
        self._camera = camera_manager
        self._detection_service = detection_service
        self._orchestration_service = orchestration_service
        self._llm_service = llm_service
        self._tts_service = tts_service
        self._settings = settings
        self._sensor_config = self._settings.SENSORS
        self._output_config = self._settings.OUTPUTS.model_dump()
        self._app_start_time = time.monotonic()

    async def full_system_reset(self):
        """
        Resets all counters, stops all hardware, and clears all in-memory state.
        This provides a comprehensive system state reset.
        """
        print("System Service: Full system reset initiated.")
        await self._orchestration_service.stop_run()
        if self._detection_service:
            await self._detection_service.reset_state()

    async def get_system_status(self) -> Dict:
        """Gathers the current health status from all components safely."""
        try:
            all_camera_statuses = self._camera.get_all_health_statuses()
            camera_statuses_payload = {
                cam_id: all_camera_statuses.get(cam_id, CameraHealthStatus.DISCONNECTED.value)
                for cam_id in ACTIVE_CAMERA_IDS
            }
            io_module_status = self._poller.get_io_health().value
            input_states = self._poller.get_current_input_states()
            output_states = self._poller.get_current_output_states()

            # --- NEW: AI Service Health Checks (run concurrently) ---
            llm_ok_task = asyncio.create_task(self._llm_service.health_check())
            tts_ok_task = asyncio.create_task(self._tts_service.health_check())
            
            # YOLO health is determined by its enabled state for now
            yolo_ok = self._settings.AI_STRATEGY.YOLO_ENABLED
            
            llm_ok, tts_ok = await asyncio.gather(llm_ok_task, tts_ok_task)
            # --- END NEW ---

            def get_input_state(channel: int) -> bool:
                index = channel - 1
                return input_states[index] if 0 <= index < len(input_states) else True 

            def get_output_state(name: str) -> bool:
                channel = self._output_config.get(name.upper())
                return output_states[channel] if channel is not None and 0 <= channel < len(output_states) else False

            return {
                "cpu_usage": psutil.cpu_percent(interval=None),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "cpu_temperature": _get_rpi_cpu_temp(),
                "uptime_seconds": int(time.monotonic() - self._app_start_time),
                "camera_statuses": camera_statuses_payload,
                "io_module_status": io_module_status,
                "sensor_1_status": not get_input_state(self._sensor_config.ENTRY_CHANNEL), 
                "sensor_2_status": not get_input_state(self._sensor_config.EXIT_CHANNEL), 
                "conveyor_relay_status": get_output_state("conveyor"),
                "gate_relay_status": get_output_state("gate"),
                "diverter_relay_status": get_output_state("diverter"),
                "led_green_status": get_output_state("led_green"),
                "led_red_status": get_output_state("led_red"),
                "buzzer_status": get_output_state("buzzer"),
                "camera_light_status": get_output_state("camera_light"),
                "camera_light_two_status": get_output_state("camera_light_two"),
                "in_flight_count": self._detection_service.get_in_flight_count() if self._detection_service else 0,
                # --- NEW: AI Service Status Payload ---
                "ai_services": {
                    "yolo": {
                        "enabled": self._settings.AI_STRATEGY.YOLO_ENABLED,
                        "status": "ok" if yolo_ok else "disabled"
                    },
                    "llm": {
                        "enabled": self._settings.AI_STRATEGY.LLM_ENABLED,
                        "status": "ok" if llm_ok else "error"
                    },
                    "tts": {
                        "enabled": self._settings.AI_STRATEGY.TTS_ENABLED,
                        "status": "ok" if tts_ok else "error"
                    }
                }
            }
        except Exception as e:
            print(f"FATAL ERROR in get_system_status: {e}")
            return {"error": "Failed to fetch system status."}

    async def emergency_stop(self):
        """Immediately stop all hardware operations via Modbus."""
        print("SYSTEM SERVICE: Initiating emergency stop of all hardware.")
        # Create a list of tasks to write to all coils concurrently
        tasks = [
            self._io.write_coil(self._output_config.get("CONVEYOR"), False),
            self._io.write_coil(self._output_config.get("GATE"), False),
            self._io.write_coil(self._output_config.get("DIVERTER"), False),
            self._io.write_coil(self._output_config.get("LED_GREEN"), False),
            self._io.write_coil(self._output_config.get("LED_RED"), True),
            self._io.write_coil(self._output_config.get("BUZZER"), False),
            self._io.write_coil(self._output_config.get("CAMERA_LIGHT"), False),
            self._io.write_coil(self._output_config.get("CAMERA_LIGHT_TWO"), False)
        ]
        await asyncio.gather(*tasks)
```

---

### `app/services/orchestration_service.py`

```python
import asyncio
import json
from enum import Enum
from typing import Optional, Any, Dict, TYPE_CHECKING
import time 

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.modbus_controller import AsyncModbusController
from app.models.profiles import ObjectProfile, CameraProfile
from app.models.run_log import RunLog, RunStatus
from app.models.event_log import EventType
from app.models.operator import Operator
from app.models.detection import DetectionEventLog
from config import ACTIVE_CAMERA_IDS, settings
from app.services.audio_service import AsyncAudioService
from app.services.llm_service import LlmApiService
from app.websocket.connection_manager import manager as websocket_manager

if TYPE_CHECKING:
    from app.services.detection_service import AsyncDetectionService

class OperatingMode(str, Enum):
    STOPPED = "Stopped"
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED_BETWEEN_BATCHES = "Paused (Between Batches)"
    POST_RUN_DELAY = "Post-Run Delay"

def _get_summary_from_llm_response(llm_response: Dict[str, Any]) -> str | None:
    try:
        return llm_response['analysis']['plain_text_summary']
    except (KeyError, TypeError):
        return None

class AsyncOrchestrationService:
    def __init__(self, modbus_controller: AsyncModbusController, db_session_factory, redis_client: redis.Redis, app_settings, audio_service: AsyncAudioService, llm_service: LlmApiService):
        self._io = modbus_controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._settings = app_settings
        self._audio_service = audio_service
        self._llm_service = llm_service
        self._mode = OperatingMode.STOPPED
        self._lock = asyncio.Lock()
        self._active_profile: Optional[ObjectProfile] = None
        self._active_run_id: Optional[int] = None
        self._active_alarm_message: Optional[str] = None
        self._run_profile_id: Optional[int] = None
        self._run_batch_code: Optional[str] = None
        self._run_operator_name: Optional[str] = None
        self._run_target_count: int = 0
        self._run_post_batch_delay_sec: int = 5
        self._current_count: int = 0
        self._output_map = self._settings.OUTPUTS
        self._completion_task: Optional[asyncio.Task] = None
        self._detection_service: Optional["AsyncDetectionService"] = None
        self._buzzer_queue = asyncio.Queue()
        self._buzzer_task: Optional[asyncio.Task] = None

    def set_detection_service(self, detection_service: "AsyncDetectionService"):
        self._detection_service = detection_service

    def beep_for(self, duration_ms: int):
        if duration_ms > 0:
            try: self._buzzer_queue.put_nowait(duration_ms)
            except asyncio.QueueFull: print("Buzzer queue is full.")

    async def _buzzer_manager(self):
        buzzer_off_time = 0.0
        is_buzzer_on = False
        while True:
            try:
                try:
                    duration_ms = await asyncio.wait_for(self._buzzer_queue.get(), timeout=0.05)
                    new_off_time = time.monotonic() + (duration_ms / 1000.0)
                    if new_off_time > buzzer_off_time: buzzer_off_time = new_off_time
                except asyncio.TimeoutError: pass
                current_time = time.monotonic()
                if current_time < buzzer_off_time:
                    if not is_buzzer_on: await self._io.write_coil(self._output_map.BUZZER, True); is_buzzer_on = True
                else:
                    if is_buzzer_on: await self._io.write_coil(self._output_map.BUZZER, False); is_buzzer_on = False
            except asyncio.CancelledError:
                if is_buzzer_on: await self._io.write_coil(self._output_map.BUZZER, False)
                break
            except Exception as e: print(f"Error in buzzer manager: {e}")

    def start_background_tasks(self):
        if self._buzzer_task is None or self._buzzer_task.done():
            self._buzzer_task = asyncio.create_task(self._buzzer_manager())

    def stop_background_tasks(self):
        if self._buzzer_task and not self._buzzer_task.done(): self._buzzer_task.cancel()
        if self._completion_task and not self._completion_task.done(): self._completion_task.cancel()

    async def initialize_hardware_state(self):
        await asyncio.gather(
            self._io.write_coil(self._output_map.CONVEYOR, False),
            self._io.write_coil(self._output_map.LED_GREEN, False),
            self._io.write_coil(self._output_map.LED_RED, True)
        )

    def get_active_run_id(self) -> Optional[int]: return self._active_run_id

    async def on_item_detected(self, serial_number: str):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            self._current_count += 1
            await websocket_manager.broadcast_json({"type": "new_item_detected", "data": {"serial_number": serial_number, "processed_count": self._current_count}})
            if self._run_target_count > 0 and self._current_count >= self._run_target_count:
                if self._completion_task is None or self._completion_task.done():
                    self._completion_task = asyncio.create_task(self._complete_and_loop_run_task())
    
    async def on_item_inspected(self, qc_status: str, **kwargs):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            if "ACCEPT" in qc_status.upper():
                if await self._audio_service._get_config("ALERT_ON_PASS", settings.AI_STRATEGY.ALERT_ON_PASS):
                    await self._audio_service.play_realtime_alert("PASS_TEMPLATE", **kwargs)
            else:
                if await self._audio_service._get_config("ALERT_ON_REJECT", settings.AI_STRATEGY.ALERT_ON_REJECT):
                    await self._audio_service.play_realtime_alert("REJECT_TEMPLATE", **kwargs)

    async def on_exit_sensor_triggered(self): self.beep_for(self._settings.BUZZER.EXIT_SENSOR_MS)
    
    async def trigger_persistent_alarm(self, message: str):
        async with self._lock:
            if self._active_alarm_message: return
            self._active_alarm_message = message
        print(f"ORCHESTRATION ALARM: {message}")
        
    async def acknowledge_alarm(self):
        async with self._lock:
            if not self._active_alarm_message: return
            self._active_alarm_message = None
        print("Alarm acknowledged by user.")

    async def trigger_run_failure(self, reason: str):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            print(f"CRITICAL RUN FAILURE: {reason}.")
            await self._audio_service.play_event_from_cache("product_stalled")
            await self._update_run_log_status(RunStatus.FAILED)
            self._mode = OperatingMode.STOPPED
            await self.initialize_hardware_state()
            if self._detection_service: await self._detection_service.reset_state()
            self._active_profile, self._active_run_id = None, None
            await self.trigger_persistent_alarm(f"Run Failed: {reason}")
    
    async def start_run(self, profile_id: int, target_count: int, post_batch_delay_sec: int, batch_code: str, operator_id: int) -> bool:
        async with self._lock:
            if self._mode in [OperatingMode.RUNNING, OperatingMode.POST_RUN_DELAY]: return False
            async with self._get_db_session() as session:
                operator = await session.get(Operator, operator_id)
                if not operator: return False
                self._run_operator_name = operator.name
            self._run_profile_id, self._run_target_count, self._run_post_batch_delay_sec, self._run_batch_code, self._run_operator_id = \
                profile_id, target_count, post_batch_delay_sec, batch_code, operator_id
            return await self._execute_start_sequence()
            
    async def _execute_start_sequence(self) -> bool:
        async with self._get_db_session() as session:
            result = await session.execute(select(ObjectProfile).options(selectinload(ObjectProfile.camera_profile)).where(ObjectProfile.id == self._run_profile_id))
            profile = result.scalar_one_or_none()
        
        if not profile or not profile.camera_profile:
             await self.trigger_persistent_alarm("Failed to start: Recipe has no camera profile.")
             return False
        if not profile.product_id:
             await self.trigger_persistent_alarm("Failed to start: Recipe is not linked to a Product.")
             return False
        
        try:
            async with self._get_db_session() as session:
                new_run_log = RunLog(batch_code=self._run_batch_code, operator_id=self._run_operator_id, product_id=profile.product_id, status=RunStatus.RUNNING)
                session.add(new_run_log); await session.commit(); await session.refresh(new_run_log)
                self._active_run_id = new_run_log.id
        except Exception as e: 
            print(f"FATAL: Could not create RunLog due to database error: {e}"); 
            return False
        
        self._active_profile = profile
        await self.acknowledge_alarm()
        
        cam_settings = profile.camera_profile
        settings_payload = {"autofocus": cam_settings.autofocus, "exposure": cam_settings.exposure, "gain": cam_settings.gain, "white_balance_temp": cam_settings.white_balance_temp, "brightness": cam_settings.brightness}
        command = {"action": "apply_settings", "settings": settings_payload}
        for cam_id in ACTIVE_CAMERA_IDS:
            await self._redis.publish(f"camera:commands:{cam_id}", json.dumps(command))
        
        self._current_count = 0
        self._mode = OperatingMode.RUNNING
        await self._io.write_coil(self._output_map.LED_RED, False)
        await self._io.write_coil(self._output_map.LED_GREEN, True)
        await self._io.write_coil(self._output_map.CONVEYOR, True)
        return True

    async def _update_run_log_status(self, status: RunStatus):
        if not self._active_run_id: return
        try:
            async with self._get_db_session() as session:
                run_log = await session.get(RunLog, self._active_run_id)
                if run_log: run_log.status, run_log.end_timestamp = status, datetime.utcnow(); await session.commit()
        except Exception as e: print(f"Error updating RunLog status: {e}")

    async def _generate_and_play_summary(self):
        if not self._active_run_id: return
        llm_language = await self._audio_service._get_config("LANGUAGE", settings.AI_STRATEGY.LANGUAGE)
        word_count = await self._audio_service._get_config("LLM_SUMMARY_WORD_COUNT", settings.AI_STRATEGY.LLM_SUMMARY_WORD_COUNT)
        model_pref = await self._audio_service._get_config("SUMMARY_LLM_MODEL", settings.AI_STRATEGY.SUMMARY_LLM_MODEL)
        async with self._get_db_session() as session:
            result = await session.execute(select(DetectionEventLog).where(DetectionEventLog.run_log_id == self._active_run_id))
            run_data = [{"qc_summary": det.details} for det in result.scalars().all() if det.details]
        
        if not run_data: return
        llm_response = await self._llm_service.summarize_batch(batch_data=run_data, language=llm_language, word_count=word_count, model_preference=model_pref)
        summary_text = _get_summary_from_llm_response(llm_response)
        if summary_text: await self._audio_service.play_pipelined_summary(summary_text)

    async def _complete_and_loop_run_task(self):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            self._mode = OperatingMode.POST_RUN_DELAY
            await self._update_run_log_status(RunStatus.COMPLETED)
            await self._audio_service.play_realtime_alert("BATCH_COMPLETE_TEMPLATE", batch_id=self._run_batch_code, total_items=self._current_count)

        await asyncio.sleep(self._settings.CONVEYOR.CONVEYOR_AUTO_STOP_DELAY_SEC)

        async with self._lock:
            if self._mode != OperatingMode.POST_RUN_DELAY: return
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            if self._detection_service: await self._detection_service.reset_state()
            if await self._audio_service._get_config("LLM_ENABLED", settings.AI_STRATEGY.LLM_ENABLED):
                asyncio.create_task(self._generate_and_play_summary())
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES

        await asyncio.sleep(self._run_post_batch_delay_sec)

        async with self._lock:
            if self._mode != OperatingMode.PAUSED_BETWEEN_BATCHES: return
            for i in range(3, 0, -1):
                await self._audio_service.play_realtime_alert("NEXT_BATCH_TEMPLATE", countdown=i)
                await asyncio.sleep(1)
            if not await self._execute_start_sequence():
                await self.stop_run()

    async def stop_run(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED: return
            if self._completion_task and not self._completion_task.done(): self._completion_task.cancel()
            if self._active_run_id: await self._update_run_log_status(RunStatus.ABORTED)
            self._mode = OperatingMode.STOPPED
            self._active_profile = None; self._active_run_id = None; self._current_count = 0
            await self.initialize_hardware_state()
            if self._detection_service: await self._detection_service.reset_state()

    def get_status(self) -> dict:
        return {
            "mode": self._mode.value,
            "active_profile": self._active_profile.name if self._active_profile else "None",
            "operator_name": self._run_operator_name,
            "batch_code": self._run_batch_code,
            "run_progress": self._current_count,
            "target_count": self._run_target_count,
            "active_alarm_message": self._active_alarm_message,
        }
```

---

### `app/services/audio_service.py`

```python
import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, Optional, Any

from app.models import Configuration, ConfigDataType
from sqlalchemy.future import select
import time

from app.services.tts_service import TtsApiService
from app.utils.tokenizer import chunk_text_by_tokens
from config import settings

TTS_CACHE_DIR = Path(__file__).parent.parent.parent / "audio_files" / "tts_cache"
TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class AsyncAudioService:
    def __init__(self, db_session_factory, tts_service: TtsApiService):
        self._get_db_session = db_session_factory
        self._tts_service = tts_service
        self._playback_task: Optional[asyncio.Task] = None
        self._config_cache: Dict[str, Any] = {}
        self._config_cache_last_updated: float = 0.0

    async def _get_config(self, key: str, default: Any) -> Any:
        if time.monotonic() - self._config_cache_last_updated > 5.0: self._config_cache.clear()
        if key in self._config_cache: return self._config_cache[key]
        async with self._get_db_session() as session:
            result = await session.execute(select(Configuration).where(Configuration.namespace == "ai_strategy", Configuration.key == key))
            config_item = result.scalar_one_or_none()
            self._config_cache_last_updated = time.monotonic()
            if config_item:
                try:
                    if config_item.data_type == ConfigDataType.BOOL: value = config_item.value.lower() in ['true', '1', 't']
                    elif config_item.data_type == ConfigDataType.INT: value = int(config_item.value)
                    elif config_item.data_type == ConfigDataType.FLOAT: value = float(config_item.value)
                    else: value = config_item.value
                    self._config_cache[key] = value
                    return value
                except (ValueError, TypeError): self._config_cache[key] = default
                return default
        self._config_cache[key] = default
        return default

    async def _execute_playback_from_stream(self, audio_bytes: bytes):
        if not audio_bytes: return
        process = None
        try:
            process = await asyncio.create_subprocess_exec("aplay", "-", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
            await process.communicate(input=audio_bytes)
        except Exception as e: print(f"[Audio Service] FATAL ERROR during stream playback: {e}")

    async def play_realtime_alert(self, template_key: str, **kwargs):
        if not await self._get_config("TTS_ENABLED", settings.AI_STRATEGY.TTS_ENABLED): return
        template = await self._get_config(template_key, getattr(settings.AI_STRATEGY, template_key, ""))
        text_to_speak = template.format(**kwargs)
        realtime_engine = await self._get_config("REALTIME_TTS_ENGINE", settings.AI_STRATEGY.REALTIME_TTS_ENGINE)
        # THIS IS THE FIX
        tts_language = await self._get_config("TTS_LANGUAGE", settings.AI_STRATEGY.TTS_LANGUAGE)
        audio_bytes = await self._tts_service.synthesize_speech(text=text_to_speak, model=realtime_engine, language=tts_language)
        if audio_bytes:
            if self._playback_task and not self._playback_task.done(): self._playback_task.cancel()
            self._playback_task = asyncio.create_task(self._execute_playback_from_stream(audio_bytes))

    async def generate_pipelined_summary_audio(self, text: str, tts_language: Optional[str] = None, engine_override: Optional[str] = None) -> Optional[bytes]:
        if not await self._get_config("TTS_ENABLED", settings.AI_STRATEGY.TTS_ENABLED): return None
        summary_engine = engine_override or await self._get_config("SUMMARY_TTS_ENGINE", settings.AI_STRATEGY.SUMMARY_TTS_ENGINE)
        # THIS IS THE FIX
        language = tts_language or await self._get_config("TTS_LANGUAGE", settings.AI_STRATEGY.TTS_LANGUAGE)
        word_count = await self._get_config("LLM_SUMMARY_WORD_COUNT", settings.AI_STRATEGY.LLM_SUMMARY_WORD_COUNT)
        chunk_count = await self._get_config("TTS_SUMMARY_CHUNK_COUNT", settings.AI_STRATEGY.TTS_SUMMARY_CHUNK_COUNT)
        tokens_per_chunk = int((word_count * 1.4) / chunk_count)
        text_chunks = chunk_text_by_tokens(text, tokens_per_chunk)
        audio_chunks = []
        for chunk in text_chunks:
            audio_bytes = await self._tts_service.synthesize_speech(text=chunk, model=summary_engine, language=language)
            if audio_bytes: audio_chunks.append(audio_bytes)
        return b"".join(audio_chunks) if audio_chunks else None

    async def play_pipelined_summary(self, text: str):
        audio_bytes = await self.generate_pipelined_summary_audio(text)
        if audio_bytes:
            if self._playback_task and not self._playback_task.done(): self._playback_task.cancel()
            self._playback_task = asyncio.create_task(self._execute_playback_from_stream(audio_bytes))

    async def pre_generate_and_cache_alert(self, template_key: str, text: str):
        summary_engine = await self._get_config("SUMMARY_TTS_ENGINE", settings.AI_STRATEGY.SUMMARY_TTS_ENGINE)
        # THIS IS THE FIX
        tts_language = await self._get_config("TTS_LANGUAGE", settings.AI_STRATEGY.TTS_LANGUAGE)
        audio_bytes = await self._tts_service.synthesize_speech(text=text, model=summary_engine, language=tts_language)
        if audio_bytes:
            filepath = TTS_CACHE_DIR / f"{template_key}.wav"
            async with aiofiles.open(filepath, "wb") as f: await f.write(audio_bytes)
            print(f"Audio Service: Successfully cached '{filepath.name}'.")
        else: print(f"Audio Service: FAILED to pre-generate audio for '{template_key}'.")

    # The other methods like play_event_from_cache and _execute_playback_from_file are unchanged.
    async def play_event_from_cache(self, event_key: str):
        if not await self._get_config("TTS_ENABLED", settings.AI_STRATEGY.TTS_ENABLED): return
        filepath = TTS_CACHE_DIR / f"{event_key}.wav"
        if not filepath.exists():
            static_path = Path(__file__).parent.parent.parent / "audio_files" / f"{event_key}.mp3"
            if not static_path.exists():
                print(f"Audio Service WARNING: No audio for event '{event_key}'.")
                return
            filepath = static_path
        if self._playback_task and not self._playback_task.done():
            self._playback_task.cancel()
        self._playback_task = asyncio.create_task(self._execute_playback_from_file(filepath))

    async def _execute_playback_from_file(self, filepath: Path):
        process = None
        try:
            player_cmd = "aplay" if filepath.suffix.lower() == ".wav" else "mpg123"
            args = ['-q', str(filepath)] if player_cmd == 'mpg123' else [str(filepath)]
            process = await asyncio.create_subprocess_exec(player_cmd, *args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
            await process.communicate()
        except Exception as e:
            print(f"[Audio Service] FATAL ERROR during file playback: {e}")
```

---

### `app/models/__init__.py`

```python
# rpi_counter_fastapi-apintrigation/app/models/__init__.py

"""
Makes key database components available for easy import.
This pattern simplifies imports for sessions, the base model class,
and all defined ORM models.
"""
from .database import Base, get_async_session, engine
from .detection import DetectionEventLog
from .system_status import SystemStatus
from .event_log import EventLog
# --- THIS IS THE FIX ---
# We now import and expose ConfigDataType alongside Configuration.
from .configuration import Configuration, ConfigDataType
# --- END OF FIX ---
from .profiles import CameraProfile, ObjectProfile
from .product import Product, ProductStatus
from .operator import Operator, OperatorStatus
from .run_log import RunLog, RunStatus


__all__ = [
    "Base",
    "get_async_session",
    "engine",
    "DetectionEventLog",
    "SystemStatus",
    "EventLog",
    "Configuration",
    "ConfigDataType", # <-- ADD THIS LINE
    "CameraProfile",
    "ObjectProfile",
    "Product",
    "ProductStatus",
    "Operator",
    "OperatorStatus",
    "RunLog",
    "RunStatus",
]
```

---

### `app/models/product.py`

```python
# rpi_counter_fastapi-apintrigation/app/models/product.py

from sqlalchemy import Integer, String, Text, Enum, Boolean, Float # <-- Add Float
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum

from .database import Base

class ProductStatus(PyEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    size: Mapped[str] = mapped_column(String(50), nullable=True)
    
    description: Mapped[str] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    ai_model_path: Mapped[str] = mapped_column(String(255), nullable=True, default="yolov8n.pt")
    min_sensor_block_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    max_sensor_block_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)

    # --- NEW FIELDS FOR DYNAMIC QC ---
    verify_category: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verify_size: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verify_defects: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verify_ticks: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # --- NEW FIELDS FOR GEOMETRIC VALIDATION (DEEP ANALYSIS) ---
    target_angle: Mapped[float] = mapped_column(Float, nullable=True)
    angle_tolerance: Mapped[float] = mapped_column(Float, nullable=True)
    min_aspect_ratio: Mapped[float] = mapped_column(Float, nullable=True)
    max_aspect_ratio: Mapped[float] = mapped_column(Float, nullable=True)
    # --- END OF NEW FIELDS ---

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}')>"
```

---

### `app/models/run_log.py`

```python
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict, List # Import List
from sqlalchemy import Integer, String, DateTime, Enum, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .operator import Operator
from .product import Product
# The relationship needs to know about the class, but we use a string to avoid circular imports
# from .detection import DetectionEventLog 

class RunStatus(PyEnum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ABORTED = "Aborted by User"

class RunLog(Base):
    __tablename__ = "run_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    batch_code: Mapped[str] = mapped_column(String(100), index=True)
    start_timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    end_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.RUNNING)
    
    object_profile_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    operator: Mapped["Operator"] = relationship()
    product: Mapped["Product"] = relationship()
    
    # New relationship to link to all detection events for this run
    detection_events: Mapped[List["DetectionEventLog"]] = relationship(back_populates="run")

    def __repr__(self) -> str:
        return f"<RunLog(id={self.id}, batch_code='{self.batch_code}', status='{self.status.name}')>"
```

---

### `app/models/event_log.py`

```python
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict

from sqlalchemy import Integer, String, Text, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class EventType(PyEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))
    source: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<EventLog(id={self.id}, type={self.event_type}, source='{self.source}')>"
```

---

### `app/models/profiles.py`

```python
"""
NEW: Database models for storing dynamic camera and object profiles.
This allows for on-the-fly management of "recipes" for different
production runs.
"""
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
# --- PHASE 1: Import Product for relationship ---
from .product import Product

class CameraProfile(Base):
    """
    Stores a complete set of hardware settings for a camera.
    This can be reused across multiple object profiles.
    """
    __tablename__ = "camera_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Camera hardware settings
    exposure: Mapped[int] = mapped_column(Integer, default=0)
    gain: Mapped[int] = mapped_column(Integer, default=0)
    white_balance_temp: Mapped[int] = mapped_column(Integer, default=0)
    brightness: Mapped[int] = mapped_column(Integer, default=128)
    autofocus: Mapped[bool] = mapped_column(Boolean, default=True)
    
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<CameraProfile(id={self.id}, name='{self.name}')>"


class ObjectProfile(Base):
    """
    The master "recipe" for a production run. It defines an object's
    name, its sorting logic, and links to a specific camera profile.
    """
    __tablename__ = "object_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Foreign key to link to a camera hardware configuration
    camera_profile_id: Mapped[int] = mapped_column(ForeignKey("camera_profiles.id"))
    
    # Sorting logic for this specific object
    sort_offset_ms: Mapped[int] = mapped_column(Integer, default=0, comment="Time adjustment in ms for sorting (+/- from base travel time)")
    
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # SQLAlchemy relationship to easily access the linked CameraProfile object
    camera_profile: Mapped["CameraProfile"] = relationship()
    
    # --- PHASE 1: Add relationship to the Product model ---
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"), nullable=True)
    product: Mapped[Optional["Product"]] = relationship()


    def __repr__(self) -> str:
        return f"<ObjectProfile(id={self.id}, name='{self.name}')>"
```

---

### `app/models/system_status.py`

```python
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, Float, Boolean, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class CameraStatus(PyEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class GatePosition(PyEnum):
    OPEN = "open"
    CLOSED = "closed"
    MOVING = "moving"
    ERROR = "error"

class SystemStatus(Base):
    __tablename__ = "system_status_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    cpu_usage: Mapped[float] = mapped_column(Float)
    memory_usage: Mapped[float] = mapped_column(Float)
    disk_usage: Mapped[float] = mapped_column(Float)
    cpu_temperature: Mapped[float] = mapped_column(Float)
    
    camera_status: Mapped[CameraStatus] = mapped_column(Enum(CameraStatus))
    conveyor_running: Mapped[bool] = mapped_column(Boolean)
    gate_position: Mapped[GatePosition] = mapped_column(Enum(GatePosition))
    
    uptime_seconds: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"<SystemStatus(id={self.id}, time={self.timestamp})>"

```

---

### `app/models/detection.py`

```python
# rpi_counter_fastapi-dev2/app/models/detection.py

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .run_log import RunLog

class DetectionEventLog(Base):
    """
    Records a single detection event within a production run.
    This creates a permanent link between a run and its captured images.
    """
    __tablename__ = "detection_event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    serial_number: Mapped[str] = mapped_column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    run: Mapped["RunLog"] = relationship(back_populates="detection_events")

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    
    annotated_image_path: Mapped[str] = mapped_column(String, nullable=True)

    # This is the crucial column for storing the AI JSON response.
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<DetectionEventLog(id={self.id}, serial_number='{self.serial_number}')>"
```

---

### `app/models/detection_event.py`

```python
# rpi_counter_fastapi-dev_new/app/models/detection_event.py

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from typing import TYPE_CHECKING # <-- Import TYPE_CHECKING

from .database import Base

# --- THIS IS THE FIX (PART 2) ---
if TYPE_CHECKING:
    from .run_log import RunLog
# --- END OF FIX ---


class QCResult(PyEnum):
    PENDING = "Pending"
    PASS = "Pass"
    FAIL = "Fail"

class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    
    qc_result: Mapped[QCResult] = mapped_column(Enum(QCResult), default=QCResult.PENDING)
    qc_reason: Mapped[str] = mapped_column(String, nullable=True)

    run_log: Mapped["RunLog"] = relationship(back_populates="detection_events")

    def __repr__(self) -> str:
        return f"<DetectionEvent(id={self.id}, run_log_id={self.run_log_id}, image_path='{self.image_path}')>"
```

---

### `app/models/configuration.py`

```python
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class ConfigDataType(PyEnum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    JSON = "json"

class Configuration(Base):
    __tablename__ = "configurations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    namespace: Mapped[str] = mapped_column(String(100), index=True)
    key: Mapped[str] = mapped_column(String(100), index=True)
    value: Mapped[str] = mapped_column(Text)
    data_type: Mapped[ConfigDataType] = mapped_column(Enum(ConfigDataType))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    requires_restart: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    updated_by: Mapped[str] = mapped_column(String(100), default="system")

    def __repr__(self) -> str:
        return f"<Configuration(namespace='{self.namespace}', key='{self.key}')>"

```

---

### `app/models/database.py`

```python
"""
Sets up the asynchronous database engine and session management using SQLAlchemy 2.0.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase
from config import settings

# --- FIX APPLIED HERE ---
# We create a dictionary of engine arguments and conditionally add the
# pooling arguments only if we are NOT using SQLite.
engine_args = {"echo": settings.DATABASE.ECHO}

if "sqlite" not in settings.DATABASE.URL:
    # Add pooling options for databases that support it (e.g., PostgreSQL)
    print("Non-SQLite database detected, applying connection pool settings.")
    engine_args["pool_size"] = settings.DATABASE.POOL_SIZE
    engine_args["pool_timeout"] = settings.DATABASE.POOL_TIMEOUT
else:
    # For SQLite, we add a specific argument to allow it to work with FastAPI
    print("SQLite database detected, omitting pool settings.")
    engine_args["connect_args"] = {"check_same_thread": False}

# Create an async engine instance using the URL from settings
# and the conditionally built arguments.
engine = create_async_engine(
    settings.DATABASE.URL,
    **engine_args
)

# Create a factory for creating new async sessions
AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False, # Important for FastAPI dependencies
    class_=AsyncSession
)

class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models. It includes the AsyncAttrs mixin
    to enable async loading of relationships and attributes.
    """
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get an async database session per request.
    Ensures the session is always closed, even if errors occur.
    """
    async with AsyncSessionFactory() as session:
        yield session

```

---

### `app/models/operator.py`

```python
from datetime import datetime
from sqlalchemy import Integer, String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum

from .database import Base

class OperatorStatus(PyEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[OperatorStatus] = mapped_column(Enum(OperatorStatus), default=OperatorStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def __repr__(self) -> str:
        return f"<Operator(id={self.id}, name='{self.name}')>"
```

---

### `app/schemas/operators.py`

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.operator import OperatorStatus


class OperatorBase(BaseModel):
    name: str
    status: OperatorStatus = OperatorStatus.ACTIVE

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[OperatorStatus] = None

class OperatorOut(OperatorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
```

---

### `app/schemas/run_log.py`

```python
# rpi_counter_fastapi-apinaudio/app/schemas/run_log.py

from pydantic import BaseModel, ConfigDict, field_validator, computed_field
from typing import Optional, Any, Dict, List
from datetime import datetime
import pytz

from .operators import OperatorOut
from .products import ProductOut
from app.models.run_log import RunStatus
from config import settings

# --- THIS IS THE FIX: TIMEZONE CONVERSION LOGIC ---
try:
    LOCAL_TZ = pytz.timezone(settings.TIMEZONE)
except pytz.UnknownTimeZoneError:
    # Fallback to UTC if the timezone in .env is invalid
    LOCAL_TZ = pytz.utc
# --- END OF FIX ---

class DetectionEventLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime
    image_path: Optional[str] = None
    serial_number: str
    annotated_image_path: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class RunLogBase(BaseModel):
    batch_code: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    status: RunStatus
    object_profile_snapshot: Optional[Dict[str, Any]] = None

class RunLogOut(RunLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    operator: Optional[OperatorOut] = None
    product: Optional[ProductOut] = None
    
    detected_items_count: int = 0
    duration_seconds: Optional[int] = None

    # --- NEW COMPUTED FIELD FOR LOCAL TIME DISPLAY ---
    @computed_field
    @property
    def start_timestamp_local(self) -> str:
        """Returns a formatted string of the start time in the configured local timezone."""
        if not self.start_timestamp:
            return "N/A"
        # Assume DB time is naive UTC, localize it, then convert
        utc_dt = pytz.utc.localize(self.start_timestamp)
        local_dt = utc_dt.astimezone(LOCAL_TZ)
        return local_dt.strftime('%d/%m/%Y, %H:%M:%S')

    @field_validator('object_profile_snapshot', mode='before')
    def extract_target_count(cls, v):
        if isinstance(v, dict):
            return v 
        return {}
```

---

### `app/schemas/reports.py`

```python
# rpi_counter_fastapi-dev_new/app/schemas/reports.py

from pydantic import BaseModel
from typing import List, Optional
from .run_log import RunLogOut

class ReportKPIs(BaseModel):
    """Key Performance Indicators for the summary report."""
    total_runs: int
    completed_runs: int
    aborted_runs: int
    failed_runs: int
    success_rate: float # as a percentage
    
class ProductionSummaryReport(BaseModel):
    """The complete payload for the production summary report."""
    kpis: ReportKPIs
    runs: List[RunLogOut]
```

---

### `app/schemas/profiles.py`

```python
# rpi_counter_fastapi-dev2/app/schemas/profiles.py

"""
NEW: Pydantic schemas for API data validation and serialization
for the CameraProfile and ObjectProfile models.

These schemas define the expected request and response bodies for the
profile management API endpoints.
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from .products import ProductOut

# --- CameraProfile Schemas ---

class CameraProfileBase(BaseModel):
    name: str
    exposure: int = 0
    gain: int = 0
    white_balance_temp: int = 0
    brightness: int = 128
    autofocus: bool = True
    description: Optional[str] = None

class CameraProfileCreate(CameraProfileBase):
    pass

class CameraProfileUpdate(BaseModel):
    # All fields are optional for updates
    name: Optional[str] = None
    exposure: Optional[int] = None
    gain: Optional[int] = None
    
    # --- THIS IS THE FIX ---
    # The missing field is now added, allowing updates to be processed correctly.
    white_balance_temp: Optional[int] = None
    # --- END OF FIX ---
    
    brightness: Optional[int] = None
    autofocus: Optional[bool] = None
    description: Optional[str] = None

class CameraProfileOut(CameraProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- ObjectProfile Schemas (Unchanged) ---

class ObjectProfileBase(BaseModel):
    name: str
    camera_profile_id: int
    sort_offset_ms: int = 0
    description: Optional[str] = None
    product_id: Optional[int] = None

class ObjectProfileCreate(ObjectProfileBase):
    pass

class ObjectProfileUpdate(BaseModel):
    name: Optional[str] = None
    camera_profile_id: Optional[int] = None
    sort_offset_ms: Optional[int] = None
    product_id: Optional[int] = None
    description: Optional[str] = None

class ObjectProfileOut(ObjectProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    camera_profile: CameraProfileOut
    product: Optional[ProductOut] = None
```

---

### `app/schemas/products.py`

```python
# rpi_counter_fastapi-apintrigation/app/schemas/products.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.product import ProductStatus

class ProductBase(BaseModel):
    name: str
    
    category: Optional[str] = None
    size: Optional[str] = None
    
    description: Optional[str] = None
    version: str = "1.0.0"
    status: ProductStatus = ProductStatus.ACTIVE
    ai_model_path: Optional[str] = "yolov8n.pt"
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

    verify_category: bool = False
    verify_size: bool = False
    verify_defects: bool = False
    verify_ticks: bool = False

    # --- NEW FIELDS FOR GEOMETRIC VALIDATION ---
    target_angle: Optional[float] = None
    angle_tolerance: Optional[float] = None
    min_aspect_ratio: Optional[float] = None
    max_aspect_ratio: Optional[float] = None
    # --- END OF NEW FIELDS ---

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    
    category: Optional[str] = None
    size: Optional[str] = None

    description: Optional[str] = None
    version: Optional[str] = None
    status: Optional[ProductStatus] = None
    ai_model_path: Optional[str] = None
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

    verify_category: Optional[bool] = None
    verify_size: Optional[bool] = None
    verify_defects: Optional[bool] = None
    verify_ticks: Optional[bool] = None

    # --- NEW FIELDS FOR GEOMETRIC VALIDATION ---
    target_angle: Optional[float] = None
    angle_tolerance: Optional[float] = None
    min_aspect_ratio: Optional[float] = None
    max_aspect_ratio: Optional[float] = None
    # --- END OF NEW FIELDS ---

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
```

---

### `app/schemas/detection_event.py`

```python
# rpi_counter_fastapi-dev_new/app/schemas/detection_event.py

from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import Optional
import pytz

from app.models.detection_event import QCResult
from config import settings

# --- Timezone Conversion Helper ---
try:
    LOCAL_TZ = pytz.timezone(settings.TIMEZONE)
except pytz.UnknownTimeZoneError:
    LOCAL_TZ = pytz.utc
# ----------------------------------

class DetectionEventBase(BaseModel):
    timestamp: datetime
    image_path: Optional[str] = None
    qc_result: QCResult
    qc_reason: Optional[str] = None

class DetectionEventOut(DetectionEventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    run_log_id: int

    # --- NEW COMPUTED FIELD FOR LOCAL TIME DISPLAY ---
    @computed_field
    @property
    def timestamp_local(self) -> str:
        """Returns a formatted string of the event time in the configured local timezone."""
        if not self.timestamp:
            return ""
        utc_dt = pytz.utc.localize(self.timestamp)
        local_dt = utc_dt.astimezone(LOCAL_TZ)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S')
    # ----------------------------------------------------
```

---

### `scripts/load_test.py`

```python
#!/usr/bin/env python
"""
A simple asynchronous load testing script.
This script bombards an endpoint with concurrent requests to measure performance.
Requires httpx: pip install httpx
"""
import asyncio
import time
import httpx

# --- Configuration ---
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/system/status" # A lightweight endpoint is good for this
NUM_REQUESTS = 500
CONCURRENCY = 50

async def fetch(client: httpx.AsyncClient):
    """Sends a single GET request."""
    try:
        response = await client.get(f"{BASE_URL}{ENDPOINT}")
        response.raise_for_status()
        return response.status_code
    except httpx.RequestError as e:
        return e

async def run_load_test():
    """Runs the load test with the specified concurrency."""
    print(f"--- Starting Load Test ---")
    print(f"URL: {BASE_URL}{ENDPOINT}")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENCY}")
    print("--------------------------")

    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        
        async def concurrent_fetch():
            async with semaphore:
                return await fetch(client)

        start_time = time.monotonic()
        tasks = [concurrent_fetch() for _ in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
        end_time = time.monotonic()

    total_time = end_time - start_time
    successful_requests = sum(1 for r in results if isinstance(r, int) and r == 200)
    failed_requests = NUM_REQUESTS - successful_requests
    requests_per_second = successful_requests / total_time if total_time > 0 else 0

    print("\n--- Load Test Results ---")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Requests per second (RPS): {requests_per_second:.2f}")
    print("-------------------------")

if __name__ == "__main__":
    asyncio.run(run_load_test())

```

---

### `scripts/system_test.py`

```python
#!/usr/bin/env python
"""
An end-to-end test script for the Box Counter System.
This script simulates a full workflow by interacting with the running
application's API and WebSocket endpoints.

Requires:
- pip install httpx websockets
- The main application must be running.
- APP_ENV must be set to 'development' for the debug endpoint to be active.
"""
import asyncio
import httpx
import websockets
import json

BASE_URL = "http://localhost:8000"
WEBSOCKET_URL = "ws://localhost:8000/ws"

API_HEADERS = {"Content-Type": "application/json"}
# This should match the API_KEY in your .env file
PROTECTED_API_HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": "your_secret_api_key_here" 
}

async def trigger_sensor(sensor_id: int, state: str):
    """Calls the debug API to simulate a sensor event."""
    async with httpx.AsyncClient() as client:
        print(f"TEST: Triggering Sensor {sensor_id} -> {state}")
        payload = {"sensor_id": sensor_id, "new_state": state}
        try:
            res = await client.post(f"{BASE_URL}/api/v1/debug/sensor-event", json=payload, headers=API_HEADERS)
            res.raise_for_status()
            print(f"  -> API Response: {res.json()}")
        except httpx.RequestError as e:
            print(f"FATAL: Could not trigger sensor. Is the app running in 'development' mode?")
            print(f"  -> {e}")
            exit(1)

async def run_test_sequence():
    """Executes the full end-to-end test sequence."""
    print("--- Starting End-to-End System Test ---")

    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✓ WebSocket connection established.")

            # 1. Simulate a full box detection cycle
            print("\n--- Simulating Box Detection ---")
            await trigger_sensor(1, "triggered") # Box enters
            await asyncio.sleep(0.2)
            await trigger_sensor(2, "triggered") # Box reaches end
            await asyncio.sleep(0.1)
            await trigger_sensor(1, "cleared")   # Box leaves first sensor (COUNT!)
            await asyncio.sleep(0.2)
            await trigger_sensor(2, "cleared")   # Box fully exits
            
            # 2. Listen on WebSocket for count update
            print("\n--- Waiting for WebSocket update... ---")
            count_updated = False
            try:
                async for message in websocket:
                    data = json.loads(message)
                    if data.get("type") == "detection_status" and data["data"]["count"] >= 1:
                        print(f"✓ SUCCESS: WebSocket reported new count: {data['data']['count']}")
                        count_updated = True
                        break # Exit the listener loop
                    # Timeout to prevent infinite loop
                    # This is a simplified listener for the test
                    await asyncio.sleep(0.1) # Yield control
            except asyncio.TimeoutError:
                print("✗ FAILURE: Timed out waiting for WebSocket count update.")

            if not count_updated:
                # If the specific message wasn't received after a short while
                print("✗ FAILURE: Did not receive expected WebSocket message.")

            # 3. Reset the counter via API
            print("\n--- Testing Counter Reset API ---")
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/api/v1/detection/reset", headers=API_HEADERS)
                if res.status_code == 200:
                    print(f"✓ SUCCESS: Reset API returned OK.")
                else:
                    print(f"✗ FAILURE: Reset API failed with status {res.status_code}")

            # 4. Test a protected endpoint (Emergency Stop)
            print("\n--- Testing Protected API Endpoint (Emergency Stop) ---")
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/api/v1/system/emergency-stop", headers=PROTECTED_API_HEADERS)
                if res.status_code == 200:
                    print(f"✓ SUCCESS: Protected endpoint returned OK.")
                else:
                    print(f"✗ FAILURE: Protected endpoint failed with status {res.status_code}. Check your API Key.")

    except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError) as e:
        print("\n✗ FATAL: Could not connect to the application.")
        print("Please ensure the FastAPI server is running before executing this test.")
        return

    print("\n--- End-to-End System Test Finished ---")

if __name__ == "__main__":
    asyncio.run(run_test_sequence())

```

---

### `scripts/benchmark.py`

```python
#!/usr/bin/env python
"""
A simple asynchronous benchmarking script to test API endpoint performance.
Requires httpx: pip install httpx
"""
import asyncio
import time
import httpx

# --- Configuration ---
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/system/status"
NUM_REQUESTS = 200
CONCURRENCY = 20

async def fetch(client: httpx.AsyncClient):
    """Sends a single GET request."""
    try:
        response = await client.get(f"{BASE_URL}{ENDPOINT}")
        response.raise_for_status()
        return response.status_code
    except httpx.RequestError as e:
        print(f"An error occurred: {e}")
        return None

async def run_benchmark():
    """Runs the benchmark with the specified concurrency."""
    print(f"--- Starting Benchmark ---")
    print(f"URL: {BASE_URL}{ENDPOINT}")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENCY}")
    print("--------------------------")

    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        
        async def concurrent_fetch():
            async with semaphore:
                return await fetch(client)

        start_time = time.monotonic()
        tasks = [concurrent_fetch() for _ in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
        end_time = time.monotonic()

    total_time = end_time - start_time
    successful_requests = sum(1 for r in results if r == 200)
    failed_requests = NUM_REQUESTS - successful_requests
    requests_per_second = successful_requests / total_time if total_time > 0 else 0

    print("\n--- Benchmark Results ---")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Requests per second (RPS): {requests_per_second:.2f}")
    print("-------------------------")

if __name__ == "__main__":
    asyncio.run(run_benchmark())

```

---

### `config/__init__.py`

```python
"""
This file initializes the settings for the main application and derives
the list of active cameras, providing a single source of truth.
"""
from .settings import get_settings

# Create the global settings object for the main app
settings = get_settings()

# Derive the list of active camera IDs from the loaded settings
ACTIVE_CAMERA_IDS = []
# The CAMERA_MODE is read from the .env file by the AppSettings class
if settings.CAMERA_MODE in ['rpi', 'both']:
    ACTIVE_CAMERA_IDS.append('rpi')
if settings.CAMERA_MODE in ['usb', 'both']:
    ACTIVE_CAMERA_IDS.append('usb')

print(f"[Main App Config] Mode: '{settings.CAMERA_MODE}'. Active cameras: {ACTIVE_CAMERA_IDS}")
```

---

### `config/settings.py`

```python
# rpi_counter_fastapi/config/settings.py

from functools import lru_cache
from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Nested Settings Classes for Core Components ---

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SERVER_', case_sensitive=False)
    HOST: str = "0.0.0.0"
    PORT: int = 8000

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SECURITY_', case_sensitive=False)
    API_KEY: str = "your_secret_api_key_here"
    JWT_SECRET_KEY: str = Field("a_very_secret_key_that_is_at_least_32_chars_long", min_length=32)
    JWT_ALGORITHM: str = "HS256"

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_', case_sensitive=False)
    URL: str = "sqlite+aiosqlite:///./data/box_counter.db"
    ECHO: bool = False
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 30

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_', case_sensitive=False)
    HOST: str = "localhost"
    PORT: int = 6379

class BaseCameraSettings(BaseSettings):
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RpiCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_RPI_', case_sensitive=False)
    ID: str = ""
    SHUTTER_SPEED: int = Field(0, ge=0)
    ISO: int = Field(0, ge=0)
    MANUAL_FOCUS: float = Field(0.0, ge=0.0)

class UsbCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_USB_', case_sensitive=False)
    DEVICE_INDEX: int = 0
    EXPOSURE: int = 0
    GAIN: int = 0
    BRIGHTNESS: int = Field(128, ge=0, le=255)
    AUTOFOCUS: bool = True
    WHITE_BALANCE_TEMP: int = 0

class AiApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AI_API_', case_sensitive=False)
    BASE_URL: str = "http://192.168.88.97:3001"
    QC_MODEL_ID: str = "yolo11m_qc"

class LlmApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LLM_API_', case_sensitive=False)
    BASE_URL: str = "http://192.168.88.81:8000"

class TtsApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TTS_API_', case_sensitive=False)
    BASE_URL: str = "http://localhost:5003"

class OutputChannelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OUTPUTS_', case_sensitive=False)
    CONVEYOR: int = 0
    GATE: int = 1
    DIVERTER: int = 2
    LED_GREEN: int = 3
    LED_RED: int = 4
    CAMERA_LIGHT: int = 5
    BUZZER: int = 6
    CAMERA_LIGHT_TWO: int = 7

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_', case_sensitive=False)
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS_INPUTS: int = 1
    DEVICE_ADDRESS_OUTPUTS: int = 2
    TIMEOUT_SEC: float = 0.5
    POLLING_MS: int = 50

class SensorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SENSORS_', case_sensitive=False)
    ENTRY_CHANNEL: int = 1
    EXIT_CHANNEL: int = 3

class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_', case_sensitive=False)
    VERBOSE_LOGGING: bool = False

class BuzzerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BUZZER_', case_sensitive=False)
    MISMATCH_MS: int = Field(500, description="Buzzer duration in ms for a product size mismatch.")
    MANUAL_TOGGLE_MS: int = Field(200, description="Buzzer duration in ms for a manual toggle from the UI.")
    LOOP_COMPLETE_MS: int = Field(1000, description="Buzzer duration in ms when a batch loop completes.")
    EXIT_SENSOR_MS: int = Field(150, description="Buzzer duration in ms when the exit sensor is triggered.")

class ConveyorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CONVEYOR_', case_sensitive=False)
    SPEED_M_PER_SEC: float = 0.5
    CAMERA_TO_SORTER_DISTANCE_M: float = 1.0
    CONVEYOR_AUTO_STOP_DELAY_SEC: int = Field(2, description="How many seconds the conveyor runs after the last box of a batch is counted before stopping.")
    MAX_TRANSIT_TIME_SEC: float = Field(15.0, gt=0, description="Max time for a product to travel from entry to exit before a failure is triggered.")

class AiStrategySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AI_STRATEGY_', case_sensitive=False)
    YOLO_ENABLED: bool = Field(True, description="Enable/disable the primary YOLO QC analysis.")
    LLM_ENABLED: bool = Field(True, description="Enable/disable all LLM-based summarization features.")
    TTS_ENABLED: bool = Field(True, description="Enable/disable all Text-to-Speech audio feedback.")
    # --- THIS IS THE FIX ---
    LANGUAGE: str = Field("english", description="LLM Language (full name, e.g., 'english', 'bengali').")
    TTS_LANGUAGE: str = Field("en", description="TTS Language (short code, e.g., 'en', 'bn').")
    # --- END OF FIX ---
    REALTIME_TTS_ENGINE: Literal["mac", "xtts", "parler"] = Field("mac", description="TTS engine for instant, per-item feedback.")
    ALERT_ON_PASS: bool = Field(False, description="Enable audio alert for every accepted item.")
    ALERT_ON_REJECT: bool = Field(True, description="Enable audio alert for every rejected item.")
    PASS_TEMPLATE: str = Field("Item {count} accepted.", description="Text template for accepted items.")
    REJECT_TEMPLATE: str = Field("Item {count} rejected. Reason: {defects}.", description="Text template for rejected items.")
    LLM_ITEM_ANALYSIS_ENABLED: bool = Field(True, description="Enable background LLM analysis for each item.")
    LLM_ITEM_WORD_COUNT: int = Field(25, description="Target word count for the per-item LLM summary.")
    SUMMARY_TTS_ENGINE: Literal["parler", "xtts", "mac"] = Field("parler", description="High-quality TTS engine for the end-of-batch summary.")
    SUMMARY_LLM_MODEL: Literal["realtime", "high_quality"] = Field("high_quality", description="LLM model for generating the batch summary.")
    LLM_SUMMARY_WORD_COUNT: int = Field(75, description="Target word count for the detailed batch report.")
    TTS_SUMMARY_CHUNK_COUNT: int = Field(4, ge=1, le=10, description="Number of chunks to split the LLM summary into for pipelined TTS playback.")
    BATCH_COMPLETE_TEMPLATE: str = Field(
        "Batch {batch_id} for {product_name} complete. Total Items: {total_items}, Rejects: {reject_count}.",
        description="Text spoken immediately after a batch finishes."
    )
    NEXT_BATCH_TEMPLATE: str = Field(
        "Next run starting in {countdown}.",
        description="Text spoken before the next batch starts."
    )
    LLM_PROMPT_TEMPLATE: str = Field(
        "You are a helpful assistant on a factory floor. Summarize the following production batch results "
        "with an encouraging but honest tone for the operator. The top defect was {top_defect}. "
        "Batch details: {batch_data}",
        description="The master instruction given to the LLM for batch summarization."
    )


# --- Main AppSettings Container ---
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)
    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "12.0.0-HybridAI"
    APP_ENV: Literal["development", "production"] = "development"
    TIMEZONE: str = "UTC"
    CAMERA_MODE: Literal['rpi', 'usb', 'both', 'none'] = 'both'
    CAMERA_TRIGGER_DELAY_MS: int = 100
    CAMERA_CAPTURES_DIR: str = "web/static/captures"
    UI_ANIMATION_TRANSIT_TIME_SEC: int = Field(5, gt=0)
    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    REDIS: RedisSettings = RedisSettings()
    CAMERA_RPI: RpiCameraSettings = RpiCameraSettings()
    CAMERA_USB: UsbCameraSettings = UsbCameraSettings()
    AI_API: AiApiSettings = AiApiSettings()
    LLM_API: LlmApiSettings = LlmApiSettings()
    TTS_API: TtsApiSettings = TtsApiSettings()
    OUTPUTS: OutputChannelSettings = OutputChannelSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()
    LOGGING: LoggingSettings = LoggingSettings()
    CONVEYOR: ConveyorSettings = ConveyorSettings()
    BUZZER: BuzzerSettings = BuzzerSettings()
    AI_STRATEGY: AiStrategySettings = AiStrategySettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
```

---

### `services/camera_service_rpi.py`

```python
"""
Standalone Camera Service for the Raspberry Pi Camera Module.
FINAL REVISION: This script is now completely self-contained and robust.

- It now checks if the connected camera supports autofocus before attempting
  to set autofocus controls, fixing the AttributeError for fixed-focus cameras
  like the imx219. This makes the script compatible with multiple camera models.
- It correctly finds the numerical index of the camera based on the ID string.
- It continues to listen to the Redis command channel for on-the-fly profile updates.
"""
import time
import cv2
import redis
import traceback
import json
import threading
from pathlib import Path
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Global Camera Object ---
camera = None

# --- Robust Path and Configuration ---
ENV_PATH = Path(__file__).parent.parent / ".env"

class RpiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_prefix='CAMERA_RPI_', case_sensitive=False, extra='ignore')
    ID: str
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_prefix='REDIS_', case_sensitive=False, extra='ignore')
    HOST: str = 'localhost'
    PORT: int = 6379

REDIS_COMMAND_CHANNEL = "camera:commands:rpi"

def apply_camera_settings(settings_dict: dict):
    """Applies a dictionary of settings to the global picamera2 object."""
    global camera
    if camera is None:
        print("[RPI Camera Service] Error: Cannot apply settings, camera is not available.", flush=True)
        return

    print("\n--- Applying New RPi Camera Settings from Command ---", flush=True)
    from picamera2 import controls
    
    controls_to_set = {}
    
    # --- DEFINITIVE FIX: Check if the camera supports Autofocus before setting it ---
    if 'autofocus' in settings_dict:
        # Check the list of available controls for this specific camera model.
        if 'AfMode' in camera.camera_controls:
            af_mode = controls.AfMode.Continuous if settings_dict['autofocus'] else controls.AfMode.Manual
            controls_to_set['AfMode'] = af_mode
            print(f"  -> AF Mode: {af_mode.name}", flush=True)
        else:
            # If the control doesn't exist, inform the user and skip it.
            print("  -> AF Mode: Not supported by this camera model (imx219). Skipping.", flush=True)

    if 'white_balance_temp' in settings_dict:
        controls_to_set['AwbEnable'] = settings_dict['white_balance_temp'] == 0
        print(f"  -> AWB Enable: {controls_to_set['AwbEnable']}", flush=True)
    
    use_auto_exposure = True
    if 'gain' in settings_dict and settings_dict['gain'] > 0:
        controls_to_set['AnalogueGain'] = float(settings_dict['gain'])
        use_auto_exposure = False
        print(f"  -> Manual AnalogueGain: {controls_to_set['AnalogueGain']}", flush=True)
        
    if 'exposure' in settings_dict and settings_dict['exposure'] > 0:
        controls_to_set['ExposureTime'] = settings_dict['exposure']
        use_auto_exposure = False
        print(f"  -> Manual ExposureTime (µs): {controls_to_set['ExposureTime']}", flush=True)

    controls_to_set['AeEnable'] = use_auto_exposure
    print(f"  -> Auto Exposure Enable: {use_auto_exposure}", flush=True)

    if 'brightness' in settings_dict:
        scaled_brightness = (settings_dict['brightness'] / 255.0) * 2.0 - 1.0
        controls_to_set['Brightness'] = scaled_brightness
        print(f"  -> Brightness: {scaled_brightness:.2f}", flush=True)

    if controls_to_set:
        camera.set_controls(controls_to_set)
    print("-------------------------------------------\n", flush=True)

def command_listener(redis_client: redis.Redis):
    """A thread that listens for commands and applies settings."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_COMMAND_CHANNEL)
    print(f"[Command Listener] Subscribed to '{REDIS_COMMAND_CHANNEL}' for live commands.", flush=True)
    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                command = json.loads(message['data'])
                if command.get('action') == 'apply_settings':
                    settings_to_apply = command.get('settings')
                    if isinstance(settings_to_apply, dict):
                        apply_camera_settings(settings_to_apply)
            except Exception as e:
                print(f"[Command Listener] Error processing command: {e}", flush=True)

def main():
    global camera
    try:
        rpi_cam_settings = RpiSettings()
        redis_settings = RedisSettings()
    except ValidationError as e:
        if any(err.get('type') == 'missing' and err.get('loc') == ('ID',) for err in e.errors()):
            print("\n" + "="*60, "\n--- CONFIGURATION ERROR ---")
            print("FATAL: The 'CAMERA_RPI_ID' is missing from your .env file.")
            print("\nTo fix this: run 'libcamera-hello --list-cameras', copy the ID,")
            print(f"and add it to your .env file at: {ENV_PATH}")
            print("\n   CAMERA_RPI_ID='your_camera_id_here'\n" + "="*60 + "\n")
            return
        else:
            raise

    redis_client = None
    try:
        from picamera2 import Picamera2
        
        target_camera_id = rpi_cam_settings.ID
        all_cameras_info = Picamera2.global_camera_info()
        if not all_cameras_info:
            print("FATAL ERROR: No cameras found by the libcamera system. Check hardware connection.")
            return

        camera_index = None
        for i, info in enumerate(all_cameras_info):
            if info['Id'] == target_camera_id:
                camera_index = i
                break
        
        if camera_index is None:
            print("\n" + "="*70, "\n--- CAMERA NOT FOUND ERROR ---")
            print(f"FATAL: The camera ID '{target_camera_id}' from your .env file was NOT FOUND.")
            print("\nAvailable cameras are:")
            for i, info in enumerate(all_cameras_info):
                print(f"  - Index {i}: {info['Id']} ({info['Model']})")
            print("\nPlease ensure the correct ID is copied into your .env file.", "\n" + "="*70 + "\n")
            return
        
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=True)
        redis_client.ping()
        print("[RPI Camera Service] Redis connection successful.", flush=True)

        listener_thread = threading.Thread(target=command_listener, args=(redis_client,), daemon=True)
        listener_thread.start()

        print(f"[RPI Camera Service] Initializing camera at index {camera_index} (ID: {target_camera_id})", flush=True)
        camera = Picamera2(camera_index)
        
        config = camera.create_video_configuration(
            main={"size": (rpi_cam_settings.RESOLUTION_WIDTH, rpi_cam_settings.RESOLUTION_HEIGHT), "format": "RGB888"}
        )
        camera.configure(config)
        camera.set_controls({"FrameRate": rpi_cam_settings.FPS})
        
        # This will now run without crashing, as it will intelligently skip the
        # unsupported autofocus setting.
        apply_camera_settings({'autofocus': True, 'white_balance_temp': 0})
        
        camera.start()
        frame_channel = 'camera:frames:rpi'
        print(f"[RPI Camera Service] Camera started. Publishing to '{frame_channel}'.", flush=True)
        time.sleep(2) 

        while True:
            frame = camera.capture_array()
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, rpi_cam_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())

    except ImportError:
        print("[RPI Camera Service] FATAL ERROR: The 'picamera2' library is not installed.", flush=True)
    except Exception as e:
        print(f"[RPI Camera Service] FATAL ERROR: An unexpected error occurred.", flush=True)
        print(traceback.format_exc(), flush=True)
    finally:
        if 'camera' in locals() and camera and camera.is_open:
            camera.stop()
        if 'redis_client' in locals() and redis_client:
            redis_client.close()
        print("[RPI Camera Service] Exited.", flush=True)

if __name__ == "__main__":
    main()
```

---

### `services/camera_service_usb.py`

```python
# rpi_counter_fastapi-dev2/services/camera_service_usb.py

"""
Standalone Camera Service for a USB V4L2 Camera.
FINAL ARCHITECTURE: This service is now a 'dumb' command receiver.

- It NO LONGER reads camera profiles (exposure, gain, etc.) from any file.
- It loads only essential hardware constants (device index, jpeg quality) from .env.
- It starts up with simple 'auto' settings.
- It listens on a Redis channel for commands from the main application, which
  will tell it which settings to apply on the fly.
- ADDED: Verbose logging to diagnose frame publishing issues.
"""
import time
import cv2
import redis
import traceback
import json
import threading
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Constants and Paths ---
ENV_PATH = Path(__file__).parent.parent / ".env"
REDIS_COMMAND_CHANNEL = "camera:commands:usb"
camera = None # Global camera object

# --- Simple Settings Loader for Essential Hardware Config ONLY ---
class UsbHardwareSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='CAMERA_USB_',
        case_sensitive=False,
        env_file=str(ENV_PATH),
        extra='ignore'
    )
    DEVICE_INDEX: int = 0
    JPEG_QUALITY: int = 90

def apply_camera_settings(settings_dict: dict):
    """Applies a dictionary of settings to the global camera object."""
    global camera
    if camera is None or not camera.isOpened():
        print("[USB Camera Service] Error: Cannot apply settings, camera is not available.", flush=True)
        return

    print("\n--- Applying New Camera Settings from Command ---", flush=True)
    
    autofocus = settings_dict.get('autofocus', True)
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 1 if autofocus else 0)
    print(f"  -> Autofocus: {'On' if autofocus else 'Off'}", flush=True)
    
    wb_temp = settings_dict.get('white_balance_temp', 0)
    if wb_temp > 0:
        camera.set(cv2.CAP_PROP_AUTO_WB, 0)
        camera.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, wb_temp)
        print(f"  -> Manual White Balance: {wb_temp}", flush=True)
    else:
        camera.set(cv2.CAP_PROP_AUTO_WB, 1)
        print(f"  -> Auto White Balance", flush=True)
        
    gain = settings_dict.get('gain', 0)
    if gain >= 0: # Gain can be 0
        camera.set(cv2.CAP_PROP_GAIN, gain)
        print(f"  -> Manual Gain: {gain}", flush=True)
    
    brightness = settings_dict.get('brightness', 128)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print(f"  -> Brightness: {brightness}", flush=True)

    exposure = settings_dict.get('exposure', 0)
    if exposure != 0:
        # Note: The value for AUTO_EXPOSURE can vary. 1 is often 'manual', 3 is 'auto'.
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 
        camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
        print(f"  -> Manual Exposure: {exposure}", flush=True)
    else:
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        print(f"  -> Auto Exposure", flush=True)
    print("-------------------------------------------\n", flush=True)


def command_listener(redis_client: redis.Redis):
    """A thread that listens for commands and applies settings."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_COMMAND_CHANNEL)
    print(f"[Command Listener] Subscribed to '{REDIS_COMMAND_CHANNEL}' for live commands.", flush=True)
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                # Decode bytes to string, then parse JSON
                command_str = message['data'].decode('utf-8')
                command = json.loads(command_str)
                
                if command.get('action') == 'apply_settings':
                    settings_to_apply = command.get('settings')
                    if isinstance(settings_to_apply, dict):
                        apply_camera_settings(settings_to_apply)
            except Exception as e:
                print(f"[Command Listener] Error processing command: {e}", flush=True)

def main():
    global camera
    hardware_settings = UsbHardwareSettings()
    redis_client = None

    try:
        # Connect to Redis, ensuring it handles raw bytes
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
        redis_client.ping()
        print("[USB Camera Service] Redis connection successful.", flush=True)

        listener_thread = threading.Thread(target=command_listener, args=(redis_client,), daemon=True)
        listener_thread.start()

        print(f"[USB Camera Service] Opening camera at index {hardware_settings.DEVICE_INDEX}...", flush=True)
        camera = cv2.VideoCapture(hardware_settings.DEVICE_INDEX, cv2.CAP_V4L2)
        if not camera.isOpened():
            raise RuntimeError(f"Could not open camera at index {hardware_settings.DEVICE_INDEX}.")
        print("[USB Camera Service] Camera opened successfully.", flush=True)

        # Apply default "auto" settings on startup
        apply_camera_settings({})
        
        frame_channel = 'camera:frames:usb'
        print(f"[USB Camera Service] Starting capture loop. Publishing to '{frame_channel}'.", flush=True)
        time.sleep(1)

        frame_count = 0
        last_log_time = time.time()
        while True:
            ret, frame = camera.read()
            if not ret:
                print("[USB Camera Service] WARNING: camera.read() returned False. Check camera connection.", flush=True)
                time.sleep(1) 
                continue

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, hardware_settings.JPEG_QUALITY])
            # Publish the raw bytes of the JPEG image
            redis_client.publish(frame_channel, buffer.tobytes())
            frame_count += 1
            
            # Log status every 5 seconds
            current_time = time.time()
            if current_time - last_log_time >= 5.0:
                print(f"[USB Camera Service] Published {frame_count} frames to '{frame_channel}' in the last 5 seconds.", flush=True)
                frame_count = 0
                last_log_time = current_time

    except Exception as e:
        print(f"[USB Camera Service] FATAL ERROR: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
    finally:
        if camera and camera.isOpened():
            camera.release()
        if redis_client:
            redis_client.close()
        print("[USB Camera Service] Exited.", flush=True)

if __name__ == "__main__":
    main()
```

---

### `tests/test_api.py`

```python
"""
Tests for the FastAPI API endpoints.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Tests the main health check/root endpoint."""
    response = await async_client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_usage" in data
    assert "camera_status" in data
    assert data["camera_status"] == "connected" # From our mock

@pytest.mark.asyncio
async def test_get_detection_status(async_client: AsyncClient):
    """Tests the initial state of the detection endpoint."""
    response = await async_client.get("/api/v1/detection/")
    assert response.status_code == 200
    data = response.json()
    assert data["box_count"] == 0
    assert data["state"] == "IDLE"

@pytest.mark.asyncio
async def test_reset_counter(async_client: AsyncClient):
    """Tests the counter reset functionality."""
    # This is a simple test; a more complex one would simulate a count first.
    response = await async_client.post("/api/v1/detection/reset")
    assert response.status_code == 200
    assert response.json() == {"message": "Counter reset successfully."}
    
    # Verify the count is still 0
    response = await async_client.get("/api/v1/detection/")
    assert response.status_code == 200
    assert response.json()["box_count"] == 0

@pytest.mark.asyncio
async def test_conveyor_control(async_client: AsyncClient):
    """Tests starting and stopping the mock conveyor."""
    # Start the conveyor
    start_response = await async_client.post("/api/v1/gpio/conveyor/start")
    assert start_response.status_code == 200
    assert start_response.json()["message"] == "Conveyor started."

    # Check status
    status_response = await async_client.get("/api/v1/gpio/status")
    assert status_response.json()["conveyor"] == "running"

    # Stop the conveyor
    stop_response = await async_client.post("/api/v1/gpio/conveyor/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["message"] == "Conveyor stopped."
    
    # Check status again
    status_response = await async_client.get("/api/v1/gpio/status")
    assert status_response.json()["conveyor"] == "stopped"

```

---

### `tests/conftest.py`

```python
"""
Pytest configuration file for defining shared fixtures.
"""
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import all necessary components
from main import create_app
from config import settings # FIX: Import the application settings
from app.models.database import Base, get_async_session
from app.core.gpio_controller import AsyncGPIOController
from app.services.detection_service import AsyncDetectionService

# --- Database Setup for Tests ---
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
TestAsyncSessionFactory = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

# --- Auto-use Fixture to Manage Schema ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_schema() -> AsyncGenerator[None, None]:
    """Auto-used fixture to create and drop the database schema for every test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- Session Fixture ---
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a single database session for tests that need it directly."""
    async with TestAsyncSessionFactory() as session:
        yield session

# --- API Test Client Fixture ---
@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provides an async test client that correctly handles the application lifespan."""
    app = create_app()
    app.dependency_overrides[get_async_session] = lambda: db_session
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client

# --- DEFINITIVE FIX: Service Fixture ---
@pytest_asyncio.fixture(scope="function")
async def detection_service(db_session: AsyncSession) -> AsyncDetectionService:
    """
    Provides a fully initialized instance of the AsyncDetectionService
    connected to the clean test database.
    """
    gpio_controller = await AsyncGPIOController.get_instance()
    
    # FIX: The required 'sensor_config' argument is now provided.
    service = AsyncDetectionService(
        gpio_controller=gpio_controller,
        db_session_factory=TestAsyncSessionFactory,
        sensor_config=settings.SENSORS 
    )
    
    # Initialize the service, which will load its state from the (empty) DB.
    await service.initialize()
    return service
```

---

### `tests/test_models.py`

```python
"""
Tests for the SQLAlchemy database models.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# FIX APPLIED HERE: Import Detection and DetectionDirection from their specific module.
from app.models.detection import Detection, DetectionDirection

@pytest.mark.asyncio
async def test_create_detection_record(db_session: AsyncSession):
    """
    Tests the creation and retrieval of a Detection model instance.
    """
    # Create a new detection record
    new_detection = Detection(
        box_count=1,
        detection_direction=DetectionDirection.FORWARD,
        confidence_score=0.95
    )
    db_session.add(new_detection)
    await db_session.commit()
    await db_session.refresh(new_detection)

    # Retrieve it from the database
    result = await db_session.execute(select(Detection).where(Detection.id == new_detection.id))
    retrieved_detection = result.scalar_one()

    assert retrieved_detection is not None
    assert retrieved_detection.id == new_detection.id
    assert retrieved_detection.box_count == 1
    assert retrieved_detection.confidence_score == 0.95
    assert retrieved_detection.detection_direction == DetectionDirection.FORWARD

```

---

### `tests/test_services.py`

```python
"""
Tests for the business logic services.
"""
import pytest
import asyncio

from app.core.sensor_events import SensorEvent, SensorState
from app.services.detection_service import AsyncDetectionService, DetectionState

@pytest.mark.asyncio
async def test_detection_service_state_machine(detection_service: AsyncDetectionService):
    """
    Tests the full state machine logic using a pre-initialized service from a fixture.
    This pattern is robust and ensures the database is correctly set up.
    """
    # The `detection_service` is provided by the fixture in conftest.py,
    # fully initialized and connected to a clean test database.

    assert detection_service._state == DetectionState.IDLE
    assert await detection_service.get_current_count() == 0

    # 1. Box enters - trigger sensor 1
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=1, new_state=SensorState.TRIGGERED))
    assert detection_service._state == DetectionState.ENTERING

    # 2. Box hits second sensor
    await asyncio.sleep(0.2)
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=2, new_state=SensorState.TRIGGERED))
    assert detection_service._state == DetectionState.CONFIRMING_EXIT

    # 3. Box clears first sensor - THIS IS THE COUNTING EVENT
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=1, new_state=SensorState.CLEARED))
    assert detection_service._state == DetectionState.RESETTING
    assert await detection_service.get_current_count() == 1

    # 4. Box fully clears second sensor
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=2, new_state=SensorState.CLEARED))
    assert detection_service._state == DetectionState.IDLE

```
