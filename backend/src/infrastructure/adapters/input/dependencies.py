from fastapi import Depends
from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from application.use_cases.analyse_dcf_valuation import AnalyseDCFValuationUseCase
from application.use_cases.list_company_filings import ListCompanyFilingsUseCase
from application.use_cases.get_sector_performance import GetSectorPerformanceUseCase
from application.use_cases.search_tickers import SearchTickersUseCase
from application.use_cases.get_trending_tickers import GetTrendingTickersUseCase
from infrastructure.adapters.output.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.adapters.output.yfinance_adapter import YfinanceAdapter
from infrastructure.adapters.output.gemini_adapter import GeminiAdapter
from infrastructure.adapters.output.openrouter_adapter import OpenRouterAdapter
from infrastructure.adapters.output.groq_adapter import GroqAdapter
from infrastructure.adapters.output.fallback_adapter import FallbackQualitativeAdapter
from infrastructure.adapters.output.sec_edgar_adapter import SECAdapter
from infrastructure.config.settings import settings
from typing import Union
from application.ports.core_financial_ports import QuantitativeDataPort, PerformanceDataPort, OwnershipDataPort
from application.ports.llm_analysis_ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort
from application.ports.discovery_ports import SearchDataPort, TrendingDataPort
from application.ports.intrinsic_value_calculation_port import IntrinsicValueCalculationPort

# In a real production environment, these adapters can be maintained as global variables (Singletons)
# or constructed per request, depending on whether they store state (ex: DB sessions).
# As ours do not store heavy state and httpx/requests handle the pools internally,
# instantiating them here is not a problem, but we can optimize later.

from infrastructure.adapters.output.groq_translator import GroqTranslatorAdapter

_translator = GroqTranslatorAdapter()
_alpha_adapter = AlphaVantageAdapter(api_key=settings.alpha_vantage_api_key)
_yfinance_adapter = YfinanceAdapter()
_gemini_adapter = GeminiAdapter(api_key=settings.gemini_api_key, translator=_translator)
_openrouter_adapter = OpenRouterAdapter(translator=_translator)
_groq_adapter = GroqAdapter(translator=_translator)
_groq_fallback_to_openrouter = FallbackQualitativeAdapter(primary_adapter=_groq_adapter, backup_adapter=_openrouter_adapter)
_fallback_llm_adapter = FallbackQualitativeAdapter(primary_adapter=_gemini_adapter, backup_adapter=_groq_fallback_to_openrouter)

_sec_adapter = SECAdapter()

def get_translator() -> GroqTranslatorAdapter:
    """Provides the translator adapter instance."""
    return _translator

def get_quantitative_adapter() -> Union[QuantitativeDataPort, OwnershipDataPort]:
    """
    Provides the Quantitative Data Port instance based on settings.
    """
    if settings.data_provider.upper() == "YFINANCE":
        return _yfinance_adapter
    return _alpha_adapter

def get_search_adapter() -> SearchDataPort:
    """Provides the Search Data Port instance."""
    return _yfinance_adapter

def get_performance_adapter() -> PerformanceDataPort:
    """Provides the Performance Data Port instance."""
    return _yfinance_adapter

def get_trending_adapter() -> TrendingDataPort:
    """Provides the Trending Data Port instance."""
    return _yfinance_adapter

def get_llm_adapter() -> Union[SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort]:
    """
    Provides the Fallback LLM Adapter instance.
    """
    return _fallback_llm_adapter



def get_dcf_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    qual_adapter: QualitativeDataPort = Depends(get_llm_adapter),
    llm_adapter: IntrinsicValueCalculationPort = Depends(get_llm_adapter)
) -> AnalyseDCFValuationUseCase:
    """
    Builds and provides the Analyse DCF Valuation Use Case via Dependency Injection.
    """
    return AnalyseDCFValuationUseCase(
        quant_data_port=quant_adapter,
        qual_data_port=qual_adapter,
        llm_port=llm_adapter
    )

def get_earnings_report_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    llm_adapter = Depends(get_llm_adapter)
) -> EarningsReportUseCase:
    """
    Builds and provides the Earnings Report Use Case via Dependency Injection.
    """
    return EarningsReportUseCase(adapter=llm_adapter, quant_adapter=quant_adapter)

def get_quantitative_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter)
) -> QuantitativeValuationUseCase:
    """
    Builds and provides the Quantitative Valuation Use Case via Dependency Injection.
    """
    return QuantitativeValuationUseCase(adapter=quant_adapter)

def get_qualitative_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    llm_adapter = Depends(get_llm_adapter),
    translator = Depends(get_translator),
    filing_repository_port = Depends(lambda: _sec_adapter)
) -> QualitativeValuationUseCase:
    """
    Builds and provides the Qualitative Valuation Use Case via Dependency Injection.
    """
    return QualitativeValuationUseCase(
        adapter=llm_adapter, 
        quant_adapter=quant_adapter, 
        ownership_adapter=quant_adapter, 
        translator=translator,
        filing_repository_port=filing_repository_port
    )

def get_sector_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    llm_adapter = Depends(get_llm_adapter)
) -> SectorIndustrialValuationUseCase:
    """
    Builds and provides the Sector Industrial Valuation Use Case via Dependency Injection.
    """
    return SectorIndustrialValuationUseCase(
        quant_port=quant_adapter,
        sector_industrial_port=llm_adapter
    )

def get_sector_performance_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    performance_adapter: PerformanceDataPort = Depends(get_performance_adapter)
) -> GetSectorPerformanceUseCase:
    """
    Builds and provides the Sector Performance Use Case via Dependency Injection.
    """
    return GetSectorPerformanceUseCase(quant_port=quant_adapter, performance_port=performance_adapter)

def get_search_tickers_use_case(
    search_adapter: SearchDataPort = Depends(get_search_adapter)
) -> SearchTickersUseCase:
    """
    Builds and provides the Search Tickers Use Case via Dependency Injection.
    """
    return SearchTickersUseCase(search_port=search_adapter)

def get_trending_tickers_use_case(
    trending_adapter: TrendingDataPort = Depends(get_trending_adapter)
) -> GetTrendingTickersUseCase:
    """
    Builds and provides the Trending Tickers Use Case via Dependency Injection.
    """
    return GetTrendingTickersUseCase(trending_port=trending_adapter)

def get_list_company_filings_use_case() -> ListCompanyFilingsUseCase:
    """
    Builds and provides the List Company Filings Use Case via Dependency Injection.
    """
    return ListCompanyFilingsUseCase(filing_repository_port=_sec_adapter)
