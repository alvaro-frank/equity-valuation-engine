from services.quantitative_valuation_service import QuantitativeValuationService
from services.dtos import QuantitativeValuationDTO

class QuantitativeValuationController:
    """
    Controller responsible for orchestrating the stock quantitative valuation process, including fetching data from the Adapter and performing analysis using the QuantitativeValuationService.
    """
    def __init__(self, service: QuantitativeValuationService):
        """
        Initializes the controller with an injected QuantitativeValuationService.
        
        Args:
            service (QuantitativeValuationService): The service to handle the valuation logic.
        """
        self.service = service

    def run(self, ticker_symbol: str, years: int = 10):
        """
        Main method to run the quantitative valuation process for a given ticker and number of years.
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            years (int): The number of recent years to include in the analysis.
            
        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\nAnalysing: {ticker_symbol}...")
        
        try:
            result = self.service.evaluate_ticker(ticker_symbol, years=years)
            self._display_results(result)
            
        except Exception as e:
            print(f"Error: {e}")

    def _display_results(self, result: QuantitativeValuationDTO):
        """
        Nicely formats and prints the quantitative valuation results to the console.
        
        Args:
            result (QuantitativeValuationDTO): The result of the quantitative valuation analysis to display.
            
        Returns:
            None: This method prints the results directly to the console."""
        print(f"\n{'='*50}")
        print(f"REPORT: {result.ticker.name} ({result.ticker.symbol})")
        print(f"Sector: {result.ticker.sector} | Industry: {result.ticker.industry}")
        print(f"{'='*50}")

        for key, analysis in result.metrics.items():
            print(f"\nMetric: {analysis.metric_name}")
            print(f"{'Data':<15} | {'Value':>20}")
            print("-" * 40)
            
            for data_point in analysis.yearly_data:
                formatted_value = f"{data_point.value:,.2f}"
                print(f"{data_point.date:<15} | {formatted_value:>20}")
                
            if analysis.cagr is not None:
                print(f"\nCAGR ({len(analysis.yearly_data)-1} years): {analysis.cagr:>8.2f}%")
            else:
                print(f"\nCAGR: N/A (Insufficient data or zero initial value)")
            
            print("-" * 40)
        
        print(f"\n{'='*50}\n")