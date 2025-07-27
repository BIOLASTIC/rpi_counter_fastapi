"""
FINAL REVISION: Injects the SENSORS configuration object into the
SystemService to ensure it uses the correct channels for status reporting.
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import settings
from app.models.database import engine, Base, AsyncSessionFactory
from app.api.v1 import api_router as api_v1_router
from app.web.router import router as web_router
from app.websocket.router import router as websocket_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
from app.websocket.connection_manager import manager as websocket_manager
from app.middleware.metrics_middleware import MetricsMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... (startup sequence is mostly the same) ...
    print(f"--- Application starting up in {settings.APP_ENV} mode... ---")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified.")

    # Initialization Sequence
    app.state.gpio_controller = await AsyncGPIOController.get_instance()
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
        sensor_config=settings.SENSORS
    )
    await app.state.detection_service.initialize()

    app.state.sensor_handler = AsyncProximitySensorHandler(
        io_controller=app.state.io_controller,
        event_callback=app.state.detection_service.handle_sensor_event
    )
    
    # DEFINITIVE FIX: Inject the SENSORS config into the SystemService
    app.state.system_service = AsyncSystemService(
        gpio_controller=app.state.gpio_controller,
        camera_manager=app.state.camera_manager,
        sensor_handler=app.state.sensor_handler,
        db_session_factory=AsyncSessionFactory,
        sensor_config=settings.SENSORS # Pass the new settings object
    )

    # Start Background Services
    app.state.notification_service.start()
    app.state.sensor_handler.start()
    app.state.camera_manager.start()
    
    # WebSocket broadcast task
    async def broadcast_updates():
        while True:
            try:
                status = await app.state.system_service.get_system_status()
                count_status = { "count": await app.state.detection_service.get_current_count(), "state": app.state.detection_service._state.name }
                await websocket_manager.broadcast_json({"type": "system_status", "data": status})
                await websocket_manager.broadcast_json({"type": "detection_status", "data": count_status})
                await asyncio.sleep(2)
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
    # ... (shutdown logic is unchanged)
    app.state.broadcast_task.cancel()
    await app.state.sensor_handler.stop()
    app.state.notification_service.stop()
    await app.state.camera_manager.stop()
    await app.state.gpio_controller.shutdown()
    await engine.dispose()
    print("--- Application shutdown complete. ---")

def create_app() -> FastAPI:
    # ... (create_app is unchanged)
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(web_router)
    app.include_router(websocket_router)
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
    return app

app = create_app()
app.state.templates = Jinja2Templates(directory="templates")
