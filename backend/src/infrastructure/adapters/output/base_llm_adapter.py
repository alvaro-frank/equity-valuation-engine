import os
import time
import json
import hashlib
import re
from typing import Optional, Dict, Any, Type, TypeVar
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError

from application.exceptions.exceptions import RateLimitExceededError, ExternalServiceError, LLMParsingError, InvalidDocumentFormatError
from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort, TranslationPort
from application.ports.intrinsic_value_calculation_port import IntrinsicValueCalculationPort
from domain.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, CapitalAllocation, RiskDeconstruction, MoatSources, QualityPillars, MetricWithGrowth
from domain.entities.dcf import DCFAssumptions
from decimal import Decimal

from infrastructure.schemas import CompanyProfileSchema, IndustrySectorDynamicsSchema, EarningsReportSchema, DCFValuationResponseSchema
from infrastructure.utils.llm_utils import extract_json_from_response

T = TypeVar('T', bound=BaseModel)

class BaseLLMAdapter(SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort, IntrinsicValueCalculationPort, ABC):
    """
    Abstract Base Class for LLM Adapters to enforce DRY principles.
    Implements generic caching, schema validation, entity mapping, and translation logic.
    Subclasses only need to implement the actual LLM API calls.
    """
    
    def __init__(self, translator: Optional[TranslationPort] = None):
        self.translator = translator
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.llm_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    @abstractmethod
    async def _generate_company_profile(self, prompt: str, schema: Type[T]) -> dict:
        """Call the LLM API to generate the company profile JSON."""
        pass

    @abstractmethod
    async def _generate_industry_dynamics(self, prompt: str, schema: Type[T]) -> dict:
        """Call the LLM API to generate the industry dynamics JSON."""
        pass

    @abstractmethod
    async def _generate_earnings_report(self, prompt: str, pdf_file_path: str, schema: Type[T]) -> dict:
        """Call the LLM API to analyze an earnings report PDF."""
        pass

    @abstractmethod
    async def _generate_dcf_assumptions(self, prompt: str, schema: Type[T]) -> dict:
        """Call the LLM API to generate DCF assumptions."""
        pass

    def _get_cached_data(self, cache_path: str) -> Optional[dict]:
        if os.path.exists(cache_path) and time.time() - os.path.getmtime(cache_path) < 86400:
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def _set_cached_data(self, cache_path: str, data: dict):
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
        context_prompt = f"\n\nREAL-WORLD CONTEXT (USE THIS AS ABSOLUTE TRUTH):\n{context}\n" if context else ""
        
        prompt = f"""
        Act as a Senior Equity Research Analyst specializing in Fundamental Analysis. 
        Your goal is to provide a deep qualitative assessment for the company: {symbol}.{context_prompt}

        CRITICAL INSTRUCTIONS:
        - Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.
        - Accuracy & Search: You have access to Google Search (if supported). You MUST actively search for the company's most recent news, headwinds, litigations, and structural problems to fill the risk_factors and moat_trajectory. Do NOT rely on static past memory for these fields.
        - Products & Strategy Search: You MUST verify the company's current core products, recent strategic pivots, and latest revenue model (e.g. from their latest Earnings Release). Ensure products_services and strategy reflect the current year.
        - Analytical rigor: Focus on deep economic moats, structural competitive advantages, and real threats. Avoid generic marketing fluff. Do NOT be overly optimistic. If a company is struggling, explicitly state it.
        - Strict Evaluation & Headwinds: Be ruthlessly objective and highly critical. You MUST explicitly identify recent headwinds, ongoing litigations, declining business segments, supply chain issues, or new competitive threats. Acknowledge financial struggles if they exist. Do not assign high scores (4-5) for Moat or Quality unless there is indisputable evidence.
        - Independent Scoring: You MUST independently evaluate and assign a score from 1 to 5 for EACH 'moat_sources' and 'quality_pillars' metric based on the SPECIFIC company being analyzed. DO NOT copy the arbitrary numbers from the JSON example.
        - Moat Definitions:
          * Intangible Assets: Patents, brands, or regulatory licenses.
          * Switching Costs: The cost for a customer to change to a competitor.
          * Network Effect: The value of the service increases as more people use it.
          * Cost Advantage: Can the company produce goods/services at a structurally lower cost than peers? (e.g., tech giants with massive data center economies of scale often have a 4 or 5).
          * Efficient Scale: Does the market only support one or a few players economically? (e.g., a dominant search engine or natural monopoly should score high).
        - Executives: Extract the CEO and CFO. Then, from the provided real-world context, extract the next 1 or 2 most senior/relevant officers (e.g., President, COO, CTO, Chief Business Officer). Do NOT invent roles. If a role is not in the context, do not include it. You must return between 2 and 4 executives total. Clean the titles by keeping only the role, removing company names. Convert titles to UPPERCASE. Ensure 'ownership' is a float representing the percentage, or null if undisclosed.
        - Dictionaries/Lists: For 'products_services' and 'risk_factors', provide specific list of objects as shown. For 'competitors', provide a list of objects exactly as specified, enforcing one single company per item and providing its stock ticker (use "PRIVATE" if unlisted).
        - Tone: Professional, objective, and data-driven.
        - Density and Depth: DO NOT provide short or brief answers. Every text field must be highly analytical, comprehensive, and detailed, acting as a professional equity research report.
        - Comprehensive Risks: MUST provide a detailed list of at least 4 to 6 critical risk factors (e.g. Macro, Geopolitical, Internal, Competitive). Ensure these reflect CURRENT events and real recent news, not just generic possibilities.

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
            "products_services": [
                {{ "name": "Product/Service 1", "description": "Comprehensive 2-3 sentence description explaining the utility, market fit, and strategic importance." }},
                {{ "name": "Product/Service 2", "description": "Comprehensive 2-3 sentence description..." }},
                {{ "name": "Product/Service 3", "description": "Comprehensive 2-3 sentence description..." }}
            ],
            "competitive_advantage": "Deep 4-5 sentence analysis defending the existence, strength, and durability of the Moat. Explicitly cite any recent challenges to this moat.",
            "competitors": [
                {{ "name": "Competitor 1 Name", "ticker": "AAPL", "overlap": "Detailed 2-3 sentence analysis..." }},
                {{ "name": "Competitor 2 Name", "ticker": "MSFT", "overlap": "Detailed 2-3 sentence analysis..." }},
                {{ "name": "Competitor 3 Name", "ticker": "PRIVATE", "overlap": "Detailed 2-3 sentence analysis..." }}
            ],
            "management_insights": "Analysis of management quality and track record.",
            "risk_factors": [
                {{ "title": "Risk 1 Title (e.g. Geopolitical)", "description": "Detailed 2-3 sentence breakdown of the risk impact and probability. Must include recent specific headwinds." }},
                {{ "title": "Risk 2 Title (e.g. Competitive)", "description": "Detailed 2-3 sentence breakdown..." }},
                {{ "title": "Risk 3 Title (e.g. Internal)", "description": "Detailed 2-3 sentence breakdown..." }},
                {{ "title": "Risk 4 Title (e.g. Macro)", "description": "Detailed 2-3 sentence breakdown..." }}
            ],
            "historical_context_crises": "How the company navigated past major crises.",
            "moat_trajectory": "Detailed 2-3 sentence analysis of the company's competitive advantage trajectory (expanding or shrinking and why). Mention recent news.",
            "moat_sources": {{
                "intangible_assets": 1,
                "switching_costs": 1,
                "network_effect": 1,
                "cost_advantage": 1,
                "efficient_scale": 1
            }},
            "quality_pillars": {{
                "management_quality": 1,
                "business_model_resilience": 1,
                "pricing_power": 1,
                "innovation_and_growth": 1,
                "tam_expansion": 1
            }}
        }}

        Do not include any markdown formatting outside the JSON, preamble, or conversational text. Return only the raw JSON.
        CRITICAL: If you use facts from the search results, preserve numerical citation markers (e.g., [1], [2]) directly inside the JSON string values.
        """

        cache_filename = f"company_{symbol.upper()}_{language}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        cache_filename_en = f"company_{symbol.upper()}_en.json"
        cache_path_en = os.path.join(self.cache_dir, cache_filename_en)
        
        data = self._get_cached_data(cache_path)
        if not data:
            data_en = self._get_cached_data(cache_path_en)
            if not data_en:
                data_en = await self._generate_company_profile(prompt, CompanyProfileSchema)
                try:
                    CompanyProfileSchema(**data_en)
                except ValidationError as ve:
                    raise LLMParsingError(f"LLM returned invalid JSON structure: {ve}")
                self._set_cached_data(cache_path_en, data_en)
            
            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            try:
                CompanyProfileSchema(**data)
            except ValidationError as ve:
                raise LLMParsingError(f"Translator returned invalid JSON structure: {ve}")
            self._set_cached_data(cache_path, data)

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
            quality_pillars=QualityPillars(**schema_instance.quality_pillars.model_dump()),
            sources=schema_instance.sources
        )

    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
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
        
        data = self._get_cached_data(cache_path)
        if not data:
            data_en = self._get_cached_data(cache_path_en)
            if not data_en:
                data_en = await self._generate_industry_dynamics(prompt, IndustrySectorDynamicsSchema)
                self._set_cached_data(cache_path_en, data_en)
            
            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            self._set_cached_data(cache_path, data)

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

        with open(pdf_file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:12]
        cache_filename = f"earnings_{symbol.upper()}_{file_hash}_{language}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        cache_filename_en = f"earnings_{symbol.upper()}_{file_hash}_en.json"
        cache_path_en = os.path.join(self.cache_dir, cache_filename_en)
        
        data = self._get_cached_data(cache_path)
        if not data:
            data_en = self._get_cached_data(cache_path_en)
            if not data_en:
                data_en = await self._generate_earnings_report(prompt, pdf_file_path, EarningsReportSchema)
                self._set_cached_data(cache_path_en, data_en)

            data = data_en.copy()
            if language != "en" and self.translator:
                translatable_fields = {
                    "forward_guidance": data_en["forward_guidance"],
                    "moat_trajectory": data_en["moat_trajectory"],
                    "bottom_line": data_en["bottom_line"],
                    "risk_deconstruction": {
                        "macro_risks": data_en["risk_deconstruction"]["macro_risks"],
                        "internal_risks": data_en["risk_deconstruction"]["internal_risks"]
                    },
                    "capital_allocation": {
                        "infrastructure_assessment": data_en["capital_allocation"]["infrastructure_assessment"]
                    }
                }
                translated = await self.translator.translate_json(translatable_fields, language)
                data["forward_guidance"] = translated.get("forward_guidance", data["forward_guidance"])
                data["moat_trajectory"] = translated.get("moat_trajectory", data["moat_trajectory"])
                data["bottom_line"] = translated.get("bottom_line", data["bottom_line"])
                if "risk_deconstruction" in translated:
                    data["risk_deconstruction"]["macro_risks"] = translated["risk_deconstruction"].get("macro_risks", data["risk_deconstruction"]["macro_risks"])
                    data["risk_deconstruction"]["internal_risks"] = translated["risk_deconstruction"].get("internal_risks", data["risk_deconstruction"]["internal_risks"])
                if "capital_allocation" in translated and "infrastructure_assessment" in translated["capital_allocation"]:
                    data["capital_allocation"]["infrastructure_assessment"] = translated["capital_allocation"]["infrastructure_assessment"]
            
            self._set_cached_data(cache_path, data)

        schema_instance = EarningsReportSchema(**data)
        def get_metric(m):
            return MetricWithGrowth(amount=Decimal(str(m.amount)) if m and m.amount is not None else None)

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

    async def deduce_dcf_assumptions(self, ticker: str, company_profile: dict, quant_data: dict, language: str = "en") -> dict:
        prompt = f"""
        You are a top-tier Wall Street Financial Analyst specializing in Discounted Cash Flow (DCF) valuation and competitive moat assessment.
        Your task is to deduce the most realistic future growth assumptions for {ticker} based on its historical performance, business model resilience, and macroeconomic context.

        CRITICAL RULES:
        1. DO NOT calculate the intrinsic value. Your ONLY job is to provide the growth rates, WACC, and terminal growth rate. The mathematical calculation will be handled by our deterministic backend engine.
        2. Provide your assumptions for three scenarios: Bear (Pessimistic), Fair (Base Case), and Bull (Optimistic).
        3. Provide a clear, sharp, and highly analytical justification (1-2 paragraphs) for why you chose these specific rates for each scenario.
        4. Always respond strictly in English and format your response matching the provided JSON schema. All rates MUST be expressed as decimals (e.g. 15% is 0.15).

        [CONTEXT INJECTED BY US]
        COMPANY PROFILE & QUALITATIVE MOAT:
        {json.dumps(company_profile, indent=2)}

        QUANTITATIVE METRICS (FCF HISTORY & MARGINS):
        {json.dumps(quant_data, indent=2)}

        [HOW TO THINK ABOUT THE VARIABLES]
        - FCF Growth (Years 1-5): Base this on the company's recent growth trajectory, TAM expansion, and pricing power. If the moat is shrinking, penalize the Bear case heavily.
        - FCF Growth (Years 6-10): Assume a natural linear deceleration as the company and its market mature.
        - WACC (Discount Rate): Reflects the risk premium. A highly predictable, monopolistic business commands a lower WACC (0.075 - 0.09). A highly cyclical or risky business should have a higher WACC (0.10 - 0.13). Vary the WACC slightly across scenarios to reflect the perceived stability of the moat.
        - Terminal Growth Rate: Rate after year 10. This MUST be conservative. It usually ranges between 0.02 and 0.03, aligning with expected long-term global GDP growth and inflation. Never exceed 0.035 unless absolutely justifiable.

        [QUALITY EXAMPLE - FAIR SCENARIO FOR GOOG]
        "fcf_growth_1_to_5": 0.15,
        "fcf_growth_6_to_10": 0.10,
        "wacc": 0.085,
        "terminal_growth_rate": 0.025,
        "justification": "Alphabet's 'Fair' scenario assumes steady growth supported by its Cloud infrastructure and efficient AI integration. The Search moat remains resilient but faces gradual structural challenges, prompting a linear deceleration in the back half of the decade. A conservative 8.5% WACC reflects its unshakeable balance sheet and deeply entrenched ecosystem."
        
        Do not include markdown headers (like ```json), intro text, or conclusions. Return only raw JSON.
        """

        cache_filename_en = f"dcf_{ticker.upper()}_en.json"
        cache_path_en = os.path.join(self.cache_dir, cache_filename_en)
        
        data_en = self._get_cached_data(cache_path_en)
        if not data_en:
            data_en = await self._generate_dcf_assumptions(prompt, DCFValuationResponseSchema)
            self._set_cached_data(cache_path_en, data_en)

        data = data_en.copy()
        if language != "en" and self.translator:
            justifications = {
                "bear": data["bear"]["justification"],
                "fair": data["fair"]["justification"],
                "bull": data["bull"]["justification"]
            }
            translated_justifications = await self.translator.translate_json(justifications, language)
            data["bear"]["justification"] = translated_justifications.get("bear", data["bear"]["justification"])
            data["fair"]["justification"] = translated_justifications.get("fair", data["fair"]["justification"])
            data["bull"]["justification"] = translated_justifications.get("bull", data["bull"]["justification"])

        schema_instance = DCFValuationResponseSchema(**data)
        def to_dec(val): return Decimal(str(val))
            
        result = {}
        for scenario_key in ["bear", "fair", "bull"]:
            scenario_data = getattr(schema_instance, scenario_key)
            result[scenario_key] = DCFAssumptions(
                fcf_growth_1_to_5=to_dec(scenario_data.fcf_growth_1_to_5),
                fcf_growth_6_to_10=to_dec(scenario_data.fcf_growth_6_to_10),
                wacc=to_dec(scenario_data.wacc),
                terminal_growth_rate=to_dec(scenario_data.terminal_growth_rate),
                justification=scenario_data.justification
            )
            
        return result
