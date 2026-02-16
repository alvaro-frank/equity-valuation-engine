from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from services.valuation_service import ValuationService
from services.dtos import ValuationResultDTO

class ValuationController:
    def __init__(self):
        self.adapter = AlphaVantageAdapter()
        self.service = ValuationService()

    def run(self, ticker_symbol: str, years: int = 10):
        print(f"\nAnalysing: {ticker_symbol}...")
        
        try:
            stock_data = self.adapter.get_stock_fundamental_data(ticker_symbol)
            
            result = self.service.evaluate_stock(stock_data, years_to_analyze=years)
            
            self._display_results(result)
            
        except Exception as e:
            print(f"Error: {e}")

    def _display_results(self, result: ValuationResultDTO):
        print(f"\n{'='*50}")
        print(f"REPORT: {result.ticker.name} ({result.ticker.symbol})")
        print(f"Sector: {result.ticker.sector} | Industry: {result.ticker.industry}")
        print(f"{'='*50}")

        for key, analysis in result.metrics.items():
            print(f"\n📊 Metric: {analysis.metric_name}")
            print(f"{'Data':<15} | {'Value':>20}")
            print("-" * 40)
            
            for data_point in analysis.yearly_data:
                formatted_value = f"{data_point.value:,.2f}"
                print(f"{data_point.date:<15} | {formatted_value:>20}")
        
        print(f"\n{'='*50}\n")