import json
import copy
from abc import ABC, abstractmethod
from application.ports.ports import TranslationPort
from infrastructure.utils.llm_utils import extract_json_from_response

class BaseLLMTranslator(TranslationPort, ABC):
    """
    Abstract base class for all LLM-based translation adapters.
    Implements a robust flattening and re-injection strategy for JSON translations
    to prevent structural corruption and schema hallucinations by LLMs.
    """

    @abstractmethod
    async def _call_translation_api(self, prompt: str, is_json: bool) -> str:
        """
        Subclasses must implement this method to call their specific LLM provider.
        
        Args:
            prompt (str): The instruction and content to be translated.
            is_json (bool): Whether the expected output is JSON format.
            
        Returns:
            str: The raw text response from the LLM.
        """
        pass

    async def translate_json(self, data: dict, target_language: str) -> dict:
        if not data:
            return data
            
        lang_instruction = target_language
        if target_language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms or grammar."

        result_data = copy.deepcopy(data)
        
        strings_to_translate = {}
        paths = []
        
        def traverse(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in ["ticker", "sector", "industry", "sector_key", "industry_key", "sources", "moat_trajectory_status"]:
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
        3. PRESERVE any numerical citation brackets (e.g., [1], [2]) EXACTLY as they appear in the original text. Do not remove or alter them.
        4. Return ONLY valid, raw JSON. Do not include markdown formatting like ```json or any conversational text.
        
        JSON to translate:
        {json_str}
        """
        
        try:
            result_text = await self._call_translation_api(prompt=prompt, is_json=True)
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
            result_text = await self._call_translation_api(prompt=prompt, is_json=False)
            return result_text.strip()
        except Exception as e:
            print(f"Text translation failed: {e}")
            return text
