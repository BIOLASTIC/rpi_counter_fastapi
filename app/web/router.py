# rpi_counter_fastapi-dev2/app/web/router.py

"""
Web routes for serving HTML pages.
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path
import markdown2 

from app.models import get_async_session, EventLog, ObjectProfile
from config import settings, ACTIVE_CAMERA_IDS

router = APIRouter(tags=["Web Dashboard"])
PROJECT_ROOT = Path(__file__).parent.parent.parent # Define project root

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
async def read_dashboard(request: Request, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ObjectProfile).order_by(ObjectProfile.name))
    object_profiles = result.scalars().all()
    context = {"request": request, "object_profiles": object_profiles, "animation_time": settings.UI_ANIMATION_TRANSIT_TIME_SEC}
    return NoCacheTemplateResponse(request, "dashboard.html", context)

@router.get("/management/recipes", response_class=HTMLResponse)
async def read_profiles_page(request: Request):
    return NoCacheTemplateResponse(request, "profiles.html", {"request": request})

@router.get("/management/products", response_class=HTMLResponse)
async def read_products_page(request: Request):
    return NoCacheTemplateResponse(request, "products.html", {"request": request})

@router.get("/management/operators", response_class=HTMLResponse)
async def read_operators_page(request: Request):
    return NoCacheTemplateResponse(request, "operators.html", {"request": request})

@router.get("/status", response_class=HTMLResponse)
async def read_status_page(request: Request):
    return NoCacheTemplateResponse(request, "status.html", {"request": request})

@router.get("/hardware", response_class=HTMLResponse)
async def read_hardware_page(request: Request):
    return NoCacheTemplateResponse(request, "hardware.html", {"request": request, "config": settings})
    
@router.get("/run-history", response_class=HTMLResponse)
async def read_run_history_page(request: Request):
    return NoCacheTemplateResponse(request, "run_history.html", {"request": request})

# --- NEW ROUTE FOR QC TESTING PAGE ---
@router.get("/qc-testing", response_class=HTMLResponse)
async def read_qc_testing_page(request: Request):
    """Serves the manual QC API testing page."""
    return NoCacheTemplateResponse(request, "qc_testing.html", {"request": request})
# --- END NEW ROUTE ---

@router.get("/help/{page_name}", response_class=HTMLResponse)
async def read_help_page(request: Request, page_name: str):
    """
    Reads a markdown file from the docs/manuals directory, converts it to HTML,
    and renders it in a template.
    """
    # Sanitize page_name to prevent directory traversal attacks
    if ".." in page_name or "/" in page_name:
        raise HTTPException(status_code=404, detail="Help page not found.")

    file_path = PROJECT_ROOT / "docs" / "manuals" / f"{page_name}.md"
    
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Help page not found.")
        
    # Read markdown content
    markdown_text = file_path.read_text()
    
    # Convert to HTML
    html_content = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "admonitions"])
    
    # Capitalize the title for display
    title = page_name.replace("_", " ").capitalize()
    
    context = {"request": request, "title": title, "content": html_content}
    return NoCacheTemplateResponse(request, "help.html", context)

@router.get("/connections", response_class=HTMLResponse)
async def read_connections_page(request: Request):
    return NoCacheTemplateResponse(request, "connections.html", {"request": request, "config": settings})

if 'rpi' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/rpi", response_class=HTMLResponse)
    async def read_live_view_rpi(request: Request):
        return NoCacheTemplateResponse(request, "live_view_rpi.html", {"request": request})
    @router.get("/gallery/rpi", response_class=HTMLResponse)
    async def read_gallery_rpi(request: Request):
        context = {"request": request, "camera_id": "rpi", "camera_name": "RPi"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

if 'usb' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/usb", response_class=HTMLResponse)
    async def read_live_view_usb(request: Request):
        return NoCacheTemplateResponse(request, "live_view_usb.html", {"request": request})
    @router.get("/gallery/usb", response_class=HTMLResponse)
    async def read_gallery_usb(request: Request):
        context = {"request": request, "camera_id": "usb", "camera_name": "USB"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

@router.get("/logs", response_class=HTMLResponse)
async def read_logs_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(EventLog).order_by(EventLog.timestamp.desc()).limit(100))
    logs = result.scalars().all()
    context = {"request": request, "logs": logs}
    return NoCacheTemplateResponse(request, "logs.html", context)

@router.get("/api-docs", response_class=HTMLResponse)
async def read_api_docs_page(request: Request):
    openapi_schema = request.app.openapi()
    context = {"request": request, "api_title": openapi_schema.get("info", {}).get("title", "API"), "api_version": openapi_schema.get("info", {}).get("version", ""), "api_paths": openapi_schema.get("paths", {})}
    return NoCacheTemplateResponse(request, "api.html", context)

@router.get("/analytics", response_class=HTMLResponse)
async def read_analytics_page(request: Request):
    """Serves the analytics dashboard page."""
    return NoCacheTemplateResponse(request, "analytics.html", {"request": request})    