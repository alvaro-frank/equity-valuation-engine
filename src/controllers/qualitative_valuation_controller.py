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
        
        print(f"\nGENERAL DESCRIPTION AND HISTORY:")
        print(f"   - Business: {analysis.business_description}")
        print(f"   - Evolution: {analysis.company_history}")
        
        print(f"\nLEADERSHIP AND MANAGEMENT:")
        print(f"   - CEO: {analysis.ceo_name} (Ownership: {analysis.ceo_ownership})")
        print(f"   - Insights: {analysis.management_insights}")
        
        print(f"\nSHAREHOLDER STRUCTURE AND COMPETITION:")
        print(f"   - Major Shareholders: {', '.join(analysis.major_shareholders)}")
        print(f"   - Main Competitors: {', '.join(analysis.competitors)}")
        
        print(f"\nSTRATEGY AND PRODUCTS:")
        print(f"   - Revenue Model: {analysis.revenue_model}")
        print(f"   - Core Strategy: {analysis.strategy}")
        print(f"   - Offerings: {', '.join(analysis.products_services)}")
        
        print(f"\nCOMPETITIVE ADVANTAGE (MOAT):")
        print(f"   - {analysis.competitive_advantage}")
        
        print(f"\nRISK FACTORS AND RESILIENCE:")
        risks_formatted = "\n   - ".join(analysis.risk_factors)
        print(f"   - {risks_formatted}")
        print(f"   - Crisis History: {analysis.historical_context_crises}")
        
        print(f"\n{'='*60}\n")