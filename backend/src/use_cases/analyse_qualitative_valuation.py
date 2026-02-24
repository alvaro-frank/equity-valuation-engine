from domain.entities import CompanyProfile
from domain.interfaces import QualitativeDataProvider, QuantitativeDataProvider
from dtos.dtos import TickerDTO, QualitativeValuationDTO
from dataclasses import asdict

class QualitativeValuationService:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in an entity Ticker, analyses the quality, moat and background of a business, and returns a DTO containing all information about the Qualitative data of the business.
    """
    def __init__(self, adapter: QualitativeDataProvider, quant_adapter: QuantitativeDataProvider):
        """
        Initializes the QualitativeValuationService with the GeminiAdapter for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter
        
    def analyse_ticker(self, ticker_symbol: str) -> QualitativeValuationDTO:
        """
        Fetches the ticker information, such as business name, sector and industry
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            
        Returns:
            QualitativeValuationDTO: a DTO containing all information about the Qualitative data of the business.
        """
        ticker_info = self.quant_adapter.get_ticker_info(ticker_symbol)
        
        qual_data: CompanyProfile = self.adapter.analyse_company(
            symbol=ticker_info.symbol
        )
        
        ticker_dto = TickerDTO(
            symbol=ticker_info.symbol,
            name=ticker_info.name,
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )

        return QualitativeValuationDTO(
            ticker=ticker_dto,
            **asdict(qual_data)
        )