# rpi_counter_fastapi-apintrigation/main.py

import asyncio
from contextlib import asynccontextmanager
import json
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import redis.asyncio as redis

PROJECT_ROOT = Path(__file__).parent
from config import settings, ACTIVE_CAMERA_IDS
from app.models.database import engine, Base, AsyncSessionFactory
from app.api.v1 import api_router as api_v1_router
from app.web.router import router as web_router
from app.websocket.router import router as websocket_router
from app.middleware.metrics_middleware import MetricsMiddleware
if settings.APP_ENV == "development":
    from app.api.v1 import debug as debug_router
from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.modbus_poller import AsyncModbusPoller
from app.services.detection_service import AsyncDetectionService
from app.services.system_service import AsyncSystemService
from app.services.notification_service import AsyncNotificationService
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.audio_service import AsyncAudioService
from app.websocket.connection_manager import manager as websocket_manager

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
    
    app.state.redis_client = redis.from_url("redis://localhost")

    app.state.audio_service = AsyncAudioService(db_session_factory=AsyncSessionFactory)
    app.state.modbus_controller = await AsyncModbusController.get_instance()
    app.state.orchestration_service = AsyncOrchestrationService(
        modbus_controller=app.state.modbus_controller,
        db_session_factory=AsyncSessionFactory,
        redis_client=app.state.redis_client,
        app_settings=settings,
        audio_service=app.state.audio_service
    )
    app.state.notification_service = AsyncNotificationService(db_session_factory=AsyncSessionFactory)
    app.state.camera_manager = AsyncCameraManager(
        notification_service=app.state.notification_service,
        captures_dir=settings.CAMERA_CAPTURES_DIR,
        redis_client=app.state.redis_client,
        active_camera_ids=ACTIVE_CAMERA_IDS
    )
    app.state.detection_service = AsyncDetectionService(
        modbus_controller=app.state.modbus_controller,
        camera_manager=app.state.camera_manager,
        orchestration_service=app.state.orchestration_service,
        redis_client=app.state.redis_client,
        conveyor_settings=settings.CONVEYOR,
        db_session_factory=AsyncSessionFactory,
        active_camera_ids=ACTIVE_CAMERA_IDS,
        audio_service=app.state.audio_service
    )
    app.state.modbus_poller = AsyncModbusPoller(
        modbus_controller=app.state.modbus_controller,
        event_callback=app.state.detection_service.handle_sensor_event,
        sensor_config=settings.SENSORS
    )
    app.state.system_service = AsyncSystemService(
        modbus_controller=app.state.modbus_controller,
        modbus_poller=app.state.modbus_poller,
        camera_manager=app.state.camera_manager,
        detection_service=app.state.detection_service,
        orchestration_service=app.state.orchestration_service,
        settings=settings
    )
    
    # --- THIS IS THE DEFINITIVE FIX ---
    # Inject the detection_service into the orchestration_service after both are initialized.
    # This breaks the circular dependency and allows orchestration to control detection state.
    app.state.orchestration_service.set_detection_service(app.state.detection_service)
    # --- END OF FIX ---

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
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    async def qc_image_broadcaster():
        pubsub_client = redis.from_url("redis://localhost")
        pubsub = pubsub_client.pubsub()
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
                    print(f"QC Image Broadcaster: Sent new image data to UI: {image_data}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in QC Image Broadcaster loop: {e}")
                await asyncio.sleep(5)
        await pubsub_client.close()

    
    app.state.broadcast_task = asyncio.create_task(broadcast_updates())
    app.state.qc_broadcast_task = asyncio.create_task(qc_image_broadcaster())
    
    await app.state.notification_service.send_alert("INFO", "Application startup complete.")
    await app.state.audio_service.play_sound_for_event("startup_complete")
    print("--- Application startup complete. Server is online. ---")

    yield

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
    app.include_router(web_router)
    app.include_router(websocket_router)
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
    app.state.templates = Jinja2Templates(directory=str(PROJECT_ROOT / "web/templates"))
    return app

app = create_app()