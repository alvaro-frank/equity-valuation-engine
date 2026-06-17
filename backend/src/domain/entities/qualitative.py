from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from domain.exceptions.exceptions import DomainValidationError

@dataclass(frozen=True)
class MoatSources:
    """
    Quantitative evaluation (1-5) of moat sources.
    
    Attributes:
        intangible_assets (int): Evaluation of intangible assets as a moat source.
        switching_costs (int): Evaluation of switching costs as a moat source.
        network_effect (int): Evaluation of network effects as a moat source.
        cost_advantage (int): Evaluation of cost advantage as a moat source.
        efficient_scale (int): Evaluation of efficient scale as a moat source.
    """
    intangible_assets: int
    switching_costs: int
    network_effect: int
    cost_advantage: int
    efficient_scale: int

@dataclass(frozen=True)
class QualityPillars:
    """
    Quantitative evaluation (1-5) of business quality pillars.
    
    Attributes:
        management_quality (int): Evaluation of management quality.
        business_model_resilience (int): Evaluation of business model resilience.
        pricing_power (int): Evaluation of pricing power.
        innovation_and_growth (int): Evaluation of innovation and growth.
        tam_expansion (int): Evaluation of total addressable market expansion.
    """
    management_quality: int
    business_model_resilience: int
    pricing_power: int
    innovation_and_growth: int
    tam_expansion: int

@dataclass(frozen=True)
class CompanyProfile:
    """
    Represents the company and company's business model details
    
    Attributes:
        business_description (str): Summary of the business model.
        company_history (str): Details about foundation and milestones.
        key_executives (List[Dict[str, Any]]): List of key executives (e.g. CEO, CFO, COO) with name, title, and ownership.
        revenue_model (str): Detailed explanation of how the company makes money.
        strategy (str): The company's core strategic focus.
        products_services (Dict[str, str]): Main products and services offered.
        competitive_advantage (str): Competitive advantage or MOAT analysis.
        competitors (List[Dict[str, str]]): List of main competitors in the industry.
        management_insights (str): Insights on management quality and meetings.
        risk_factors (Dict[str, str]): Main risk factors for the business.
        historical_context_crises (str): History including major crises overcome.
        moat_trajectory (str): Evidence of moat trajectory (expanding/shrinking).
        moat_sources (MoatSources): Quantitative evaluation of moat sources (1-5).
        quality_pillars (QualityPillars): Quantitative evaluation of business quality pillars (1-5).
    """
    business_description: str
    company_history: str
    key_executives: List[Dict[str, Any]]
    revenue_model: str
    strategy: str
    products_services: Dict[str, str]
    competitive_advantage: str
    competitors: List[Dict[str, str]]
    management_insights: str
    risk_factors: Dict[str, str]
    historical_context_crises: str
    moat_trajectory: str
    moat_sources: MoatSources
    quality_pillars: QualityPillars
    
    def __post_init__(self):
        for exec in self.key_executives:
            ownership = exec.get('ownership')
            if ownership is not None and (ownership < 0 or ownership > 100):
                raise DomainValidationError(f"Executive ownership must be between 0 and 100%. Got {ownership}")
    
@dataclass(frozen=True)
class IndustrySectorDynamics:
    """
    Represents the company industry and sector details
    
    Attributes:
        sector (str): The broad economic sector (e.g., Technology).
        industry (str): The specific industry classification (e.g., Consumer Electronics).
        rivalry_among_competitors (Dict[str, str]): Analysis of competition intensity and key players.
        bargaining_power_of_suppliers (Dict[str, str]): Evaluation of supplier influence on pricing.
        bargaining_power_of_customers (Dict[str, str]): Evaluation of customer influence on pricing.
        threat_of_new_entrants (Dict[str, str]): Barriers to entry for new competitors.
        threat_of_obsolescence (Dict[str, str]): Risks from technological or market shifts.
        economic_sensitivity (str): How much the business is affected by economic cycles (Cyclical vs defensive).
        interest_rate_exposure (str): Impact of interest rate fluctuations on the business model.
    """
    sector: str
    industry: str
    rivalry_among_competitors: Dict[str, str]
    bargaining_power_of_suppliers: Dict[str, str]
    bargaining_power_of_customers: Dict[str, str]
    threat_of_new_entrants: Dict[str, str]
    threat_of_obsolescence: Dict[str, str]
    economic_sensitivity: str
    interest_rate_exposure: str
