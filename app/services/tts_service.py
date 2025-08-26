import httpx
from typing import Optional
from config import settings

class TtsApiService:
    """A client to interact with the external Text-to-Speech API."""
    def __init__(self):
        self.base_url = settings.TTS_API.BASE_URL
        # --- DEFINITIVE FIX: Increased timeout to handle slow AI models ---
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=90.0)

    async def synthesize_speech(
        self,
        text: str,
        model: str,
        language: Optional[str] = None,
        speaker: Optional[str] = None,
        emotion: Optional[str] = None,
        desc: Optional[str] = None
    ) -> Optional[bytes]:
        if not settings.AI_STRATEGY.TTS_ENABLED:
            return None 

        payload = {"text": text, "model": model}

        if model == "xtts":
            if language:
                payload["language"] = language
            if speaker:
                payload["speaker"] = speaker
        
        elif model == "parler":
            if desc:
                payload["desc"] = desc
        
        elif model == "mac":
            if language:
                payload["language"] = language
            if language == "en":
                payload["emotion"] = emotion or "neutral"

        try:
            response = await self.client.post("/tts", json=payload)
            response.raise_for_status()
            
            if response.content and len(response.content) > 1024:
                 return response.content
            else:
                print(f"TTS Service WARNING: Received 200 OK but audio content was empty. Silent failure in TTS engine likely.")
                return None

        except httpx.RequestError as e:
            print(f"TTS Service ERROR: Could not connect to TTS API at {e.request.url}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"TTS Service ERROR: API returned status {e.response.status_code}. Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"TTS Service ERROR: An unexpected error occurred during synthesis: {e}")
            return None

    async def health_check(self) -> bool:
        if not settings.AI_STRATEGY.TTS_ENABLED:
            return False
        try:
            response = await self.client.get("/health", timeout=2.0)
            return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False
