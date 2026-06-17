import json
import re
from openai import AsyncOpenAI
from application.ports.ports import TranslationPort
from infrastructure.utils.llm_utils import extract_json_from_response
import os

class GroqTranslatorAdapter(TranslationPort):
    """
    A translation adapter for translating JSON data using the Groq API.
    """
    def __init__(self, api_key: str = None):
        """
        Initializes the Groq client with the provided API key or environment variable.
        
        Args:
            api_key (str): The API key for authenticating with the Groq API. If
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
        )
        self.model_id = os.getenv('TRANSLATOR_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
        
    async def translate_json(self, data: dict, target_language: str) -> dict:
        """
        Translates the string values of a JSON object to the target language.
        
        Args:
            data (dict): The JSON data to be translated.
            target_language (str): The language to translate the text into (e.g., 'en' for English, 'es' for Spanish).
            
        Returns:
            dict: A new dictionary with the same structure but with all string values translated to the target
        """
        if not data:
            return data
            
        lang_instruction = target_language
        if target_language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms or grammar."

        import copy
        result_data = copy.deepcopy(data)
        
        strings_to_translate = {}
        paths = []
        
        def traverse(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in ["ticker", "sector", "industry", "sector_key", "industry_key"] and isinstance(v, str):
                        continue
                    if isinstance(v, str):
                        # Avoid translating pure numbers or very short codes
                        if len(v.strip()) > 1 and not v.strip().isnumeric():
                            strings_to_translate[str(len(paths))] = v
                            paths.append((obj, k))
                    else:
                        traverse(v)
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    if isinstance(v, str):
                        if len(v.strip()) > 1 and not v.strip().isnumeric():
                            strings_to_translate[str(len(paths))] = v
                            paths.append((obj, i))
                    else:
                        traverse(v)

        traverse(result_data)
        
        if not strings_to_translate:
            return result_data
            
        json_str = json.dumps(strings_to_translate)
        
        prompt = f"""
        You are a precise JSON translation engine. 
        Your ONLY task is to translate the string values of the following flat JSON object to the target language: '{lang_instruction}'.
        
        CRITICAL RULES:
        1. Translate ALL string values to the target language.
        2. KEEP the numeric JSON keys exactly the same. Do not change the keys.
        3. Return ONLY valid, raw JSON. Do not include markdown formatting like ```json or any conversational text.
        
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
            translated_dict = extract_json_from_response(result_text)
            
            for idx_str, translated_text in translated_dict.items():
                if idx_str.isdigit():
                    idx = int(idx_str)
                    if idx < len(paths):
                        parent_obj, key = paths[idx]
                        parent_obj[key] = translated_text
                        
            return result_data
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

