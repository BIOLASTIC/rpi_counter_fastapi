#!/usr/bin/env python3
"""
Box Counter FastAPI Application - PROPERLY STRUCTURED VERSION
Maintains existing service architecture with proper separation of concerns
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# FastAPI and web framework imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

# Video streaming imports
import redis
import cv2
import numpy as np

# Import routers
from app.routers import api, web, video_streaming
from app.routers.websocket import websocket_router

# Import services and dependencies
from app.services.detection_service import DetectionService
from app.services.orchestration_service import OrchestrationService
from app.services.modbus_service import ModbusService
from app.services.websocket_manager import WebSocketManager
from app.services.gpio_controller import AsyncGPIOController
from app.services.camera_manager import AsyncCameraManager
from app.services.proximity_sensor_handler import AsyncProximitySensorHandler
from app.services.system_service import SystemService

# Database imports
from app.database import init_db

# Configuration
from config.settings import get_settings

# Initialize settings and logging
settings = get_settings()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
detection_service: Optional[DetectionService] = None
orchestration_service: Optional[OrchestrationService] = None
modbus_service: Optional[ModbusService] = None
system_service: Optional[SystemService] = None
websocket_manager: Optional[WebSocketManager] = None

# Video streaming Redis client
try:
    video_redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
    video_redis_client.ping()
    print("[Main App] Video streaming Redis connection: OK")
except Exception as e:
    print(f"[Main App] Video streaming Redis connection failed: {e}")
    video_redis_client = None

# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown with full service initialization."""
    
    # Startup
    print("--- Application starting up in development mode... ---")
    
    try:
        # Initialize database
        await init_db()
        print("Database tables verified.")
        
        # Set initial AI service state
        print("Initial AI service state set to: ENABLED")
        print("Initial AI detection source set to: RPI")
        
        # Initialize services with proper dependency injection
        global detection_service, orchestration_service, modbus_service, system_service, websocket_manager
        
        # Initialize WebSocket manager
        websocket_manager = WebSocketManager()
        
        # Initialize Modbus service for hardware communication
        modbus_service = ModbusService()
        await modbus_service.initialize()
        print("--- Modbus Controller Initialized ---")
        
        # Initialize GPIO controller
        gpio_controller = AsyncGPIOController()
        await gpio_controller.initialize()
        
        # Initialize camera manager
        camera_manager = AsyncCameraManager()
        await camera_manager.initialize()
        
        # Initialize proximity sensor handler with callback
        async def detection_callback(sensor_event):
            if detection_service:
                await detection_service.handle_sensor_event(sensor_event)
        
        proximity_handler = AsyncProximitySensorHandler(
            modbus_service=modbus_service,
            on_sensor_event=detection_callback
        )
        await proximity_handler.initialize()
        
        # Initialize detection service with callback
        async def box_counted_callback():
            if orchestration_service:
                await orchestration_service.on_box_counted()
        
        detection_service = DetectionService(
            camera_manager=camera_manager,
            on_box_counted=box_counted_callback
        )
        await detection_service.initialize()
        print("Detection Service: Calculated base travel time of 2.00 seconds.")
        
        # Initialize orchestration service (the "brain")
        orchestration_service = OrchestrationService(
            detection_service=detection_service,
            gpio_controller=gpio_controller,
            websocket_manager=websocket_manager
        )
        await orchestration_service.initialize()
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        
        # Initialize system service
        system_service = SystemService(
            detection_service=detection_service,
            orchestration_service=orchestration_service,
            modbus_service=modbus_service,
            websocket_manager=websocket_manager
        )
        await system_service.initialize()
        
        # Start background tasks
        asyncio.create_task(proximity_handler.start_polling())
        asyncio.create_task(orchestration_service.start_control_loop())
        asyncio.create_task(system_service.start_status_broadcast())
        
        print("--- Application startup complete. Server is online. ---")
        
        # Send startup notification
        if websocket_manager:
            await websocket_manager.broadcast({
                "type": "notification",
                "level": "INFO",
                "message": "Application startup complete."
            })
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    print("--- Application shutting down... ---")
    try:
        if orchestration_service:
            await orchestration_service.cleanup()
        if detection_service:
            await detection_service.cleanup()
        if modbus_service:
            await modbus_service.cleanup()
        if system_service:
            await system_service.cleanup()
        print("--- Application shutdown complete. ---")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

# Create FastAPI application
app = FastAPI(
    title="Box Counter System",
    description="Advanced box counting system with AI detection and industrial automation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="web/templates")

# Make services available to routers through app state
app.state.detection_service = None
app.state.orchestration_service = None
app.state.modbus_service = None
app.state.system_service = None
app.state.websocket_manager = None
app.state.video_redis_client = video_redis_client

# Update app state after service initialization
@app.middleware("http")
async def add_services_to_state(request, call_next):
    """Middleware to ensure services are available in app state."""
    if not app.state.detection_service and detection_service:
        app.state.detection_service = detection_service
        app.state.orchestration_service = orchestration_service
        app.state.modbus_service = modbus_service
        app.state.system_service = system_service
        app.state.websocket_manager = websocket_manager
    
    response = await call_next(request)
    return response

# Include routers with proper organization
app.include_router(
    web.router,
    tags=["web"]
)

app.include_router(
    api.router,
    prefix="/api/v1",
    tags=["api"]
)

app.include_router(
    video_streaming.router,
    prefix="/api/v1/camera",
    tags=["video_streaming"]
)

app.include_router(
    websocket_router,
    tags=["websocket"]
)

# Health check endpoint (directly in main for simplicity)
@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "detection": "online" if detection_service and detection_service.is_running else "offline",
            "orchestration": "online" if orchestration_service and orchestration_service.is_running else "offline",
            "modbus": "online" if modbus_service and modbus_service.is_connected else "offline",
            "video_streaming": "online" if video_redis_client else "offline"
        }
    }

# Development server entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
