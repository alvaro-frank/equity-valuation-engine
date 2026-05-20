from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
import json
import re
from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, MetricWithGrowth, CapitalAllocation, RiskDeconstruction
from decimal import Decimal
from infrastructure.schemas.gemini_schemas import CompanyProfileSchema, IndustrySectorDynamicsSchema, EarningsReportSchema
from typing import Optional

load_dotenv()

class GeminiAdapter(SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort):
    """
    Adapter that leverages Google's Gemini LLM to generate qualitative research.
    
    It transforms raw company and industry queries into structured Domain Entities 
    by enforcing a strict JSON schema via system prompting.
    """
    def __init__(self, client: Optional[genai.Client] = None):
        """
        Initializes the Gemini client using the API key from environment variables.
        """
        self.client = client or genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = 'gemini-2.5-flash'
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.gemini_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    async def analyse_company(self, symbol: str) -> CompanyProfile:
        """
        Uses Gemini to generate qualitative analysis report. 
        
        Args:
            symbol(str): The ticker symbol to be analysed
            
        Returns:
            CompanyProfile: A Domain Entity containing the qualitative data of the business
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
        
        cache_filename = f"company_{symbol.upper()}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        
        if os.path.exists(cache_path):
            file_age_seconds = time.time() - os.path.getmtime(cache_path)
            
            if file_age_seconds < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = None
            else:
                data = None 
        else:
            data = None
            
        if not data:
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=CompanyProfileSchema,
                        temperature=0.2,
                    )
                )
                
                data = json.loads(response.text)
                
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                    
            except Exception as e: 
                raise ConnectionError(f"Connection Error: {e}")
                
        schema_instance = CompanyProfileSchema(**data)
        
        return CompanyProfile(
            business_description=schema_instance.business_description,
            company_history=schema_instance.company_history,
            ceo_name=schema_instance.ceo_name,
            ceo_ownership=Decimal(str(schema_instance.ceo_ownership)),
            major_shareholders={s.name: Decimal(str(s.ownership)) for s in schema_instance.major_shareholders},
            revenue_model=schema_instance.revenue_model,
            strategy=schema_instance.strategy,
            products_services={p.name: p.description for p in schema_instance.products_services},
            competitive_advantage=schema_instance.competitive_advantage,
            competitors={c.name: c.overlap for c in schema_instance.competitors},
            management_insights=schema_instance.management_insights,
            risk_factors={r.title: r.description for r in schema_instance.risk_factors},
            historical_context_crises=schema_instance.historical_context_crises
        )
    
    async def analyse_industry(self, sector: str, industry: str) -> IndustrySectorDynamics:
        """
        Uses Gemini to perform a deep-dive analysis of industry dynamics and macro factors.
        
        Args:
            sector (str): The sector to be analysed
            industry (str): The industry to be analysed
        
        Returns:
            IndustrySectorDynamics: A Domain Entity containing the data given the sector and industry
        """
        prompt = f"""
        Act as a Senior Equity Research Analyst and Industry Strategist. 
        Perform a comprehensive fundamental analysis of the following market:
        SECTOR: {sector}
        INDUSTRY: {industry}

        CORE FRAMEWORK: Use Porter's Five Forces to evaluate structural profitability and competitive intensity.

        INSTRUCTIONS FOR JSON DICTIONARIES (Sections 1-5):
        For each force, identify 2-4 key factors. Return them as a dictionary where the KEY is a short, descriptive title (e.g., "Capital Intensity") and the VALUE is a professional analysis.

        REQUIRED ANALYSIS POINTS:
        1. Rivalry among Competitors: Intensity of competition, market concentration, and exit barriers.
        2. Bargaining Power of Suppliers: Supplier concentration, uniqueness of inputs, and switching costs.
        3. Bargaining Power of Customers: Buyer volume, price sensitivity, and ability to substitute.
        4. Threat of New Entrants: Barriers to entry (patents, economies of scale, regulatory hurdles).
        5. Threat of Obsolescence: Technology disruption risks and evolution of consumer preferences.
        6. Economic Sensitivity: Correlation with GDP, cyclicality (Cyclical vs. Defensive), and demand elasticity.
        7. Interest Rate Exposure: Impact on capital expenditures (CAPEX), financing costs, and consumer spending power.

        OUTPUT FORMAT:
        Return ONLY a valid JSON object following this exact schema:
        {{
            "sector": "{sector}",
            "industry": "{industry}",
            "rivalry_among_competitors": {{ "Key Factor": "Analysis..." }},
            "bargaining_power_of_suppliers": {{ "Key Factor": "Analysis..." }},
            "bargaining_power_of_customers": {{ "Key Factor": "Analysis..." }},
            "threat_of_new_entrants": {{ "Key Factor": "Analysis..." }},
            "threat_of_obsolescence": {{ "Key Factor": "Analysis..." }},
            "economic_sensitivity": "Detailed narrative about economic cycles.",
            "interest_rate_exposure": "Detailed narrative about rate impacts."
        }}

        Do not include markdown headers (like ```json), intro text, or conclusions. Return only raw JSON.
        """
        
        safe_sector = re.sub(r'[^a-zA-Z0-9]', '_', sector)
        safe_industry = re.sub(r'[^a-zA-Z0-9]', '_', industry)
        cache_filename = f"industry_{safe_sector}_{safe_industry}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        
        if os.path.exists(cache_path):
            file_age_seconds = time.time() - os.path.getmtime(cache_path)
            
            if file_age_seconds < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = None
            else:
                data = None 
        else:
            data = None
            
        if not data:
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=IndustrySectorDynamicsSchema,
                        temperature=0.2,
                    )
                )
                
                data = json.loads(response.text)
                
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                    
            except Exception as e: 
                raise ConnectionError(f"Connection Error: {e}")
                
        schema_instance = IndustrySectorDynamicsSchema(**data)
        
        return IndustrySectorDynamics(
            sector=schema_instance.sector,
            industry=schema_instance.industry,
            rivalry_among_competitors={f.factor: f.analysis for f in schema_instance.rivalry_among_competitors},
            bargaining_power_of_suppliers={f.factor: f.analysis for f in schema_instance.bargaining_power_of_suppliers},
            bargaining_power_of_customers={f.factor: f.analysis for f in schema_instance.bargaining_power_of_customers},
            threat_of_new_entrants={f.factor: f.analysis for f in schema_instance.threat_of_new_entrants},
            threat_of_obsolescence={f.factor: f.analysis for f in schema_instance.threat_of_obsolescence},
            economic_sensitivity=schema_instance.economic_sensitivity,
            interest_rate_exposure=schema_instance.interest_rate_exposure
        )

    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str) -> EarningsReport:
        """
        Uses Gemini to perform a deep-dive analysis of a company's earnings report.
        
        Args:
            symbol (str): The stock ticker symbol to fetch fundamental data for.
            pdf_file_path (str): The path to the PDF file containing the earnings report.
            
        Returns:
            EarningsReport: A Domain Entity containing the earnings report analysis.
        """
        prompt = f"""
        You are a Senior Equity Analyst focused on long-term value investing. I am providing the full text of an Earnings Report for the company "{symbol}". Ignore short-term stock reactions and Wall Street consensus. Focus exclusively on underlying business fundamentals.

        Perform a deep-dive analysis and return ONLY a structured JSON object. Do not include markdown formatting, code blocks, or conversational text.

        Extract and synthesize the following fields:

        1. period_end_date: (String) The end date of the fiscal period.
        2. core_performance: (Object) Extract Adjusted (Non-GAAP) Revenue, Adjusted EPS, Adjusted EBITDA margin, and Free Cash Flow. For each metric, return an object with two floats: 'amount' and 'yoy_growth' (percentage).
        3. capital_allocation: (Object) Detail exact amounts (as floats) spent on 'share_buybacks', 'dividends', and 'capex_rd'. Also provide an 'infrastructure_assessment' string assessing if infrastructure investment is accelerating or decelerating.
        4. forward_guidance: (String) Summary of management's projections for the next quarter/year (Raise, Lower, or Maintain).
        5. moat_trajectory: (String) Evidence of pricing power, market share changes, or competitive advantage expanding/shrinking.
        6. risk_deconstruction: (Object) Separate headwinds into two string lists: 'macro_risks' (external) and 'internal_risks' (execution/product).
        7. bottom_line: (String) A brutal, concise summary answering: Did the underlying business execute well, or are structural cracks forming?
        """

        pdf_basename = os.path.basename(pdf_file_path).replace(".pdf", "")
        cache_filename = f"earnings_{symbol.upper()}_{pdf_basename}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)

        if os.path.exists(cache_path):
            file_age_seconds = time.time() - os.path.getmtime(cache_path)
            
            if file_age_seconds < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = None
            else:
                data = None 
        else:
            data = None

        if data is None:
            uploaded_file = await self.client.aio.files.upload(file=pdf_file_path)

            try:
                response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EarningsReportSchema,
                    temperature=0.2,
                )
            )
            
                data = json.loads(response.text)
            
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

            except Exception as e: 
                raise ConnectionError(f"Connection Error: {e}")

        schema_instance = EarningsReportSchema(**data)

        return EarningsReport(
            period_end_date=schema_instance.period_end_date,
            core_performance=CorePerformance(
                adjusted_revenue=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.adjusted_revenue.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.adjusted_revenue.yoy_growth))
                ),
                adjusted_eps=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.adjusted_eps.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.adjusted_eps.yoy_growth))
                ),
                adjusted_ebitda_margin=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.adjusted_ebitda_margin.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.adjusted_ebitda_margin.yoy_growth))
                ),
                free_cash_flow=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.free_cash_flow.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.free_cash_flow.yoy_growth))
                )
            ),
            capital_allocation=CapitalAllocation(
                share_buybacks=Decimal(str(schema_instance.capital_allocation.share_buybacks)),
                dividends=Decimal(str(schema_instance.capital_allocation.dividends)),
                capex_rd=Decimal(str(schema_instance.capital_allocation.capex_rd)),
                infrastructure_assessment=schema_instance.capital_allocation.infrastructure_assessment
            ),
            forward_guidance=schema_instance.forward_guidance,
            moat_trajectory=schema_instance.moat_trajectory,
            risk_deconstruction=RiskDeconstruction(
                macro_risks=schema_instance.risk_deconstruction.macro_risks,
                internal_risks=schema_instance.risk_deconstruction.internal_risks
            ),
            bottom_line=schema_instance.bottom_line
        )