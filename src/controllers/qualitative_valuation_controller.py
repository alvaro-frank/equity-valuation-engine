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
        """
        self.service = service

    def run(self, ticker_symbol: str):
        """
        Main method to run the qualitative valuation process for a given ticker.

        Args:
            ticker_symbol (str): The stock ticker symbol to analyze.

        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\nA realizar Análise Qualitativa com Gemini IA para {ticker_symbol}...")
        
        try:
            analysis = self.service.analyze_ticker(ticker_symbol)
            self._display_qualitative_report(analysis)

        except Exception as e:
            print(f"Erro na análise qualitativa: {e}")

    def _display_qualitative_report(self, analysis: QualitativeValuationDTO):
        """
        Nicely formats and prints the qualitative valuation results to the console.

        Args:
            analysis (QualitativeValuationDTO): The result of the qualitative valuation analysis to display.

        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\n{'='*60}")
        print(f"ANÁLISE QUALITATIVA: {analysis.ticker.name}")
        print(f"{'='*60}")
        
        print(f"\nHISTÓRIA DA EMPRESA:")
        print(analysis.company_history)
        
        print(f"\nMODELO DE NEGÓCIO:")
        print(analysis.business_description)
        
        print(f"\n{'='*60}\n")