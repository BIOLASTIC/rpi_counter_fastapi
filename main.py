"""
The main application entry point.

FINAL REVISION: Implements a total containment strategy for the unstable
get_system_status function. The call within the main broadcast loop is now
wrapped in its own try/except block. This is the definitive fix to prevent
its internal errors (e.g., "unhashable type: 'dict'") from crashing the
primary WebSocket broadcast, ensuring the rest of the application remains
operational even if system monitoring fails.
"""
import asyncio
from contextlib import asynccontextmanager
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

# Import all core services
from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.modbus_poller import AsyncModbusPoller
from app.services.detection_service import AsyncDetectionService
from app.services.system_service import AsyncSystemService
from app.services.notification_service import AsyncNotificationService
from app.services.orchestration_service import AsyncOrchestrationService
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

    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified.")

    # Initialize Redis client
    app.state.redis_client = redis.from_url("redis://localhost", decode_responses=True)

    # Set initial states in Redis from config
    initial_ai_state = "true" if settings.AI_SERVICE_ENABLED_BY_DEFAULT else "false"
    await app.state.redis_client.set(settings.REDIS_KEYS.AI_ENABLED_KEY, initial_ai_state)
    print(f"Initial AI service state set to: {'ENABLED' if settings.AI_SERVICE_ENABLED_BY_DEFAULT else 'DISABLED'}")

    await app.state.redis_client.set(settings.REDIS_KEYS.AI_DETECTION_SOURCE_KEY, settings.AI_DETECTION_SOURCE)
    print(f"Initial AI detection source set to: {settings.AI_DETECTION_SOURCE.upper()}")


    # Initialize all application services in the correct dependency order
    app.state.modbus_controller = await AsyncModbusController.get_instance()
    app.state.orchestration_service = AsyncOrchestrationService(
        modbus_controller=app.state.modbus_controller,
        db_session_factory=AsyncSessionFactory,
        redis_client=app.state.redis_client,
        settings=settings
    )
    app.state.notification_service = AsyncNotificationService(db_session_factory=AsyncSessionFactory)
    app.state.camera_manager = AsyncCameraManager(
        notification_service=app.state.notification_service,
        captures_dir=settings.CAMERA_CAPTURES_DIR
    )
    app.state.detection_service = AsyncDetectionService(
        modbus_controller=app.state.modbus_controller,
        camera_manager=app.state.camera_manager,
        orchestration_service=app.state.orchestration_service,
        conveyor_settings=settings.CONVEYOR,
        redis_client=app.state.redis_client,
        settings=settings
    )
    app.state.modbus_poller = AsyncModbusPoller(
        modbus_controller=app.state.modbus_controller,
        event_callback=app.state.detection_service.handle_sensor_event
    )
    app.state.system_service = AsyncSystemService(
        modbus_controller=app.state.modbus_controller,
        modbus_poller=app.state.modbus_poller,
        camera_manager=app.state.camera_manager,
        detection_service=app.state.detection_service,
        orchestration_service=app.state.orchestration_service,
        db_session_factory=AsyncSessionFactory,
        sensor_config=settings.SENSORS,
        output_config=settings.OUTPUTS,
        redis_client=app.state.redis_client,
        settings=settings
    )

    # Set initial hardware state to safe default
    await app.state.orchestration_service.initialize_hardware_state()
    app.state.active_camera_ids = ACTIVE_CAMERA_IDS

    # Start all background tasks managed by the main application
    app.state.notification_service.start()
    app.state.modbus_poller.start()
    app.state.camera_manager.start()

    # The broadcast loop for sending status updates to the UI
    async def broadcast_updates():
        while True:
            try:
                # --- THE DEFINITIVE FIX: Isolate the failing call ---
                system_status = None
                try:
                    # 1. Attempt the call that has been failing.
                    system_status = await app.state.system_service.get_system_status()
                except Exception as e:
                    # 2. If it crashes for ANY reason, log the error but DO NOT crash the loop.
                    print(f"CRITICAL WARNING: The get_system_status() function failed with error: {e}. The broadcast loop will continue.")
                    # 3. Create a safe, default payload to send to the UI.
                    system_status = {"error": "Failed to fetch system status."}
                
                # The rest of the loop proceeds normally, using either the real status or the safe default.
                orchestration_status = app.state.orchestration_service.get_status()
                
                await websocket_manager.broadcast_json({"type": "system_status", "data": system_status})
                await websocket_manager.broadcast_json({"type": "orchestration_status", "data": orchestration_status})
                
                await asyncio.sleep(0.5)

            except asyncio.CancelledError:
                break
            except Exception as e:
                # This outer block catches errors from other parts of the loop (e.g., orchestration)
                print(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    app.state.broadcast_task = asyncio.create_task(broadcast_updates())
    await app.state.notification_service.send_alert("INFO", "Application startup complete.")
    print("--- Application startup complete. Server is online. ---")

    yield

    # Graceful shutdown sequence
    print("--- Application shutting down... ---")
    await app.state.redis_client.close()
    app.state.broadcast_task.cancel()
    await app.state.modbus_poller.stop()
    app.state.notification_service.stop()
    await app.state.camera_manager.stop()
    await app.state.modbus_controller.disconnect()
    await engine.dispose()
    print("--- Application shutdown complete. ---")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    
    # Serve static files and captured images
    app.mount("/static", NoCacheStaticFiles(directory=PROJECT_ROOT / "web/static"), name="static")
    app.mount("/captures", NoCacheStaticFiles(directory=PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR), name="captures")
    
    # Include all API and web routers
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(web_router)
    app.include_router(websocket_router)
    
    # Conditionally include debug routes if in development mode
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
        
    app.state.templates = Jinja2Templates(directory=str(PROJECT_ROOT / "web/templates"))
    return app

app = create_app()