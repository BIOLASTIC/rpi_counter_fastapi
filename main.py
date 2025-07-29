"""
FINAL REVISION: The main application entry point, now fully corrected.
- It no longer imports the problematic `camera_config.py`.
- It correctly imports `settings` and the derived `ACTIVE_CAMERA_IDS` list from the
  main `config` module, which is the application's single source of truth.
- It correctly sets `app.state.active_camera_ids` during the lifespan startup, making
  the camera configuration available to the Jinja2 templates. This resolves the
  `UndefinedError`.
"""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

# The definitive source for application settings and derived configurations
from config import settings, ACTIVE_CAMERA_IDS
from app.models.database import engine, Base, AsyncSessionFactory
from app.api.v1 import api_router as api_v1_router
from app.api.v1 import orchestration as orchestration_router
from app.web.router import router as web_router
from app.websocket.router import router as websocket_router
from app.middleware.metrics_middleware import MetricsMiddleware

if settings.APP_ENV == "development":
    from app.api.v1 import debug as debug_router

# Import all application components
from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.usr8000_client import AsyncUSRIOController
from app.core.proximity_sensor import AsyncProximitySensorHandler
from app.services.detection_service import AsyncDetectionService
from app.services.system_service import AsyncSystemService
from app.services.notification_service import AsyncNotificationService
from app.services.orchestration_service import AsyncOrchestrationService
from app.websocket.connection_manager import manager as websocket_manager

class NoCacheStaticFiles(StaticFiles):
    """Static files with cache-control headers to prevent stale browser caches."""
    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application's startup and shutdown events."""
    print(f"--- Application starting up in {settings.APP_ENV} mode... ---")

    # Create base and sub-directories for captures for all active cameras
    base_captures_dir = Path(settings.CAMERA_CAPTURES_DIR)
    base_captures_dir.mkdir(parents=True, exist_ok=True)
    for cam_id in ACTIVE_CAMERA_IDS:
        (base_captures_dir / cam_id).mkdir(exist_ok=True)
    print(f"Image capture directory '{settings.CAMERA_CAPTURES_DIR}' ready for: {ACTIVE_CAMERA_IDS}.")

    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified.")

    # Initialize all services and controllers
    app.state.gpio_controller = await AsyncGPIOController.get_instance()
    
    app.state.notification_service = AsyncNotificationService(
        gpio_controller=app.state.gpio_controller,
        db_session_factory=AsyncSessionFactory
    )
    
    app.state.camera_manager = AsyncCameraManager(
        notification_service=app.state.notification_service,
        captures_dir=settings.CAMERA_CAPTURES_DIR
    )
    
    app.state.orchestration_service = AsyncOrchestrationService(
        gpio=app.state.gpio_controller
    )
    await app.state.orchestration_service.initialize_hardware_state()

    app.state.io_controller = AsyncUSRIOController()
    
    app.state.detection_service = AsyncDetectionService(
        gpio_controller=app.state.gpio_controller,
        db_session_factory=AsyncSessionFactory,
        sensor_config=settings.SENSORS,
        camera_manager=app.state.camera_manager,
        on_box_counted=app.state.orchestration_service.on_box_counted
    )
    await app.state.detection_service.initialize()

    app.state.sensor_handler = AsyncProximitySensorHandler(
        io_controller=app.state.io_controller,
        event_callback=app.state.detection_service.handle_sensor_event
    )
    
    app.state.system_service = AsyncSystemService(
        gpio_controller=app.state.gpio_controller,
        camera_manager=app.state.camera_manager,
        sensor_handler=app.state.sensor_handler,
        db_session_factory=AsyncSessionFactory,
        sensor_config=settings.SENSORS
    )

    # This makes the active camera list available to all templates via `request.app.state`.
    app.state.active_camera_ids = ACTIVE_CAMERA_IDS

    # Start all background tasks
    app.state.notification_service.start()
    app.state.sensor_handler.start()
    app.state.camera_manager.start()

    async def broadcast_updates():
        """The main websocket loop that pushes data to the frontend."""
        while True:
            try:
                system_status = await app.state.system_service.get_system_status()
                count_status = { "total_count": await app.state.detection_service.get_current_total_count() }
                orchestration_status = app.state.orchestration_service.get_status()
                
                system_status['camera_statuses'] = app.state.camera_manager.get_all_health_statuses()
                system_status['last_event_images'] = {
                    cam_id: app.state.camera_manager.get_last_event_image_path(cam_id)
                    for cam_id in ACTIVE_CAMERA_IDS
                }

                # Broadcast all status updates
                await websocket_manager.broadcast_json({"type": "system_status", "data": system_status})
                await websocket_manager.broadcast_json({"type": "detection_status", "data": count_status})
                await websocket_manager.broadcast_json({"type": "orchestration_status", "data": orchestration_status})

                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    app.state.broadcast_task = asyncio.create_task(broadcast_updates())
    
    await app.state.notification_service.send_alert("INFO", "Application startup complete.")
    print("--- Application startup complete. Server is online. ---")
    
    yield # The application is now running
    
    print("--- Application shutting down... ---")
    app.state.broadcast_task.cancel()
    await app.state.sensor_handler.stop()
    app.state.notification_service.stop()
    await app.state.camera_manager.stop()
    await app.state.gpio_controller.shutdown()
    await engine.dispose()
    print("--- Application shutdown complete. ---")

def create_app() -> FastAPI:
    """Creates and configures the main FastAPI application instance."""
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    
    # Add middleware
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    
    # Mount static directories
    app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")
    app.mount("/captures", NoCacheStaticFiles(directory=settings.CAMERA_CAPTURES_DIR), name="captures")
    
    # Include all API and web routers
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(orchestration_router.router, prefix="/api/v1/orchestration", tags=["Orchestration"])
    app.include_router(web_router)
    app.include_router(websocket_router)
    
    # Conditionally include debug router
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
        
    return app

# Main application instance
app = create_app()
app.state.templates = Jinja2Templates(directory="templates")