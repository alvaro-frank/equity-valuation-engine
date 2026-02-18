from infrastructure.gemini_adapter import GeminiAdapter
from services.dtos import QualitativeValuationDTO, TickerDTO

class QualitativeValuationService:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in a TickerDTO, analyzes the quality, moat and background of a business, and returns a QualitativeValuationDTO containing the analysis results.
    """
    def __init__(self, gemini_adapter: GeminiAdapter):
        """
        Initializes the QualitativeValuationService with the GeminiAdapter for AI-driven analysis.
        """
        self.gemini_adapter = gemini_adapter

    def analyze_business(self, ticker_dto: TickerDTO) -> QualitativeValuationDTO:
        """
        Analyzes the qualitative aspects of a business, such as its history and business model, using AI analysis.
        
        Args:
            ticker_dto (TickerDTO): The data transfer object containing the ticker's metadata.
            
        Returns:
            QualitativeValuationDTO: The result of the qualitative analysis, including history and business description.
        """
        analysis_dict = self.gemini_adapter.analyse_company(
            symbol=ticker_dto.symbol
        )
        
        analysis_dict.pop("ticker", None)
        
        return QualitativeValuationDTO(
            ticker=ticker_dto,
            **analysis_dict
        )