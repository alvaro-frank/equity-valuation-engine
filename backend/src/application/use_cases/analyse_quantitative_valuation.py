from application.ports.ports import QuantitativeDataPort
from domain.entities.entities import FinancialYear
from application.dtos.dtos import TickerResult, MetricYearlyResult, MetricAnalysisResult, QuantitativeValuationResult
from dataclasses import fields
from decimal import Decimal
from typing import List

class QuantitativeValuationUseCase:
    """
    Service responsible for performing stock quantitative valuation analysis based on the provided stock data, including financial metrics across multiple fiscal years.
    This service takes in a List of Financial Years, analyses the financial metrics for a specified number of recent years, and returns a DTO containing all information about the Quantitative data of the business.
    """
    def __init__(self, adapter: QuantitativeDataPort):
        """
        Initializes the QuantitativeValuationUseCase with the QuantitativeDataPort to fetch fundamental business data.
        """
        self.adapter = adapter
        
    def evaluate_ticker(self, ticker_symbol: str, years: int = 5) -> QuantitativeValuationResult:
        """
        Performs a full quantitative evaluation of a stock by fetching its data and analyzing 
        core financial metrics over a rolling window of years.

        Args:
            ticker_symbol (str): The stock market ticker symbol (e.g., 'AAPL').
            years (int): The number of recent fiscal years to include in the trend analysis. 
                         Defaults to 5.

        Returns:
            QuantitativeValuationResult: a DTO containing all information about the Quantitative data of the business.
        """
        ticker = self.adapter.get_ticker_info(ticker_symbol)
        financial_years = self.adapter.get_stock_fundamental_data(ticker_symbol)
        
        all_fields = [f.name for f in fields(FinancialYear)]
        excluded_fields = ["fiscal_date_ending"]
        
        ratio_fields = [
            "total_equity", "gross_margin", "operating_margin", 
            "net_margin", "roe", "roic", "debt_to_equity"
        ]
        
        metrics_to_analyse = [f for f in all_fields if f not in excluded_fields] + ratio_fields
        
        ticker_dto = TickerResult(
            symbol=ticker.symbol,
            name=ticker.name,
            sector=ticker.sector,
            industry=ticker.industry
        )
        
        metrics_dtos = {}
        for metric in metrics_to_analyse:
            yearly_dtos = []
            raw_values = []
            
            for fy in financial_years[:years]:
                val = getattr(fy, metric)
                yearly_dtos.append(MetricYearlyResult(date=fy.fiscal_date_ending, value=val))
                raw_values.append(val)
                
            cagr = self.calculate_cagr(raw_values)
            
            formatted_name = metric.replace("_", " ").title()
            
            metrics_dtos[metric] = MetricAnalysisResult(
                metric_name=formatted_name,
                yearly_data=yearly_dtos,
                cagr=cagr
            )

        return QuantitativeValuationResult(ticker=ticker_dto, metrics=metrics_dtos)
    
    @staticmethod
    def calculate_cagr(values: List[Decimal]) -> Decimal | None:
        """
        
        """
        if len(values) < 2:
            return None
            
        begin_val = values[-1]
        end_val = values[0]
        
        if begin_val <= 0 or end_val <= 0:
            return None
        
        periods = len(values) - 1
        
        try:
            cagr = ((end_val / begin_val) ** (Decimal(1) / Decimal(periods)) - 1) * 100
            return round(cagr, 2)
        except Exception:
            return None