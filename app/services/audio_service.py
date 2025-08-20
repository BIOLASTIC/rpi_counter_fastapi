# rpi_counter_fastapi-apintrigation/app/services/audio_service.py

import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.models import Configuration, ConfigDataType

# Define the location for audio files and a list of valid event types.
AUDIO_DIR = Path(__file__).parent.parent.parent / "audio_files"
AUDIO_DIR.mkdir(exist_ok=True)  # Ensure the directory exists

VALID_EVENTS = {
    "system": [
        "startup_complete",
        "product_stalled",
        "alarm_acknowledged"
    ],
    "quality_control": [
        "ACCEPT",
        "REJECT_LOW_LIGHT",
        "REJECT_DISTORTION",
        "REJECT_MISSING_OBJECT",
        "REJECT_OTHERS",
        "REJECT_FORIEGN_OBJECT"
    ],
    "product_category": [
        "BL-CARRY-BAGS",
        "EW-Tissue-Paper",
        "BB-CARRY-BAGS"
    ]
}


class AsyncAudioService:
    """
    A service to manage and play audio alerts based on system events.
    This version supports interruptible playback.
    """
    def __init__(self, db_session_factory):
        self._get_db_session = db_session_factory
        # This task will hold the currently running playback coroutine
        self._playback_task: Optional[asyncio.Task] = None

    async def get_audio_files(self) -> List[str]:
        """Returns a sorted list of available audio files."""
        files = [f.name for f in AUDIO_DIR.glob("*.wav")] + [f.name for f in AUDIO_DIR.glob("*.mp3")]
        return sorted(files)

    async def get_event_mappings(self) -> Dict[str, str]:
        """Retrieves the current event-to-sound-file mappings from the database."""
        mappings = {}
        async with self._get_db_session() as session:
            result = await session.execute(
                select(Configuration).where(Configuration.namespace == "audio_alerts")
            )
            for config_item in result.scalars().all():
                mappings[config_item.key] = config_item.value
        return mappings

    async def save_event_mappings(self, mappings: Dict[str, str]):
        """Saves a full set of event-to-sound-file mappings to the database."""
        async with self._get_db_session() as session:
            # Clear existing mappings for audio alerts
            await session.execute(
                delete(Configuration).where(Configuration.namespace == "audio_alerts")
            )

            # Add new mappings
            for event, filename in mappings.items():
                if filename:
                    new_mapping = Configuration(
                        namespace="audio_alerts",
                        key=event,
                        value=filename,
                        data_type=ConfigDataType.STRING,
                        description=f"Audio alert for {event} event."
                    )
                    session.add(new_mapping)
            await session.commit()

    async def save_audio_file(self, filename: str, content: bytes):
        """Saves an uploaded audio file to the designated directory."""
        safe_filename = Path(filename).name
        filepath = AUDIO_DIR / safe_filename
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(content)

    def delete_audio_file(self, filename: str) -> bool:
        """Deletes an audio file. Returns True on success, False otherwise."""
        safe_filename = Path(filename).name
        filepath = AUDIO_DIR / safe_filename
        if filepath.exists() and filepath.is_file():
            filepath.unlink()
            return True
        return False

    async def _execute_playback(self, event_name: str):
        """
        Internal coroutine that handles the actual subprocess execution.
        This task is designed to be cancelled, and it ensures the subprocess is killed on cancellation.
        """
        process = None
        try:
            mapping = await self.get_event_mappings()
            filename = mapping.get(event_name)

            if not filename:
                return

            filepath = AUDIO_DIR / Path(filename).name
            if not filepath.exists():
                print(f"[Audio Service] WARNING: Sound file '{filename}' for event '{event_name}' not found.")
                return

            # Use -q (quiet) flag for players to prevent console spam
            player_cmd = "aplay" if filepath.suffix.lower() == ".wav" else "mpg123"
            args = ['-q', str(filepath)] if player_cmd == 'mpg123' else [str(filepath)]

            process = await asyncio.create_subprocess_exec(
                player_cmd, *args,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE
            )
            
            _, stderr = await process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode().strip() if stderr else "Unknown player error"
                print(f"[Audio Service] ERROR: Player for '{filename}' exited with code {process.returncode}. Stderr: {error_message}")

        except asyncio.CancelledError:
            # This is expected when a sound is interrupted.
            # The 'finally' block will handle the cleanup.
            print(f"[Audio Service] Playback for event '{event_name}' was interrupted by a new request.")
            raise # Re-raise the exception so the task is properly marked as cancelled.
        except Exception as e:
            print(f"[Audio Service] FATAL ERROR during playback execution: {e}")
        finally:
            # This block is crucial. It ensures that if the task is cancelled,
            # the underlying audio player process is killed immediately.
            if process and process.returncode is None:
                try:
                    process.terminate()
                    await process.wait()
                    print(f"[Audio Service] Terminated running audio process.")
                except ProcessLookupError:
                    # Process might have already finished between the check and terminate
                    pass
                except Exception as e:
                    print(f"[Audio Service] Error during process termination: {e}")

    async def play_sound_for_event(self, event_name: str):
        """
        Looks up the audio file for an event and plays it, immediately interrupting
        any sound that is currently playing.
        """
        # If a sound playback task is already running, cancel it.
        if self._playback_task and not self._playback_task.done():
            self._playback_task.cancel()
        
        # Start a new, independent playback task for the new event.
        self._playback_task = asyncio.create_task(self._execute_playback(event_name))

