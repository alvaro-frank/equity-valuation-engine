from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass(frozen=True)
class Price:
    """
    Represents the current price of a stock, including the amount and currency.
    
    Attributes:
        amount (Decimal): The price amount.
        currency (str): The currency of the price (e.g., USD).
    """
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError(f"Domain Error: Price amount cannot be negative. Got {self.amount}")
        
    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"
 
@dataclass(frozen=True)
class Ticker:
    """
    Represents the ticker information of a stock, including symbol, name, sector, and industry.
    
    Attributes:
        symbol (str): The stock ticker symbol (e.g., AAPL).
        name (str): The company name associated with the ticker.
        sector (str): The sector in which the company operates.
        industry (str): The industry classification of the company.
        market_cap (Decimal | None): The current, live market capitalization of the company.
        pe_ratio (Decimal | None): The current, live Price-to-Earnings ratio.
        forward_pe (Decimal | None): The forecasted Forward Price-to-Earnings ratio.
        current_price (Decimal | None): The current, live stock price.
        business_description (str | None): Long description of the business.
        profit_margins (Decimal | None): Profit margin ratio.
        revenue_growth (Decimal | None): Revenue growth ratio.
        company_officers (List[Dict[str, Any]]): List of company officers with name and title.
    """
    symbol: str
    name: str = ""
    sector: str = "Unknown"
    sector_key: str | None = None
    industry: str = "Unknown"
    industry_key: str | None = None
    market_cap: Decimal | None = None
    pe_ratio: Decimal | None = None
    forward_pe: Decimal | None = None
    current_price: Decimal | None = None
    regular_market_change: Decimal | None = None
    regular_market_change_percent: Decimal | None = None
    business_description: str | None = None
    profit_margins: Decimal | None = None
    revenue_growth: Decimal | None = None
    company_officers: List[Dict[str, Any]] = field(default_factory=list)
        
    def __str__(self):
        return f"{self.symbol} - {self.name} ({self.sector}/{self.industry})"

@dataclass(frozen=True)
class BaseFinancialPeriod:
    """
    Base class representing the financial data for a specific fiscal period.
    Contains all shared metrics and properties between Years and Quarters.
    """
    fiscal_date_ending: str
    
    revenue: Decimal
    ebitda: Decimal
    
    gross_profit: Decimal
    operating_income: Decimal
    net_income: Decimal
    
    operating_cash_flow: Decimal
    capital_expenditures: Decimal
    
    shares_outstanding: Decimal
    
    short_term_debt: Decimal
    long_term_debt: Decimal
    total_debt: Decimal
    
    accounts_payable: Decimal
    current_liabilities: Decimal
    total_liabilities: Decimal
    
    cash_and_equivalents: Decimal
    accounts_receivable: Decimal
    inventory: Decimal
    current_assets: Decimal
    net_ppe: Decimal
    intangible_assets: Decimal
    total_assets: Decimal
    
    depreciation_and_amortization: Decimal | None = None
    stock_based_compensation: Decimal | None = None
    net_investing_cash_flow: Decimal | None = None
    dividends_paid: Decimal | None = None
    stock_repurchases: Decimal | None = None
    net_debt_issued: Decimal | None = None
    net_financing_cash_flow: Decimal | None = None
    
    def __post_init__(self):
        if self.shares_outstanding < 0:
            raise ValueError(f"Domain Error: Shares outstanding cannot be negative. Got {self.shares_outstanding}")
        if self.total_assets < 0:
            raise ValueError(f"Domain Error: Total assets cannot be negative. Got {self.total_assets}")
        if self.total_debt < 0:
            raise ValueError(f"Domain Error: Total debt cannot be negative. Got {self.total_debt}")

    @property
    def period_end_price(self) -> Decimal:
        """To be implemented by subclasses"""
        raise NotImplementedError

    @property
    def total_equity(self) -> Decimal:
        return self.total_assets - self.total_liabilities

    @property
    def gross_margin(self) -> Decimal | None:
        if self.revenue == Decimal("0"):
            return None
        return round((self.gross_profit / self.revenue) * 100, 2)

    @property
    def operating_margin(self) -> Decimal | None:
        if self.revenue == Decimal("0"):
            return None
        return round((self.operating_income / self.revenue) * 100, 2)

    @property
    def net_margin(self) -> Decimal | None:
        if self.revenue == Decimal("0"):
            return None
        return round((self.net_income / self.revenue) * 100, 2)

    @property
    def roe(self) -> Decimal | None:
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round((self.net_income / equity) * 100, 2)

    @property
    def roic(self) -> Decimal | None:
        invested_capital = self.total_debt + self.total_equity
        if invested_capital <= Decimal("0"):
            return None
        return round((self.net_income / invested_capital) * 100, 2)

    @property
    def debt_to_equity(self) -> Decimal | None:
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round(self.total_debt / equity, 2)

    @property
    def market_cap(self) -> Decimal:
        return self.shares_outstanding * self.period_end_price

    @property
    def pe_ratio(self) -> Decimal | None:
        if self.net_income <= Decimal("0"):
            return None
        return round(self.market_cap / self.net_income, 2)

    @property
    def current_ratio(self) -> Decimal | None:
        if self.current_liabilities <= Decimal("0"):
            return None
        return round(self.current_assets / self.current_liabilities, 2)

    @property
    def enterprise_value(self) -> Decimal:
        return self.market_cap + self.total_debt - self.cash_and_equivalents

    @property
    def ev_to_ebitda(self) -> Decimal | None:
        if self.ebitda <= Decimal("0"):
            return None
        return round(self.enterprise_value / self.ebitda, 2)

    @property
    def pb_ratio(self) -> Decimal | None:
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round(self.market_cap / equity, 2)

    @property
    def ps_ratio(self) -> Decimal | None:
        if self.revenue <= Decimal("0"):
            return None
        return round(self.market_cap / self.revenue, 2)

    @property
    def free_cash_flow(self) -> Decimal:
        return self.operating_cash_flow - abs(self.capital_expenditures)

    @property
    def fcf_yield(self) -> Decimal | None:
        if self.market_cap == Decimal("0"):
            return None
        fcf = self.operating_cash_flow - abs(self.capital_expenditures)
        return round((fcf / self.market_cap) * 100, 2)

    @property
    def eps(self) -> Decimal | None:
        if self.shares_outstanding == Decimal("0"):
            return None
        return round(self.net_income / self.shares_outstanding, 2)

@dataclass(frozen=True)
class FinancialYear(BaseFinancialPeriod):
    """Represents the financial data for a specific fiscal year."""
    year_end_price: Decimal = Decimal("0")

    @property
    def period_end_price(self) -> Decimal:
        return self.year_end_price

@dataclass(frozen=True)
class FinancialQuarter(BaseFinancialPeriod):
    """Represents the financial data for a specific fiscal quarter."""
    quarter_end_price: Decimal = Decimal("0")

    @property
    def period_end_price(self) -> Decimal:
        return self.quarter_end_price

    @property
    def roic(self) -> Decimal | None:
        """Override ROIC to use NOPAT for quarters."""
        invested_capital = self.total_assets - self.total_liabilities + self.short_term_debt + self.long_term_debt - self.cash_and_equivalents
        if invested_capital == Decimal("0"):
            return None
        nopat = self.operating_income * Decimal("0.8") # Assumes 20% tax rate
        return round((nopat / invested_capital) * 100, 2)

@dataclass(frozen=True)
class MetricWithGrowth:
    """
    Represents a financial metric with its corresponding Year-over-Year (YoY) growth.
    
    Attributes:
        amount (Optional[Decimal]): The absolute value or margin of the metric (e.g., revenue amount, EPS value, or margin percentage).
        yoy_growth (Optional[Decimal]): The year-over-year growth percentage.
    """
    amount: Optional[Decimal] = None
    yoy_growth: Optional[Decimal] = None

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
    
@dataclass(frozen=True)
class MoatSources:
    """Quantitative evaluation (1-5) of moat sources."""
    intangible_assets: int
    switching_costs: int
    network_effect: int
    cost_advantage: int
    efficient_scale: int

@dataclass(frozen=True)
class QualityPillars:
    """Quantitative evaluation (1-5) of business quality pillars."""
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
        competitors (Dict[str, str]): Main competitors in the industry.
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
    competitors: Dict[str, str]
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
                raise ValueError(f"Domain Error: Executive ownership must be between 0 and 100%. Got {ownership}")
    
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