import os
import json
import time
import re
from openai import AsyncOpenAI
import pymupdf4llm
from dotenv import load_dotenv
from decimal import Decimal
from typing import Optional

from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, MetricWithGrowth, CapitalAllocation, RiskDeconstruction
from infrastructure.schemas.gemini_schemas import CompanyProfileSchema, IndustrySectorDynamicsSchema, EarningsReportSchema

load_dotenv()

class OpenRouterAdapter(SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort):
    """
    Adapter that leverages OpenRouter (specifically DeepSeek) to generate qualitative research.
    """
    def __init__(self, api_key: Optional[str] = None):
        if not api_key:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is required")
        
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
            
        # self.model_id = 'deepseek/deepseek-chat'
        self.model_id = 'deepseek/deepseek-chat' # Use standard deepseek v3/v4 depending on availability
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.openrouter_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_json_from_response(self, text: str) -> dict:
        """Helper to extract json from markdown response."""
        text = text.strip()
        # Find the first { and the last }
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            text = text[start_idx:end_idx+1]
        else:
            raise ValueError("No JSON object found in response.")
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}. Raw text: {text}")

    async def analyse_company(self, symbol: str) -> CompanyProfile:
        prompt = f"""
        Act as a Senior Equity Research Analyst specializing in Fundamental Analysis. 
        Your goal is to provide a deep qualitative assessment for the company: {symbol}.

        CRITICAL INSTRUCTIONS:
        - Accuracy: Use the most recent public information available up to your knowledge cutoff.
        - Data Types: 'ceo_ownership' must be a numeric representing a percentage (e.g., 3.5).
        - Lists of Objects: For 'major_shareholders', 'products_services', 'competitors', and 'risk_factors', provide a list of objects as specified in the schema.
        - Tone: Professional, objective, and data-driven.

        REQUIRED JSON STRUCTURE:
        Return ONLY a valid JSON object following this exact schema:
        {{
            "business_description": "A 3-4 sentence summary of core operations.",
            "company_history": "Key milestones from foundation to present.",
            "ceo_name": "Full name of current CEO.",
            "ceo_ownership": 5,
            "major_shareholders": [
                {{ "name": "Shareholder Name", "ownership": 14.5 }},
                {{ "name": "Other Name", "ownership": 9.8 }}
            ],
            "revenue_model": "Detailed explanation of revenue streams.",
            "strategy": "Core strategic focus and future outlook.",
            "products_services": [
                {{ "name": "Product/Service A", "description": "Brief description of utility" }}
            ],
            "competitive_advantage": "Detailed MOAT analysis.",
            "competitors": [
                {{ "name": "Competitor Name", "overlap": "Main area of overlap/competition" }}
            ],
            "management_insights": "Analysis of management quality and track record.",
            "risk_factors": [
                {{ "title": "Risk Title", "description": "Detailed impact description" }}
            ],
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
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                
                data = self._get_json_from_response(response.choices[0].message.content)
                
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
        prompt = f"""
        Act as a Senior Equity Research Analyst and Industry Strategist. 
        Perform a comprehensive fundamental analysis of the following market:
        SECTOR: {sector}
        INDUSTRY: {industry}

        CORE FRAMEWORK: Use Porter's Five Forces to evaluate structural profitability and competitive intensity.

        INSTRUCTIONS FOR JSON ARRAYS (Sections 1-5):
        For each force, identify 2-4 key factors. Return them as a LIST of objects, where each object has a 'factor' (short, descriptive title) and an 'analysis' (professional analysis).

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
            "rivalry_among_competitors": [ {{ "factor": "Key Factor", "analysis": "Analysis..." }} ],
            "bargaining_power_of_suppliers": [ {{ "factor": "Key Factor", "analysis": "Analysis..." }} ],
            "bargaining_power_of_customers": [ {{ "factor": "Key Factor", "analysis": "Analysis..." }} ],
            "threat_of_new_entrants": [ {{ "factor": "Key Factor", "analysis": "Analysis..." }} ],
            "threat_of_obsolescence": [ {{ "factor": "Key Factor", "analysis": "Analysis..." }} ],
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
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                
                data = self._get_json_from_response(response.choices[0].message.content)
                
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
        prompt = f"""
        You are a Senior Equity Analyst focused on long-term value investing. I am providing the full text of an Earnings Report for the company "{symbol}". Ignore short-term stock reactions and Wall Street consensus. Focus exclusively on underlying business fundamentals.

        Perform a deep-dive analysis and return ONLY a structured JSON object. Do not include markdown formatting, code blocks, or conversational text.

        Extract and synthesize the following fields EXACTLY as named:

        {{
            "ticker": "String: The stock ticker symbol",
            "period_end_date": "String: The end date of the fiscal period",
            "core_performance": {{
                "adjusted_revenue": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "adjusted_eps": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "adjusted_ebitda_margin": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "free_cash_flow": {{ "amount": 0.0, "yoy_growth": 0.0 }}
            }},
            "capital_allocation": {{
                "share_buybacks": 0.0,
                "dividends": 0.0,
                "capex_rd": 0.0,
                "infrastructure_assessment": "String: Assess if infrastructure investment is accelerating or decelerating"
            }},
            "forward_guidance": "String: Detailed 2-3 sentence analysis of management's forward-looking projections and guidance",
            "moat_trajectory": "String: Detailed 2-3 sentence analysis of the company's competitive advantage trajectory (e.g., is pricing power expanding or shrinking and why)",
            "risk_deconstruction": {{
                "macro_risks": ["String", "String"],
                "internal_risks": ["String", "String"]
            }},
            "bottom_line": "String: A brutal, concise summary answering if the business executed well or if structural cracks are forming."
        }}
        """

        pdf_basename = os.path.basename(pdf_file_path).replace(".pdf", "")
        cache_filename = f"earnings_{symbol.upper()}_{pdf_basename}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)

        if os.path.exists(cache_path):
            file_age_seconds = time.time() - os.path.getmtime(cache_path)
            if file_age_seconds < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    # Validate cache before accepting it
                    EarningsReportSchema(**cached_data)
                    data = cached_data
                except Exception:
                    data = None
            else:
                data = None 
        else:
            data = None

        if data is None:
            # Extract markdown text from PDF
            md_text = pymupdf4llm.to_markdown(pdf_file_path)
            
            # Combine prompt and PDF text
            full_prompt = prompt + f"\n\n--- EARNINGS REPORT TEXT ---\n\n{md_text}"

            try:
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[{"role": "user", "content": full_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                
                data = self._get_json_from_response(response.choices[0].message.content)
            
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                    
                schema_instance = EarningsReportSchema(**data)

            except Exception as e: 
                raise ConnectionError(f"OpenRouter Fallback Error: {e}")

        # Ensure schema instance exists
        if 'schema_instance' not in locals():
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
