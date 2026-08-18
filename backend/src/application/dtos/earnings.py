from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Dict, List, Optional
from datetime import datetime
from .core import TickerResult
from .qualitative import SourceInfoDTO

class MetricWithGrowthResult(BaseModel):
    """
    Data Transfer Object representing a financial metric extracted from an earnings report.
    """
    model_config = ConfigDict(frozen=True)
    amount: Optional[Decimal] = Field(None, description="The absolute value or margin of the metric")
    yoy_growth: Optional[Decimal] = Field(None, description="The YoY growth percentage or point difference")

class CorePerformanceResult(BaseModel):
    """
    Data Transfer Object representing the core performance metrics of the company.
    """
    model_config = ConfigDict(frozen=True)
    revenue: MetricWithGrowthResult = Field(..., description="Revenue with YoY growth")
    eps: MetricWithGrowthResult = Field(..., description="EPS with YoY growth")
    gross_margin: MetricWithGrowthResult = Field(..., description="Gross Margin with YoY growth")
    operating_margin: MetricWithGrowthResult = Field(..., description="Operating Margin with YoY growth")
    net_margin: MetricWithGrowthResult = Field(..., description="Net Margin with YoY growth")
    free_cash_flow: MetricWithGrowthResult = Field(..., description="Free Cash Flow with YoY growth")

class CapitalAllocationResult(BaseModel):
    """
    Data Transfer Object representing the capital allocation of the company.
    """
    model_config = ConfigDict(frozen=True)
    share_buybacks: Optional[Decimal] = Field(None, description="Amount spent on Share Buybacks")
    dividends: Optional[Decimal] = Field(None, description="Amount spent on Dividends")
    capex_rd: Optional[Decimal] = Field(None, description="Amount spent on CapEx/R&D")
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
    Data Transfer Object representing the analysis of an earnings report, including performance, guidance, management tone, and specific value investing metrics.
    """
    model_config = ConfigDict(frozen=True)
    
    sources: Dict[str, SourceInfoDTO] = Field(
        ..., 
        description="Mapping of numerical citations to source document pages/sections and exact quotes"
    )
    ticker: TickerResult
    period_end_date: str = Field(..., description="The end date of the fiscal period")
    core_performance: Optional[CorePerformanceResult] = Field(None, description="Core non-GAAP performance metrics")
    capital_allocation: CapitalAllocationResult = Field(..., description="Capital allocation and infrastructure assessment")
    forward_guidance: str = Field(..., description="Summary of forward guidance (Raise/Lower/Maintain)")
    moat_trajectory_status: str = Field(..., description="Moat trajectory status (EXPANDING, STABLE, SHRINKING)")
    moat_trajectory_description: str = Field(..., description="Evidence of moat trajectory")
    risk_deconstruction: RiskDeconstructionResult = Field(..., description="Macro and internal risk breakdown")
    bottom_line: str = Field(..., description="Brutal, concise summary of business execution")
    transcript: Optional[List['TranscriptStatementResult']] = Field(None, description="The full earnings call transcript")

class TranscriptStatementResult(BaseModel):
    """
    DTO for a single spoken statement by a participant during the earnings call.
    """
    speaker: str
    title: str
    content: str
    sentiment: Optional[float] = None

class EarningsCallTranscriptResult(BaseModel):
    """
    DTO for the full earnings call transcript.
    """
    ticker: str
    quarter: int
    year: int
    date: datetime
    transcripts: List[TranscriptStatementResult]
