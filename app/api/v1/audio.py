# rpi_counter_fastapi-apintrigation/app/api/v1/audio.py

from fastapi import APIRouter, Depends, Request, UploadFile, File, Form, HTTPException
from typing import Dict, List

from app.services.audio_service import AsyncAudioService, VALID_EVENTS

router = APIRouter()

def get_audio_service(request: Request) -> AsyncAudioService:
    return request.app.state.audio_service

@router.get("/config")
async def get_audio_config(
    service: AsyncAudioService = Depends(get_audio_service)
):
    """
    Returns all necessary data for the audio settings page:
    - A list of available audio files.
    - A dictionary of current event-to-file mappings.
    - The structure of valid events.
    """
    audio_files = await service.get_audio_files()
    mappings = await service.get_event_mappings()
    return {
        "audio_files": audio_files,
        "mappings": mappings,
        "valid_events": VALID_EVENTS
    }

@router.post("/mappings")
async def save_mappings(
    mappings: Dict[str, str],
    service: AsyncAudioService = Depends(get_audio_service)
):
    """Saves the event-to-file mappings."""
    await service.save_event_mappings(mappings)
    return {"message": "Audio alert mappings saved successfully."}

@router.post("/upload")
async def upload_audio_file(
    file: UploadFile = File(...),
    service: AsyncAudioService = Depends(get_audio_service)
):
    """Uploads a new audio file."""
    if not (file.filename.endswith('.wav') or file.filename.endswith('.mp3')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .wav and .mp3 are supported.")
    
    contents = await file.read()
    await service.save_audio_file(file.filename, contents)
    return {"message": f"File '{file.filename}' uploaded successfully."}

@router.delete("/files/{filename}")
async def delete_audio_file(
    filename: str,
    service: AsyncAudioService = Depends(get_audio_service)
):
    """Deletes an audio file from the server."""
    success = service.delete_audio_file(filename)
    if not success:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")
    return {"message": f"File '{filename}' deleted successfully."}