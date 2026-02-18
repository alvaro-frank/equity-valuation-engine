from services.qualitative_valuation_service import QualitativeValuationService
from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from services.dtos import QualitativeValuationDTO

class QualitativeValuationController:
    """
    Controller responsible for orchestrating the stock qualitative valuation process, including fetching data from the Adapter and performing analysis using the QualitativeValuationService.
    """
    def __init__(self, service: QualitativeValuationService):
        """
        Initializes the QualitativeValuationController with the necessary data adapter and qualitative analysis service.
        
        Args:
            service (QualitativeValuationService): The service to handle the valuation logic.
        """
        self.service = service

    def run(self, ticker_symbol: str):
        """
        Main method to run the qualitative valuation process for a given ticker.

        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.

        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\nA realizar Análise Qualitativa com Gemini IA para {ticker_symbol}...")
        
        try:
            analysis = self.service.analyse_ticker(ticker_symbol)
            self._display_qualitative_report(analysis)

        except Exception as e:
            print(f"Qualitative analysis error: {e}")

    def _display_qualitative_report(self, analysis: QualitativeValuationDTO):
        """
        Nicely formats and prints the qualitative valuation results to the console.

        Args:
            analysis (QualitativeValuationDTO): The result of the qualitative valuation analysis to display.

        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\n{'='*60}")
        print(f"QUALITATIVE ANALYSIS: {analysis.ticker.name}")
        print(f"{'='*60}")
        
        print(f"\nBUSINESS HISTORY:")
        print(analysis.company_history)
        
        print(f"\nBUSINESS MODEL:")
        print(analysis.business_description)
        
        print(f"\n{'='*60}\n")