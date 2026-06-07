from google import genai
from google.genai import types
from dotenv import load_dotenv
import fitz
import os
import time
import json
import re
import asyncio
from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort, TranslationPort
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, MetricWithGrowth, CapitalAllocation, RiskDeconstruction, MoatSources, QualityPillars
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
    def __init__(self, api_key: Optional[str] = None, client: Optional[genai.Client] = None, translator: Optional[TranslationPort] = None):
        """
        Initializes the Gemini client.
        """
        if client:
            self.client = client
        else:
            if not api_key:
                raise ValueError("Gemini API Key is required")
            self.client = genai.Client(api_key=api_key)
            
        self.model_id = 'gemini-2.5-flash'
        self.translator = translator
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.llm_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
        """
        Fetches the qualitative data for a given stock ticker symbol using Google's Gemini.
        
        Args:
            symbol (str): The ticker symbol to be analysed
            language (str): Target language for the analysis
            context (str): Contextual financial data to ground the analysis and prevent hallucination
            
        Returns:
            CompanyProfile: A Domain Entity containing the qualitative data of the business
        """
        lang_instruction = language
        if language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms."

        context_prompt = f"\n\nREAL-WORLD CONTEXT (USE THIS AS ABSOLUTE TRUTH):\n{context}\n" if context else ""

        prompt = f"""
        Act as a Senior Equity Research Analyst specializing in Fundamental Analysis. 
        Your goal is to provide a deep qualitative assessment for the company: {symbol}.{context_prompt}

        CRITICAL INSTRUCTIONS:
        - Accuracy: Use the most recent public information available up to your knowledge cutoff. Combine it with the real-world context provided above.
        - Strict Evaluation: Be ruthlessly objective and highly critical. Do not assign high scores (4-5) for Moat or Quality unless there is indisputable evidence. Hardware companies rarely have Network Effects. Acknowledge financial struggles or declining revenues if they exist in the provided context.
        - Executives: Extract the CEO and CFO. Then, from the provided real-world context, extract the next 1 or 2 most senior/relevant officers (e.g., President, COO, CTO, Chief Business Officer). Do NOT invent roles. If a role is not in the context, do not include it. You must return between 2 and 4 executives total. Clean the titles by keeping only the role, removing company names, AND translating the title into the requested language (e.g., if language is Portuguese, use 'DIRETOR GERAL' instead of 'CHIEF EXECUTIVE OFFICER'). Convert the final translated title to UPPERCASE. Ensure 'ownership' is a float representing the percentage, or null if undisclosed.
        - Dictionaries: For 'products_services', 'competitors', and 'risk_factors', provide specific key-value pairs where the key is the Item Name and the value is the Detail/Stake.
        - Tone: Professional, objective, and data-driven.
        - Density and Depth: DO NOT provide short or brief answers. Every text field must be highly analytical, comprehensive, and detailed, acting as a professional equity research report.
        - Language: Generate the analysis text in the following language: {lang_instruction}. IMPORTANT: The JSON keys must remain strictly in English as defined by the schema.

        REQUIRED JSON STRUCTURE:
        Return ONLY a valid JSON object following this exact schema:
        {{
            "business_description": "A comprehensive 4-6 sentence deep dive into the core operations and business model.",
            "company_history": "Key milestones from foundation to present.",
            "key_executives": [
                {{ "name": "Name A", "title": "CHIEF EXECUTIVE OFFICER", "ownership": 5.2 }},
                {{ "name": "Name B", "title": "CHIEF FINANCIAL OFFICER", "ownership": 1.2 }},
                {{ "name": "Name C", "title": "PRESIDENT & CHIEF INVESTMENT OFFICER", "ownership": 0.5 }},
                {{ "name": "Name D", "title": "CHIEF TECHNOLOGY OFFICER", "ownership": 0.1 }}
            ],
            "revenue_model": "Highly detailed explanation (3-4 sentences) of all major revenue streams, pricing power, and monetization strategy.",
            "strategy": "Core strategic focus and future outlook.",
            "products_services": {{
                "Product/Service A": "Comprehensive 2-3 sentence description explaining the utility, market fit, and strategic importance.",
                "Product/Service B": "Comprehensive 2-3 sentence description explaining the utility, market fit, and strategic importance."
            }},
            "competitive_advantage": "Deep 4-5 sentence analysis defending the existence, strength, and durability of the Moat.",
            "competitors": {{
                "Competitor Name": "Detailed 2-3 sentence analysis of competitive dynamics, market share battles, and specific overlap."
            }},
            "management_insights": "Analysis of management quality and track record.",
            "risk_factors": {{
                "Risk Title": "Detailed 2-3 sentence breakdown of the risk impact and probability."
            }},
            "historical_context_crises": "How the company navigated past major crises.",
            "moat_trajectory": "Detailed 2-3 sentence analysis of the company's competitive advantage trajectory (expanding or shrinking and why).",
            "moat_sources": {{
                "intangible_assets": 4,
                "switching_costs": 3,
                "network_effect": 5,
                "cost_advantage": 2,
                "efficient_scale": 1
            }},
            "quality_pillars": {{
                "management_quality": 4,
                "business_model_resilience": 5,
                "pricing_power": 4,
                "innovation_and_growth": 3,
                "tam_expansion": 4
            }}
        }}

        Do not include any markdown formatting, preamble, or conversational text. Return only the raw JSON.
        """
        
        cache_filename = f"company_{symbol.upper()}_{language}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        
        cache_filename_en = f"company_{symbol.upper()}_en.json"
        cache_path_en = os.path.join(self.cache_dir, cache_filename_en)
        
        data = None
        if os.path.exists(cache_path):
            if time.time() - os.path.getmtime(cache_path) < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    pass
                    
        if not data:
            data_en = None
            if os.path.exists(cache_path_en):
                if time.time() - os.path.getmtime(cache_path_en) < 86400:
                    try:
                        with open(cache_path_en, 'r', encoding='utf-8') as f:
                            data_en = json.load(f)
                    except Exception:
                        pass
                        
            if not data_en:
                # Force English for base extraction
                prompt_en = prompt.replace(lang_instruction, "English")
                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=prompt_en,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=CompanyProfileSchema,
                            temperature=0.0,
                        )
                    )
                    data_en = json.loads(response.text)
                    with open(cache_path_en, 'w', encoding='utf-8') as f:
                        json.dump(data_en, f, indent=4)
                except Exception as e: 
                    raise ConnectionError(f"Connection Error: {e}")
            
            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

        schema_instance = CompanyProfileSchema(**data)
        
        return CompanyProfile(
            business_description=schema_instance.business_description,
            company_history=schema_instance.company_history,
            key_executives=[{"name": e.name, "title": e.title, "ownership": float(e.ownership) if e.ownership is not None else None} for e in schema_instance.key_executives],
            revenue_model=schema_instance.revenue_model,
            strategy=schema_instance.strategy,
            products_services={p.name: p.description for p in schema_instance.products_services},
            competitive_advantage=schema_instance.competitive_advantage,
            competitors={c.name: c.overlap for c in schema_instance.competitors},
            management_insights=schema_instance.management_insights,
            risk_factors={r.title: r.description for r in schema_instance.risk_factors},
            historical_context_crises=schema_instance.historical_context_crises,
            moat_trajectory=schema_instance.moat_trajectory,
            moat_sources=MoatSources(**schema_instance.moat_sources.model_dump()),
            quality_pillars=QualityPillars(**schema_instance.quality_pillars.model_dump())
        )
    
    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
        """
        Uses Gemini to perform a deep-dive analysis of industry dynamics and macro factors.
        
        Args:
            sector (str): The sector to be analysed
            industry (str): The industry to be analysed
        
        Returns:
            IndustrySectorDynamics: A Domain Entity containing the data given the sector and industry
        """
        lang_instruction = language
        if language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms."

        prompt = f"""
        Act as a Senior Equity Research Analyst and Industry Strategist. 
        Perform a comprehensive fundamental analysis of the following market:
        SECTOR: {sector}
        INDUSTRY: {industry}

        CORE FRAMEWORK: Use Porter's Five Forces to evaluate structural profitability and competitive intensity.

        INSTRUCTIONS FOR JSON DICTIONARIES (Sections 1-5):
        For each force, identify 2-4 key factors. Return them as a dictionary where the KEY is a short, descriptive title (e.g., "Capital Intensity") and the VALUE is a professional analysis.
        Language: Generate the analysis text in the following language: {lang_instruction}. IMPORTANT: The JSON keys must remain strictly in English as defined by the schema.

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
        cache_filename = f"industry_{safe_sector}_{safe_industry}_{language}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        
        cache_filename_en = f"industry_{safe_sector}_{safe_industry}_en.json"
        cache_path_en = os.path.join(self.cache_dir, cache_filename_en)
        
        data = None
        if os.path.exists(cache_path):
            if time.time() - os.path.getmtime(cache_path) < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    pass

        if not data:
            data_en = None
            if os.path.exists(cache_path_en):
                if time.time() - os.path.getmtime(cache_path_en) < 86400:
                    try:
                        with open(cache_path_en, 'r', encoding='utf-8') as f:
                            data_en = json.load(f)
                    except Exception:
                        pass

            if not data_en:
                # Force English for base extraction
                prompt_en = prompt.replace(lang_instruction, "English")
                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=prompt_en,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=IndustrySectorDynamicsSchema,
                            temperature=0.0,
                        )
                    )
                    data_en = json.loads(response.text)
                    with open(cache_path_en, 'w', encoding='utf-8') as f:
                        json.dump(data_en, f, indent=4)
                except Exception as e: 
                    raise ConnectionError(f"Connection Error: {e}")
            
            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

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

    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en") -> EarningsReport:
        """
        Uses Gemini to perform a deep-dive analysis of a company's earnings report.
        
        Args:
            symbol (str): The stock ticker symbol to fetch fundamental data for.
            pdf_file_path (str): The path to the PDF file containing the earnings report.
            
        Returns:
            EarningsReport: A Domain Entity containing the earnings report analysis.
        """
        lang_instruction = language
        if language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms."

        prompt = f"""
        You are a Senior Equity Analyst focused on long-term value investing. I am providing the full text of an Earnings Report for the company "{symbol}". Ignore short-term stock reactions and Wall Street consensus. Focus exclusively on underlying business fundamentals.

        Perform a deep-dive analysis and return ONLY a structured JSON object. Do not include markdown formatting, code blocks, or conversational text.
        Language: Generate the analysis text in the following language: {lang_instruction}. IMPORTANT: The JSON keys must remain strictly in English as defined by the schema.

        Extract and synthesize the following fields EXACTLY as named.
        CRITICAL: For margins and yoy_growth, output as whole percentages (e.g. 66.3 for 66.3%) and NOT as decimals (e.g. 0.663). For amounts, use Billions if applicable.

        1. period_end_date: (String) The end date of the fiscal period.
        2. core_performance: (Object) Extract Adjusted (Non-GAAP) Revenue, Adjusted EPS, Adjusted Gross Margin, Adjusted Operating Margin, Adjusted Net Margin, and Free Cash Flow. For each metric, return an object with two floats: 'amount' and 'yoy_growth' (percentage).
        3. capital_allocation: (Object) Detail exact amounts (as floats) spent on 'share_buybacks', 'dividends', and 'capex_rd'. Also provide an 'infrastructure_assessment' string containing a full 2-3 sentence paragraph assessing the "why" behind the CapEx (e.g. accelerating for AI buildout, or cutting back to preserve cash). Do not just provide a single word.
        4. forward_guidance: (String) Detailed 2-3 sentence analysis of management's forward-looking projections and guidance.
        5. moat_trajectory: (String) Detailed 2-3 sentence analysis of the company's competitive advantage trajectory (e.g., is pricing power expanding or shrinking and why).
        6. risk_deconstruction: (Object) Separate headwinds into two string lists: 'macro_risks' (external) and 'internal_risks' (execution/product).
        7. bottom_line: (String) A brutal, concise summary answering: Did the underlying business execute well, or are structural cracks forming?
        """

        import hashlib
        with open(pdf_file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:12]
        cache_filename = f"earnings_{symbol.upper()}_{file_hash}_{language}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        
        cache_filename_en = f"earnings_{symbol.upper()}_{file_hash}_en.json"
        cache_path_en = os.path.join(self.cache_dir, cache_filename_en)
        
        data = None
        if os.path.exists(cache_path):
            if time.time() - os.path.getmtime(cache_path) < 86400:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    pass

        if not data:
            data_en = None
            if os.path.exists(cache_path_en):
                if time.time() - os.path.getmtime(cache_path_en) < 86400:
                    try:
                        with open(cache_path_en, 'r', encoding='utf-8') as f:
                            data_en = json.load(f)
                    except Exception:
                        pass

            if not data_en:
                # Need to run Gemini for EN
                uploaded_file = await self.client.aio.files.upload(file=pdf_file_path)
                file_info = await self.client.aio.files.get(name=uploaded_file.name)
                while file_info.state.name == "PROCESSING":
                    import asyncio
                    await asyncio.sleep(2)
                    file_info = await self.client.aio.files.get(name=uploaded_file.name)
                    
                if file_info.state.name == "FAILED":
                    raise ValueError("Gemini failed to process the uploaded PDF document.")

                prompt_en = prompt.replace(lang_instruction, "English")
                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=[prompt_en, uploaded_file],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=EarningsReportSchema,
                            temperature=0.0,
                        )
                    )
                    data_en = json.loads(response.text)
                    with open(cache_path_en, 'w', encoding='utf-8') as f:
                        json.dump(data_en, f, indent=4)
                except Exception as e: 
                    raise ConnectionError(f"Connection Error: {e}")

            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

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

                adjusted_gross_margin=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.adjusted_gross_margin.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.adjusted_gross_margin.yoy_growth))
                ),
                adjusted_operating_margin=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.adjusted_operating_margin.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.adjusted_operating_margin.yoy_growth))
                ),
                adjusted_net_margin=MetricWithGrowth(
                    amount=Decimal(str(schema_instance.core_performance.adjusted_net_margin.amount)),
                    yoy_growth=Decimal(str(schema_instance.core_performance.adjusted_net_margin.yoy_growth))
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