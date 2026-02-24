from services.quantitative_valuation_service import QuantitativeValuationService
from dtos.dtos import QuantitativeValuationDTO, MetricAnalysisDTO, TickerDTO, MetricYearlyDTO

class QuantitativeValuationController:
    """
    Controller responsible for orchestrating the stock quantitative valuation process performing analysis using the QuantitativeValuationService.
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
            None: This method creates the QuantitativeValuationDTO.
        """
        try:
            ticker_entity, analyses_entities = self.service.evaluate_ticker(ticker_symbol, years)

            ticker_dto = TickerDTO(
                symbol=ticker_entity.symbol,
                name=ticker_entity.name,
                sector=ticker_entity.sector,
                industry=ticker_entity.industry
            )

            metrics_dtos = {}
            for analysis in analyses_entities:
                metrics_dtos[analysis.metric_name.lower()] = MetricAnalysisDTO(
                    metric_name=analysis.metric_name,
                    yearly_data=[MetricYearlyDTO(date=p.date, value=p.value) for p in analysis.yearly_data],
                    cagr=analysis.cagr
                )

            final_dto = QuantitativeValuationDTO(ticker=ticker_dto, metrics=metrics_dtos)

            self._display_results(final_dto)

        except Exception as e:
            print(f"Error: {e}")

    def _display_results(self, result: QuantitativeValuationDTO):
        """
        Nicely formats and prints the quantitative valuation results to the console.
        
        Args:
            result (QuantitativeValuationDTO): The result of the quantitative valuation analysis to display.
            
        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\n{'='*50}")
        print(f"REPORT: {result.ticker.name} ({result.ticker.symbol})")
        print(f"Sector: {result.ticker.sector} | Industry: {result.ticker.industry}")
        print(f"{'='*50}")

        for analysis in result.metrics.values():
            print(f"\nMetric: {analysis.metric_name}")
            print(f"{'Date':<15} | {'Value':>20}")
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