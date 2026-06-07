import os
import json
import time
import re
from openai import AsyncOpenAI
import pymupdf4llm
from dotenv import load_dotenv
from decimal import Decimal
from typing import Optional

from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort, TranslationPort
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport, CorePerformance, MetricWithGrowth, CapitalAllocation, RiskDeconstruction, MoatSources, QualityPillars
from infrastructure.schemas.gemini_schemas import CompanyProfileSchema, IndustrySectorDynamicsSchema, EarningsReportSchema

load_dotenv()

class OpenRouterAdapter(SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort):
    """
    Adapter that leverages OpenRouter (specifically DeepSeek) to generate qualitative research.
    """
    def __init__(self, api_key: Optional[str] = None, client: Optional[AsyncOpenAI] = None, translator: Optional[TranslationPort] = None):
        """
        Initializes the OpenRouter client.
        """
        if client:
            self.client = client
        else:
            if not api_key:
                api_key = os.getenv("OPENROUTER_API_KEY")
                if not api_key:
                    raise ValueError("OPENROUTER_API_KEY is required")
            
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            
        self.translator = translator
        self.model_id = 'deepseek/deepseek-chat' # Use standard deepseek v3/v4 depending on availability
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.llm_cache')
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

    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
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
        - Data Types: 'ceo_ownership' must be a numeric representing a percentage (e.g., 3.5).
        - Lists of Objects: For 'major_shareholders' include the top investors, both institutional (e.g. Vanguard) and individual/insiders (e.g. Founders, CEO) if they hold significant stakes. For 'products_services', 'competitors', and 'risk_factors', provide a list of objects as specified in the schema.
        - Tone: Professional, objective, and data-driven.
        - Language: Generate the analysis text in the following language: {lang_instruction}. 
        - CRITICAL: DO NOT TRANSLATE THE JSON KEYS. They must remain exactly as shown below (e.g. "business_description", "major_shareholders").

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
                    temperature=0.0,
                    max_tokens=4000,
                )
                
                if not getattr(response, 'choices', None) or len(response.choices) == 0:
                    raise ValueError(f"OpenRouter API returned no choices. Response: {getattr(response, 'model_dump_json', lambda: str(response))()}")
                
                content = response.choices[0].message.content
                if content is None:
                    raise ValueError("OpenRouter API returned None for message content.")
                
                data = self._get_json_from_response(content)
                
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
            historical_context_crises=schema_instance.historical_context_crises,
            moat_trajectory=schema_instance.moat_trajectory,
            moat_sources=MoatSources(**schema_instance.moat_sources.model_dump()),
            quality_pillars=QualityPillars(**schema_instance.quality_pillars.model_dump())
        )

    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
        lang_instruction = language
        if language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms."

        prompt = f"""
        Act as a Senior Equity Research Analyst and Industry Strategist. 
        Perform a comprehensive fundamental analysis of the following market:
        SECTOR: {sector}
        INDUSTRY: {industry}

        CORE FRAMEWORK: Use Porter's Five Forces to evaluate structural profitability and competitive intensity.

        INSTRUCTIONS FOR JSON ARRAYS (Sections 1-5):
        For each force, identify 2-4 key factors. Return them as a LIST of objects, where each object has a 'factor' (short, descriptive title) and an 'analysis' (professional analysis).
        Language: Generate the analysis text in the following language: {lang_instruction}.
        CRITICAL: DO NOT TRANSLATE THE JSON KEYS. They must remain exactly as shown below (e.g. "rivalry_among_competitors").

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
                    response = await self.client.chat.completions.create(
                        model=self.model_id,
                        messages=[
                            {"role": "system", "content": "You are a machine that outputs only raw, valid JSON."},
                            {"role": "user", "content": prompt_en}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.0,
                        max_tokens=4000
                    )
                    data_en = self._get_json_from_response(response.choices[0].message.content)
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
        lang_instruction = language
        if language == "pt":
            lang_instruction = "Portuguese (European / pt-PT). DO NOT use Brazilian Portuguese terms."

        prompt = f"""
        You are a Senior Equity Analyst focused on long-term value investing. I am providing the full text of an Earnings Report for the company "{symbol}". Ignore short-term stock reactions and Wall Street consensus. Focus exclusively on underlying business fundamentals.

        Perform a deep-dive analysis and return ONLY a structured JSON object. Do not include markdown formatting, code blocks, or conversational text.
        Language: Generate the analysis text in the following language: {lang_instruction}. 
        CRITICAL: DO NOT TRANSLATE THE JSON KEYS. They must remain exactly as shown below (e.g. "core_performance", "adjusted_revenue").

        Extract and synthesize the following fields EXACTLY as named:

        {{
            "ticker": "String: The stock ticker symbol",
            "period_end_date": "String: The end date of the fiscal period",
            "core_performance": {{
                "adjusted_revenue": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "adjusted_eps": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "adjusted_gross_margin": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "adjusted_operating_margin": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "adjusted_net_margin": {{ "amount": 0.0, "yoy_growth": 0.0 }},
                "free_cash_flow": {{ "amount": 0.0, "yoy_growth": 0.0 }}
            }},
            "capital_allocation": {{
                "share_buybacks": 0.0,
                "dividends": 0.0,
                "capex_rd": 0.0,
                "infrastructure_assessment": "String: Detailed 2-3 sentence paragraph explaining the 'why' behind the CapEx/R&D (e.g., accelerating for AI buildout, cutting back for margins). Do not just provide a single word."
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

        import hashlib
        with open(pdf_file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:12]
        cache_filename = f"earnings_{symbol.upper()}_{file_hash}_{language}.json"
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
            
            # Truncate text to avoid exceeding token limits (approx 25k tokens)
            if len(md_text) > 100000:
                md_text = md_text[:100000] + "\n\n[TEXT TRUNCATED DUE TO LENGTH LIMITS]"
            
            # Combine prompt and PDF text
            full_prompt = prompt + f"\n\n--- EARNINGS REPORT TEXT ---\n\n{md_text}"

            try:
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[{"role": "user", "content": full_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.0,
                    max_tokens=4000,
                )
                
                if not getattr(response, 'choices', None) or len(response.choices) == 0:
                    raise ValueError(f"OpenRouter API returned no choices. Response: {getattr(response, 'model_dump_json', lambda: str(response))()}")
                
                content = response.choices[0].message.content
                if content is None:
                    raise ValueError("OpenRouter API returned None for message content.")
                
                data = self._get_json_from_response(content)
            
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
