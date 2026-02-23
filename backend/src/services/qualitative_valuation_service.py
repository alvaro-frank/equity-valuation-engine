from domain.entities import CompanyProfile, Ticker
from domain.interfaces import QualitativeDataProvider, QuantitativeDataProvider

class QualitativeValuationService:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in an entity Ticker, analyses the quality, moat and background of a business, and returns a tuple[Ticker, CompanyProfile] containing the analysis results.
    """
    def __init__(self, adapter: QualitativeDataProvider, quant_adapter: QuantitativeDataProvider):
        """
        Initializes the QualitativeValuationService with the GeminiAdapter for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter

    def analyse_business(self, ticker: Ticker) -> tuple[Ticker, CompanyProfile]:
        """
        analyses the qualitative aspects of a business, such as its history and business model, using AI analysis.
        
        Args:
            ticker (Ticker): The Domain Entity containing the ticker's metadata.
            
        Returns:
            tuple[Ticker, CompanyProfile]: a tuple containing Ticker and CompanyProfile entities.
        """
        qual_data: CompanyProfile = self.adapter.analyse_company(
            symbol=ticker.symbol
        )
        
        return ticker, qual_data
        
    def analyse_ticker(self, ticker_symbol: str) -> tuple[Ticker, CompanyProfile]:
        """
        Fetches the ticker information, such as business name, sector and industry
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            
        Returns:
            tuple[Ticker, CompanyProfile]: a tuple containing Ticker and CompanyProfile entities.
        """
        ticker_info = self.quant_adapter.get_ticker_info(ticker_symbol)
        return self.analyse_business(ticker_info)