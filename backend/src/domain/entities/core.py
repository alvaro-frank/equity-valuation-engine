from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from domain.exceptions.exceptions import DomainValidationError

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
            raise DomainValidationError(f"Price amount cannot be negative. Got {self.amount}")
        
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
        sector_key (str | None): A normalized key for the sector, used for mapping to ETFs.
        industry (str): The industry classification of the company.
        industry_key (str | None): A normalized key for the industry, used for mapping to ETFs.
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
    beta: Decimal | None = None
    company_officers: List[Dict[str, Any]] = field(default_factory=list)
        
    def __str__(self):
        return f"{self.symbol} - {self.name} ({self.sector}/{self.industry})"
