"""
FastAPI dependencies for handling security aspects like API key auth and rate limiting.
"""
import time
from typing import Dict, List
from fastapi import Request, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

# --- API Key Authentication ---
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    """
    Dependency that verifies the X-API-Key header against the configured API_KEY.
    """
    if api_key == settings.SECURITY.API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

# --- Simple In-Memory Rate Limiting ---
rate_limit_db: Dict[str, List[float]] = {}
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_TIMEFRAME = 60

async def rate_limiter(request: Request):
    """
    Dependency that provides simple IP-based rate limiting.
    """
    client_ip = request.client.host
    current_time = time.monotonic()

    if client_ip not in rate_limit_db:
        rate_limit_db[client_ip] = []

    rate_limit_db[client_ip] = [
        t for t in rate_limit_db[client_ip] if t > current_time - RATE_LIMIT_TIMEFRAME
    ]

    if len(rate_limit_db[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Limit is {RATE_LIMIT_REQUESTS} per {RATE_LIMIT_TIMEFRAME} seconds.",
        )
    
    rate_limit_db[client_ip].append(current_time)