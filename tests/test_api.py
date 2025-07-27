"""
Tests for the FastAPI API endpoints.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Tests the main health check/root endpoint."""
    response = await async_client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_usage" in data
    assert "camera_status" in data
    assert data["camera_status"] == "connected" # From our mock

@pytest.mark.asyncio
async def test_get_detection_status(async_client: AsyncClient):
    """Tests the initial state of the detection endpoint."""
    response = await async_client.get("/api/v1/detection/")
    assert response.status_code == 200
    data = response.json()
    assert data["box_count"] == 0
    assert data["state"] == "IDLE"

@pytest.mark.asyncio
async def test_reset_counter(async_client: AsyncClient):
    """Tests the counter reset functionality."""
    # This is a simple test; a more complex one would simulate a count first.
    response = await async_client.post("/api/v1/detection/reset")
    assert response.status_code == 200
    assert response.json() == {"message": "Counter reset successfully."}
    
    # Verify the count is still 0
    response = await async_client.get("/api/v1/detection/")
    assert response.status_code == 200
    assert response.json()["box_count"] == 0

@pytest.mark.asyncio
async def test_conveyor_control(async_client: AsyncClient):
    """Tests starting and stopping the mock conveyor."""
    # Start the conveyor
    start_response = await async_client.post("/api/v1/gpio/conveyor/start")
    assert start_response.status_code == 200
    assert start_response.json()["message"] == "Conveyor started."

    # Check status
    status_response = await async_client.get("/api/v1/gpio/status")
    assert status_response.json()["conveyor"] == "running"

    # Stop the conveyor
    stop_response = await async_client.post("/api/v1/gpio/conveyor/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["message"] == "Conveyor stopped."
    
    # Check status again
    status_response = await async_client.get("/api/v1/gpio/status")
    assert status_response.json()["conveyor"] == "stopped"
