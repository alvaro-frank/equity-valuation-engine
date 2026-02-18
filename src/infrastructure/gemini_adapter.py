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
        Act as a Senior Equity Research Analyst. Provide a professional qualitative analysis for: {symbol}.
        
        INSTRUCTIONS:
        1. Business Description: Summarize the core business model.
        2. Company History: Detail the foundation and evolution.
        3. CEO: Current CEO name and background.
        4. CEO Ownership: Estimated % of shares held by the CEO.
        5. Major Shareholders: Main institutional or individual owners.
        6. Revenue Model: How exactly they generate money.
        7. Strategy: Core strategic focus for the next few years.
        8. Products & Services: List main offerings.
        9. MOAT: Sustainable competitive advantages.
        10. Competitors: Main rivals.
        11. Management: Evaluation of execution and quality.
        12. Risks: Critical threats.
        13. Crises: Major historical crises overcome.

        OUTPUT FORMAT:
        Return ONLY a valid JSON object:
        {{
            "ticker": "{symbol}",
            "business_description": "...",
            "company_history": "...",
            "ceo_name": "...",
            "ceo_ownership": "...",
            "major_shareholders": ["...", "..."],
            "revenue_model": "...",
            "strategy": "...",
            "products_services": ["...", "..."],
            "competitive_advantage": "...",
            "competitors": ["...", "..."],
            "management_insights": "...",
            "risk_factors": ["Risk 1", "Risk 2", "Risk 3"],
            "historical_context_crises": "..."
        }}
        """
        
        response = self.model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        
        return QualitativeDataDTO.model_validate_json(clean_json)