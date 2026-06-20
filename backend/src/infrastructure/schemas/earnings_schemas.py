from pydantic import BaseModel, Field
from typing import List, Optional

class MetricWithGrowthSchema(BaseModel):
    """
    Represents a financial metric extracted from an earnings report.
    YoY growth is calculated deterministically in the frontend using quantitative API data.
    """
    amount: Optional[float] = None

class CorePerformanceSchema(BaseModel):
    """
    Represents the core non-GAAP performance metrics of the company.
    """
    adjusted_revenue: Optional[MetricWithGrowthSchema] = None
    adjusted_eps: Optional[MetricWithGrowthSchema] = None
    adjusted_gross_margin: Optional[MetricWithGrowthSchema] = None
    adjusted_operating_margin: Optional[MetricWithGrowthSchema] = None
    adjusted_net_margin: Optional[MetricWithGrowthSchema] = None
    free_cash_flow: Optional[MetricWithGrowthSchema] = None

class CapitalAllocationSchema(BaseModel):
    """
    Represents the capital allocation of the company.
    """
    share_buybacks: float
    dividends: float
    capex_rd: float
    infrastructure_assessment: str

class RiskDeconstructionSchema(BaseModel):
    """
    Represents the risk deconstruction of the company.
    """
    macro_risks: List[str]
    internal_risks: List[str]

class SourceCitation(BaseModel):
    """
    A specific citation source.
    """
    citation_number: int
    source_text: str

class EarningsReportSchema(BaseModel):
    """
    Schema for earnings report analysis focused on Value Investing.
    """
    period_end_date: str
    core_performance: CorePerformanceSchema
    capital_allocation: CapitalAllocationSchema
    forward_guidance: str
    moat_trajectory: str
    risk_deconstruction: RiskDeconstructionSchema
    bottom_line: str
    sources: List[SourceCitation] = Field(
        ..., 
        description="List of numerical citations used in the text and their source document section or page"
    )
