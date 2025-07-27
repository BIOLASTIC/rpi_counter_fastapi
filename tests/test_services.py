"""
Tests for the business logic services.
"""
import pytest
import asyncio

from app.core.sensor_events import SensorEvent, SensorState
from app.services.detection_service import AsyncDetectionService, DetectionState

@pytest.mark.asyncio
async def test_detection_service_state_machine(detection_service: AsyncDetectionService):
    """
    Tests the full state machine logic using a pre-initialized service from a fixture.
    This pattern is robust and ensures the database is correctly set up.
    """
    # The `detection_service` is provided by the fixture in conftest.py,
    # fully initialized and connected to a clean test database.

    assert detection_service._state == DetectionState.IDLE
    assert await detection_service.get_current_count() == 0

    # 1. Box enters - trigger sensor 1
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=1, new_state=SensorState.TRIGGERED))
    assert detection_service._state == DetectionState.ENTERING

    # 2. Box hits second sensor
    await asyncio.sleep(0.2)
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=2, new_state=SensorState.TRIGGERED))
    assert detection_service._state == DetectionState.CONFIRMING_EXIT

    # 3. Box clears first sensor - THIS IS THE COUNTING EVENT
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=1, new_state=SensorState.CLEARED))
    assert detection_service._state == DetectionState.RESETTING
    assert await detection_service.get_current_count() == 1

    # 4. Box fully clears second sensor
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=2, new_state=SensorState.CLEARED))
    assert detection_service._state == DetectionState.IDLE
