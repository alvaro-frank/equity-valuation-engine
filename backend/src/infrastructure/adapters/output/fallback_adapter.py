from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort
from application.ports.intrinsic_value_calculation_port import IntrinsicValueCalculationPort
from application.exceptions.exceptions import ExternalServiceError, RateLimitExceededError, LLMParsingError
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport

class FallbackQualitativeAdapter(SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort, IntrinsicValueCalculationPort):
    """
    An adapter that implements the fallback pattern.
    It attempts to use the primary adapter first. If it fails, it falls back to the secondary adapter.
    """
    def __init__(self, primary_adapter, backup_adapter):
        """
        Initializes the fallback adapter with a primary and a backup adapter.
        
        Args:
            primary_adapter: The main adapter to attempt first.
            backup_adapter: The fallback adapter to use if the primary fails.
        """
        self.primary = primary_adapter
        self.backup = backup_adapter

    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
        """
        Attempts to fetch qualitative data for a company using the primary adapter. If it fails, it falls back to the backup adapter.
        
        Args:
            symbol (str): The stock ticker symbol to be analysed.
            language (str): Target language for the analysis.
            context (str): Contextual financial data to ground the analysis and prevent hallucination.
            
        Returns:
            CompanyProfile: Domain Entity containing the qualitative data of the business.
        """
        try:
            return await self.primary.analyse_company(symbol, language=language, context=context)
        except (ExternalServiceError, RateLimitExceededError, LLMParsingError) as e:
            print(f"Primary adapter failed for analyse_company: {e}. Falling back to backup adapter.")
            return await self.backup.analyse_company(symbol, language=language, context=context)

    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
        """
        Attempts to fetch industry and sector dynamics data using the primary adapter. If it fails, it falls back to the backup adapter.
        
        Args:
            sector (str): The industry sector to be analysed.
            industry (str): The specific industry to be analysed.
            language (str): Target language for the analysis.
            
        Returns:
            IndustrySectorDynamics: Domain Entity containing the industry and sector dynamics data.
        """
        try:
            return await self.primary.analyse_industry(sector, industry, language=language)
        except (ExternalServiceError, RateLimitExceededError, LLMParsingError) as e:
            print(f"Primary adapter failed for analyse_industry: {e}. Falling back to backup adapter.")
            return await self.backup.analyse_industry(sector, industry, language=language)

    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en") -> EarningsReport:
        """
        Attempts to analyse an earnings report using the primary adapter. If it fails, it falls back to the backup adapter.
        
        Args:
            symbol (str): The stock ticker symbol.
            pdf_file_path (str): The path to the PDF file containing the earnings report.
            language (str): Target language for the analysis.
            
        Returns:
            EarningsReport: Domain Entity containing the analysed earnings report data.
        """
        try:
            return await self.primary.analyse_earnings_report(symbol, pdf_file_path, language=language)
        except (ExternalServiceError, RateLimitExceededError, LLMParsingError) as e:
            print(f"Primary adapter failed for analyse_earnings_report: {e}. Falling back to backup adapter.")
            return await self.backup.analyse_earnings_report(symbol, pdf_file_path, language=language)

    async def deduce_dcf_assumptions(self, ticker: str, company_profile: dict, quant_data: dict, language: str = "en") -> dict:
        """
        Attempts to deduce DCF assumptions using the primary adapter. If it fails, falls back to the backup adapter.
        """
        try:
            return await self.primary.deduce_dcf_assumptions(ticker, company_profile, quant_data, language)
        except (ExternalServiceError, RateLimitExceededError, LLMParsingError) as e:
            print(f"Primary adapter failed for deduce_dcf_assumptions: {e}. Falling back to backup adapter.")
            return await self.backup.deduce_dcf_assumptions(ticker, company_profile, quant_data, language)
