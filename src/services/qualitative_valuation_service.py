from domain.interfaces import QualitativeDataProvider, QuantitativeDataProvider
from services.dtos import QualitativeValuationDTO, QualitativeDataDTO, TickerDTO

class QualitativeValuationService:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in a TickerDTO, analyses the quality, moat and background of a business, and returns a QualitativeValuationDTO containing the analysis results.
    """
    def __init__(self, adapter: QualitativeDataProvider, quant_adapter: QuantitativeDataProvider):
        """
        Initializes the QualitativeValuationService with the GeminiAdapter for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter

    def analyse_business(self, ticker_dto: TickerDTO) -> QualitativeValuationDTO:
        """
        analyses the qualitative aspects of a business, such as its history and business model, using AI analysis.
        
        Args:
            ticker_dto (TickerDTO): The data transfer object containing the ticker's metadata.
            
        Returns:
            QualitativeValuationDTO: The result of the qualitative analysis, including history and business description.
        """
        qual_data: QualitativeDataDTO = self.adapter.analyse_company(
            symbol=ticker_dto.symbol
        )
        
        return QualitativeValuationDTO(
            ticker=ticker_dto,
            business_description=qual_data.business_description,
            company_history=qual_data.company_history
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