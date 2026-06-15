import json_repair
from application.exceptions.exceptions import LLMParsingError

def extract_json_from_response(text: str) -> dict:
    """
    Helper to extract json from markdown response.
    
    Args:
        text (str): The raw text response from the LLM, which may contain markdown formatting or extraneous text.
    
    Returns:
        dict: The extracted JSON object parsed into a Python dictionary.
    """
    text = text.strip()
    # Find the first { and the last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
        text = text[start_idx:end_idx+1]
    else:
        raise LLMParsingError("No JSON object found in response.")
    
    try:
        # Use json_repair to robustly handle LLM hallucinations like trailing commas or extra braces
        repaired_json = json_repair.loads(text)
        
        # In rare cases, json_repair might return a string if the input was completely broken
        if not isinstance(repaired_json, dict) and not isinstance(repaired_json, list):
             raise LLMParsingError("Parsed result is not a valid JSON object or array.")
             
        return repaired_json
    except Exception as e:
        raise LLMParsingError(f"Failed to parse JSON: {e}. Raw text: {text}")
