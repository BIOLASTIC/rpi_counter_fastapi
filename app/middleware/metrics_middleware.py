"""
FastAPI middleware to calculate and report request processing time.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.monotonic()
        response = await call_next(request)
        process_time = time.monotonic() - start_time
        response.headers["X-Process-Time-Seconds"] = str(process_time)
        print(f"Request {request.method} {request.url.path} processed in {process_time:.4f} seconds")
        return response
