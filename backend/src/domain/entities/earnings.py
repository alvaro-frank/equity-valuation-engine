from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass(frozen=True)
class MetricWithGrowth:
    """
    Represents a financial metric extracted from an earnings report.
    
    Attributes:
        amount (Optional[Decimal]): The absolute value or margin of the metric (e.g., revenue amount, EPS value, or margin percentage).
    
    Note:
        YoY growth is calculated deterministically in the frontend using quantitative API data.
    """
    amount: Optional[Decimal] = None

@dataclass(frozen=True)
class CorePerformance:
    """
    Represents the core non-GAAP financial performance metrics of a company for a specific period.
    
    Attributes:
        adjusted_revenue (MetricWithGrowth): The adjusted revenue figure and its year-over-year growth.
        adjusted_eps (MetricWithGrowth): The adjusted earnings per share figure and its year-over-year growth.
        adjusted_gross_margin (MetricWithGrowth): The adjusted gross margin percentage and its year-over-year change.
        adjusted_operating_margin (MetricWithGrowth): The adjusted operating margin percentage and its year-over-year change.
        adjusted_net_margin (MetricWithGrowth): The adjusted net margin percentage and its year-over-year change.
        free_cash_flow (MetricWithGrowth): The free cash flow figure and its year-over-year growth.
    """
    adjusted_revenue: MetricWithGrowth
    adjusted_eps: MetricWithGrowth
    adjusted_gross_margin: MetricWithGrowth
    adjusted_operating_margin: MetricWithGrowth
    adjusted_net_margin: MetricWithGrowth
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
    share_buybacks: Decimal
    dividends: Decimal
    capex_rd: Decimal
    infrastructure_assessment: str

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
        moat_trajectory (str): Evidence of moat trajectory.
        risk_deconstruction (RiskDeconstruction): Risk deconstruction.
        bottom_line (str): Brutal, concise summary of business execution.
    """
    period_end_date: str
    core_performance: CorePerformance
    capital_allocation: CapitalAllocation
    forward_guidance: str
    moat_trajectory: str
    risk_deconstruction: RiskDeconstruction
    bottom_line: str
    sources: Dict[str, str]
