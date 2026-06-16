from pydantic import BaseModel, Field
from typing import List, Optional



class ProductService(BaseModel):
    """
    Represents a specific product or service offered by the company.
    """
    name: str
    description: str

class Competitor(BaseModel):
    """
    Details regarding a direct or indirect competitor in the market.
    """
    name: str
    ticker: str
    overlap: str

class RiskFactor(BaseModel):
    """
    A specific risk that could materially affect the company's performance or operations.
    """
    title: str
    description: str

class MoatSourcesSchema(BaseModel):
    """Quantitative evaluation (1-5) of moat sources."""
    intangible_assets: int
    switching_costs: int
    network_effect: int
    cost_advantage: int
    efficient_scale: int

class QualityPillarsSchema(BaseModel):
    """Quantitative evaluation (1-5) of business quality pillars."""
    management_quality: int
    business_model_resilience: int
    pricing_power: int
    innovation_and_growth: int
    tam_expansion: int

class KeyExecutive(BaseModel):
    """
    Details of a key executive in the company.
    """
    name: str
    title: str
    ownership: Optional[float] = None

class CompanyProfileSchema(BaseModel):
    """
    Comprehensive profile and business model analysis of a specific company.
    """
    company_history: str
    key_executives: List[KeyExecutive]
    revenue_model: str
    strategy: str
    products_services: List[ProductService]
    competitive_advantage: str
    competitors: List[Competitor]
    management_insights: str
    risk_factors: List[RiskFactor]
    historical_context_crises: str
    moat_trajectory: str
    moat_sources: MoatSourcesSchema
    quality_pillars: QualityPillarsSchema

class ForceFactor(BaseModel):
    """
    An individual analytical component of an industry force (e.g., Porter's Five Forces).
    """
    factor: str
    analysis: str

class IndustrySectorDynamicsSchema(BaseModel):
    """
    Schema for comprehensive industry and sector analysis.
    """
    sector: str
    industry: str
    rivalry_among_competitors: List[ForceFactor]
    bargaining_power_of_suppliers: List[ForceFactor]
    bargaining_power_of_customers: List[ForceFactor]
    threat_of_new_entrants: List[ForceFactor]
    threat_of_obsolescence: List[ForceFactor]
    economic_sensitivity: str
    interest_rate_exposure: str

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
    ticker: str
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