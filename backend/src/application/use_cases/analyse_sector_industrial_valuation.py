from application.ports.ports import QuantitativeDataPort, SectorIndustrialDataPort
from domain.entities.entities import IndustrySectorDynamics
from application.dtos.dtos import TickerResult, SectorIndustrialValuationResult
from dataclasses import asdict

class SectorIndustrialValuationUseCase:
    """
    Service responsible for orchestrating the industry and sector analysis.
    It fetches sector metadata for a ticker and uses AI to perform a structural analysis.
    """
    def __init__(self, quant_port: QuantitativeDataPort, sector_industrial_port: SectorIndustrialDataPort):
        """
        Initializes the service with qualitative (AI) and quantitative (Financial Data) ports.
        
        Args:
            qual_port (QualitativeDataPort): Port for AI industry analysis.
            quant_port (QuantitativeDataPort): Port for ticker and sector metadata.
        """
        self.quant_port = quant_port
        self.sector_industrial_port = sector_industrial_port

    def evaluate_industry_by_ticker(self, ticker_symbol: str) -> SectorIndustrialValuationResult:
        """
        Main entry point to analyse an industry based on a specific company ticker.
        
        Args:
            ticker_symbol (str): The stock ticker to identify the sector and industry.
            
        Returns:
            SectorIndustrialValuationResult: a DTO containing all information about the Industry and Sector.
        """
        ticker_info = self.quant_port.get_ticker_info(ticker_symbol)
        
        analysis: IndustrySectorDynamics = self.sector_industrial_port.analyse_industry(
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )
        
        ticker_dto = TickerResult(
            symbol=ticker_info.symbol,
            name=ticker_info.name,
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )
        
        return SectorIndustrialValuationResult(
            ticker=ticker_dto,
            **asdict(analysis)
        )