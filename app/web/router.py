"""
FINAL REVISION: The source of the Jinja2 TemplateNotFound error is fixed.
- All template paths in this file have been corrected to remove the 'pages/'
  prefix, matching the new, simplified flat template directory structure.
REVISED: The gallery routes now use a single, dynamic template.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, EventLog, ObjectProfile
from config import settings, ACTIVE_CAMERA_IDS

router = APIRouter(tags=["Web Dashboard"])

def NoCacheTemplateResponse(request: Request, name: str, context: dict):
    """A helper that adds no-cache headers and injects global context."""
    templates = request.app.state.templates
    context['active_camera_ids'] = ACTIVE_CAMERA_IDS
    context['camera_profiles'] = getattr(request.app.state, 'camera_profiles', [])
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return templates.TemplateResponse(name, context, headers=headers)


@router.get("/", response_class=HTMLResponse)
async def read_dashboard(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """Passes the list of object profiles to the main dashboard."""
    result = await db.execute(select(ObjectProfile).order_by(ObjectProfile.name))
    object_profiles = result.scalars().all()
    
    context = {
        "request": request,
        "object_profiles": object_profiles,
        "animation_time": settings.UI_ANIMATION_TRANSIT_TIME_SEC
    }
    return NoCacheTemplateResponse(request, "dashboard.html", context)

@router.get("/profiles", response_class=HTMLResponse)
async def read_profiles_page(request: Request):
    """Renders the main profile management page."""
    return NoCacheTemplateResponse(request, "profiles.html", {"request": request})

@router.get("/status", response_class=HTMLResponse)
async def read_status_page(request: Request):
    return NoCacheTemplateResponse(request, "status.html", {"request": request})

@router.get("/hardware", response_class=HTMLResponse)
async def read_hardware_page(request: Request):
    return NoCacheTemplateResponse(request, "hardware.html", {"request": request, "config": settings})

@router.get("/connections", response_class=HTMLResponse)
async def read_connections_page(request: Request):
    return NoCacheTemplateResponse(request, "connections.html", {"request": request, "config": settings})

# Conditionally add routes based on config
if 'rpi' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/rpi", response_class=HTMLResponse)
    async def read_live_view_rpi(request: Request):
        return NoCacheTemplateResponse(request, "live_view_rpi.html", {"request": request})

    # --- THE FIX: Use the generic 'gallery.html' template ---
    @router.get("/gallery/rpi", response_class=HTMLResponse)
    async def read_gallery_rpi(request: Request):
        # Pass the camera_id to the template
        context = {"request": request, "camera_id": "rpi", "camera_name": "RPi"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

if 'usb' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/usb", response_class=HTMLResponse)
    async def read_live_view_usb(request: Request):
        return NoCacheTemplateResponse(request, "live_view_usb.html", {"request": request})

    # --- THE FIX: Use the generic 'gallery.html' template ---
    @router.get("/gallery/usb", response_class=HTMLResponse)
    async def read_gallery_usb(request: Request):
        # Pass the camera_id to the template
        context = {"request": request, "camera_id": "usb", "camera_name": "USB"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

@router.get("/logs", response_class=HTMLResponse)
async def read_logs_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(EventLog).order_by(EventLog.timestamp.desc()).limit(100)
    )
    logs = result.scalars().all()
    context = {"request": request, "logs": logs}
    return NoCacheTemplateResponse(request, "logs.html", context)

@router.get("/api-docs", response_class=HTMLResponse)
async def read_api_docs_page(request: Request):
    openapi_schema = request.app.openapi()
    context = {
        "request": request,
        "api_title": openapi_schema.get("info", {}).get("title", "API"),
        "api_version": openapi_schema.get("info", {}).get("version", ""),
        "api_paths": openapi_schema.get("paths", {})
    }
    return NoCacheTemplateResponse(request, "api.html", context)