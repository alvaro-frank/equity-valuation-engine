from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
import json
import re
from application.exceptions.exceptions import RateLimitExceededError, ConfigurationError, ExternalServiceError, InvalidDocumentFormatError
from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort, TranslationPort
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, MetricWithGrowth, CapitalAllocation, RiskDeconstruction, MoatSources, QualityPillars
from decimal import Decimal
from infrastructure.schemas.llm_schemas import CompanyProfileSchema, IndustrySectorDynamicsSchema, EarningsReportSchema

def _remove_additional_properties(d):
    """
    Recursively removes 'additionalProperties' from a JSON schema dictionary.
    This is required because Gemini Developer API rejects schemas with 'additionalProperties': False,
    which Pydantic v2 includes by default.
    """
    if isinstance(d, dict):
        if "additionalProperties" in d:
            del d["additionalProperties"]
        for k, v in d.items():
            _remove_additional_properties(v)
    elif isinstance(d, list):
        for item in d:
            _remove_additional_properties(item)
    return d
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
        
        Args:
            api_key (Optional[str]): The API key for authenticating with the Gemini API. Required if no client is provided.
            client (Optional[genai.Client]): An optional pre-initialized Gemini client. If not provided, a new client will be created using the api_key.
            translator (Optional[TranslationPort]): An optional translation port to handle translations of the generated content. If not provided, no translation will be performed.
        """
        if client:
            self.client = client
        else:
            if not api_key:
                raise ConfigurationError("Gemini API Key is required")
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
        context_prompt = f"\n\nREAL-WORLD CONTEXT (USE THIS AS ABSOLUTE TRUTH):\n{context}\n" if context else ""

        prompt = f"""
        Act as a Senior Equity Research Analyst specializing in Fundamental Analysis. 
        Your goal is to provide a deep qualitative assessment for the company: {symbol}.{context_prompt}

        CRITICAL INSTRUCTIONS:
        - Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.
        - Accuracy: Use the most recent public information available up to your knowledge cutoff. Combine it with the real-world context provided above.
        - Strict Evaluation: Be ruthlessly objective and highly critical. Do not assign high scores (4-5) for Moat or Quality unless there is indisputable evidence. Hardware companies rarely have Network Effects. Acknowledge financial struggles or declining revenues if they exist in the provided context.
        - Executives: Extract the CEO and CFO. Then, from the provided real-world context, extract the next 1 or 2 most senior/relevant officers (e.g., President, COO, CTO, Chief Business Officer). Do NOT invent roles. If a role is not in the context, do not include it. You must return between 2 and 4 executives total. Clean the titles by keeping only the role, removing company names. Convert titles to UPPERCASE. Ensure 'ownership' is a float representing the percentage, or null if undisclosed.
        - Dictionaries/Lists: For 'products_services' and 'risk_factors', provide specific key-value pairs. For 'competitors', provide a list of objects exactly as specified, enforcing one single company per item and providing its stock ticker (use "PRIVATE" if unlisted).
        - Tone: Professional, objective, and data-driven.
        - Density and Depth: DO NOT provide short or brief answers. Every text field must be highly analytical, comprehensive, and detailed, acting as a professional equity research report.
        - Comprehensive Risks: MUST provide a detailed list of at least 4 to 6 critical risk factors (e.g. Macro, Geopolitical, Internal, Competitive).

        QUALITY EXAMPLES (follow this tone and depth):
        GOOD competitive_advantage: "Apple's ecosystem creates a powerful flywheel: high switching costs from iCloud lock-in, iOS app investments, and seamless hardware-software integration drive 93% retention rates. The Services segment, growing at 14% YoY, monetizes this captive base with 78% gross margins, creating a durable revenue stream less vulnerable to hardware cycles."
        BAD competitive_advantage: "Apple has a strong brand and makes popular products that people like to buy."

        REQUIRED JSON STRUCTURE:
        Return ONLY a valid JSON object following this exact schema:
        {{
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
                "Product/Service 1": "Comprehensive 2-3 sentence description explaining the utility, market fit, and strategic importance.",
                "Product/Service 2": "Comprehensive 2-3 sentence description...",
                "Product/Service 3": "Comprehensive 2-3 sentence description..."
            }},
            "competitive_advantage": "Deep 4-5 sentence analysis defending the existence, strength, and durability of the Moat.",
            "competitors": [
                {{ "name": "Competitor 1 Name", "ticker": "AAPL", "overlap": "Detailed 2-3 sentence analysis..." }},
                {{ "name": "Competitor 2 Name", "ticker": "MSFT", "overlap": "Detailed 2-3 sentence analysis..." }},
                {{ "name": "Competitor 3 Name", "ticker": "PRIVATE", "overlap": "Detailed 2-3 sentence analysis..." }}
            ],
            "management_insights": "Analysis of management quality and track record.",
            "risk_factors": {{
                "Risk 1 Title (e.g. Geopolitical)": "Detailed 2-3 sentence breakdown of the risk impact and probability.",
                "Risk 2 Title (e.g. Competitive)": "Detailed 2-3 sentence breakdown...",
                "Risk 3 Title (e.g. Internal)": "Detailed 2-3 sentence breakdown...",
                "Risk 4 Title (e.g. Macro)": "Detailed 2-3 sentence breakdown..."
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
                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=_remove_additional_properties(CompanyProfileSchema.model_json_schema()),
                            temperature=0.0,
                        )
                    )
                    data_en = json.loads(response.text)
                    with open(cache_path_en, 'w', encoding='utf-8') as f:
                        json.dump(data_en, f, indent=4)
                except Exception as e: 
                    error_str = str(e).lower()
                    if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                        raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
                    raise ExternalServiceError(f"Gemini API Error: {e}")
            
            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

        schema_instance = CompanyProfileSchema(**data)
        
        return CompanyProfile(
            business_description="", # Injected later by UseCase
            company_history=schema_instance.company_history,
            key_executives=[{"name": e.name, "title": e.title, "ownership": float(e.ownership) if e.ownership is not None else None} for e in schema_instance.key_executives],
            revenue_model=schema_instance.revenue_model,
            strategy=schema_instance.strategy,
            products_services={p.name: p.description for p in schema_instance.products_services},
            competitive_advantage=schema_instance.competitive_advantage,
            competitors=[{"name": c.name, "ticker": c.ticker, "overlap": c.overlap} for c in schema_instance.competitors],
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
            language (str): Target language for the analysis
        
        Returns:
            IndustrySectorDynamics: A Domain Entity containing the data given the sector and industry
        """
        prompt = f"""
        Act as a Senior Equity Research Analyst and Industry Strategist. 
        Perform a comprehensive fundamental analysis of the following market:
        SECTOR: {sector}
        INDUSTRY: {industry}

        CORE FRAMEWORK: Use Porter's Five Forces to evaluate structural profitability and competitive intensity.
        Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.

        INSTRUCTIONS FOR JSON DICTIONARIES (Sections 1-5):
        For each force, identify 2-4 key factors. Return them as a dictionary where the KEY is a short, descriptive title (e.g., "Capital Intensity") and the VALUE is a professional analysis.

        QUALITY EXAMPLES (follow this tone and depth):
        GOOD rivalry_among_competitors: "The cloud infrastructure market exhibits intense but rational competition among three dominant hyperscalers (AWS 31%, Azure 25%, GCP 11%), with high exit barriers from long-term enterprise contracts and massive sunk costs in data center infrastructure."
        BAD rivalry_among_competitors: "There is a lot of competition in this industry."

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

        CRITICAL: YOU MUST INCLUDE ALL FIELDS IN THE OUTPUT. DO NOT OMIT 'interest_rate_exposure'. 
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
                    IndustrySectorDynamicsSchema(**data)
                except Exception:
                    data = None

        if not data:
            data_en = None
            if os.path.exists(cache_path_en):
                if time.time() - os.path.getmtime(cache_path_en) < 86400:
                    try:
                        with open(cache_path_en, 'r', encoding='utf-8') as f:
                            data_en = json.load(f)
                        IndustrySectorDynamicsSchema(**data_en)
                    except Exception:
                        data_en = None

            if not data_en:
                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=_remove_additional_properties(IndustrySectorDynamicsSchema.model_json_schema()),
                            temperature=0.0,
                            max_output_tokens=8192
                        )
                    )
                    data_en = json.loads(response.text)
                    with open(cache_path_en, 'w', encoding='utf-8') as f:
                        json.dump(data_en, f, indent=4)
                except Exception as e: 
                    error_str = str(e).lower()
                    if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                        raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
                    raise ExternalServiceError(f"Gemini API Error: {e}")
            
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
            language (str): Target language for the analysis
            
        Returns:
            EarningsReport: A Domain Entity containing the earnings report analysis.
        """
        prompt = f"""
        You are a Senior Equity Analyst focused on long-term value investing. I am providing the full text of an Earnings Report for the company "{symbol}". Ignore short-term stock reactions and Wall Street consensus. Focus exclusively on underlying business fundamentals.

        Perform a deep-dive analysis and return ONLY a structured JSON object. Do not include markdown formatting, code blocks, or conversational text.
        Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.

        Extract and synthesize the following fields EXACTLY as named.
        CRITICAL: For margins, output as whole percentages (e.g. 66.3 for 66.3%) and NOT as decimals (e.g. 0.663). ALWAYS output absolute monetary amounts strictly in BILLIONS. For example, 500 million must be written as 0.5. 17.6 billion must be written as 17.6. NEVER output raw large numbers. If a metric is fundamentally not applicable to the business model (like gross margin for a bank), output null.

        1. period_end_date: (String) The end date of the fiscal period.
        2. core_performance: (Object) Extract Adjusted (Non-GAAP) Revenue, Adjusted EPS, Adjusted Gross Margin, Adjusted Operating Margin, Adjusted Net Margin, and Free Cash Flow. For each metric, return an object with a single float field: 'amount'. Do NOT include any growth or YoY calculations — those are computed externally from verified data.
        3. capital_allocation: (Object) Detail exact amounts (as floats, in billions) spent on 'share_buybacks', 'dividends', and 'capex_rd'. Also provide an 'infrastructure_assessment' string containing a full 2-3 sentence paragraph assessing the "why" behind the CapEx (e.g. accelerating for AI buildout, or cutting back to preserve cash). Do not just provide a single word.
        4. forward_guidance: (String) Detailed 2-3 sentence analysis of management's forward-looking projections and guidance.
        5. moat_trajectory: (String) Detailed 2-3 sentence analysis of the company's competitive advantage trajectory (e.g., is pricing power expanding or shrinking and why).
        6. risk_deconstruction: (Object) Separate headwinds into two string lists: 'macro_risks' (external) and 'internal_risks' (execution/product).
        7. bottom_line: (String) A brutal, concise summary answering: Did the underlying business execute well, or are structural cracks forming?
        8. sources: (List of Objects) You MUST provide inline numerical citations (e.g. [1], [2]) directly within your narrative text for fields like 'infrastructure_assessment', 'forward_guidance', 'moat_trajectory', and 'bottom_line' whenever you extract specific insights, data points, or management quotes. Then, in this 'sources' array, return a list of objects each containing 'citation_number' (integer) and 'source_text' (string) (e.g. [{{"citation_number": 1, "source_text": "MD&A Page 15"}}]).

        QUALITY EXAMPLES (follow this tone and depth):
        GOOD bottom_line: "Alphabet executed strongly: Search revenue grew 12% YoY driven by AI Overviews adoption, Cloud crossed the $12B annualized run-rate with 28% margins, and the $70B buyback signals management's confidence in sustained free cash flow generation [1]. The key risk is a potential deceleration in ad spend if macro conditions deteriorate [2]."
        BAD bottom_line: "The company did well this quarter and beat expectations."
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
                    raise InvalidDocumentFormatError("Gemini failed to process the uploaded PDF document.")

                try:
                    response = await self.client.aio.models.generate_content(
                        model=self.model_id,
                        contents=[prompt, uploaded_file],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=_remove_additional_properties(EarningsReportSchema.model_json_schema()),
                            temperature=0.0,
                        )
                    )
                    data_en = json.loads(response.text)
                    with open(cache_path_en, 'w', encoding='utf-8') as f:
                        json.dump(data_en, f, indent=4)
                except Exception as e: 
                    error_str = str(e).lower()
                    if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "exhausted" in error_str:
                        raise RateLimitExceededError(f"Gemini Rate Limit: {e}")
                    raise ExternalServiceError(f"Gemini API Error: {e}")

            if language != "en" and self.translator:
                # Exclude 'sources' from translation — document references stay in original language
                data_to_translate = {k: v for k, v in data_en.items() if k != "sources"}
                data = await self.translator.translate_json(data_to_translate, language)
                data["sources"] = data_en.get("sources", [])
            else:
                data = data_en
                
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

        schema_instance = EarningsReportSchema(**data)

        def to_dec(val):
            return Decimal(str(val)) if val is not None else None

        def get_metric(metric_schema):
            if metric_schema is None:
                return MetricWithGrowth(amount=None)
            return MetricWithGrowth(
                amount=to_dec(metric_schema.amount)
            )

        return EarningsReport(
            period_end_date=schema_instance.period_end_date,
            core_performance=CorePerformance(
                adjusted_revenue=get_metric(schema_instance.core_performance.adjusted_revenue),
                adjusted_eps=get_metric(schema_instance.core_performance.adjusted_eps),
                adjusted_gross_margin=get_metric(schema_instance.core_performance.adjusted_gross_margin),
                adjusted_operating_margin=get_metric(schema_instance.core_performance.adjusted_operating_margin),
                adjusted_net_margin=get_metric(schema_instance.core_performance.adjusted_net_margin),
                free_cash_flow=get_metric(schema_instance.core_performance.free_cash_flow)
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
            bottom_line=schema_instance.bottom_line,
            sources={str(src.citation_number): src.source_text for src in schema_instance.sources}
        )