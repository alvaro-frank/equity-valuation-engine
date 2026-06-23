from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Dict, List, Optional
from .core import TickerResult
from .qualitative import SourceInfoDTO

class MetricWithGrowthResult(BaseModel):
    """
    Data Transfer Object representing a financial metric extracted from an earnings report.
    YoY growth is calculated deterministically in the frontend using quantitative API data.
    """
    model_config = ConfigDict(frozen=True)
    amount: Optional[Decimal] = Field(None, description="The absolute value or margin of the metric")

class CorePerformanceResult(BaseModel):
    """
    Data Transfer Object representing the core performance metrics of the company.
    """
    model_config = ConfigDict(frozen=True)
    adjusted_revenue: MetricWithGrowthResult = Field(..., description="Adjusted Revenue with YoY growth")
    adjusted_eps: MetricWithGrowthResult = Field(..., description="Adjusted EPS with YoY growth")
    adjusted_gross_margin: MetricWithGrowthResult = Field(..., description="Adjusted Gross Margin with YoY growth")
    adjusted_operating_margin: MetricWithGrowthResult = Field(..., description="Adjusted Operating Margin with YoY growth")
    adjusted_net_margin: MetricWithGrowthResult = Field(..., description="Adjusted Net Margin with YoY growth")
    free_cash_flow: MetricWithGrowthResult = Field(..., description="Free Cash Flow with YoY growth")

class CapitalAllocationResult(BaseModel):
    """
    Data Transfer Object representing the capital allocation of the company.
    """
    model_config = ConfigDict(frozen=True)
    share_buybacks: Decimal = Field(..., description="Amount spent on Share Buybacks")
    dividends: Decimal = Field(..., description="Amount spent on Dividends")
    capex_rd: Decimal = Field(..., description="Amount spent on CapEx/R&D")
    infrastructure_assessment: str = Field(..., description="Assessment of infrastructure investment (accelerating/decelerating)")

class RiskDeconstructionResult(BaseModel):
    """
    Data Transfer Object for the risk deconstruction of the company.
    """
    model_config = ConfigDict(frozen=True)
    macro_risks: List[str] = Field(..., description="List of external/macro risks")
    internal_risks: List[str] = Field(..., description="List of internal/execution risks")

class EarningsReportResult(BaseModel):
    """
    Data Transfer Object for the comprehensive value-investing focused earnings report valuation.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult
    period_end_date: str = Field(..., description="The end date of the fiscal period")
    core_performance: CorePerformanceResult = Field(..., description="Core non-GAAP performance metrics")
    capital_allocation: CapitalAllocationResult = Field(..., description="Capital allocation and infrastructure assessment")
    forward_guidance: str = Field(..., description="Summary of forward guidance (Raise/Lower/Maintain)")
    moat_trajectory_status: str = Field(..., description="Moat trajectory status (EXPANDING, STABLE, SHRINKING)")
    moat_trajectory_description: str = Field(..., description="Evidence of moat trajectory")
    risk_deconstruction: RiskDeconstructionResult = Field(..., description="Macro and internal risk breakdown")
    bottom_line: str = Field(..., description="Brutal, concise summary of business execution")
    sources: Dict[str, SourceInfoDTO] = Field(
        ..., 
        description="Mapping of numerical citations to source document pages/sections (e.g. {'1': 'MD&A Page 15'})"
    )
