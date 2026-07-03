from google import genai
from google.genai import types
import json
import asyncio
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from application.exceptions.exceptions import RateLimitExceededError, ConfigurationError, ExternalServiceError, InvalidDocumentFormatError
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
            raw_text = response.text
            sources = []
            try:
                if hasattr(response, 'candidates') and response.candidates:
                    gm = getattr(response.candidates[0], 'grounding_metadata', None)
                    if gm:
                        # Extract sources
                        if hasattr(gm, 'grounding_chunks') and gm.grounding_chunks:
                            for i, chunk in enumerate(gm.grounding_chunks):
                                web = getattr(chunk, 'web', None)
                                if web and getattr(web, 'uri', None):
                                    title = getattr(web, 'title', 'source')
                                    sources.append({"citation_id": str(i + 1), "url": web.uri, "title": title})
                        
                        # Inject citations into raw_text
                        if hasattr(gm, 'grounding_supports') and gm.grounding_supports:
                            # Sort by end_index descending to avoid offset shifting
                            supports_sorted = sorted(
                                [s for s in gm.grounding_supports if hasattr(s, 'segment') and s.segment],
                                key=lambda s: s.segment.end_index, 
                                reverse=True
                            )
                            for support in supports_sorted:
                                end_idx = support.segment.end_index
                                indices = getattr(support, 'grounding_chunk_indices', [])
                                if indices:
                                    citation_nums = [str(idx + 1) for idx in indices]
                                    citation_str = f" [{', '.join(citation_nums)}]"
                                    raw_text = raw_text[:end_idx] + citation_str + raw_text[end_idx:]
                                    
            except Exception as meta_e:
                print(f"Warning: Failed to extract grounding metadata: {meta_e}")

            data_en = extract_json_from_response(raw_text)
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
                    response_schema=schema,
                    temperature=0.0,
                    max_output_tokens=8192
                )
            )
            return extract_json_from_response(response.text)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")

    async def _generate_earnings_report(self, prompt: str, pdf_file_path: str, schema: Type[T]) -> dict:
        uploaded_file = None
        try:
            uploaded_file = await self.client.aio.files.upload(file=pdf_file_path)
            file_info = await self.client.aio.files.get(name=uploaded_file.name)
            while file_info.state.name == "PROCESSING":
                await asyncio.sleep(2)
                file_info = await self.client.aio.files.get(name=uploaded_file.name)
                
            if file_info.state.name == "FAILED":
                raise InvalidDocumentFormatError("Gemini failed to process the uploaded document.")

            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0
                )
            )
            return json.loads(response.text)
        except Exception as e: 
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

    async def _generate_dcf_assumptions(self, prompt: str, schema: Type[T]) -> dict:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0,
                )
            )
            return json.loads(response.text)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
            raise ExternalServiceError(f"Gemini API Error: {e}")