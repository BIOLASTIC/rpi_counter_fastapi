from fastapi import APIRouter
from . import system, detection, gpio, camera, profiles, orchestration

api_router = APIRouter()

# This file acts as a "switchboard" for all the v1 API endpoints.
# Each line below connects another file's routes to the main app.

api_router.include_router(system.router, prefix="/system", tags=["System & Monitoring"])
api_router.include_router(detection.router, prefix="/detection", tags=["Box Detection"])
api_router.include_router(gpio.router, prefix="/gpio", tags=["Hardware Control"])
api_router.include_router(camera.router, prefix="/camera", tags=["Camera"])

# --- THE CRITICAL FIX IS HERE ---
# These two lines register the new endpoints for managing and controlling
# production runs and profiles. Without them, the application doesn't
# know those routes exist, causing the 404 Not Found error.
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profile Management"])
api_router.include_router(orchestration.router, prefix="/orchestration", tags=["Run Orchestration"])