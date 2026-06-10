import json
import asyncio
from openai import AsyncOpenAI
from application.ports.ports import TranslationPort
import os

class GroqTranslatorAdapter(TranslationPort):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
        )
        self.model_id = os.getenv('TRANSLATOR_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
        
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
        1. Translate ALL string values to the target language.
        2. DO NOT translate the main structural schema keys (e.g., sector, industry, rivalry_among_competitors, macro_risks, core_performance, etc).
        3. If a JSON key is inside an inner dictionary and acts as a dynamic title/factor (e.g. "Intensity of Competition", "Regulatory Hurdles"), YOU MUST TRANSLATE IT to the target language.
        4. DO NOT modify numbers, booleans, or null values.
        5. Maintain the exact same JSON structure and arrays.
        6. Return ONLY valid, raw JSON. Do not include markdown formatting like ```json or any conversational text.
        
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
            
            # Robust JSON extraction
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                result_text = result_text[start_idx:end_idx+1]
                
            return json.loads(result_text.strip())
        except Exception as e:
            print(f"Translation failed: {e}")
            return data # Fallback to original data if translation fails

    async def translate_text(self, text: str, target_language: str) -> str:
        if not text or target_language == "en":
            return text
            
        lang_instruction = target_language
        if target_language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms or grammar."

        prompt = f"""
        Translate the following text to {lang_instruction}.
        
        CRITICAL RULES:
        1. Maintain the professional and financial tone of the original text.
        2. Return ONLY the translated text. Do not include any conversational text, preamble, or quotes.
        
        Original Text:
        {text}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Text translation failed: {e}")
            return text

