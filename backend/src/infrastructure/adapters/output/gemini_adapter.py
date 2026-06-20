from google import genai
from google.genai import types
import json
import asyncio
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from application.exceptions.exceptions import RateLimitExceededError, ConfigurationError, ExternalServiceError, InvalidDocumentFormatError
from application.ports.ports import TranslationPort
from infrastructure.utils.llm_utils import extract_json_from_response
from .base_llm_adapter import BaseLLMAdapter

T = TypeVar('T', bound=BaseModel)

def _remove_additional_properties(d):
    """
    Recursively removes 'additionalProperties' from a JSON schema dictionary.
    This is required because Gemini Developer API rejects schemas with 'additionalProperties': False,
    which Pydantic v2 includes by default.
    """
    if isinstance(d, dict):
        if "additionalProperties" in d:
            del d["additionalProperties"]
        for k, v in d.items():
            _remove_additional_properties(v)
    elif isinstance(d, list):
        for item in d:
            _remove_additional_properties(item)
    return d

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
            
        self.model_id = 'gemini-2.5-flash'

    async def _generate_company_profile(self, prompt: str, schema: Type[T]) -> dict:
        strict_search_mandate = "\n\nCRITICAL MANDATE: You MUST actively trigger the Google Search tool. Your response will be REJECTED if you do not use the search tool."
        current_prompt = prompt + strict_search_mandate
        
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=current_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    tools=[{"google_search": {}}]
                )
            )
            data_en = extract_json_from_response(response.text)
            
            # Extract grounding metadata URLs from Google Search
            sources = {}
            try:
                if hasattr(response, 'candidates') and response.candidates:
                    if hasattr(response.candidates[0], 'grounding_metadata') and response.candidates[0].grounding_metadata:
                        gm = response.candidates[0].grounding_metadata
                        if hasattr(gm, 'grounding_chunks') and gm.grounding_chunks:
                            for i, chunk in enumerate(gm.grounding_chunks):
                                if hasattr(chunk, 'web') and chunk.web:
                                    if hasattr(chunk.web, 'uri') and chunk.web.uri:
                                        sources[str(i + 1)] = chunk.web.uri
            except Exception as meta_e:
                print(f"Warning: Failed to extract grounding metadata: {meta_e}")
            
            data_en['sources'] = sources
            return data_en
        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")

    async def _generate_industry_dynamics(self, prompt: str, schema: Type[T]) -> dict:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=_remove_additional_properties(schema.model_json_schema()),
                    temperature=0.0,
                    max_output_tokens=8192
                )
            )
            return json.loads(response.text)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")

    async def _generate_earnings_report(self, prompt: str, pdf_file_path: str, schema: Type[T]) -> dict:
        uploaded_file = await self.client.aio.files.upload(file=pdf_file_path)
        file_info = await self.client.aio.files.get(name=uploaded_file.name)
        while file_info.state.name == "PROCESSING":
            await asyncio.sleep(2)
            file_info = await self.client.aio.files.get(name=uploaded_file.name)
            
        if file_info.state.name == "FAILED":
            raise InvalidDocumentFormatError("Gemini failed to process the uploaded PDF document.")

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=_remove_additional_properties(schema.model_json_schema()),
                    temperature=0.0
                )
            )
            return json.loads(response.text)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")
        finally:
            try:
                await self.client.aio.files.delete(name=uploaded_file.name)
            except Exception:
                pass

    async def _generate_dcf_assumptions(self, prompt: str, schema: Type[T]) -> dict:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=_remove_additional_properties(schema.model_json_schema()),
                    temperature=0.0,
                )
            )
            return json.loads(response.text)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")