import os
import json
import asyncio
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from openai import AsyncOpenAI
import fitz

from application.exceptions.exceptions import RateLimitExceededError, ConfigurationError, ExternalServiceError, InvalidDocumentFormatError
from application.ports.ports import TranslationPort
from infrastructure.utils.llm_utils import extract_json_from_response
from .base_llm_adapter import BaseLLMAdapter

T = TypeVar('T', bound=BaseModel)

class OpenRouterAdapter(BaseLLMAdapter):
    """
    Adapter that leverages OpenRouter to generate qualitative research.
    """
    def __init__(self, api_key: Optional[str] = None, client: Optional[AsyncOpenAI] = None, translator: Optional[TranslationPort] = None):
        super().__init__(translator=translator)
        if client:
            self.client = client
        else:
            if not api_key:
                api_key = os.getenv("OPENROUTER_API_KEY")
                if not api_key:
                    raise ConfigurationError("OPENROUTER_API_KEY is required")
            
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            
        self.model_id = os.getenv('OPENROUTER_MODEL', 'openrouter/free')

    async def _generate_company_profile(self, prompt: str, schema: Type[T]) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=8000,
            )
            content = response.choices[0].message.content
            return extract_json_from_response(content)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"OpenRouter Rate Limit: {e}")
            raise ExternalServiceError(f"OpenRouter API Error: {e}")

    async def _generate_industry_dynamics(self, prompt: str, schema: Type[T]) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=8000,
            )
            content = response.choices[0].message.content
            return extract_json_from_response(content)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"OpenRouter Rate Limit: {e}")
            raise ExternalServiceError(f"OpenRouter API Error: {e}")

    async def _generate_earnings_report(self, prompt: str, pdf_file_path: str, schema: Type[T]) -> dict:
        try:
            doc = fitz.open(pdf_file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            
            if not text.strip():
                raise InvalidDocumentFormatError("OpenRouter failed: No text could be extracted from the PDF.")
                
            MAX_CHARS = 100000
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS] + "...[TRUNCATED]"
                
            full_prompt = f"{prompt}\n\n[EARNINGS REPORT TEXT]\n{text}"
            
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.0,
                max_tokens=8000,
            )
            content = response.choices[0].message.content
            return extract_json_from_response(content)
        except InvalidDocumentFormatError:
            raise
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"OpenRouter Rate Limit: {e}")
            raise ExternalServiceError(f"OpenRouter API Error: {e}")

    async def _generate_dcf_assumptions(self, prompt: str, schema: Type[T]) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000,
            )
            content = response.choices[0].message.content
            return extract_json_from_response(content)
        except Exception as e: 
            error_str = str(e).lower()
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                raise RateLimitExceededError(f"OpenRouter Rate Limit: {e}")
            raise ExternalServiceError(f"OpenRouter API Error: {e}")
