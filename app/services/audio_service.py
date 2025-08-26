import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, Optional, Any

from app.models import Configuration, ConfigDataType
from sqlalchemy.future import select
import time

from app.services.tts_service import TtsApiService
from app.utils.tokenizer import chunk_text_by_tokens
from config import settings

TTS_CACHE_DIR = Path(__file__).parent.parent.parent / "audio_files" / "tts_cache"
TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class AsyncAudioService:
    def __init__(self, db_session_factory, tts_service: TtsApiService):
        self._get_db_session = db_session_factory
        self._tts_service = tts_service
        self._playback_task: Optional[asyncio.Task] = None
        self._config_cache: Dict[str, Any] = {}
        self._config_cache_last_updated: float = 0.0

    async def _get_config(self, key: str, default: Any) -> Any:
        if time.monotonic() - self._config_cache_last_updated > 5.0: self._config_cache.clear()
        if key in self._config_cache: return self._config_cache[key]
        async with self._get_db_session() as session:
            result = await session.execute(select(Configuration).where(Configuration.namespace == "ai_strategy", Configuration.key == key))
            config_item = result.scalar_one_or_none()
            self._config_cache_last_updated = time.monotonic()
            if config_item:
                try:
                    if config_item.data_type == ConfigDataType.BOOL: value = config_item.value.lower() in ['true', '1', 't']
                    elif config_item.data_type == ConfigDataType.INT: value = int(config_item.value)
                    elif config_item.data_type == ConfigDataType.FLOAT: value = float(config_item.value)
                    else: value = config_item.value
                    self._config_cache[key] = value
                    return value
                except (ValueError, TypeError): self._config_cache[key] = default
                return default
        self._config_cache[key] = default
        return default

    async def _execute_playback_from_stream(self, audio_bytes: bytes):
        if not audio_bytes: return
        process = None
        try:
            process = await asyncio.create_subprocess_exec("aplay", "-", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
            await process.communicate(input=audio_bytes)
        except Exception as e: print(f"[Audio Service] FATAL ERROR during stream playback: {e}")

    async def play_realtime_alert(self, template_key: str, **kwargs):
        if not await self._get_config("TTS_ENABLED", settings.AI_STRATEGY.TTS_ENABLED): return
        template = await self._get_config(template_key, getattr(settings.AI_STRATEGY, template_key, ""))
        text_to_speak = template.format(**kwargs)
        realtime_engine = await self._get_config("REALTIME_TTS_ENGINE", settings.AI_STRATEGY.REALTIME_TTS_ENGINE)
        # THIS IS THE FIX
        tts_language = await self._get_config("TTS_LANGUAGE", settings.AI_STRATEGY.TTS_LANGUAGE)
        audio_bytes = await self._tts_service.synthesize_speech(text=text_to_speak, model=realtime_engine, language=tts_language)
        if audio_bytes:
            if self._playback_task and not self._playback_task.done(): self._playback_task.cancel()
            self._playback_task = asyncio.create_task(self._execute_playback_from_stream(audio_bytes))

    async def generate_pipelined_summary_audio(self, text: str, tts_language: Optional[str] = None, engine_override: Optional[str] = None) -> Optional[bytes]:
        if not await self._get_config("TTS_ENABLED", settings.AI_STRATEGY.TTS_ENABLED): return None
        summary_engine = engine_override or await self._get_config("SUMMARY_TTS_ENGINE", settings.AI_STRATEGY.SUMMARY_TTS_ENGINE)
        # THIS IS THE FIX
        language = tts_language or await self._get_config("TTS_LANGUAGE", settings.AI_STRATEGY.TTS_LANGUAGE)
        word_count = await self._get_config("LLM_SUMMARY_WORD_COUNT", settings.AI_STRATEGY.LLM_SUMMARY_WORD_COUNT)
        chunk_count = await self._get_config("TTS_SUMMARY_CHUNK_COUNT", settings.AI_STRATEGY.TTS_SUMMARY_CHUNK_COUNT)
        tokens_per_chunk = int((word_count * 1.4) / chunk_count)
        text_chunks = chunk_text_by_tokens(text, tokens_per_chunk)
        audio_chunks = []
        for chunk in text_chunks:
            audio_bytes = await self._tts_service.synthesize_speech(text=chunk, model=summary_engine, language=language)
            if audio_bytes: audio_chunks.append(audio_bytes)
        return b"".join(audio_chunks) if audio_chunks else None

    async def play_pipelined_summary(self, text: str):
        audio_bytes = await self.generate_pipelined_summary_audio(text)
        if audio_bytes:
            if self._playback_task and not self._playback_task.done(): self._playback_task.cancel()
            self._playback_task = asyncio.create_task(self._execute_playback_from_stream(audio_bytes))

    async def pre_generate_and_cache_alert(self, template_key: str, text: str):
        summary_engine = await self._get_config("SUMMARY_TTS_ENGINE", settings.AI_STRATEGY.SUMMARY_TTS_ENGINE)
        # THIS IS THE FIX
        tts_language = await self._get_config("TTS_LANGUAGE", settings.AI_STRATEGY.TTS_LANGUAGE)
        audio_bytes = await self._tts_service.synthesize_speech(text=text, model=summary_engine, language=tts_language)
        if audio_bytes:
            filepath = TTS_CACHE_DIR / f"{template_key}.wav"
            async with aiofiles.open(filepath, "wb") as f: await f.write(audio_bytes)
            print(f"Audio Service: Successfully cached '{filepath.name}'.")
        else: print(f"Audio Service: FAILED to pre-generate audio for '{template_key}'.")

    # The other methods like play_event_from_cache and _execute_playback_from_file are unchanged.
    async def play_event_from_cache(self, event_key: str):
        if not await self._get_config("TTS_ENABLED", settings.AI_STRATEGY.TTS_ENABLED): return
        filepath = TTS_CACHE_DIR / f"{event_key}.wav"
        if not filepath.exists():
            static_path = Path(__file__).parent.parent.parent / "audio_files" / f"{event_key}.mp3"
            if not static_path.exists():
                print(f"Audio Service WARNING: No audio for event '{event_key}'.")
                return
            filepath = static_path
        if self._playback_task and not self._playback_task.done():
            self._playback_task.cancel()
        self._playback_task = asyncio.create_task(self._execute_playback_from_file(filepath))

    async def _execute_playback_from_file(self, filepath: Path):
        process = None
        try:
            player_cmd = "aplay" if filepath.suffix.lower() == ".wav" else "mpg123"
            args = ['-q', str(filepath)] if player_cmd == 'mpg123' else [str(filepath)]
            process = await asyncio.create_subprocess_exec(player_cmd, *args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
            await process.communicate()
        except Exception as e:
            print(f"[Audio Service] FATAL ERROR during file playback: {e}")