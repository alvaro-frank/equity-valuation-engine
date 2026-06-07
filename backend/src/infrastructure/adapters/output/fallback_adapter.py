from application.ports.ports import SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort
from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport

class FallbackQualitativeAdapter(SectorIndustrialDataPort, EarningsReportPort, QualitativeDataPort):
    """
    An adapter that implements the fallback pattern.
    It attempts to use the primary adapter first. If it fails, it falls back to the secondary adapter.
    """
    def __init__(self, primary_adapter, backup_adapter):
        self.primary = primary_adapter
        self.backup = backup_adapter

    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
        try:
            return await self.primary.analyse_company(symbol, language=language, context=context)
        except Exception as e:
            print(f"Primary adapter failed for analyse_company: {e}. Falling back to backup adapter.")
            return await self.backup.analyse_company(symbol, language=language, context=context)

    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
        try:
            return await self.primary.analyse_industry(sector, industry, language=language)
        except Exception as e:
            print(f"Primary adapter failed for analyse_industry: {e}. Falling back to backup adapter.")
            return await self.backup.analyse_industry(sector, industry, language=language)

    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en") -> EarningsReport:
        try:
            return await self.primary.analyse_earnings_report(symbol, pdf_file_path, language=language)
        except Exception as e:
            print(f"Primary adapter failed for analyse_earnings_report: {e}. Falling back to backup adapter.")
            return await self.backup.analyse_earnings_report(symbol, pdf_file_path, language=language)
