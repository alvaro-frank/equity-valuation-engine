from decimal import Decimal
from typing import List
from services.dtos import StockDataDTO, ValuationResultDTO, MetricAnalysisDTO, MetricYearlyDTO, FinancialYearDTO

class ValuationService:
    def evaluate_stock(self, stock_dto: StockDataDTO, years_to_analyze: int = 5) -> ValuationResultDTO:
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
        yearly_data = []

        for yr in years:
            current_value = getattr(yr, field_name, Decimal("0"))
            
            yearly_data.append(MetricYearlyDTO(
                date=yr.fiscal_date_ending,
                value=current_value
            ))

        return MetricAnalysisDTO(
            metric_name=field_name.replace("_", " ").title(),
            yearly_data=yearly_data,
        )