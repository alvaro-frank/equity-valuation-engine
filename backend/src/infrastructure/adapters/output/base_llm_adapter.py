import os
import time
import json
import hashlib
import re
import asyncio

from typing import Optional, Type, TypeVar
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError
from infrastructure.schemas import BusinessModelSchema, MoatAnalysisSchema, RiskCatalystSchema
from application.exceptions.exceptions import LLMParsingError
from domain.exceptions.exceptions import DomainValidationError
from loguru import logger
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
    async def _generate_company_profile(self, prompt: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        """Call the LLM API to generate the company profile JSON."""
        pass

    @abstractmethod
    async def _generate_industry_dynamics(self, prompt: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        """Call the LLM API to generate the industry dynamics JSON."""
        pass

    @abstractmethod
    async def _generate_earnings_report(self, prompt: str, pdf_file_path: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        """Call the LLM API to analyze an earnings report PDF."""
        pass

    @abstractmethod
    async def _generate_earnings_from_context(self, prompt: str, context: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
        """Call the LLM API to analyze an earnings report from structured context."""
        pass

    @abstractmethod
    async def _generate_dcf_assumptions(self, prompt: str, schema: Type[T], model_id: str = "gemini-2.5-flash") -> dict:
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



    async def analyse_company(self, symbol: str, language: str = "en", context: str = "", structured_filings: 'StructuredFilingDTO' = None) -> CompanyProfile:
        cache_filename = f"company_{symbol.upper()}_{language}.json"
        target_dir = os.path.join(self.cache_dir, symbol.upper(), "analysis")
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, cache_filename)
        cache_filename_en = f"company_{symbol.upper()}_en.json"
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
        context_dir = os.path.join(target_dir, "context")
        os.makedirs(context_dir, exist_ok=True)
        cache_distilled = os.path.join(context_dir, f"distilled_{symbol.upper()}_en.json")
        cache_biz = os.path.join(context_dir, f"business_{symbol.upper()}_en.json")
        cache_moat = os.path.join(context_dir, f"moat_{symbol.upper()}_en.json")
        cache_risks = os.path.join(context_dir, f"risks_{symbol.upper()}_en.json")

        
        data = self._get_cached_data(cache_path)
        if not data:
            data_en = self._get_cached_data(cache_path_en)
            if not data_en:
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                agent_path = os.path.join(base_dir, "llm", "agents", "company-profiler", "agent.md")
                skill_business = os.path.join(base_dir, "llm", "agents", "company-profiler", "skills", "extract_business.md")
                skill_moat = os.path.join(base_dir, "llm", "agents", "company-profiler", "skills", "analyze_moat.md")
                skill_risks = os.path.join(base_dir, "llm", "agents", "company-profiler", "skills", "analyze_risks.md")
                
                with open(agent_path, 'r', encoding='utf-8') as f:
                    agent_prompt = f.read()
                with open(skill_business, 'r', encoding='utf-8') as f:
                    business_prompt = f.read()
                with open(skill_moat, 'r', encoding='utf-8') as f:
                    moat_prompt = f.read()
                with open(skill_risks, 'r', encoding='utf-8') as f:
                    risks_prompt = f.read()
                    
                business_context = f"\n\nREAL-WORLD CONTEXT (USE THIS AS ABSOLUTE TRUTH):\n{context}\n" if context else ""
                moat_context = business_context
                risks_context = business_context
                
                if structured_filings:
                    quant_metrics = context
                    
                    if structured_filings.is_exact_match and structured_filings.exact_sections:
                        logger.info(f"[Orchestrator] Exact sections found via edgartools (Via 1). Skipping SEC Distiller LLM.")
                        
                        # Dynamically combine relevant generic sections
                        # Since the SECAdapter now strictly limits the cached dictionary to the 3 target dates (Latest 10-K, Latest 10-Q, YoY 10-Q), 
                        # we can safely just check for the item name without worrying about intermediate quarters.
                        business_items = [f"--- {k} ---\n{v}" for k, v in structured_filings.exact_sections.items() if "10-K" in k and k.endswith("ITEM 1")]
                        risk_items = [f"--- {k} ---\n{v}" for k, v in structured_filings.exact_sections.items() if k.endswith("ITEM 1A")]
                        mda_items = [f"--- {k} ---\n{v}" for k, v in structured_filings.exact_sections.items() if ("10-K" in k and (k.endswith("ITEM 7") or k.endswith("ITEM 7A"))) or ("10-Q" in k and k.endswith("ITEM 2"))]
                        
                        biz_text = "\n\n".join(business_items)
                        risk_text = "\n\n".join(risk_items)
                        mda_text = "\n\n".join(mda_items)
                        
                        business_context = f"{quant_metrics}\n\nEXACT BUSINESS FACTS (FROM SEC 10-K):\n{biz_text}\n"
                        moat_context = f"{quant_metrics}\n\nEXACT COMPETITIVE & MD&A FACTS (FROM SEC 10-K/10-Q):\n{mda_text}\n"
                        risks_context = f"{quant_metrics}\n\nEXACT RISK FACTS (FROM SEC 10-K/10-Q):\n{risk_text}\n"
                    elif structured_filings.markdown_content:
                        logger.info(f"[Orchestrator] Exact extraction failed. Running sec-parser markdown through SEC Distiller (Via 2)...")
                        distiller_agent_path = os.path.join(base_dir, "llm", "agents", "sec-distiller", "agent.md")
                        with open(distiller_agent_path, 'r', encoding='utf-8') as f:
                            distiller_prompt = f.read().replace("{raw_filing_text}", structured_filings.markdown_content)
                        
                        from infrastructure.schemas.qualitative_schemas import SECDistillerSchema
                        try:
                            distilled_data = self._get_cached_data(cache_distilled)
                            if distilled_data:
                                logger.info(f"[Orchestrator] Cache hit for SEC Distiller for {symbol}, skipping API call.")
                            else:
                                logger.info(f"[Orchestrator] Starting SEC Distiller on Markdown content for {symbol}...")
                                distilled_data = await self._generate_company_profile(distiller_prompt, SECDistillerSchema, model_id="gemini-2.5-flash")
                                logger.info(f"[Orchestrator] SEC Distiller completed successfully for {symbol}.")
                                SECDistillerSchema(**distilled_data) # Validate
                                self._set_cached_data(cache_distilled, distilled_data)
                            
                            business_context = f"\n\nREAL-WORLD CONTEXT:\n{quant_metrics}\n\nDISTILLED BUSINESS FACTS:\n{distilled_data.get('business_context', '')}\n"
                            moat_context = f"\n\nREAL-WORLD CONTEXT:\n{quant_metrics}\n\nDISTILLED COMPETITIVE FACTS:\n{distilled_data.get('moat_context', '')}\n"
                            risks_context = f"\n\nREAL-WORLD CONTEXT:\n{quant_metrics}\n\nDISTILLED RISK FACTS:\n{distilled_data.get('risk_context', '')}\n"
                        except Exception as e:
                            logger.error(f"[Orchestrator-Error] SECDistiller failed for {symbol}: {e}")
                            raise e # Fail fast to prevent 429 Rate Limit amplification on the 3 parallel agents


                agent_prompt_biz = agent_prompt.replace("{symbol}", symbol).replace("{context}", business_context)
                agent_prompt_moat = agent_prompt.replace("{symbol}", symbol).replace("{context}", moat_context)
                agent_prompt_risks = agent_prompt.replace("{symbol}", symbol).replace("{context}", risks_context)
                
                p_business = f"{agent_prompt_biz}\n\n{business_prompt}"
                p_moat = f"{agent_prompt_moat}\n\n{moat_prompt}"
                p_risks = f"{agent_prompt_risks}\n\n{risks_prompt}"
                
                res_biz = self._get_cached_data(cache_biz)
                res_moat = self._get_cached_data(cache_moat)
                res_risk = self._get_cached_data(cache_risks)

                tasks = []
                async def run_and_cache(task_coro, cache_path, schema):
                    res = await task_coro
                    try:
                        schema(**res)
                        self._set_cached_data(cache_path, res)
                        return res
                    except ValidationError as ve:
                        raise LLMParsingError(f"LLM returned invalid JSON structure from a sub-agent: {ve}")

                if res_biz:
                    logger.info(f"[Orchestrator] Cache hit for Business Agent for {symbol}.")
                else:
                    task_biz_coro = self._generate_company_profile(p_business, BusinessModelSchema, model_id="gemini-3.1-pro-preview")
                    tasks.append(("biz", run_and_cache(task_biz_coro, cache_biz, BusinessModelSchema)))
                
                if res_moat:
                    logger.info(f"[Orchestrator] Cache hit for Moat Agent for {symbol}.")
                else:
                    task_moat_coro = self._generate_company_profile(p_moat, MoatAnalysisSchema, model_id="gemini-3.1-pro-preview")
                    tasks.append(("moat", run_and_cache(task_moat_coro, cache_moat, MoatAnalysisSchema)))

                if res_risk:
                    logger.info(f"[Orchestrator] Cache hit for Risk Agent for {symbol}.")
                else:
                    task_risk_coro = self._generate_company_profile(p_risks, RiskCatalystSchema, model_id="gemini-3.1-pro-preview")
                    tasks.append(("risk", run_and_cache(task_risk_coro, cache_risks, RiskCatalystSchema)))

                if tasks:
                    import time
                    start_time = time.time()
                    logger.info(f"[Orchestrator] Dispatching {len(tasks)} parallel agents for {symbol}...")
                    
                    coros = [t[1] for t in tasks]
                    results = await asyncio.gather(*coros, return_exceptions=True)
                    
                    # Check for exceptions (if one failed, we raise it, but the successful ones were already saved)
                    for res in results:
                        if isinstance(res, Exception):
                            raise res
                            
                    # Map results back
                    for i, (name, coro) in enumerate(tasks):
                        if name == "biz": res_biz = results[i]
                        elif name == "moat": res_moat = results[i]
                        elif name == "risk": res_risk = results[i]
                        
                    elapsed = time.time() - start_time
                    logger.info(f"[Orchestrator] Parallel agents resolved successfully in {elapsed:.2f}s for {symbol}.")
                import re
                def reindex_agent_citations(agent_dict, start_idx):
                    if not agent_dict.get("sources"):
                        return agent_dict, start_idx
                    num_sources = len(agent_dict["sources"])
                    id_map = {}
                    for i, src in enumerate(agent_dict["sources"]):
                        old_id = str(src.get("citation_id", i+1))
                        new_id = str(start_idx + i)
                        id_map[old_id] = new_id
                        src["citation_id"] = new_id

                    def update_strings(obj):
                        if isinstance(obj, str):
                            def replacer(match):
                                c_id = match.group(1)
                                if c_id in id_map:
                                    return f"[{id_map[c_id]}]"
                                return match.group(0)
                            return re.sub(r'\[(\d+)\]', replacer, obj)
                        elif isinstance(obj, dict):
                            return {k: update_strings(v) if k != "sources" else v for k, v in obj.items()}
                        elif isinstance(obj, list):
                            return [update_strings(x) for x in obj]
                        return obj

                    agent_dict = update_strings(agent_dict)
                    return agent_dict, start_idx + num_sources

                next_idx = 1
                res_biz, next_idx = reindex_agent_citations(res_biz, next_idx)
                res_moat, next_idx = reindex_agent_citations(res_moat, next_idx)
                res_risk, next_idx = reindex_agent_citations(res_risk, next_idx)

                # Merge the results
                data_en = {**res_biz, **res_moat, **res_risk}
                
                # Merge sources robustly
                all_sources = []
                for res in [res_biz, res_moat, res_risk]:
                    all_sources.extend(res.get("sources", []))
                data_en["sources"] = all_sources
                
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
            key_executives=[{"name": e.name, "title": e.title} for e in schema_instance.key_executives],
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
            sources={s.citation_id: EntitySourceInfo(source_name=s.source_name, exact_quote=s.exact_quote) for s in schema_instance.sources}
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
        - CITATIONS: You MUST provide inline numerical citations (e.g. [1], [2], [3]) directly within your analysis text to back up your claims. CRITICAL: You must provide EXACTLY 1 citation per Porter factor (yielding approximately 15-20 total citations across the document). DO NOT group everything into a single [1] citation.
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
                {{ "citation_id": "1", "source_name": "Exact Document Name (e.g., META_10-Q_Q2_2026.txt)", "exact_quote": "SHORT exact sentence (max 1-2 sentences) from the context. CRITICAL: DO NOT use double quotes inside this text." }},
                {{ "citation_id": "2", "source_name": "Exact Document Name", "exact_quote": "Another SHORT exact sentence from the context. Replace internal quotes with single quotes." }}
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
                data_en = await self._generate_industry_dynamics(prompt, IndustrySectorDynamicsSchema, model_id="gemini-2.5-flash")
                try:
                    IndustrySectorDynamicsSchema(**data_en)
                except ValidationError as ve:
                    raise LLMParsingError(f"LLM returned invalid JSON structure: {ve}")
                self._set_cached_data(cache_path_en, data_en)
            
            if language != "en" and self.translator:
                data = await self.translator.translate_json(data_en, language)
            else:
                data = data_en
                
            try:
                IndustrySectorDynamicsSchema(**data)
            except ValidationError as ve:
                raise LLMParsingError(f"Translator returned invalid JSON structure: {ve}")
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
            sources={s.citation_id: EntitySourceInfo(source_name=s.source_name, exact_quote=s.exact_quote) for s in schema_instance.sources}
        )

    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en", focus_period: str = None) -> EarningsReport:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        agent_path = os.path.join(base_dir, "llm", "agents", "earnings-analyst", "agent.md")
        skill_path = os.path.join(base_dir, "llm", "agents", "earnings-analyst", "skills", "analyze_pdf.md")
        
        with open(agent_path, 'r', encoding='utf-8') as f:
            base_prompt = f.read().split("---")[-1].strip()
            
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_prompt = f.read().split("---")[-1].strip()
            
        focus_instruction = ""
        if focus_period:
            focus_instruction = f"\nCRITICAL: The user requested an analysis exclusively for the period {focus_period}. This document is an annual report, but you MUST isolate and extract ONLY the performance, guidance, and events pertaining to {focus_period}, ignoring the rest of the year."

        prompt = f"{base_prompt}\n\n{skill_prompt}\n\n{focus_instruction}".replace("{symbol}", symbol)

        if focus_period:
            if len(focus_period) >= 6 and focus_period[:4].isdigit():
                fp_formatted = focus_period[4:] + focus_period[:4]
            else:
                fp_formatted = focus_period
            cache_filename = f"earnings_{fp_formatted}_{language}.json"
            cache_filename_en = f"earnings_{fp_formatted}_en.json"
        else:
            with open(pdf_file_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:12]
            cache_filename = f"earnings_{symbol.upper()}_{file_hash}_{language}.json"
            cache_filename_en = f"earnings_{symbol.upper()}_{file_hash}_en.json"
            
        target_dir = os.path.join(self.cache_dir, symbol.upper(), "analysis", "earnings")
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, cache_filename)
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
        data = self._get_cached_data(cache_path)
        if not data:
            data_en = self._get_cached_data(cache_path_en)
            if not data_en:
                data_en = await self._generate_earnings_report(prompt, pdf_file_path, EarningsReportSchema, model_id="gemini-2.5-flash")
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

        return EarningsReport(
            period_end_date=schema_instance.period_end_date,

            capital_allocation=CapitalAllocation(
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
            sources={str(src.citation_number): EntitySourceInfo(source_name=src.source_name, exact_quote=src.source_text) for src in schema_instance.sources}
        )

    async def analyse_earnings_from_context(self, symbol: str, context: str, language: str = "en", focus_period: str = None) -> EarningsReport:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        agent_path = os.path.join(base_dir, "llm", "agents", "earnings-analyst", "agent.md")
        skill_path = os.path.join(base_dir, "llm", "agents", "earnings-analyst", "skills", "analyze_context.md")
        
        with open(agent_path, 'r', encoding='utf-8') as f:
            base_prompt = f.read().split("---")[-1].strip()
            
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_prompt = f.read().split("---")[-1].strip()
            
        prompt = f"{base_prompt}\n\n{skill_prompt}\n\nContext:\n{context}".replace("{symbol}", symbol)
        
        import hashlib
        
        if focus_period:
            if len(focus_period) >= 6 and focus_period[:4].isdigit():
                fp_formatted = focus_period[4:] + focus_period[:4]
            else:
                fp_formatted = focus_period
            cache_filename = f"earnings_{fp_formatted}_{language}.json"
            cache_filename_en = f"earnings_{fp_formatted}_en.json"
        else:
            context_hash = hashlib.md5(context.encode('utf-8')).hexdigest()[:12]
            cache_filename = f"earnings_{symbol.upper()}_{context_hash}_{language}.json"
            cache_filename_en = f"earnings_{symbol.upper()}_{context_hash}_en.json"
            
        target_dir = os.path.join(self.cache_dir, symbol.upper(), "analysis", "earnings")
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, cache_filename)
        cache_path_en = os.path.join(target_dir, cache_filename_en)
        
        data = self._get_cached_data(cache_path)
        if not data:
            data_en = self._get_cached_data(cache_path_en)
            if not data_en:
                data_en = await self._generate_earnings_from_context(prompt, context, EarningsReportSchema, model_id="gemini-2.5-flash")
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


        return EarningsReport(
            period_end_date=schema_instance.period_end_date,

            capital_allocation=CapitalAllocation(
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
            sources={str(src.citation_number): EntitySourceInfo(source_name=src.source_name, exact_quote=src.source_text) for src in schema_instance.sources}
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
            data_en = await self._generate_dcf_assumptions(prompt, DCFValuationResponseSchema, model_id="gemini-2.5-flash")
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
