import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiAdapter:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_company(self, ticker: str) -> dict:
        """
        Uses Gemini to generate qualitative analysis report. 
        """
        prompt = f"""
        Act as a Senior Equity Research Analyst specializing in fundamental analysis. 

        Your task is to provide a concise qualitative summary for the company with the ticker: {ticker}.

        INSTRUCTIONS:
        1. Summarize the "Business Description" focusing on the core business model and how the company makes money.
        2. Provide a "Company History" highlighting the foundation and at least 3 major strategic milestones.
        4. The tone must be professional, objective, and data-driven.

        OUTPUT FORMAT:
        You MUST return ONLY a valid JSON object. Do not include markdown headers like ```json or any conversational text. The JSON must follow this schema:

        {{
            "ticker": "{ticker}",
            "business_description": "A concise 3-4 sentence summary of the business model.",
            "company_history": "A paragraph detailing foundation and key historical pivots."
        }}
        """
        
        response = self.model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_json)