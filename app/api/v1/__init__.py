from fastapi import APIRouter
from . import system, detection, gpio, camera

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["System & Monitoring"])
api_router.include_router(detection.router, prefix="/detection", tags=["Box Detection"])
api_router.include_router(gpio.router, prefix="/gpio", tags=["Hardware Control"])
api_router.include_router(camera.router, prefix="/camera", tags=["Camera"])
