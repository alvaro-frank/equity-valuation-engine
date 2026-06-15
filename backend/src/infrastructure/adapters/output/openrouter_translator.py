import json
import re
from openai import AsyncOpenAI
from application.ports.ports import TranslationPort
from infrastructure.utils.llm_utils import extract_json_from_response
import os

class OpenRouterTranslatorAdapter(TranslationPort):
    """
    A translation adapter for translating JSON data using the OpenRouter API.
    """
    def __init__(self, api_key: str = None):
        """
        Initializes the OpenRouter client with the provided API key or environment variable.
        
        Args:
            api_key (str): The API key for authenticating with the OpenRouter API. If not provided, it will be read from the OPENROUTER_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.model_id = os.getenv('TRANSLATOR_MODEL', 'google/gemini-2.5-flash-api')
        
    async def translate_json(self, data: dict, target_language: str) -> dict:
        """
        Translates the string values of a JSON object to the target language using the OpenRouter API.
        
        Args:
            data (dict): The JSON data to be translated.
            target_language (str): The language to translate the text into (e.g., 'en' for English, 'es' for Spanish).
            
        Returns:
            dict: A new dictionary with the same structure but with all string values translated to the target
        """
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
        3. BE EXTREMELY CAREFUL with JSON syntax. Do not add stray brackets or commas.
        4. Maintain the exact same JSON structure and arrays. Ensure every array and object is properly closed.
        5. Return ONLY valid, raw JSON. Do not include markdown formatting like ```json or any conversational text.
        6. CAUTION: 'economic_sensitivity' and 'interest_rate_exposure' are STRING fields, not arrays! DO NOT add a closing bracket ']' or '],' after their values. 
        7. DO NOT omit 'interest_rate_exposure' or any other field. YOU MUST RETURN THE EXACT SAME NUMBER OF KEYS.
        
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
                
            # Auto-repair common hallucination: '],' after a string field
            result_text = re.sub(r'\]\s*,\s*"interest_rate_exposure"', ',\n"interest_rate_exposure"', result_text)
            
            translated_dict = extract_json_from_response(result_text)
            
            # Re-inject original structural keys to prevent frontend dictionary misses
            if "sector" in data:
                translated_dict["sector"] = data["sector"]
            if "industry" in data:
                translated_dict["industry"] = data["industry"]
            if "ticker" in data and isinstance(data["ticker"], dict):
                if "sector" in data["ticker"]:
                    translated_dict["ticker"]["sector"] = data["ticker"]["sector"]
                if "industry" in data["ticker"]:
                    translated_dict["ticker"]["industry"] = data["ticker"]["industry"]
                    
            return translated_dict
        except Exception as e:
            print(f"Translation failed: {e}")
            return data # Fallback to original data if translation fails

    async def translate_text(self, text: str, target_language: str) -> str:
        """
        Translates a text string to the target language.

        Args:
            text (str): The text to be translated.
            target_language (str): The language to translate the text into.

        Returns:
            str: The translated text.
        """
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
