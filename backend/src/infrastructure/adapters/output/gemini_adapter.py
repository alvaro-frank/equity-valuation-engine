from google import genai
from loguru import logger
from google.genai import types
import json
import asyncio
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from application.exceptions.exceptions import RateLimitExceededError, ConfigurationError, ExternalServiceError, InvalidDocumentFormatError, LLMParsingError
from application.ports.translation_port import TranslationPort
from infrastructure.utils.llm_utils import extract_json_from_response
from .base_llm_adapter import BaseLLMAdapter

T = TypeVar('T', bound=BaseModel)

class GeminiAdapter(BaseLLMAdapter):
    """
    Adapter that leverages Google's Gemini LLM to generate qualitative research and DCF assumptions.
    """
    def __init__(self, api_key: Optional[str] = None, client: Optional[genai.Client] = None, translator: Optional[TranslationPort] = None):
        super().__init__(translator=translator)
        if client:
            self.client = client
        else:
            if not api_key:
                raise ConfigurationError("Gemini API Key is required")
            self.client = genai.Client(api_key=api_key)

    async def _generate_company_profile(self, prompt: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        import time
        start_time = time.time()
        logger.info(f"[LLM - {schema.__name__}] Dispatching request to {model_id}...")
        try:
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0,
                        response_mime_type="application/json",
                        response_schema=schema
                    )
                ),
                timeout=120.0
            )
            elapsed = time.time() - start_time
            logger.info(f"[LLM - {schema.__name__}] {model_id} responded successfully in {elapsed:.2f}s")
            raw_text = response.text
            data_en = json.loads(raw_text)
            return data_en
        except Exception as e:
            logger.error(f"[LLM-Error] Gemini API Error during _generate_company_profile: {e}")
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")

    async def _generate_industry_dynamics(self, prompt: str, schema: Type[T], model_id: str = "gemini-3.1-pro-preview") -> dict:
        import time
        start_time = time.time()
        logger.info(f"[LLM - {schema.__name__}] Dispatching request to {model_id}...")
        try:
            response = await self.client.aio.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0,
                    max_output_tokens=8192
                )
            )
            elapsed = time.time() - start_time
            logger.info(f"[LLM - {schema.__name__}] {model_id} responded successfully in {elapsed:.2f}s")
            data_en = extract_json_from_response(response.text)
            return data_en
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")

    async def _generate_earnings_report(self, prompt: str, pdf_file_path: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        import time
        logger.info(f"[LLM - {schema.__name__}] Uploading PDF document for earnings report analysis...")
        uploaded_file = None
        try:
            uploaded_file = await self.client.aio.files.upload(file=pdf_file_path)
            file_info = await self.client.aio.files.get(name=uploaded_file.name)
            while file_info.state.name == "PROCESSING":
                await asyncio.sleep(2)
                file_info = await self.client.aio.files.get(name=uploaded_file.name)
                
            if file_info.state.name == "FAILED":
                logger.error("[LLM-Error] Document processing failed on Gemini servers.")
                raise InvalidDocumentFormatError("Gemini failed to process the uploaded document.")

            start_time = time.time()
            logger.info(f"[LLM - {schema.__name__}] Dispatching PDF analysis request to {model_id}...")
            response = await self.client.aio.models.generate_content(
                model=model_id,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0
                )
            )
            elapsed = time.time() - start_time
            logger.info(f"[LLM - {schema.__name__}] {model_id} PDF analysis completed in {elapsed:.2f}s")
            return json.loads(response.text)
        except Exception as e: 
            logger.error(f"[LLM-Error] Gemini API Error during _generate_earnings_report: {e}")
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            elif isinstance(e, InvalidDocumentFormatError):
                raise
            raise ExternalServiceError(f"Gemini API Error: {e}")
        finally:
            if uploaded_file is not None:
                try:
                    await self.client.aio.files.delete(name=uploaded_file.name)
                except Exception:
                    pass

    async def _generate_earnings_from_context(self, prompt: str, context: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        import time
        start_time = time.time()
        logger.info(f"[LLM - {schema.__name__}] Dispatching earnings context request to {model_id}...")
        try:
            response = await self.client.aio.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0
                )
            )
            elapsed = time.time() - start_time
            logger.info(f"[LLM] Resolved successfully in {elapsed:.2f}s.")
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"[LLM-Error] Gemini API Error during _generate_earnings_from_context: {e}")
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")

    async def _generate_dcf_assumptions(self, prompt: str, schema: Type[T], model_id: str = "gemini-3.1-pro-preview") -> dict:
        import time
        start_time = time.time()
        logger.info(f"[LLM - {schema.__name__}] Dispatching DCF assumptions request to {model_id}...")
        try:
            response = await self.client.aio.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0
                )
            )
            elapsed = time.time() - start_time
            logger.info(f"[LLM - {schema.__name__}] {model_id} responded successfully in {elapsed:.2f}s")
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"[LLM-Error] Gemini API Error during _generate_dcf_assumptions: {e}")
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")