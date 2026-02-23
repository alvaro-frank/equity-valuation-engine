from domain.entities import CompanyProfile, Ticker
from domain.interfaces import QualitativeDataProvider, QuantitativeDataProvider
from services.dtos import QualitativeValuationDTO, TickerDTO
from dataclasses import asdict

class QualitativeValuationService:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in an entity Ticker, analyses the quality, moat and background of a business, and returns a QualitativeValuationDTO containing the analysis results.
    """
    def __init__(self, adapter: QualitativeDataProvider, quant_adapter: QuantitativeDataProvider):
        """
        Initializes the QualitativeValuationService with the GeminiAdapter for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter

    def analyse_business(self, ticker: Ticker) -> QualitativeValuationDTO:
        """
        analyses the qualitative aspects of a business, such as its history and business model, using AI analysis.
        
        Args:
            ticker (Ticker): The Domain Entity containing the ticker's metadata.
            
        Returns:
            QualitativeValuationDTO: The result of the qualitative analysis, including history and business description.
        """
        qual_data: CompanyProfile = self.adapter.analyse_company(
            symbol=ticker.symbol
        )
        
        return QualitativeValuationDTO(
            ticker=TickerDTO(symbol=ticker.symbol, name=ticker.name, sector=ticker.sector, industry=ticker.industry),
            **asdict(qual_data)
        )
        
    def analyse_ticker(self, ticker_symbol: str) -> QualitativeValuationDTO:
        """
        Fetches the ticker information, such as business name, sector and industry
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            
        Returns: 
            QualitativeValuationDTO: The result of the qualitative analysis, including history and business description.
        """
        ticker_info = self.quant_adapter.get_ticker_info(ticker_symbol)
        return self.analyse_business(ticker_info)