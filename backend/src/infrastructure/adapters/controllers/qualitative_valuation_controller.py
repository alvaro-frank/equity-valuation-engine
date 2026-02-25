from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.dtos.dtos import QualitativeValuationDTO
from dataclasses import asdict

class QualitativeValuationController:
    """
    Controller responsible for orchestrating the stock qualitative valuation process, including fetching data from the Adapter and performing analysis using the QualitativeValuationUseCase.
    """
    def __init__(self, service: QualitativeValuationUseCase):
        """
        Initializes the QualitativeValuationController with the qualitative analysis service.
        
        Args:
            service (QualitativeValuationUseCase): The service to handle the valuation logic.
        """
        self.service = service

    def run(self, ticker_symbol: str):
        """
        Main method to run the qualitative valuation process for a given ticker.

        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.

        Returns:
            None: This method creates the QualitativeValuationDTO.
        """
        try:
            analysis_dto = self.service.analyse_ticker(ticker_symbol)

            self._display_qualitative_report(analysis_dto)

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
        print(f"   - CEO: {analysis.ceo_name} (Ownership: {analysis.ceo_ownership}%)")
        print(f"   - Insights: {analysis.management_insights}")
        
        print(f"\nMAJOR SHAREHOLDERS:")
        for title, ownership in analysis.major_shareholders.items():
            print(f"   - {title}: {ownership}%")
        
        print(f"\nCOMPETITION:")
        for title, description in analysis.competitors.items():
            print(f"   - {title}: {description}")
        
        print(f"\nSTRATEGY AND PRODUCTS:")
        print(f"   - Revenue Model: {analysis.revenue_model}")
        print(f"   - Core Strategy: {analysis.strategy}")
        for title, description in analysis.products_services.items():
            print(f"   - {title}: {description}")
        
        print(f"\nCOMPETITIVE ADVANTAGE (MOAT):")
        print(f"   - {analysis.competitive_advantage}")
        
        print(f"\nRISK FACTORS:")
        for title, description in analysis.risk_factors.items():
            print(f"   - {title}: {description}")
            
        print(f"\nRESILIENCE:")
        print(f"   - Crisis History: {analysis.historical_context_crises}")
        
        print(f"\n{'='*60}\n")