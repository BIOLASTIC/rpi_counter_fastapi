"""
Tests for the SQLAlchemy database models.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# FIX APPLIED HERE: Import Detection and DetectionDirection from their specific module.
from app.models.detection import Detection, DetectionDirection

@pytest.mark.asyncio
async def test_create_detection_record(db_session: AsyncSession):
    """
    Tests the creation and retrieval of a Detection model instance.
    """
    # Create a new detection record
    new_detection = Detection(
        box_count=1,
        detection_direction=DetectionDirection.FORWARD,
        confidence_score=0.95
    )
    db_session.add(new_detection)
    await db_session.commit()
    await db_session.refresh(new_detection)

    # Retrieve it from the database
    result = await db_session.execute(select(Detection).where(Detection.id == new_detection.id))
    retrieved_detection = result.scalar_one()

    assert retrieved_detection is not None
    assert retrieved_detection.id == new_detection.id
    assert retrieved_detection.box_count == 1
    assert retrieved_detection.confidence_score == 0.95
    assert retrieved_detection.detection_direction == DetectionDirection.FORWARD
