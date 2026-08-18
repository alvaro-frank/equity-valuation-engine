from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Dict, List, Any
from .core import TickerResult

class SectorPerformanceResult(BaseModel):
    """
    Data Transfer Object representing the sector performance relative to a benchmark.
    """
    company_ticker: str = Field(..., description="The ticker of the company being analyzed")
    sector: str = Field(..., description="The sector name")
    industry: str = Field(..., description="The industry name")
    sector_etf: str = Field(..., description="The Sector ETF ticker")
    industry_etf: Optional[str] = Field(None, description="The Industry ETF ticker (if available)")
    benchmark_ticker: str = Field(..., description="The benchmark ticker (e.g., SPY)")
    chart_data: List[Dict[str, Any]] = Field(..., description="Historical chart data")

class MetricYearlyResult(BaseModel):
    """
    Data Transfer Object representing the value of a specific financial metric for a given fiscal year.
    """
    model_config = ConfigDict(frozen=True)
    
    date: str = Field(..., description="Fiscal year end date")
    value: Decimal | None = Field(..., description="Value of the metric for the year")

class MetricQuarterlyResult(BaseModel):
    """
    Data Transfer Object representing the value of a specific financial metric for a given fiscal quarter.
    """
    model_config = ConfigDict(frozen=True)
    
    date: str = Field(..., description="Fiscal quarter end date")
    value: Decimal | None = Field(..., description="Value of the metric for the quarter")
    yoy_growth: Decimal | None = Field(None, description="Year-over-Year growth relative to the same quarter in the previous year")
    
class MetricAnalysisResult(BaseModel):
    """
    Data Transfer Object representing the analysis of a specific financial metric across multiple fiscal years.
    """
    model_config = ConfigDict(frozen=True)
    
    metric_name: str = Field(..., description="Name of the metric (e.g., Revenue, Net Income)")
    yearly_data: List[MetricYearlyResult] = Field(..., description="List of yearly values for the metric")
    cagr: Optional[Decimal] = Field(..., description="Compound Annual Growth Rate (CAGR) for the metric across the analysed years")

class QuantitativeValuationResult(BaseModel):
    """
    Data Transfer Object representing the results of the stock quantitative valuation analysis, including the ticker information and a dictionary of metric analyses.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult = Field(..., description="Ticker metadata and live pricing")
    metrics: Dict[str, MetricAnalysisResult] = Field(..., description="Detailed yearly analysis per metric")
    quarterly_metrics: Optional[Dict[str, List[MetricQuarterlyResult]]] = Field(default_factory=dict, description="Detailed quarterly data per metric")
