"""
REVISED: The import for camera configuration has been fixed.
It no longer imports from the deleted `camera_config.py`. Instead, it imports
`ACTIVE_CAMERA_IDS` from the main application's centralized config module.
The logic has been updated to check for camera IDs in the list.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, EventLog
from config import settings

# --- THE FIX: Import from the main config module, not camera_config ---
from config import ACTIVE_CAMERA_IDS

router = APIRouter(tags=["Web Dashboard"])

def NoCacheTemplateResponse(request: Request, name: str, context: dict):
    templates = request.app.state.templates
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return templates.TemplateResponse(name, context, headers=headers)

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return NoCacheTemplateResponse(request, "dashboard/index.html", {"request": request})

@router.get("/status", response_class=HTMLResponse)
async def read_status_page(request: Request):
    return NoCacheTemplateResponse(request, "dashboard/status.html", {"request": request})

@router.get("/hardware", response_class=HTMLResponse)
async def read_hardware_page(request: Request):
    return NoCacheTemplateResponse(request, "dashboard/hardware.html", {"request": request, "config": settings})

@router.get("/connections", response_class=HTMLResponse)
async def read_connections_page(request: Request):
    return NoCacheTemplateResponse(request, "dashboard/connections.html", {"request": request, "config": settings})

# --- Conditionally add routes based on config ---
# --- THE FIX: Logic now checks if 'rpi' or 'usb' are in the list ---
if 'rpi' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/rpi", response_class=HTMLResponse)
    async def read_live_view_rpi(request: Request):
        # Renamed the template to be more specific
        return NoCacheTemplateResponse(request, "dashboard/live_view_rpi.html", {"request": request})

    @router.get("/gallery/rpi", response_class=HTMLResponse)
    async def read_gallery_rpi(request: Request):
        # Renamed the template to be more specific
        return NoCacheTemplateResponse(request, "dashboard/gallery_rpi.html", {"request": request})

if 'usb' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/usb", response_class=HTMLResponse)
    async def read_live_view_usb(request: Request):
        return NoCacheTemplateResponse(request, "dashboard/live_view_usb.html", {"request": request})

    @router.get("/gallery/usb", response_class=HTMLResponse)
    async def read_gallery_usb(request: Request):
        return NoCacheTemplateResponse(request, "dashboard/gallery_usb.html", {"request": request})

@router.get("/logs", response_class=HTMLResponse)
async def read_logs_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(EventLog).order_by(EventLog.timestamp.desc()).limit(100)
    )
    logs = result.scalars().all()
    context = {"request": request, "logs": logs}
    return NoCacheTemplateResponse(request, "dashboard/logs.html", context)

@router.get("/api-docs", response_class=HTMLResponse)
async def read_api_docs_page(request: Request):
    openapi_schema = request.app.openapi()
    context = {
        "request": request,
        "api_title": openapi_schema.get("info", {}).get("title", "API"),
        "api_version": openapi_schema.get("info", {}).get("version", ""),
        "api_paths": openapi_schema.get("paths", {})
    }
    return NoCacheTemplateResponse(request, "dashboard/api.html", context)