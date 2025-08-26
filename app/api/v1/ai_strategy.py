from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Configuration, ConfigDataType, get_async_session
from sqlalchemy.future import select
from sqlalchemy import delete
import asyncio
import logging

from config import settings
from app.services.audio_service import AsyncAudioService
from app.services.llm_service import LlmApiService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_audio_service(request: Request) -> AsyncAudioService: return request.app.state.audio_service
def get_llm_service(request: Request) -> LlmApiService: return request.app.state.llm_service

def _get_summary_from_llm_response(llm_response: Dict[str, Any]) -> str | None:
    try:
        return llm_response['analysis']['plain_text_summary']
    except (KeyError, TypeError):
        return None

# --- THIS IS THE FIX (Part 1): A single, complete dictionary for all tests ---
def _get_full_test_data() -> Dict[str, Any]:
    """Provides a comprehensive dictionary with all possible keys for template formatting."""
    return {
        "count": 123,
        "defects": "Test Defect",
        "batch_id": "TEST-001",
        "product_name": "Test Product",
        "total_items": 1000,
        "reject_count": 50,
        "countdown": 3,
        "qc_status": "REJECT",
        "type": "TEST_TYPE",
        "size": "Medium",
        "wait_time": 30,
        "top_defect": "Cosmetic Blemish"
    }
# --- END OF FIX ---

@router.get("/", response_model=Dict[str, Any])
async def get_ai_strategy(db: AsyncSession = Depends(get_async_session)):
    strategy = {}
    try:
        result = await db.execute(select(Configuration).where(Configuration.namespace == "ai_strategy"))
        for item in result.scalars().all():
            try:
                if item.data_type == ConfigDataType.BOOL: strategy[item.key] = item.value.lower() in ['true', '1', 't']
                elif item.data_type == ConfigDataType.INT: strategy[item.key] = int(item.value)
                elif item.data_type == ConfigDataType.FLOAT: strategy[item.key] = float(item.value)
                else: strategy[item.key] = item.value
            except (ValueError, TypeError): continue
        default_strategy = settings.AI_STRATEGY.model_dump()
        for key, value in default_strategy.items():
            if key not in strategy: strategy[key] = value
        return strategy
    except Exception: return settings.AI_STRATEGY.model_dump()

@router.post("/", status_code=200)
async def save_ai_strategy(strategy: Dict[str, Any], db: AsyncSession = Depends(get_async_session), audio_service: AsyncAudioService = Depends(get_audio_service)):
    if not strategy: raise HTTPException(status_code=400, detail="No strategy data provided")
    try:
        async with db.begin():
            await db.execute(delete(Configuration).where(Configuration.namespace == "ai_strategy"))
            default_strategy = settings.AI_STRATEGY.model_dump()
            template_keys = []
            for key, value in strategy.items():
                default_value = default_strategy.get(key)
                data_type = ConfigDataType.STRING
                if isinstance(default_value, bool): data_type = ConfigDataType.BOOL
                elif isinstance(default_value, int): data_type = ConfigDataType.INT
                elif isinstance(default_value, float): data_type = ConfigDataType.FLOAT
                db.add(Configuration(namespace="ai_strategy", key=key, value=str(value), data_type=data_type))
                if key.endswith("_TEMPLATE") and isinstance(value, str) and value.strip():
                    template_keys.append((key, value))
        if hasattr(audio_service, '_config_cache'): audio_service._config_cache.clear()
        for key, value in template_keys:
            asyncio.create_task(audio_service.pre_generate_and_cache_alert(key, value))
        return {"message": "AI & Audio strategy saved successfully."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save settings: {str(e)}")

@router.post("/test-audio")
async def test_audio_template(payload: Dict[str, str], audio_service: AsyncAudioService = Depends(get_audio_service)):
    template_key, text = payload.get("template_key"), payload.get("text")
    engine_override, tts_language = payload.get("engine"), payload.get("tts_language")
    
    # --- THIS IS THE FIX (Part 2): Correct Error Handling and Complete Test Data ---
    try:
        if not all([template_key, text, engine_override, tts_language]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        formatted_text = text.format(**_get_full_test_data())
        audio_bytes = await audio_service._tts_service.synthesize_speech(text=formatted_text, model=engine_override, language=tts_language)

        if not audio_bytes:
            raise HTTPException(status_code=500, detail="TTS service returned empty audio data")
        
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise # Re-raise FastAPI's exceptions directly
    except Exception as e:
        # Catches other errors like the KeyError
        raise HTTPException(status_code=500, detail=f"Failed to generate test audio: {str(e)}")
    # --- END OF FIX ---

@router.post("/test-item-pipeline", status_code=200)
async def test_item_pipeline(request: Request, llm_service: LlmApiService = Depends(get_llm_service), audio_service: AsyncAudioService = Depends(get_audio_service)):
    try:
        payload = await request.json()
        engine_override, llm_language, tts_language = payload.get("engine"), payload.get("llm_language"), payload.get("tts_language")
        if not all([engine_override, llm_language, tts_language]):
            raise HTTPException(status_code=400, detail="Missing required fields in pipeline test.")
        
        test_item_data = {"qc_summary": {"overall_status": "REJECTED_COSMETIC_BLEMISH"}}
        word_count = payload.get("word_count", settings.AI_STRATEGY.LLM_ITEM_WORD_COUNT)
        
        llm_response = await llm_service.analyze_item(item_data=test_item_data, language=llm_language, word_count=word_count)
        summary_text = _get_summary_from_llm_response(llm_response)
        
        if not summary_text: raise HTTPException(status_code=400, detail="LLM service failed to generate a valid item summary.")
        
        audio_bytes = await audio_service._tts_service.synthesize_speech(text=summary_text, model=engine_override, language=tts_language)
        
        if not audio_bytes: raise HTTPException(status_code=500, detail="TTS service failed to synthesize audio.")
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

@router.post("/test-summary-pipeline", status_code=200)
async def test_summary_pipeline(request: Request, llm_service: LlmApiService = Depends(get_llm_service), audio_service: AsyncAudioService = Depends(get_audio_service)):
    try:
        payload = await request.json()
        engine_override, llm_language, tts_language = payload.get("engine"), payload.get("llm_language"), payload.get("tts_language")
        if not all([engine_override, llm_language, tts_language]):
            raise HTTPException(status_code=400, detail="Missing required fields in pipeline test.")

        test_batch_data = [{"qc_summary": {"overall_status": "ACCEPTED"}}, {"qc_summary": {"overall_status": "REJECTED_MINOR_DEFECT"}}]
        word_count = payload.get("word_count", settings.AI_STRATEGY.LLM_SUMMARY_WORD_COUNT)
        model_pref = payload.get("model_preference", settings.AI_STRATEGY.SUMMARY_LLM_MODEL)
        
        llm_response = await llm_service.summarize_batch(batch_data=test_batch_data, language=llm_language, word_count=word_count, model_preference=model_pref)
        summary_text = _get_summary_from_llm_response(llm_response)
        
        if not summary_text: raise HTTPException(status_code=400, detail="LLM Service returned an invalid summary.")

        audio_bytes = await audio_service.generate_pipelined_summary_audio(summary_text, tts_language=tts_language, engine_override=engine_override)

        if not audio_bytes: raise HTTPException(status_code=500, detail="TTS service failed to generate summary audio.")
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))