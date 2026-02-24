from domain.interfaces import QualitativeDataProvider, QuantitativeDataProvider
from domain.entities import IndustrySectorDynamics
from dtos.dtos import TickerDTO, SectorValuationDTO
from dataclasses import asdict

class SectorValuationService:
    """
    Service responsible for orchestrating the industry and sector analysis.
    It fetches sector metadata for a ticker and uses AI to perform a structural analysis.
    """
    def __init__(self, qual_provider: QualitativeDataProvider, quant_provider: QuantitativeDataProvider):
        """
        Initializes the service with qualitative (AI) and quantitative (Financial Data) providers.
        
        Args:
            qual_provider (QualitativeDataProvider): Provider for AI industry analysis.
            quant_provider (QuantitativeDataProvider): Provider for ticker and sector metadata.
        """
        self.qual_provider = qual_provider
        self.quant_provider = quant_provider

    def evaluate_industry_by_ticker(self, ticker_symbol: str) -> SectorValuationDTO:
        """
        Main entry point to analyse an industry based on a specific company ticker.
        
        Args:
            ticker_symbol (str): The stock ticker to identify the sector and industry.
            
        Returns:
            SectorValuationDTO: a DTO containing all information about the Industry and Sector.
        """
        ticker_info = self.quant_provider.get_ticker_info(ticker_symbol)
        
        analysis: IndustrySectorDynamics = self.qual_provider.analyse_industry(
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )
        
        ticker_dto = TickerDTO(
            symbol=ticker_info.symbol,
            name=ticker_info.name,
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )
        
        return SectorValuationDTO(
            ticker=ticker_dto,
            **asdict(analysis)
        )