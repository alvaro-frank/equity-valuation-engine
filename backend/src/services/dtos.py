from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Dict, List

class TickerDTO(BaseModel):
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
    name: Optional[str] = Field(None, description="Company name")
    sector: Optional[str] = Field("Unknown", description="Sector of the company")
    industry: Optional[str] = Field("Unknown", description="Industry of the company")
    
class MetricYearlyDTO(BaseModel):
    """
    Data Transfer Object representing the value of a specific financial metric for a given fiscal year.
    
    Attributes:
        date (str): The fiscal year end date.
        value (Decimal): The value of the metric for that year.
    """
    model_config = ConfigDict(frozen=True)

    date: str = Field(..., description="Fiscal year end date")
    value: Decimal = Field(..., description="Value of the metric for the year")
    
class MetricAnalysisDTO(BaseModel):
    """
    Data Transfer Object representing the analysis of a specific financial metric across multiple fiscal years.
    
    Attributes:
        metric_name (str): The name of the financial metric being analysed (e.g., Revenue, Net Income).
        yearly_data (List[MetricYearlyDTO]): A list of the metric's values for each fiscal year analysed.
        cagr (Decimal): The Compound Annual Growth Rate (CAGR) for the metric across the analysed years, expressed as a percentage.
    """
    model_config = ConfigDict(frozen=True)

    metric_name: str = Field(..., description="Name of the metric (e.g., Revenue, Net Income)")
    yearly_data: List[MetricYearlyDTO] = Field(..., description="List of yearly values for the metric")
    cagr: Decimal = Field(..., description="Compound Annual Growth Rate (CAGR) for the metric across the analysed years")
    
class QuantitativeValuationDTO(BaseModel):
    """
    Data Transfer Object representing the results of the stock quantitative valuation analysis, including the ticker information and a dictionary of metric analyses.
    
    Attributes:
        ticker (TickerDTO): Ticker information of the stock.
        metrics (Dict[str, MetricAnalysisDTO]): A dictionary where the key is the metric name and the value is the analysis of that metric across years.
    """
    model_config = ConfigDict(frozen=True)

    ticker: TickerDTO = Field(..., description="Ticker information")
    metrics: Dict[str, MetricAnalysisDTO] = Field(..., description="Dictionary of metric analyses by metric name")
    
class QualitativeValuationDTO(BaseModel):
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
        management_insights (str): Insights on management quality and meetings.
        risk_factors (Dict[str, str]): Main risk factors for the business.
        historical_context_crises (str): History including major crises overcome.
    """
    model_config = ConfigDict(frozen=True)

    ticker: TickerDTO
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
    
class SectorValuationDTO(BaseModel):
    """
    Result DTO for the comprehensive industry and sector valuation report.
    
    Attributes:
    """
    model_config = ConfigDict(frozen=True)

    ticker: TickerDTO
    sector: str = Field(..., description="The broad sector name")
    industry: str = Field(..., description="The specific industry name")
    rivalry_among_competitors: Dict[str, str] = Field(..., description="Analysis of intensity of competition")
    bargaining_power_of_suppliers: Dict[str, str] = Field(..., description="Analysis of supplier leverage")
    bargaining_power_of_customers: Dict[str, str] = Field(..., description="Analysis of customer leverage")
    threat_of_new_entrants: Dict[str, str] = Field(..., description="Barriers to entry and new competition")
    threat_of_obsolescence: Dict[str, str] = Field(..., description="Risk of technological or market displacement")
    economic_sensitivity: str = Field(..., description="How the industry reacts to economic cycles")
    interest_rate_exposure: str = Field(..., description="Impact of interest rate fluctuations on the sector")