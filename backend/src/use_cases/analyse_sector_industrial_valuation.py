from domain.interfaces import QualitativeDataProvider, QuantitativeDataProvider
from domain.entities import IndustrySectorDynamics, Ticker
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

    def evaluate_industry_by_ticker(self, ticker_symbol: str) -> tuple[Ticker, IndustrySectorDynamics]:
        """
        Main entry point to analyse an industry based on a specific company ticker.
        
        Args:
            ticker_symbol (str): The stock ticker to identify the sector and industry.
            
        Returns:
            tuple[Ticker, IndustrySectorDynamics]: a tuple containing Ticker and IndustrySectorDynamics Entities.
        """
        ticker_info = self.quant_provider.get_ticker_info(ticker_symbol)
        
        analysis: IndustrySectorDynamics = self.qual_provider.analyse_industry(
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )
        
        return ticker_info, analysis