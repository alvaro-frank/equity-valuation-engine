from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from domain.entities.qualitative import SourceInfo

@dataclass(frozen=True)
class MetricWithGrowth:
    """
    Represents a financial metric extracted from an earnings report.
    
    Attributes:
        amount (Optional[Decimal]): The absolute value or margin of the metric.
        yoy_growth (Optional[Decimal]): The year-over-year growth percentage (or point difference for margins).
    """
    amount: Optional[Decimal] = None
    yoy_growth: Optional[Decimal] = None

@dataclass(frozen=True)
class CorePerformance:
    """
    Represents the core GAAP financial performance metrics of a company for a specific period.
    
    Attributes:
        revenue (MetricWithGrowth): The revenue figure and its year-over-year growth.
        eps (MetricWithGrowth): The earnings per share figure and its year-over-year growth.
        gross_margin (MetricWithGrowth): The gross margin percentage and its year-over-year change.
        operating_margin (MetricWithGrowth): The operating margin percentage and its year-over-year change.
        net_margin (MetricWithGrowth): The net margin percentage and its year-over-year change.
        free_cash_flow (MetricWithGrowth): The free cash flow figure and its year-over-year growth.
    """
    revenue: MetricWithGrowth
    eps: MetricWithGrowth
    gross_margin: MetricWithGrowth
    operating_margin: MetricWithGrowth
    net_margin: MetricWithGrowth
    free_cash_flow: MetricWithGrowth

@dataclass(frozen=True)
class CapitalAllocation:
    """
    Represents the capital allocation decisions made by the company.
    
    Attributes:
        share_buybacks (Decimal): Amount spent on share buybacks.
        dividends (Decimal): Amount spent on dividends.
        capex_rd (Decimal): Amount spent on CapEx and R&D.
        infrastructure_assessment (str): Assessment of infrastructure investment (accelerating/decelerating).
    """
    infrastructure_assessment: str
    share_buybacks: Optional[Decimal] = None
    dividends: Optional[Decimal] = None
    capex_rd: Optional[Decimal] = None

@dataclass(frozen=True)
class RiskDeconstruction:
    """
    Represents the risk deconstruction of the company.
    
    Attributes:
        macro_risks (List[str]): List of macro risks.
        internal_risks (List[str]): List of internal risks.
    """
    macro_risks: List[str]
    internal_risks: List[str]

@dataclass(frozen=True)
class EarningsReport:
    """
    Represents the comprehensive earnings report valuation of a company.
    
    Attributes:
        period_end_date (str): The end date of the fiscal period.
        core_performance (CorePerformance): Core non-GAAP performance metrics.
        capital_allocation (CapitalAllocation): Capital allocation decisions.
        forward_guidance (str): Summary of forward guidance.
        moat_trajectory_status (str): Moat trajectory status (EXPANDING, STABLE, SHRINKING).
        moat_trajectory_description (str): Evidence of moat trajectory.
        risk_deconstruction (RiskDeconstruction): Risk deconstruction.
        bottom_line (str): Brutal, concise summary of business execution.
    """
    period_end_date: str
    capital_allocation: CapitalAllocation
    forward_guidance: str
    moat_trajectory_status: str
    moat_trajectory_description: str
    risk_deconstruction: RiskDeconstruction
    bottom_line: str
    sources: Dict[str, SourceInfo]
    core_performance: Optional[CorePerformance] = None

@dataclass(frozen=True)
class TranscriptStatement:
    """
    Represents a single spoken statement by a participant during the earnings call.
    """
    speaker: str
    title: str
    content: str
    sentiment: Optional[float] = None

@dataclass(frozen=True)
class EarningsCallTranscript:
    """
    Represents the full earnings call event, aggregating all spoken statements.
    """
    ticker: str
    quarter: int
    year: int
    date: datetime
    transcripts: List[TranscriptStatement]
