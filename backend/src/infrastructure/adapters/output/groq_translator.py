import os
from openai import AsyncOpenAI
from .base_llm_translator import BaseLLMTranslator

class GroqTranslatorAdapter(BaseLLMTranslator):
    """
    A translation adapter for translating JSON data using the Groq API.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
        )
        self.model_id = os.getenv('TRANSLATOR_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')

    async def _call_translation_api(self, prompt: str, is_json: bool) -> str:
        response = await self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": "You are a machine that outputs only raw, valid JSON." if is_json else "You are a highly precise translator machine."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=8000
        )
        return response.choices[0].message.content.strip()
