"""
NEW: API endpoints for managing Camera and Object profiles.

This provides the full CRUD (Create, Read, Update, Delete) functionality
required for a UI to manage production "recipes" dynamically without
restarting the application.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, CameraProfile, ObjectProfile, Product
from app.schemas.profiles import (
    CameraProfileCreate, CameraProfileUpdate, CameraProfileOut,
    ObjectProfileCreate, ObjectProfileUpdate, ObjectProfileOut
)

router = APIRouter()

# --- Camera Profile Endpoints ---

@router.post("/camera", status_code=201, response_model=CameraProfileOut)
async def create_camera_profile(
    profile_in: CameraProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new camera profile."""
    # Check if a profile with the same name already exists
    result = await db.execute(select(CameraProfile).where(CameraProfile.name == profile_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"A camera profile with the name '{profile_in.name}' already exists."
        )
    
    new_profile = CameraProfile(**profile_in.model_dump())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile

@router.get("/camera", response_model=List[CameraProfileOut])
async def get_all_camera_profiles(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all camera profiles."""
    result = await db.execute(select(CameraProfile).order_by(CameraProfile.name))
    return result.scalars().all()

@router.get("/camera/{profile_id}", response_model=CameraProfileOut)
async def get_camera_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single camera profile by its ID."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    return profile

@router.put("/camera/{profile_id}", response_model=CameraProfileOut)
async def update_camera_profile(
    profile_id: int,
    profile_in: CameraProfileUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing camera profile."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    
    update_data = profile_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
        
    await db.commit()
    await db.refresh(profile)
    return profile

@router.delete("/camera/{profile_id}", status_code=204)
async def delete_camera_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete a camera profile."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    
    # Check if any ObjectProfile is using this CameraProfile
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.camera_profile_id == profile_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this camera profile. It is currently in use by one or more object profiles."
        )

    await db.delete(profile)
    await db.commit()
    return None

# --- Object Profile Endpoints ---

@router.post("/object", status_code=201, response_model=ObjectProfileOut)
async def create_object_profile(
    profile_in: ObjectProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new object profile."""
    # Check if an object profile with the same name already exists
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.name == profile_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"An object profile with the name '{profile_in.name}' already exists."
        )
    
    # --- PHASE 1: Validate that the product_id exists if provided ---
    if profile_in.product_id:
        product = await db.get(Product, profile_in.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {profile_in.product_id} not found.")

    new_profile = ObjectProfile(**profile_in.model_dump())
    db.add(new_profile)
    await db.commit()
    # We need to load the relationships to return them in the response
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == new_profile.id)
    )
    return result.scalar_one()


@router.get("/object", response_model=List[ObjectProfileOut])
async def get_all_object_profiles(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all object profiles, including their linked camera and product profiles."""
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .order_by(ObjectProfile.name)
    )
    return result.scalars().all()

@router.get("/object/{profile_id}", response_model=ObjectProfileOut)
async def get_object_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single object profile by ID."""
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
    return profile

@router.put("/object/{profile_id}", response_model=ObjectProfileOut)
async def update_object_profile(
    profile_id: int,
    profile_in: ObjectProfileUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing object profile."""
    # Use selectinload to fetch the profile and its related camera_profile in one go
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
        
    update_data = profile_in.model_dump(exclude_unset=True)

    # --- PHASE 1: Validate that the product_id exists if provided ---
    if "product_id" in update_data and update_data["product_id"]:
         product = await db.get(Product, update_data["product_id"])
         if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {update_data['product_id']} not found.")

    for key, value in update_data.items():
        setattr(profile, key, value)
        
    await db.commit()
    # Refresh to ensure all data, including relationships, is up to date
    await db.refresh(profile, attribute_names=['product']) # Eagerly refresh the product relationship
    await db.refresh(profile)
    return profile

@router.delete("/object/{profile_id}", status_code=204)
async def delete_object_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete an object profile."""
    profile = await db.get(ObjectProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
        
    await db.delete(profile)
    await db.commit()
    return None