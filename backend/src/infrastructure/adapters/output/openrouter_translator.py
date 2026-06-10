import json
import asyncio
from openai import AsyncOpenAI
from application.ports.ports import TranslationPort
import os

class OpenRouterTranslatorAdapter(TranslationPort):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.model_id = os.getenv('TRANSLATOR_MODEL', 'openrouter/free')
        
    async def translate_json(self, data: dict, target_language: str) -> dict:
        if not data:
            return data
            
        json_str = json.dumps(data)
        
        lang_instruction = target_language
        if target_language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms or grammar."

        prompt = f"""
        You are a precise JSON translation engine. 
        Your ONLY task is to translate the string values of the following JSON object to the target language: '{lang_instruction}'.
        
        CRITICAL RULES:
        1. DO NOT translate or modify ANY JSON keys.
        2. DO NOT modify numbers, booleans, or null values.
        3. Maintain the exact same JSON structure and arrays.
        4. Return ONLY valid, raw JSON. Do not include markdown formatting like ```json or any conversational text.
        
        JSON to translate:
        {json_str}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": "You are a machine that outputs only raw, valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=8000
            )
            
            result_text = response.choices[0].message.content.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
                
            return json.loads(result_text.strip())
        except Exception as e:
            print(f"Translation failed: {e}")
            return data # Fallback to original data if translation fails
