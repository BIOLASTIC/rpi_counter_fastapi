"""Routes for serving the HTML web dashboard and new pages."""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, EventLog
from config import settings

router = APIRouter(tags=["Web Dashboard"])

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("dashboard/index.html", {"request": request})

@router.get("/status", response_class=HTMLResponse)
async def read_status_page(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("dashboard/status.html", {"request": request})

@router.get("/hardware", response_class=HTMLResponse)
async def read_hardware_page(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("dashboard/hardware.html", {"request": request, "config": settings})

@router.get("/logs", response_class=HTMLResponse)
async def read_logs_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    templates = request.app.state.templates
    result = await session.execute(
        select(EventLog).order_by(EventLog.timestamp.desc()).limit(100)
    )
    logs = result.scalars().all()
    return templates.TemplateResponse("dashboard/logs.html", {"request": request, "logs": logs})

@router.get("/api-docs", response_class=HTMLResponse)
async def read_api_docs_page(request: Request):
    """
    This route generates a custom API documentation page.
    It fetches the auto-generated OpenAPI schema from the FastAPI app instance.
    """
    templates = request.app.state.templates
    # The openapi_schema is a dictionary containing all API info
    openapi_schema = request.app.openapi()
    return templates.TemplateResponse("dashboard/api.html", {
        "request": request,
        "api_title": openapi_schema.get("info", {}).get("title", "API"),
        "api_version": openapi_schema.get("info", {}).get("version", ""),
        "api_paths": openapi_schema.get("paths", {})
    })
