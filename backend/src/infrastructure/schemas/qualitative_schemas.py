from pydantic import BaseModel
from typing import List, Optional, Dict

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

class NearTermCatalyst(BaseModel):
    """
    Details regarding an upcoming event and its potential impact on the stock.
    """
    event: str
    impact: str

class SourceInfo(BaseModel):
    url: str
    title: str

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
    capital_allocation_strategy: str
    near_term_catalysts: List[NearTermCatalyst]
    risk_factors: List[RiskFactor]
    historical_context_crises: str
    moat_trajectory_status: str
    moat_trajectory_description: str
    moat_sources: MoatSourcesSchema
    quality_pillars: QualityPillarsSchema
    sources: Dict[str, SourceInfo] = {}

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
