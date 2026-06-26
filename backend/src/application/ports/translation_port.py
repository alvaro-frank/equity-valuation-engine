from abc import ABC, abstractmethod

class TranslationPort(ABC):
    """
    Interface for translating raw JSON data via an LLM or Translation API.
    """
    @abstractmethod
    async def translate_json(self, data: dict, target_language: str) -> dict:
        """
        Translates the string values of a JSON dictionary to the target language, preserving keys and structure.
        
        Args:            
            data (dict): The JSON data to be translated.
            target_language (str): The language to translate the text into (e.g., 'en' for English, 'es' for Spanish).
        
        Returns:
            dict: A new dictionary with the same structure but with all string values translated to the target
        """
        pass
        
    @abstractmethod
    async def translate_text(self, text: str, target_language: str) -> str:
        """
        Translates a plain string to the target language.
        
        Args:
            text (str): The text to be translated.
            target_language (str): The language to translate the text into (e.g., 'en' for English, 'es' for Spanish).
        
        Returns:
            str: The translated text.
        """
        pass
