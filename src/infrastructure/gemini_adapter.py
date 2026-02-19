import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
from domain.interfaces import QualitativeDataProvider
from services.dtos import QualitativeDataDTO

load_dotenv()

class GeminiAdapter(QualitativeDataProvider):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyse_company(self, symbol: str) -> QualitativeDataDTO:
        """
        Uses Gemini to generate qualitative analysis report. 
        
        Args:
            symbol(str): The ticker symbol to be analysed
            
        Returns:
            QualitativeDataDTO: A data transfer object containing the qualitative data of the business
        """
        prompt = f"""
        Act as a Senior Equity Research Analyst specializing in Fundamental Analysis. 
        Your goal is to provide a deep qualitative assessment for the company: {symbol}.

        CRITICAL INSTRUCTIONS:
        - Accuracy: Use the most recent public information available up to your knowledge cutoff.
        - Data Types: 'ceo_ownership' must be a numeric representing a percentage (e.g., 3.5).
        - Dictionaries: For 'major_shareholders', 'products_services', 'competitors', and 'risk_factors', provide specific key-value pairs where the key is the Item Name and the value is the Detail/Stake.
        - Tone: Professional, objective, and data-driven.

        REQUIRED JSON STRUCTURE:
        Return ONLY a valid JSON object following this exact schema:
        {{
            "ticker": "{symbol}",
            "business_description": "A 3-4 sentence summary of core operations.",
            "company_history": "Key milestones from foundation to present.",
            "ceo_name": "Full name of current CEO.",
            "ceo_ownership": 5,
            "major_shareholders": {{
                "Shareholder Name": 14.5,
                "Other Name": 9.8
            }},
            "revenue_model": "Detailed explanation of revenue streams.",
            "strategy": "Core strategic focus and future outlook.",
            "products_services": {{
                "Product/Service A": "Brief description of utility",
                "Product/Service B": "Brief description of utility"
            }},
            "competitive_advantage": "Detailed MOAT analysis.",
            "competitors": {{
                "Competitor Name": "Main area of overlap/competition"
            }},
            "management_insights": "Analysis of management quality and track record.",
            "risk_factors": {{
                "Risk Title": "Detailed impact description"
            }},
            "historical_context_crises": "How the company navigated past major crises."
        }}

        Do not include any markdown formatting, preamble, or conversational text. Return only the raw JSON.
        """
        
        response = self.model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        
        return QualitativeDataDTO.model_validate_json(clean_json)