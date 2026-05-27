from fastapi import Depends
from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from infrastructure.adapters.output.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.adapters.output.yfinance_adapter import YfinanceAdapter
from infrastructure.adapters.output.gemini_adapter import GeminiAdapter
from infrastructure.config.settings import settings
from typing import Union
from application.ports.ports import QuantitativeDataPort, QuarterlyDataPort

# In a real production environment, these adapters can be maintained as global variables (Singletons)
# or constructed per request, depending on whether they store state (ex: DB sessions).
# As ours do not store heavy state and httpx/requests handle the pools internally,
# instantiating them here is not a problem, but we can optimize later.

_alpha_adapter = AlphaVantageAdapter(api_key=settings.alpha_vantage_api_key)
_yfinance_adapter = YfinanceAdapter()
_gemini_adapter = GeminiAdapter(api_key=settings.gemini_api_key)

def get_quantitative_adapter() -> Union[QuantitativeDataPort, QuarterlyDataPort]:
    """
    Provides the Quantitative/Quarterly Data Port instance based on settings.
    """
    if settings.data_provider.upper() == "YFINANCE":
        return _yfinance_adapter
    return _alpha_adapter

def get_gemini_adapter() -> GeminiAdapter:
    """
    Provides the GeminiAdapter instance.
    """
    return _gemini_adapter

def get_earnings_report_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    gemini_adapter: GeminiAdapter = Depends(get_gemini_adapter)
) -> EarningsReportUseCase:
    """
    Builds and provides the Earnings Report Use Case via Dependency Injection.
    """
    return EarningsReportUseCase(adapter=gemini_adapter, quant_adapter=quant_adapter)

def get_quantitative_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter)
) -> QuantitativeValuationUseCase:
    """
    Builds and provides the Quantitative Valuation Use Case via Dependency Injection.
    """
    return QuantitativeValuationUseCase(adapter=quant_adapter, quarterly_adapter=quant_adapter)

def get_qualitative_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    gemini_adapter: GeminiAdapter = Depends(get_gemini_adapter)
) -> QualitativeValuationUseCase:
    """
    Builds and provides the Qualitative Valuation Use Case via Dependency Injection.
    """
    return QualitativeValuationUseCase(adapter=gemini_adapter, quant_adapter=quant_adapter)

def get_sector_use_case(
    quant_adapter: QuantitativeDataPort = Depends(get_quantitative_adapter),
    gemini_adapter: GeminiAdapter = Depends(get_gemini_adapter)
) -> SectorIndustrialValuationUseCase:
    """
    Builds and provides the Sector Industrial Valuation Use Case via Dependency Injection.
    """
    return SectorIndustrialValuationUseCase(quant_port=quant_adapter, sector_industrial_port=gemini_adapter)
