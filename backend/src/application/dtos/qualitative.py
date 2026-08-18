from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Dict, List, Any, Optional
from .core import TickerResult

class MoatSourcesResult(BaseModel):
    """
    Data Transfer Object representing the evaluation of different moat sources.
    """
    intangible_assets: int = Field(..., description="Score 1-5 for Intangible Assets")
    switching_costs: int = Field(..., description="Score 1-5 for Switching Costs")
    network_effect: int = Field(..., description="Score 1-5 for Network Effect")
    cost_advantage: int = Field(..., description="Score 1-5 for Cost Advantage")
    efficient_scale: int = Field(..., description="Score 1-5 for Efficient Scale")

class QualityPillarsResult(BaseModel):
    """
    Data Transfer Object representing the evaluation of different quality pillars.
    """
    management_quality: int = Field(..., description="Score 1-5 for Management Quality")
    business_model_resilience: int = Field(..., description="Score 1-5 for Business Model Resilience")
    pricing_power: int = Field(..., description="Score 1-5 for Pricing Power")
    innovation_and_growth: int = Field(..., description="Score 1-5 for Innovation and Growth")
    tam_expansion: int = Field(..., description="Score 1-5 for TAM Expansion")

class SourceInfoDTO(BaseModel):
    """
    Data Transfer Object representing information about a source used in the research.
    """
    source_name: Optional[str] = None
    exact_quote: str

class NearTermCatalystDTO(BaseModel):
    """
    Data Transfer Object representing a near-term catalyst.
    """
    event: str
    impact: str

class QualitativeValuationResult(BaseModel):
    """
    Data Transfer Object representing the stock qualitative valuation analysis, including the ticker information, business description and company history.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult
    business_description: str = Field(..., description="Description of business operations")
    company_history: str = Field(None, description="History of company foundation and evolution")
    key_executives: List[Dict[str, Any]] = Field(..., description="List of key executives with name and title")
    major_shareholders: Dict[str, Decimal] = Field(..., description="Shareholder name mapping to their ownership type/stakes")
    revenue_model: str = Field(..., description="Detailed explanation of how the company makes money")
    strategy: str = Field(..., description="The company's core strategic focus")
    products_services: Dict[str, str] = Field(..., description="Product name mapping to its function")
    competitive_advantage: str = Field(..., description="Competitive advantage or MOAT analysis")
    competitors: List[Dict[str, str]] = Field(..., description="List of competitors with name, ticker, and competitive overlap")
    management_insights: str = Field(..., description="Insights on management quality and meetings")
    capital_allocation_strategy: str = Field("", description="Detailed analysis of how management deploys Free Cash Flow")
    near_term_catalysts: List[NearTermCatalystDTO] = Field(default_factory=list, description="Upcoming events that could re-rate the stock")
    risk_factors: Dict[str, str] = Field(..., description="Risk title mapping to detailed description")
    historical_context_crises: str = Field(..., description="History including major crises overcome")
    moat_trajectory_status: str = Field(..., description="Moat trajectory status (EXPANDING, STABLE, SHRINKING)")
    moat_trajectory_description: str = Field(..., description="Detailed analysis of the moat trajectory")
    moat_sources: MoatSourcesResult = Field(..., description="Quantitative evaluation of moat sources (1-5)")
    quality_pillars: QualityPillarsResult = Field(..., description="Quantitative evaluation of business quality pillars (1-5)")
    sources: Dict[str, SourceInfoDTO] = Field(default_factory=dict, description="Google Search citation mapping")

class SectorIndustrialValuationResult(BaseModel):
    """
    Data Transfer Object representing the sector and industry valuation analysis, including the ticker information, sector and industry names, and Porter's Five Forces analysis.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult
    sector: str = Field(..., description="The broad sector name")
    industry: str = Field(..., description="The specific industry name")
    rivalry_among_competitors: Dict[str, str] = Field(..., description="Analysis of intensity of competition")
    bargaining_power_of_suppliers: Dict[str, str] = Field(..., description="Analysis of supplier leverage")
    bargaining_power_of_customers: Dict[str, str] = Field(..., description="Analysis of customer leverage")
    threat_of_new_entrants: Dict[str, str] = Field(..., description="Barriers to entry and new competition")
    threat_of_obsolescence: Dict[str, str] = Field(..., description="Risk of technological or market displacement")
    economic_sensitivity: str = Field(..., description="How the industry reacts to economic cycles")
    interest_rate_exposure: str = Field(..., description="Impact of interest rate fluctuations on the sector")
    sources: Dict[str, SourceInfoDTO] = Field(default_factory=dict, description="Sources used in the analysis")
