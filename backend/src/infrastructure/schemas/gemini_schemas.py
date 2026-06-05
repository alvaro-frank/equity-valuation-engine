from pydantic import BaseModel
from typing import Dict, List

class Shareholder(BaseModel):
    """
    Represents a major shareholder of the company.

    Attributes:
        name (str): The name of the individual or institutional investor.
        ownership (float): The percentage of total shares owned by the shareholder.
    """
    name: str
    ownership: float

class ProductService(BaseModel):
    """
    Represents a specific product or service offered by the company.

    Attributes:
        name (str): The official name of the product or service line.
        description (str): A brief overview of what the product/service does and its market value.
    """
    name: str
    description: str

class Competitor(BaseModel):
    """
    Details regarding a direct or indirect competitor in the market.

    Attributes:
        name (str): The name of the competing company.
        overlap (str): Description of the market segments or products where competition is most intense.
    """
    name: str
    overlap: str

class RiskFactor(BaseModel):
    """
    A specific risk that could materially affect the company's performance or operations.

    Attributes:
        title (str): The category or name of the risk (e.g., Regulatory, Supply Chain).
        description (str): Detailed explanation of the potential impact and likelihood.
    """
    title: str
    description: str

class CompanyProfileSchema(BaseModel):
    """
    Comprehensive profile and business model analysis of a specific company.

    Attributes:
        business_description (str): High-level overview of the company's core operations.
        company_history (str): Timeline and narrative of the company's evolution.
        ceo_name (str): Name of the current Chief Executive Officer.
        ceo_ownership (float): Percentage of the company owned by the CEO.
        major_shareholders (List[Shareholder]): List of entities holding significant equity stakes.
        revenue_model (str): Explanation of how the company generates income.
        strategy (str): The company's long-term strategic goals and roadmap.
        products_services (List[ProductService]): Portfolio of the company's offerings.
        competitive_advantage (str): The company's 'moat' or unique strengths (e.g., brand, scale).
        competitors (List[Competitor]): Analysis of the competitive landscape.
        management_insights (str): Evaluation of the leadership team's quality and track record.
        risk_factors (List[RiskFactor]): Identified threats to the business model.
        historical_context_crises (str): How the company handled past economic downturns or internal crises.
        moat_trajectory (str): Evidence of moat trajectory (expanding/shrinking).
    """
    business_description: str
    company_history: str
    ceo_name: str
    ceo_ownership: float
    major_shareholders: List[Shareholder]
    revenue_model: str
    strategy: str
    products_services: List[ProductService]
    competitive_advantage: str
    competitors: List[Competitor]
    management_insights: str
    risk_factors: List[RiskFactor]
    historical_context_crises: str
    moat_trajectory: str

class ForceFactor(BaseModel):
    """
    An individual analytical component of an industry force (e.g., Porter's Five Forces).

    Attributes:
        factor (str): The specific element being analyzed (e.g., Switching Costs).
        analysis (str): Qualitative evaluation of how this factor impacts the industry.
    """
    factor: str
    analysis: str

class IndustrySectorDynamicsSchema(BaseModel):
    """
    Schema for comprehensive industry and sector analysis.

    Attributes:
        sector (str): The broad economic sector (e.g., Technology).
        industry (str): The specific industry classification (e.g., Consumer Electronics).
        rivalry_among_competitors (List[ForceFactor]): Analysis of competition intensity and key players.
        bargaining_power_of_suppliers (List[ForceFactor]): Evaluation of supplier influence on pricing and terms.
        bargaining_power_of_customers (List[ForceFactor]): Evaluation of customer influence on pricing and terms.
        threat_of_new_entrants (List[ForceFactor]): Barriers to entry and threat from new market participants.
        threat_of_obsolescence (List[ForceFactor]): Risks from technological shifts or alternative products.
        economic_sensitivity (str): How much the business is affected by economic cycles (Cyclical vs defensive).
        interest_rate_exposure (str): Impact of interest rate fluctuations on the industry's profitability.
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
    Represents a financial metric with its year-over-year growth percentage.
    
    Attributes:
        amount (float): The absolute value or margin of the metric.
        yoy_growth (float): The Year-over-Year growth percentage.
    """
    amount: float
    yoy_growth: float

class CorePerformanceSchema(BaseModel):
    """
    Represents the core non-GAAP performance metrics of the company.
    
    Attributes:
        adjusted_revenue (MetricWithGrowthSchema): Adjusted Revenue with YoY growth.
        adjusted_eps (MetricWithGrowthSchema): Adjusted EPS with YoY growth.
        adjusted_gross_margin (MetricWithGrowthSchema): Adjusted Gross Margin with YoY growth.
        adjusted_operating_margin (MetricWithGrowthSchema): Adjusted Operating Margin with YoY growth.
        adjusted_net_margin (MetricWithGrowthSchema): Adjusted Net Margin with YoY growth.
        free_cash_flow (MetricWithGrowthSchema): Free Cash Flow with YoY growth.
    """
    adjusted_revenue: MetricWithGrowthSchema
    adjusted_eps: MetricWithGrowthSchema
    adjusted_gross_margin: MetricWithGrowthSchema
    adjusted_operating_margin: MetricWithGrowthSchema
    adjusted_net_margin: MetricWithGrowthSchema
    free_cash_flow: MetricWithGrowthSchema

class CapitalAllocationSchema(BaseModel):
    """
    Represents the capital allocation of the company.
    
    Attributes:
        share_buybacks (float): Amount spent on Share Buybacks.
        dividends (float): Amount spent on Dividends.
        capex_rd (float): Amount spent on CapEx/R&D.
        infrastructure_assessment (str): Assessment of infrastructure investment (accelerating/decelerating).
    """
    share_buybacks: float
    dividends: float
    capex_rd: float
    infrastructure_assessment: str

class RiskDeconstructionSchema(BaseModel):
    """
    Represents the risk deconstruction of the company.
    
    Attributes:
        macro_risks (List[str]): List of external/macro risks.
        internal_risks (List[str]): List of internal/execution risks.
    """
    macro_risks: List[str]
    internal_risks: List[str]

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