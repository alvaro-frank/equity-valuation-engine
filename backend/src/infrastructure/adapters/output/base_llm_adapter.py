import os
import time
import json
import hashlib
import re
from typing import Optional, Type, TypeVar
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError

from application.exceptions.exceptions import LLMParsingError
from application.ports.llm_analysis_ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort
from application.ports.translation_port import TranslationPort
from application.ports.intrinsic_value_calculation_port import IntrinsicValueCalculationPort
from domain.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, CapitalAllocation, RiskDeconstruction, MoatSources, QualityPillars, MetricWithGrowth
from domain.entities.qualitative import NearTermCatalyst, SourceInfo as EntitySourceInfo
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
        - RAG & COMPARATIVE ANALYSIS MANDATE: Attached at the bottom are the latest OFFICIAL SEC Filings. You are NOT just extracting text. You MUST perform a comparative analysis across the provided documents.
          * If multiple 10-Q documents are provided, you MUST explicitly compare the target quarter against the homologous quarter to identify decelerations in growth, margin compression, or shifting management tone.
          * If multiple 10-K documents are provided, you MUST explicitly compare the fiscal years to evaluate structural changes in the Moat Trajectory and Capital Allocation execution.
          * Your 'management_insights', 'moat_trajectory_description', 'strategy', and 'risk_factors' fields MUST explicitly reference these YoY/QoQ comparisons.
        - Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.
        - Extreme Recency & Search Mandate: You MUST actively use Google Search to find the most recent Earnings Call, Investor Day, and breaking news from the LAST 6 MONTHS. Your analysis MUST be anchored in the current year. Do NOT rely on pre-2023 memory.
        - Quantitative Precision: EVERY claim about growth, margins, market share, product success, or strategic shifts MUST be backed by a specific hard number and date (e.g., "Grew 14% YoY in Q3 2023", "Holds a 65% market share as of late 2023", "Revenue target of $5B by 2025"). DO NOT use vague terms like "strong growth", "significant share", or "market leader" without quantifying it.
        - Quantitative Anchors: Whenever analyzing the 'competitive_advantage' or 'revenue_model', you MUST explicitly cite structural financial metrics if available (e.g., Gross Margins, Operating Margins, ROIC, or FCF generation) to prove the qualitative thesis. A moat without margin or ROIC expansion is not a moat.
        - Analytical Rigor & Value Investing Lens: Write like a ruthless, data-driven hedge fund analyst. Focus on structural competitive advantages (Moats), unit economics, and real existential threats. Strip out ALL corporate marketing fluff.
        - Ruthless Objectivity: Be brutally honest. If a company is struggling, losing market share, or facing severe macroeconomic headwinds, you MUST explicitly state it and quantify the damage. Do not assign high scores (4-5) for Moat or Quality without indisputable, quantified evidence.
        - Independent Scoring: You MUST independently evaluate and assign a score from 1 to 5 for EACH 'moat_sources' and 'quality_pillars' metric based on the SPECIFIC company being analyzed. DO NOT copy the arbitrary numbers from the JSON example.
        - Moat Definitions:
          * Intangible Assets: Patents, brands, or regulatory licenses.
          * Switching Costs: The cost for a customer to change to a competitor.
          * Network Effect: The value of the service increases as more people use it.
          * Cost Advantage: Can the company produce goods/services at a structurally lower cost than peers?
          * Efficient Scale: Does the market only support one or a few players economically?
        - Executives: Extract the CEO and CFO. Then, from the provided real-world context, extract the next 1 or 2 most senior/relevant officers. Do NOT invent roles. Clean the titles by keeping only the role, removing company names. Convert titles to UPPERCASE. Ensure 'ownership' is a float representing the percentage, or null if undisclosed.
        - Competitors: Enforce exactly ONE single company per item, providing its official stock ticker (use "PRIVATE" if unlisted). The 'overlap' must explicitly detail where they compete and quantify the competitor's threat.
        - Tone: Professional, highly critical, objective, and data-heavy.
        - Density and Depth: DO NOT provide brief answers. Every text field must be highly analytical, comprehensive, and packed with facts, acting as a professional institutional research report.
        - Comprehensive Risks: MUST provide a detailed list of at least 4 to 6 critical risk factors. Ensure these reflect CURRENT events and real recent news, with specific dates or numbers (e.g. "Q4 2023 supply chain disruption causing $200M impact").

        QUALITY EXAMPLES (follow this tone and depth):
        GOOD competitive_advantage: "Apple's ecosystem creates a powerful flywheel: high switching costs from iCloud lock-in, iOS app investments, and seamless hardware-software integration drive 93% retention rates. The Services segment, growing at 14% YoY in Q3 2023, monetizes this captive base with 78% gross margins, creating a durable revenue stream less vulnerable to hardware cycles."
        BAD competitive_advantage: "Apple has a strong brand and makes popular products that people like to buy."

        REQUIRED JSON STRUCTURE:
        Return ONLY a valid JSON object following this exact schema:
        {{
            "company_history": "Key milestones from foundation to present, heavily emphasizing the strategic shifts of the last 3 years with precise dates.",
            "key_executives": [
                {{ "name": "Name A", "title": "CHIEF EXECUTIVE OFFICER", "ownership": 5.2 }},
                {{ "name": "Name B", "title": "CHIEF FINANCIAL OFFICER", "ownership": 1.2 }},
                {{ "name": "Name C", "title": "PRESIDENT & CHIEF INVESTMENT OFFICER", "ownership": 0.5 }},
                {{ "name": "Name D", "title": "CHIEF TECHNOLOGY OFFICER", "ownership": 0.1 }}
            ],
            "revenue_model": "Highly detailed explanation (3-4 sentences) of all major revenue streams, pricing power, and monetization strategy. Must include recent revenue breakdown percentages and margin or growth metrics if available.",
            "strategy": "Core strategic focus and future outlook, anchored in recent management commentary (e.g. latest earnings call).",
            "products_services": [
                {{ "name": "Product/Service 1", "description": "Comprehensive 2-3 sentence description explaining the utility, market fit, and strategic importance, including recent traction data." }},
                {{ "name": "Product/Service 2", "description": "Comprehensive 2-3 sentence description..." }},
                {{ "name": "Product/Service 3", "description": "Comprehensive 2-3 sentence description..." }}
            ],
            "competitive_advantage": "Deep 4-5 sentence analysis defending the existence, strength, and durability of the Moat. Explicitly anchor the analysis in ROIC, gross margins, or market share metrics.",
            "competitors": [
                {{ "name": "Competitor 1 Name", "ticker": "AAPL", "overlap": "Detailed 2-3 sentence analysis of direct overlap and competitive threat..." }},
                {{ "name": "Competitor 2 Name", "ticker": "MSFT", "overlap": "Detailed 2-3 sentence analysis..." }},
                {{ "name": "Competitor 3 Name", "ticker": "PRIVATE", "overlap": "Detailed 2-3 sentence analysis..." }}
            ],
            "management_insights": "Analysis of management quality, execution track record, and integrity.",
            "capital_allocation_strategy": "Detailed analysis of how management deploys Free Cash Flow: CapEx intensity, M&A track record, share buybacks, and dividend policy.",
            "near_term_catalysts": [
                {{ "event": "Catalyst 1 Name", "impact": "Detailed 2-3 sentence breakdown of how this upcoming event could positively or negatively re-rate the stock in the next 12-24 months." }}
            ],
            "risk_factors": [
                {{ "title": "Risk 1 Title (e.g. Geopolitical)", "description": "Detailed 2-3 sentence breakdown of the risk impact and probability. Must include recent specific headwinds and quantifiable data." }},
                {{ "title": "Risk 2 Title (e.g. Competitive)", "description": "Detailed 2-3 sentence breakdown..." }},
                {{ "title": "Risk 3 Title (e.g. Internal)", "description": "Detailed 2-3 sentence breakdown..." }},
                {{ "title": "Risk 4 Title (e.g. Macro)", "description": "Detailed 2-3 sentence breakdown..." }}
            ],
            "historical_context_crises": "How the company navigated past major crises and recent macro challenges (e.g. 2022 inflation, recent industry downturns).",
            "moat_trajectory_status": "EXPANDING/STABLE/SHRINKING",
            "moat_trajectory_description": "Detailed 2-3 sentence analysis of why the competitive advantage trajectory is shifting. Mention recent news.",
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
        """

        cache_filename = f"company_{symbol.upper()}_{language}.json"
        target_dir = os.path.join(self.cache_dir, symbol.upper(), "analysis")
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, cache_filename)
        cache_filename_en = f"company_{symbol.upper()}_en.json"
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
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

        if "sources" in data and isinstance(data["sources"], dict):
            new_sources = []
            for k, v in data["sources"].items():
                v["citation_id"] = str(k)
                new_sources.append(v)
            data["sources"] = new_sources

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
            moat_trajectory_status=schema_instance.moat_trajectory_status,
            moat_trajectory_description=schema_instance.moat_trajectory_description,
            moat_sources=MoatSources(**schema_instance.moat_sources.model_dump()),
            quality_pillars=QualityPillars(**schema_instance.quality_pillars.model_dump()),
            capital_allocation_strategy=schema_instance.capital_allocation_strategy,
            near_term_catalysts=[NearTermCatalyst(event=c.event, impact=c.impact) for c in schema_instance.near_term_catalysts],
            sources={s.citation_id: EntitySourceInfo(url=s.url, title=s.title) for s in schema_instance.sources}
        )

    async def analyse_industry(self, sector: str, industry: str, language: str = "en", ticker: str = "", context: str = "") -> IndustrySectorDynamics:
        context_prompt = f"\n\nREAL-WORLD CONTEXT (USE THIS AS ABSOLUTE TRUTH):\n{context}\n" if context else ""

        prompt = f"""
        Act as a Senior Equity Research Analyst and Industry Strategist. 
        Perform a comprehensive fundamental analysis of the following market from the perspective of {ticker}:
        SECTOR: {sector}
        INDUSTRY: {industry}
        {context_prompt}

        CORE FRAMEWORK: Use Porter's Five Forces to evaluate structural profitability and competitive intensity.
        Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.

        CRITICAL INSTRUCTIONS:
        - RAG & CONTEXT MANDATE: Attached at the top is the REAL-WORLD CONTEXT (recent SEC filings). You MUST anchor your analysis on these documents. Extract precise market share, supplier dependency, buyer concentration, and barriers to entry that the company explicitly mentions.
        - CITATIONS: You MUST provide inline numerical citations (e.g. [1], [2], [3]) directly within your analysis text to back up your claims. For EACH distinct claim or quote, create a NEW sequential citation number. DO NOT group everything into a single [1] citation.
        - Perspective: Evaluate the forces exclusively from the point of view of the specific company ({ticker}) operating in its unique micro-niche within the industry.

        INSTRUCTIONS FOR SECTIONS 1-5:
        For each force, identify 2-4 key factors. Return them as an ARRAY of objects, where each object has a "factor" (short title) and an "analysis" (professional analysis with citations).

        QUALITY EXAMPLES (follow this tone and depth):
        GOOD rivalry_among_competitors: [{{"factor": "Market Concentration", "analysis": "The cloud infrastructure market exhibits intense but rational competition among three dominant hyperscalers (AWS 31%, Azure 25%, GCP 11%) [1], with high exit barriers from long-term enterprise contracts [2]."}}]

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
            "rivalry_among_competitors": [ {{ "factor": "Key Factor", "analysis": "Analysis with citations [1]..." }} ],
            "bargaining_power_of_suppliers": [ {{ "factor": "Key Factor", "analysis": "Analysis with citations [2]..." }} ],
            "bargaining_power_of_customers": [ {{ "factor": "Key Factor", "analysis": "Analysis with citations [3]..." }} ],
            "threat_of_new_entrants": [ {{ "factor": "Key Factor", "analysis": "Analysis with citations [4]..." }} ],
            "threat_of_obsolescence": [ {{ "factor": "Key Factor", "analysis": "Analysis with citations [5]..." }} ],
            "economic_sensitivity": "Detailed narrative about economic cycles with citations [6].",
            "interest_rate_exposure": "Detailed narrative about rate impacts with citations [7].",
            "sources": [
                {{ "citation_id": "1", "url": "SEC EDGAR", "title": "SHORT exact sentence (max 1-2 sentences) from the context. CRITICAL: DO NOT use double quotes inside this text." }},
                {{ "citation_id": "2", "url": "SEC EDGAR", "title": "Another SHORT exact sentence from the context. Replace internal quotes with single quotes." }}
            ]
        }}

        CRITICAL: YOU MUST INCLUDE ALL FIELDS IN THE OUTPUT. DO NOT OMIT 'interest_rate_exposure' or 'sources'. 
        Do not include markdown headers (like ```json), intro text, or conclusions. Return only raw JSON.
        """
        
        safe_sector = re.sub(r'[^a-zA-Z0-9]', '_', sector)
        safe_industry = re.sub(r'[^a-zA-Z0-9]', '_', industry)
        cache_filename = f"industry_{safe_sector}_{safe_industry}_{language}.json"
        
        if ticker:
            target_dir = os.path.join(self.cache_dir, ticker.upper(), "analysis")
        else:
            target_dir = os.path.join(self.cache_dir, "industries")
            
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, cache_filename)
        
        cache_filename_en = f"industry_{safe_sector}_{safe_industry}_en.json"
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
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

        if "sources" in data and isinstance(data["sources"], dict):
            new_sources = []
            for k, v in data["sources"].items():
                v["citation_id"] = str(k)
                new_sources.append(v)
            data["sources"] = new_sources

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
            interest_rate_exposure=schema_instance.interest_rate_exposure,
            sources={s.citation_id: EntitySourceInfo(url=s.url, title=s.title) for s in schema_instance.sources}
        )

    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en", focus_period: str = None) -> EarningsReport:
        focus_instruction = ""
        if focus_period:
            focus_instruction = f"\n\n        CRITICAL: The user requested an analysis exclusively for the period {focus_period}. This document is an annual report, but you MUST isolate and extract ONLY the performance, guidance, and events pertaining to {focus_period}, ignoring the rest of the year."

        prompt = f"""
        You are a Senior Equity Analyst focused on long-term value investing. I am providing the full text of an Earnings Report for the company "{symbol}". Ignore short-term stock reactions and Wall Street consensus. Focus exclusively on underlying business fundamentals.{focus_instruction}

        Perform a deep-dive analysis and return ONLY a structured JSON object. Do not include markdown formatting, code blocks, or conversational text.
        Language: Generate ALL analysis text strictly in English. The JSON keys must remain in English as defined by the schema.

        CRITICAL MATHEMATICAL RULES:
        - For margins, output as whole percentages (e.g. 66.3 for 66.3%) and NOT as decimals (e.g. 0.663).
        - ALWAYS output absolute monetary amounts strictly in BILLIONS. For example, 500 million must be written as 0.5. 17.6 billion must be written as 17.6. NEVER output raw large numbers.
        - If a metric is fundamentally not applicable to the business model (like gross margin for a bank), output null.

        CRITICAL TEMPORAL SCOPE:
        - If the document is a quarterly report (10-Q), you MUST extract financial figures (Revenue, Margins, Cash Flows, CapEx) exclusively from the isolated 'Three Months Ended' column. NEVER extract the 'Six Months Ended', 'Nine Months Ended' or 'Year-to-Date' cumulative columns.
        - If the document is an annual report (10-K), extract the full fiscal year figures.

        Extract and synthesize the following fields EXACTLY as named.

        1. period_end_date: (String) The end date of the fiscal period strictly in 'YYYY-MM-DD' format.
        2. core_performance: (Object) Extract Adjusted (Non-GAAP) Revenue, Adjusted EPS, Adjusted Gross Margin, Adjusted Operating Margin, Adjusted Net Margin, and Free Cash Flow. Free Cash Flow MUST be calculated as 'Net Cash from Operations' minus 'CapEx' (Additions to property and equipment). For each metric, return an object with a single float field: 'amount'. Do NOT include any growth or YoY calculations — those are computed externally from verified data.
        3. capital_allocation: (Object) Detail exact amounts (as floats, in billions) spent on 'share_buybacks', 'dividends', and 'capex_rd'. Also provide an 'infrastructure_assessment' string containing a full 2-3 sentence paragraph assessing the "why" behind the CapEx. You MUST extract specific hardware names, exact geographic locations of new facilities, specific project names, or exact financial sub-allocations if mentioned. Assess whether this CapEx cycle appears Defensive or Offensive. Explicitly IGNORE generic corporate jargon like "meeting customer needs" or "investing for the future".
        4. forward_guidance: (String) Detailed 2-3 sentence analysis of management's forward-looking projections and guidance.
        5. moat_trajectory_status: (String) Exactly "EXPANDING", "STABLE", or "SHRINKING".
        5b. moat_trajectory_description: (String) Detailed 2-3 sentence analysis of the company's competitive advantage trajectory.
        6. risk_deconstruction: (Object) Separate headwinds into two string lists (arrays of strings): 'macro_risks' (external) and 'internal_risks' (execution/product). Each individual risk must be a separate string element in the array. You MUST include numerical citations directly inside each string.
        7. bottom_line: (String) A brutal, concise summary answering: Did the underlying business execute well, or are structural cracks forming?
        8. sources: (List of Objects) You MUST provide inline numerical citations (e.g. [1], [2]) directly within your narrative text for fields like 'infrastructure_assessment', 'forward_guidance', 'moat_trajectory_description', 'risk_deconstruction', and 'bottom_line'. Then, in this 'sources' array, return a list of objects each containing 'citation_number' (integer) and 'source_text' (string). 
        CRITICAL: The 'source_text' MUST be the exact raw quote or sentence from the document that proves your claim (e.g. "Cloud revenue grew 24% driven by AI workload demand"). DO NOT just provide page numbers or section titles. Citations must be strictly sequential (1, 2, 3...) with no skipped numbers.

        QUALITY EXAMPLES (follow this tone and depth):
        GOOD bottom_line: "Alphabet executed strongly: Search revenue grew 12% YoY driven by AI Overviews adoption, Cloud crossed the $12B annualized run-rate with 28% margins, and the $70B buyback signals management's confidence in sustained free cash flow generation [1]. The key risk is a potential deceleration in ad spend if macro conditions deteriorate [2]."
        BAD bottom_line: "The company did well this quarter and beat expectations."
        GOOD infrastructure_assessment: "CapEx surged to $30.8B, aggressively allocated to scaling Azure's AI infrastructure. Management is securing scarce GPU supply and building next-gen liquid-cooled datacenters, signaling an offensive land-grab in AI compute. This massive capital intensity will compress near-term operating margins but is designed to lock in long-term enterprise AI workloads."
        BAD infrastructure_assessment: "The company is spending more on datacenters to meet growing AI demand and serve customers better."
        """

        with open(pdf_file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:12]
        cache_filename = f"earnings_{symbol.upper()}_{file_hash}_{language}.json"
        target_dir = os.path.join(self.cache_dir, symbol.upper(), "analysis")
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, cache_filename)
        cache_filename_en = f"earnings_{symbol.upper()}_{file_hash}_en.json"
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
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
                    "moat_trajectory_description": data_en["moat_trajectory_description"],
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
                data["moat_trajectory_description"] = translated.get("moat_trajectory_description", data["moat_trajectory_description"])
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
                share_buybacks=Decimal(str(schema_instance.capital_allocation.share_buybacks)) if schema_instance.capital_allocation.share_buybacks is not None else None,
                dividends=Decimal(str(schema_instance.capital_allocation.dividends)) if schema_instance.capital_allocation.dividends is not None else None,
                capex_rd=Decimal(str(schema_instance.capital_allocation.capex_rd)) if schema_instance.capital_allocation.capex_rd is not None else None,
                infrastructure_assessment=schema_instance.capital_allocation.infrastructure_assessment
            ),
            forward_guidance=schema_instance.forward_guidance,
            moat_trajectory_status=schema_instance.moat_trajectory_status,
            moat_trajectory_description=schema_instance.moat_trajectory_description,
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
        target_dir = os.path.join(self.cache_dir, ticker.upper(), "analysis")
        os.makedirs(target_dir, exist_ok=True)
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
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
