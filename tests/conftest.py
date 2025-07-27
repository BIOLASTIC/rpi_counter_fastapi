"""
Pytest configuration file for defining shared fixtures.
"""
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import all necessary components
from main import create_app
from app.models.database import Base, get_async_session
from app.core.gpio_controller import AsyncGPIOController
from app.services.detection_service import AsyncDetectionService

# --- Database Setup for Tests ---
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
TestAsyncSessionFactory = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

# --- Auto-use Fixture to Manage Schema ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_schema() -> AsyncGenerator[None, None]:
    """Auto-used fixture to create and drop the database schema for every test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- Session Fixture ---
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a single database session for tests that need it directly."""
    async with TestAsyncSessionFactory() as session:
        yield session

# --- API Test Client Fixture ---
@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provides an async test client that correctly handles the application lifespan."""
    app = create_app()
    app.dependency_overrides[get_async_session] = lambda: db_session
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client

# --- DEFINITIVE FIX: Service Fixture ---
@pytest_asyncio.fixture(scope="function")
async def detection_service() -> AsyncDetectionService:
    """
    Provides a fully initialized instance of the AsyncDetectionService
    connected to the clean test database.
    """
    gpio_controller = await AsyncGPIOController.get_instance()
    service = AsyncDetectionService(
        gpio_controller=gpio_controller,
        db_session_factory=TestAsyncSessionFactory
    )
    # Initialize the service, which will load its state from the (empty) DB.
    await service.initialize()
    return service
