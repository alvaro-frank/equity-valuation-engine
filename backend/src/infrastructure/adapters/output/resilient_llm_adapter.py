from typing import Union, Dict, Any
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from application.ports.llm_analysis_ports import QualitativeDataPort, SectorIndustrialDataPort, EarningsReportPort
from application.ports.intrinsic_value_calculation_port import IntrinsicValueCalculationPort
from application.exceptions.exceptions import RateLimitExceededError, ExternalServiceError
from domain.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport
from domain.entities.dcf import DCFAssumptions
from application.dtos import StructuredFilingDTO

class ResilientLLMAdapter(QualitativeDataPort, SectorIndustrialDataPort, EarningsReportPort, IntrinsicValueCalculationPort):
    """
    Adapter that wraps around another LLM adapter to provide resilience against rate limits and external service errors.
    """
    
    def __init__(self, base_adapter: Union[QualitativeDataPort, SectorIndustrialDataPort, EarningsReportPort, IntrinsicValueCalculationPort]):
        self.base = base_adapter
        
    @retry(
        retry=retry_if_exception_type((RateLimitExceededError, ExternalServiceError)),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def analyse_company(self, symbol: str, language: str = "en", context: str = "", structured_filings: 'StructuredFilingDTO' = None) -> CompanyProfile:
        return await self.base.analyse_company(symbol, language, context, structured_filings)

    @retry(
        retry=retry_if_exception_type((RateLimitExceededError, ExternalServiceError)),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en", focus_period: str = None) -> EarningsReport:
        return await self.base.analyse_earnings_report(symbol, pdf_file_path, language, focus_period)

    @retry(
        retry=retry_if_exception_type((RateLimitExceededError, ExternalServiceError)),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def analyse_industry(self, sector: str, industry: str, language: str = "en", ticker: str = "", context: str = "") -> IndustrySectorDynamics:
        return await self.base.analyse_industry(sector, industry, language, ticker, context)

    @retry(
        retry=retry_if_exception_type((RateLimitExceededError, ExternalServiceError)),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def deduce_dcf_assumptions(self, ticker: str, company_profile: Dict[str, Any], quant_data: Dict[str, Any], language: str = "en") -> Dict[str, DCFAssumptions]:
        return await self.base.deduce_dcf_assumptions(ticker, company_profile, quant_data, language)
