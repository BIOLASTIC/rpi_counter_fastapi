from fastapi import APIRouter

# Import the MODULES where the routers are defined.
from . import system
from . import detection
from . import outputs
from . import camera
from . import profiles
from . import orchestration

# Create the main router for the v1 API.
api_router = APIRouter()

# Include the `router` OBJECT from each of the imported modules.
# This creates a one-way flow and prevents circular imports.
api_router.include_router(system.router, prefix="/system", tags=["System & Monitoring"])
api_router.include_router(detection.router, prefix="/detection", tags=["Box Detection"])
api_router.include_router(outputs.router, prefix="/outputs", tags=["Hardware Control"])
api_router.include_router(camera.router, prefix="/camera", tags=["Camera"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profile Management"])
api_router.include_router(orchestration.router, prefix="/orchestration", tags=["Run Orchestration"])