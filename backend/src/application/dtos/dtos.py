from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Dict, List

class TickerSearchResult(BaseModel):
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    exchange: str = Field(..., description="Exchange name")

class TickerSearchResponse(BaseModel):
    results: List[TickerSearchResult] = Field(..., description="List of search results")

class TrendingTickerDTO(BaseModel):
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    rating: Optional[str] = Field(None, description="Analyst rating")
    weight: Optional[float] = Field(None, description="Market weight in sector/industry")

class TrendingTickersResponse(BaseModel):
    results: List[TrendingTickerDTO] = Field(..., description="List of trending tickers")

class TickerResult(BaseModel):
    """
    Data Transfer Object representing the ticker information of a stock, including symbol, name, sector, and industry.
    
    Attributes:
        symbol (str): The stock ticker symbol (e.g., AAPL).
        name (str): The company name associated with the ticker.
        sector (str): The sector in which the company operates.
        industry (str): The industry classification of the company.
    """
    model_config = ConfigDict(frozen=True)
    
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    sector: str = Field(..., description="Company sector")
    sector_key: Optional[str] = Field(None, description="yfinance sector key")
    industry: str = Field(..., description="Company industry")
    industry_key: Optional[str] = Field(None, description="yfinance industry key")
    market_cap: Optional[Decimal] = Field(None, description="Current market capitalization")
    pe_ratio: Optional[Decimal] = Field(None, description="Live Price-to-Earnings Ratio")
    forward_pe: Optional[Decimal] = Field(None, description="Forward Price-to-Earnings Ratio")
    current_price: Optional[Decimal] = Field(None, description="Live Stock Price")
    regular_market_change: Optional[Decimal] = Field(None, description="Live Market Price Change")
    regular_market_change_percent: Optional[Decimal] = Field(None, description="Live Market Price Change Percentage")

class MetricYearlyResult(BaseModel):
    """
    Data Transfer Object representing the value of a specific financial metric for a given fiscal year.
    
    Attributes:
        date (str): The fiscal year end date.
        value (Decimal): The value of the metric for that year.
    """
    model_config = ConfigDict(frozen=True)
    
    date: str = Field(..., description="Fiscal year end date")
    value: Decimal | None = Field(..., description="Value of the metric for the year")

class MetricQuarterlyResult(BaseModel):
    """
    Data Transfer Object representing the value of a specific financial metric for a given fiscal quarter.
    
    Attributes:
        date (str): The fiscal quarter end date.
        value (Decimal): The value of the metric for that quarter.
    """
    model_config = ConfigDict(frozen=True)
    
    date: str = Field(..., description="Fiscal quarter end date")
    value: Decimal | None = Field(..., description="Value of the metric for the quarter")
    
class MetricAnalysisResult(BaseModel):
    """
    Data Transfer Object representing the analysis of a specific financial metric across multiple fiscal years.
    
    Attributes:
        metric_name (str): The name of the financial metric being analysed (e.g., Revenue, Net Income).
        yearly_data (List[MetricYearlyResult]): A list of the metric's values for each fiscal year analysed.
        cagr (Decimal): The Compound Annual Growth Rate (CAGR) for the metric across the analysed years, expressed as a percentage.
    """
    model_config = ConfigDict(frozen=True)
    
    metric_name: str = Field(..., description="Name of the metric (e.g., Revenue, Net Income)")
    yearly_data: List[MetricYearlyResult] = Field(..., description="List of yearly values for the metric")
    cagr: Optional[Decimal] = Field(..., description="Compound Annual Growth Rate (CAGR) for the metric across the analysed years")

class QuantitativeValuationResult(BaseModel):
    """
    Data Transfer Object representing the results of the stock quantitative valuation analysis, including the ticker information and a dictionary of metric analyses.
    
    Attributes:
        ticker (TickerResult): Ticker information of the stock.
        metrics (Dict[str, MetricAnalysisResult]): A dictionary where the key is the metric name and the value is the analysis of that metric across years.
        quarterly_metrics (Dict[str, List[MetricQuarterlyResult]]): A dictionary where the key is the metric name and the value is a list of quarterly results.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult = Field(..., description="Ticker metadata and live pricing")
    metrics: Dict[str, MetricAnalysisResult] = Field(..., description="Detailed yearly analysis per metric")
    quarterly_metrics: Optional[Dict[str, List[MetricQuarterlyResult]]] = Field(default_factory=dict, description="Detailed quarterly data per metric")

class QualitativeValuationResult(BaseModel):
    """
    Data Transfer Object representing the stock qualitative valuation analysis, including the ticker information, business description and company history.
    
    Attributes:
        ticker (str): Ticker symbol.
        business_description (str): Summary of the business model.
        company_history (str): Details about foundation and milestones.
        ceo_name (str): Name of the current CEO.
        ceo_ownership (Decimal): Percentage of shares owned by the CEO.
        major_shareholders (Dict[str, Decimal]): List of top major shareholders.
        revenue_model (str): Detailed explanation of how the company makes money.
        strategy (str): The company's core strategic focus.
        products_services (Dict[str, str]): Main products and services offered.
        competitive_advantage (str): Competitive advantage or MOAT analysis.
        competitors (Dict[str, str]): Main competitors in the industry.
        risk_factors (Dict[str, str]): Main risk factors for the business.
        historical_context_crises (str): History including major crises overcome.
        moat_trajectory (str): Evidence of moat trajectory (expanding/shrinking).
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult
    business_description: str = Field(..., description="Description of business operations")
    company_history: str = Field(None, description="History of company foundation and evolution")
    ceo_name: str = Field(..., description="Name of the current CEO")
    ceo_ownership: Decimal = Field(..., description="Percentage of shares owned by the CEO")
    major_shareholders: Dict[str, Decimal] = Field(..., description="Shareholder name mapping to their ownership type/stakes")
    revenue_model: str = Field(..., description="Detailed explanation of how the company makes money")
    strategy: str = Field(..., description="The company's core strategic focus")
    products_services: Dict[str, str] = Field(..., description="Product name mapping to its function")
    competitive_advantage: str = Field(..., description="Competitive advantage or MOAT analysis")
    competitors: Dict[str, str] = Field(..., description="Competitor name mapping to the competitive overlap")
    management_insights: str = Field(..., description="Insights on management quality and meetings")
    risk_factors: Dict[str, str] = Field(..., description="Risk title mapping to detailed description")
    historical_context_crises: str = Field(..., description="History including major crises overcome")
    moat_trajectory: str = Field(..., description="Evidence of moat trajectory (expanding/shrinking)")

class SectorIndustrialValuationResult(BaseModel):
    """
    Result DTO for the comprehensive industry and sector valuation report.
    
    Attributes:
        ticker (TickerResult): Ticker information of the stock.
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

class MetricWithGrowthResult(BaseModel):
    """
    Result DTO for a metric with its year-over-year growth.
    
    Attributes:
        amount (Decimal): The absolute value or margin of the metric.
        yoy_growth (Decimal): The Year-over-Year growth percentage.
    """
    model_config = ConfigDict(frozen=True)
    amount: Decimal = Field(..., description="The absolute value or margin of the metric")
    yoy_growth: Decimal = Field(..., description="The Year-over-Year growth percentage")

class CorePerformanceResult(BaseModel):
    """
    Result DTO for the core performance of the company.
    
    Attributes:
        adjusted_revenue (MetricWithGrowthResult): Adjusted Revenue with YoY growth.
        adjusted_eps (MetricWithGrowthResult): Adjusted EPS with YoY growth.
        free_cash_flow (MetricWithGrowthResult): Free Cash Flow with YoY growth.
    """
    model_config = ConfigDict(frozen=True)
    adjusted_revenue: MetricWithGrowthResult = Field(..., description="Adjusted Revenue with YoY growth")
    adjusted_eps: MetricWithGrowthResult = Field(..., description="Adjusted EPS with YoY growth")
    adjusted_gross_margin: MetricWithGrowthResult = Field(..., description="Adjusted Gross Margin with YoY growth")
    adjusted_operating_margin: MetricWithGrowthResult = Field(..., description="Adjusted Operating Margin with YoY growth")
    adjusted_net_margin: MetricWithGrowthResult = Field(..., description="Adjusted Net Margin with YoY growth")
    free_cash_flow: MetricWithGrowthResult = Field(..., description="Free Cash Flow with YoY growth")

class CapitalAllocationResult(BaseModel):
    """
    Result DTO for the capital allocation of the company.
    
    Attributes:
        share_buybacks (Decimal): Amount spent on Share Buybacks.
        dividends (Decimal): Amount spent on Dividends.
        capex_rd (Decimal): Amount spent on CapEx/R&D.
        infrastructure_assessment (str): Assessment of infrastructure investment (accelerating/decelerating).
    """
    model_config = ConfigDict(frozen=True)
    share_buybacks: Decimal = Field(..., description="Amount spent on Share Buybacks")
    dividends: Decimal = Field(..., description="Amount spent on Dividends")
    capex_rd: Decimal = Field(..., description="Amount spent on CapEx/R&D")
    infrastructure_assessment: str = Field(..., description="Assessment of infrastructure investment (accelerating/decelerating)")

class RiskDeconstructionResult(BaseModel):
    """
    Result DTO for the risk deconstruction of the company.
    
    Attributes:
        macro_risks (List[str]): List of external/macro risks.
        internal_risks (List[str]): List of internal/execution risks.
    """
    model_config = ConfigDict(frozen=True)
    macro_risks: List[str] = Field(..., description="List of external/macro risks")
    internal_risks: List[str] = Field(..., description="List of internal/execution risks")

class EarningsReportResult(BaseModel):
    """
    Result DTO for the comprehensive value-investing focused earnings report valuation.
    
    Attributes:
        ticker (TickerResult): Ticker information of the stock.
        period_end_date (str): The end date of the fiscal period.
        core_performance (CorePerformanceResult): Core non-GAAP performance metrics.
        capital_allocation (CapitalAllocationResult): Capital allocation and infrastructure assessment.
        forward_guidance (str): Summary of forward guidance.
        moat_trajectory (str): Evidence of moat trajectory.
        risk_deconstruction (RiskDeconstructionResult): Risk deconstruction.
        bottom_line (str): Brutal, concise summary of business execution.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult
    period_end_date: str = Field(..., description="The end date of the fiscal period")
    core_performance: CorePerformanceResult = Field(..., description="Core non-GAAP performance metrics")
    capital_allocation: CapitalAllocationResult = Field(..., description="Capital allocation and infrastructure assessment")
    forward_guidance: str = Field(..., description="Summary of forward guidance (Raise/Lower/Maintain)")
    moat_trajectory: str = Field(..., description="Evidence of moat trajectory (expanding/shrinking)")
    risk_deconstruction: RiskDeconstructionResult = Field(..., description="Macro and internal risk breakdown")
    bottom_line: str = Field(..., description="Brutal, concise summary of business execution")