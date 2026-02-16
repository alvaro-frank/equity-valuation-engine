from decimal import Decimal
from typing import List
from services.dtos import StockDataDTO, ValuationResultDTO, MetricAnalysisDTO, MetricYearlyDTO, FinancialYearDTO

class ValuationService:
    """
    Service responsible for performing stock valuation analysis based on the provided stock data, including financial metrics across multiple fiscal years.
    This service takes in a StockDataDTO, analyzes the financial metrics for a specified number of recent years, and returns a ValuationResultDTO containing the analysis results.
    """
    def evaluate_stock(self, stock_dto: StockDataDTO, years_to_analyze: int = 5) -> ValuationResultDTO:
        """
        Evaluates the stock's financial data and performs analysis on key metrics for a specified number of recent years.
        
        Args:
            stock_dto (StockDataDTO): The data transfer object containing the stock's fundamental data, including financial years and current price.
            years_to_analyze (int): The number of recent fiscal years to include in the analysis (default is 5).
            
        Returns:
            ValuationResultDTO: The result of the valuation analysis.
        """
        all_fields = list(FinancialYearDTO.model_fields.keys())
        excluded_fields = ["fiscal_date_ending"]
        all_years = sorted(stock_dto.financial_years, key=lambda x: x.fiscal_date_ending)
        analysis_years = all_years[-years_to_analyze:]
        
        metrics_to_check = [f for f in all_fields if f not in excluded_fields]
        analysis_map = {}

        for field in metrics_to_check:
            analysis = self._analyze_specific_metric(analysis_years, field)
            analysis_map[field] = analysis

        return ValuationResultDTO(
            ticker=stock_dto.ticker,
            metrics=analysis_map
        )

    def _analyze_specific_metric(self, years: List, field_name: str) -> MetricAnalysisDTO:
        """
        Analyzes a specific financial metric across multiple fiscal years and prepares the data for presentation.
        
        Args:
            years (List[FinancialYearDTO]): The list of financial years to analyze.
            field_name (str): The name of the financial metric field to analyze (e.g., "revenue", "net_income").
            
        Returns:
            MetricAnalysisDTO: The analysis of the specified metric across the given years.
        """
        yearly_data = []

        for yr in years:
            current_value = getattr(yr, field_name, Decimal("0"))
            
            yearly_data.append(MetricYearlyDTO(
                date=yr.fiscal_date_ending,
                value=current_value
            ))
            
        cagr = None
        if len(years) >= 2:
            begin_val = getattr(years[0], field_name, Decimal("0"))
            end_val = getattr(years[-1], field_name, Decimal("0"))
            t = len(years) - 1

            if begin_val > 0:
                ratio = float(end_val / begin_val)
                if ratio > 0:
                    cagr_val = (pow(ratio, (1 / t)) - 1) * 100
                    cagr = Decimal(str(round(cagr_val, 2)))

        return MetricAnalysisDTO(
            metric_name=field_name.replace("_", " ").title(),
            yearly_data=yearly_data,
            cagr=cagr if cagr is not None else Decimal("0")
        )