from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Dict, List, Any

class TickerSearchDTO(BaseModel):
    """
    Data Transfer Object representing a search result for a stock ticker, including symbol, name, and exchange.
    """
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    exchange: str = Field(..., description="Exchange name")

class TickerSearchResult(BaseModel):
    """
    Data Transfer Object representing the results of a stock ticker search.
    """
    results: List[TickerSearchDTO] = Field(..., description="List of search results")

class TrendingTickerDTO(BaseModel):
    """
    Data Transfer Object representing a trending stock ticker, including symbol, name, and performance metrics.
    """
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    rating: Optional[str] = Field(None, description="Analyst rating")
    weight: Optional[float] = Field(None, description="Market weight in sector/industry")

class TrendingTickerResult(BaseModel):
    """
    Data Transfer Object representing the results of a trending stock ticker search.
    """
    results: List[TrendingTickerDTO] = Field(..., description="List of trending tickers")

class SectorPerformanceResult(BaseModel):
    """
    Data Transfer Object representing the sector performance relative to a benchmark.
    """
    company_ticker: str = Field(..., description="The ticker of the company being analyzed")
    sector: str = Field(..., description="The sector name")
    industry: str = Field(..., description="The industry name")
    sector_etf: str = Field(..., description="The Sector ETF ticker")
    industry_etf: Optional[str] = Field(None, description="The Industry ETF ticker (if available)")
    benchmark_ticker: str = Field(..., description="The benchmark ticker (e.g., SPY)")
    chart_data: List[Dict[str, Any]] = Field(..., description="Historical chart data")

class TickerResult(BaseModel):
    """
    Data Transfer Object representing the ticker information of a stock, including symbol, name, sector, and industry.
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
    """
    model_config = ConfigDict(frozen=True)
    
    date: str = Field(..., description="Fiscal year end date")
    value: Decimal | None = Field(..., description="Value of the metric for the year")

class MetricQuarterlyResult(BaseModel):
    """
    Data Transfer Object representing the value of a specific financial metric for a given fiscal quarter.
    """
    model_config = ConfigDict(frozen=True)
    
    date: str = Field(..., description="Fiscal quarter end date")
    value: Decimal | None = Field(..., description="Value of the metric for the quarter")
    
class MetricAnalysisResult(BaseModel):
    """
    Data Transfer Object representing the analysis of a specific financial metric across multiple fiscal years.
    """
    model_config = ConfigDict(frozen=True)
    
    metric_name: str = Field(..., description="Name of the metric (e.g., Revenue, Net Income)")
    yearly_data: List[MetricYearlyResult] = Field(..., description="List of yearly values for the metric")
    cagr: Optional[Decimal] = Field(..., description="Compound Annual Growth Rate (CAGR) for the metric across the analysed years")

class QuantitativeValuationResult(BaseModel):
    """
    Data Transfer Object representing the results of the stock quantitative valuation analysis, including the ticker information and a dictionary of metric analyses.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult = Field(..., description="Ticker metadata and live pricing")
    metrics: Dict[str, MetricAnalysisResult] = Field(..., description="Detailed yearly analysis per metric")
    quarterly_metrics: Optional[Dict[str, List[MetricQuarterlyResult]]] = Field(default_factory=dict, description="Detailed quarterly data per metric")

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

class QualitativeValuationResult(BaseModel):
    """
    Data Transfer Object representing the stock qualitative valuation analysis, including the ticker information, business description and company history.
    """
    model_config = ConfigDict(frozen=True)
    
    ticker: TickerResult
    business_description: str = Field(..., description="Description of business operations")
    company_history: str = Field(None, description="History of company foundation and evolution")
    key_executives: List[Dict[str, Any]] = Field(..., description="List of key executives with name, title, and ownership")
    major_shareholders: Dict[str, Decimal] = Field(..., description="Shareholder name mapping to their ownership type/stakes")
    revenue_model: str = Field(..., description="Detailed explanation of how the company makes money")
    strategy: str = Field(..., description="The company's core strategic focus")
    products_services: Dict[str, str] = Field(..., description="Product name mapping to its function")
    competitive_advantage: str = Field(..., description="Competitive advantage or MOAT analysis")
    competitors: List[Dict[str, str]] = Field(..., description="List of competitors with name, ticker, and competitive overlap")
    management_insights: str = Field(..., description="Insights on management quality and meetings")
    risk_factors: Dict[str, str] = Field(..., description="Risk title mapping to detailed description")
    historical_context_crises: str = Field(..., description="History including major crises overcome")
    moat_trajectory: str = Field(..., description="Evidence of moat trajectory (expanding/shrinking)")
    moat_sources: MoatSourcesResult = Field(..., description="Quantitative evaluation of moat sources (1-5)")
    quality_pillars: QualityPillarsResult = Field(..., description="Quantitative evaluation of business quality pillars (1-5)")

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

class MetricWithGrowthResult(BaseModel):
    """
    Data Transfer Object representing a financial metric extracted from an earnings report.
    YoY growth is calculated deterministically in the frontend using quantitative API data.
    """
    model_config = ConfigDict(frozen=True)
    amount: Optional[Decimal] = Field(None, description="The absolute value or margin of the metric")

class CorePerformanceResult(BaseModel):
    """
    Data Transfer Object representing the core performance metrics of the company.
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
    Data Transfer Object representing the capital allocation of the company.
    """
    model_config = ConfigDict(frozen=True)
    share_buybacks: Decimal = Field(..., description="Amount spent on Share Buybacks")
    dividends: Decimal = Field(..., description="Amount spent on Dividends")
    capex_rd: Decimal = Field(..., description="Amount spent on CapEx/R&D")
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
    Data Transfer Object for the comprehensive value-investing focused earnings report valuation.
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
    sources: Dict[str, str] = Field(
        ..., 
        description="Mapping of numerical citations to source document pages/sections (e.g. {'1': 'MD&A Page 15'})"
    )