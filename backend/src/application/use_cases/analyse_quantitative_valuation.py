from domain.ports import QuantitativeDataProvider
from domain.entities import FinancialYear, QuantitativeAnalysis, MetricPoint
from application.dtos.dtos import TickerDTO, MetricYearlyDTO, MetricAnalysisDTO, QuantitativeValuationDTO
from dataclasses import fields

class QuantitativeValuationUseCase:
    """
    Service responsible for performing stock quantitative valuation analysis based on the provided stock data, including financial metrics across multiple fiscal years.
    This service takes in a Stock Entity, analyses the financial metrics for a specified number of recent years, and returns a DTO containing all information about the Quantitative data of the business.
    """
    def __init__(self, adapter: QuantitativeDataProvider):
        """
        Initializes the QuantitativeValuationUseCase with the QuantitativeDataProvider to fetch fundamental business data.
        """
        self.adapter = adapter
        
    def evaluate_ticker(self, ticker_symbol: str, years: int = 5) -> QuantitativeValuationDTO:
        """
        Performs a full quantitative evaluation of a stock by fetching its data and analyzing 
        core financial metrics over a rolling window of years.

        Args:
            ticker_symbol (str): The stock market ticker symbol (e.g., 'AAPL').
            years (int): The number of recent fiscal years to include in the trend analysis. 
                         Defaults to 5.

        Returns:
            QuantitativeValuationDTO: a DTO containing all information about the Quantitative data of the business.
        """
        ticker = self.adapter.get_ticker_info(ticker_symbol)
        stock_data = self.adapter.get_stock_fundamental_data(ticker_symbol)
        
        all_fields = [f.name for f in fields(FinancialYear)]
        excluded_fields = ["fiscal_date_ending"]
        
        metrics_to_analyse = [f for f in all_fields if f not in excluded_fields]

        analyses_entities = [
            self._analyse_metric(stock_data.financial_years, metric, years)
            for metric in metrics_to_analyse
        ]
        
        ticker_dto = TickerDTO(
            symbol=ticker.symbol,
            name=ticker.name,
            sector=ticker.sector,
            industry=ticker.industry
        )
        
        metrics_dtos = {}
        for analysis in analyses_entities:
            yearly_dtos = [
                MetricYearlyDTO(date=p.date, value=p.value) 
                for p in analysis.yearly_data
            ]
            
            metrics_dtos[analysis.metric_name.lower()] = MetricAnalysisDTO(
                metric_name=analysis.metric_name,
                yearly_data=yearly_dtos,
                cagr=analysis.cagr
            )

        return QuantitativeValuationDTO(ticker=ticker_dto, metrics=metrics_dtos)
        
    def _analyse_metric(self, financial_years, field_name: str, years: int) -> QuantitativeAnalysis:
        """
        Extracts a specific financial metric from the historical data and encapsulates it 
        into a QuantitativeAnalysis object.

        Args:
            financial_years (List[FinancialYear]): The raw historical financial data.
            field_name (str): The name of the attribute to extract from each FinancialYear.
            years (int): The maximum number of years to extract, starting from the most recent.

        Returns:
            QuantitativeAnalysis: An object containing the time-series data (MetricPoints) 
                                  and the derived growth metrics (CAGR).
        """
        points = [
            MetricPoint(date=fy.fiscal_date_ending, value=getattr(fy, field_name))
            for fy in financial_years[:years]
        ]

        return QuantitativeAnalysis.create_analysis(field_name.replace("_", " ").title(), points)