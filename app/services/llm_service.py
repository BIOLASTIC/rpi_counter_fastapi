import httpx
import json
import re
from typing import Optional, Any, Dict, List

from config import settings

class LlmApiService:
    """A client to interact with the external LLM Summarization API."""
    def __init__(self):
        self.base_url = settings.LLM_API.BASE_URL
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    # --- FIX: The parsing logic now lives inside the service that owns the data format. ---
    def _parse_llm_response(self, response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Robustly parses multiple possible JSON response structures from the LLM API."""
        if not response_data:
            return None
        
        # Case 1: The response is already in the simple, direct format.
        if 'analysis' in response_data and isinstance(response_data.get('analysis'), dict):
            print("LLM Service INFO: Parsed simple/direct LLM response format.")
            return response_data

        # Case 2: The response is the complex format with embedded JSON.
        try:
            text_content = response_data['choices'][0]['text']
            # This regex is more robust for cleaning the JSON string
            cleaned_text = re.sub(r'```json\s*|\s*```', '', text_content).strip()
            parsed_json = json.loads(cleaned_text)
            
            # The parsed content might be the final object, or it might be nested
            if 'analysis' in parsed_json:
                 print("LLM Service INFO: Parsed complex/embedded LLM response format.")
                 return parsed_json
            else:
                 # Handle cases where the embedded text IS the analysis object
                 print("LLM Service INFO: Parsed complex/embedded LLM response (direct content).")
                 return {"analysis": parsed_json}

        except (KeyError, IndexError, json.JSONDecodeError, TypeError) as e:
            print(f"LLM Service CRITICAL ERROR: Failed to parse any known LLM response format. Error: {e}. Raw data: {response_data}")
            return None

    async def analyze_item(
        self,
        item_data: Dict[str, Any],
        language: str,
        word_count: int,
        model_preference: str = "realtime"
    ) -> Optional[Dict[str, Any]]:
        """Generates a summary for a single QC item."""
        if not settings.AI_STRATEGY.LLM_ENABLED: return None

        payload = {
            "item_data": item_data, "language": language, "word_count": word_count,
            "max_tokens": int(word_count * 3.5), "model_preference": model_preference
        }
        try:
            response = await self.client.post("/item_analysis", json=payload)
            response.raise_for_status()
            # --- FIX: The parsing is now done here, returning a clean dictionary ---
            return self._parse_llm_response(response.json())
        except httpx.RequestError as e:
            print(f"LLM Service ERROR: Could not connect to LLM API at {e.request.url}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"LLM Service ERROR: API returned status {e.response.status_code}. Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"LLM Service ERROR: An unexpected error occurred during item analysis: {e}")
            return None

    async def summarize_batch(
        self,
        batch_data: List[Dict[str, Any]],
        language: str,
        word_count: int,
        model_preference: str = "high_quality"
    ) -> Optional[Dict[str, Any]]:
        """Generates a summary for an entire batch of items."""
        if not settings.AI_STRATEGY.LLM_ENABLED: return None

        payload = {
            "batch_data": batch_data, "language": language, "word_count": word_count,
            "max_tokens": int(word_count * 2.5), "model_preference": model_preference
        }
        try:
            response = await self.client.post("/batch_summary", json=payload)
            response.raise_for_status()
            # --- FIX: The parsing is also done here for consistency ---
            return self._parse_llm_response(response.json())
        except Exception as e:
            print(f"LLM Service ERROR: An unexpected error occurred during batch summary: {e}")
            return None

    async def health_check(self) -> bool:
        """Performs a simple health check on the LLM API."""
        if not settings.AI_STRATEGY.LLM_ENABLED: return False
        try:
            response = await self.client.get("/health", timeout=2.0)
            return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False