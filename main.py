"""
FINAL REVISION: Reduces the WebSocket broadcast delay for a more
responsive UI, complementing the faster sensor polling settings.
"""
import asyncio
import time
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

from config import settings
from app.models.database import engine, Base, AsyncSessionFactory
from app.api.v1 import api_router as api_v1_router
from app.api.v1 import orchestration as orchestration_router
from app.web.router import router as web_router
from app.websocket.router import router as websocket_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

if settings.APP_ENV == "development":
    from app.api.v1 import debug as debug_router

# Import all components
from app.core.gpio_controller import AsyncGPIOController
from app.core.camera_manager import AsyncCameraManager
from app.core.usr8000_client import AsyncUSRIOController
from app.core.proximity_sensor import AsyncProximitySensorHandler
from app.services.detection_service import AsyncDetectionService
from app.services.system_service import AsyncSystemService
from app.services.notification_service import AsyncNotificationService
from app.services.orchestration_service import AsyncOrchestrationService
from app.websocket.connection_manager import manager as websocket_manager
from app.middleware.metrics_middleware import MetricsMiddleware

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
    Path(settings.CAMERA.CAPTURES_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Image capture directory '{settings.CAMERA.CAPTURES_DIR}' is ready.")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified.")

    app.state.gpio_controller = await AsyncGPIOController.get_instance()
    
    app.state.orchestration_service = AsyncOrchestrationService(
        gpio=app.state.gpio_controller
    )
    await app.state.orchestration_service.initialize_hardware_state()

    app.state.notification_service = AsyncNotificationService(
        gpio_controller=app.state.gpio_controller,
        db_session_factory=AsyncSessionFactory
    )
    app.state.camera_manager = AsyncCameraManager(
        notification_service=app.state.notification_service
    )
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

    app.state.notification_service.start()
    app.state.sensor_handler.start()
    app.state.camera_manager.start()
    
    async def broadcast_updates():
        while True:
            try:
                # Get status from all services
                system_status = await app.state.system_service.get_system_status()
                count_status = { "total_count": await app.state.detection_service.get_current_total_count() }
                orchestration_status = app.state.orchestration_service.get_status()
                
                # Add image paths to the system status payload
                system_status['last_event_image'] = app.state.camera_manager.get_last_event_image_path()
                system_status['last_surveillance_image'] = app.state.camera_manager.get_last_surveillance_image_path()

                # Broadcast all statuses
                await websocket_manager.broadcast_json({"type": "system_status", "data": system_status})
                await websocket_manager.broadcast_json({"type": "detection_status", "data": count_status})
                await websocket_manager.broadcast_json({"type": "orchestration_status", "data": orchestration_status})

                # --- PERFORMANCE FIX: Send updates 10x faster ---
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    app.state.broadcast_task = asyncio.create_task(broadcast_updates())
    
    await app.state.notification_service.send_alert("INFO", "Application startup complete.")
    print("--- Application startup complete. Server is online. ---")
    yield
    
    print("--- Application shutting down... ---")
    app.state.broadcast_task.cancel()
    await app.state.sensor_handler.stop()
    app.state.notification_service.stop()
    await app.state.camera_manager.stop()
    await app.state.gpio_controller.shutdown()
    await engine.dispose()
    print("--- Application shutdown complete. ---")

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    
    app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")
    app.mount("/captures", NoCacheStaticFiles(directory=settings.CAMERA.CAPTURES_DIR), name="captures")
    
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(orchestration_router.router, prefix="/api/v1/orchestration", tags=["Orchestration"])
    app.include_router(web_router)
    app.include_router(websocket_router)
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
    return app

app = create_app()
app.state.templates = Jinja2Templates(directory="templates")