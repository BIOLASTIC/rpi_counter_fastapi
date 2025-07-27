"""
Sets up the asynchronous database engine and session management using SQLAlchemy 2.0.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase
from config import settings

# --- FIX APPLIED HERE ---
# We create a dictionary of engine arguments and conditionally add the
# pooling arguments only if we are NOT using SQLite.
engine_args = {"echo": settings.DATABASE.ECHO}

if "sqlite" not in settings.DATABASE.URL:
    # Add pooling options for databases that support it (e.g., PostgreSQL)
    print("Non-SQLite database detected, applying connection pool settings.")
    engine_args["pool_size"] = settings.DATABASE.POOL_SIZE
    engine_args["pool_timeout"] = settings.DATABASE.POOL_TIMEOUT
else:
    # For SQLite, we add a specific argument to allow it to work with FastAPI
    print("SQLite database detected, omitting pool settings.")
    engine_args["connect_args"] = {"check_same_thread": False}

# Create an async engine instance using the URL from settings
# and the conditionally built arguments.
engine = create_async_engine(
    settings.DATABASE.URL,
    **engine_args
)

# Create a factory for creating new async sessions
AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False, # Important for FastAPI dependencies
    class_=AsyncSession
)

class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models. It includes the AsyncAttrs mixin
    to enable async loading of relationships and attributes.
    """
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get an async database session per request.
    Ensures the session is always closed, even if errors occur.
    """
    async with AsyncSessionFactory() as session:
        yield session
