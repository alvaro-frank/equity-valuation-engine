from decimal import Decimal
from dataclasses import dataclass
from typing import Dict

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
    """
    symbol: str
    name: str = ""
    sector: str = "Unknown"
    industry: str = "Unknown"
        
    def __str__(self):
        return f"{self.symbol} - {self.name} ({self.sector}/{self.industry})"

@dataclass(frozen=True)
class FinancialYear:
    """
    Represents the financial data for a specific fiscal year, including various financial metrics.
    
    Attributes:
        fiscal_date_ending (str): The fiscal year end date.
        revenue (Decimal): Total revenue for the year.
        ebitda (Decimal): EBITDA for the year.
        gross_profit (Decimal): Gross profit for the year.
        operating_income (Decimal): Operating income for the year.
        net_income (Decimal): Net income for the year.
        operating_cash_flow (Decimal): Operating cash flow for the year.
        capital_expenditures (Decimal): Capital expenditures for the year.
        shares_outstanding (Decimal): Shares outstanding at fiscal year end.
        short_term_debt (Decimal): Short-term debt at fiscal year end.
        long_term_debt (Decimal): Long-term debt at fiscal year end.
        total_debt (Decimal): Total debt at fiscal year end.
        total_assets (Decimal): Total assets at fiscal year end.
        total_liabilities (Decimal): Total liabilities at fiscal year end.
        cash_and_equivalents (Decimal): Cash and equivalents at fiscal year end.
        year_end_price (Decimal): The close price at fiscal year end
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
    
    total_assets: Decimal
    total_liabilities: Decimal
    cash_and_equivalents: Decimal
    
    year_end_price: Decimal
    
    def __post_init__(self):
        if self.shares_outstanding < 0:
            raise ValueError(f"Domain Error: Shares outstanding cannot be negative. Got {self.shares_outstanding}")
        if self.total_assets < 0:
            raise ValueError(f"Domain Error: Total assets cannot be negative. Got {self.total_assets}")
        if self.total_debt < 0:
            raise ValueError(f"Domain Error: Total debt cannot be negative. Got {self.total_debt}")
        
    @property
    def total_equity(self) -> Decimal:
        """
        Calculates the total shareholder equity by subtracting total liabilities from total assets.

        Returns:
            Decimal: The total equity of the business.
        """
        return self.total_assets - self.total_liabilities
    
    @property
    def gross_margin(self) -> Decimal:
        """
        Calculates the gross profit margin as a percentage of total revenue.

        Returns:
            Decimal: The gross margin percentage, rounded to two decimal places.
        """
        if self.revenue == Decimal("0"):
            return Decimal("0")
        
        return round((self.gross_profit / self.revenue) * 100, 2)
    
    @property
    def operating_margin(self) -> Decimal:
        """
        Calculates the operating profit margin, representing the percentage of revenue remaining after operating expenses.

        Returns:
            Decimal: The operating margin percentage, rounded to two decimal places.
        """
        if self.revenue == Decimal("0"):
            return Decimal("0")
        
        return round((self.operating_income / self.revenue) * 100, 2)
    
    @property
    def net_margin(self) -> Decimal:
        """
        Calculates the net profit margin, representing the percentage of revenue that results in net income.

        Returns:
            Decimal: The net margin percentage, rounded to two decimal places.
        """
        if self.revenue == Decimal("0"):
            return Decimal("0")
        
        return round((self.net_income / self.revenue) * 100, 2)
    
    @property
    def roe(self) -> Decimal | None:
        """
        Calculates the Return on Equity (ROE), measuring profitability relative to shareholder equity.

        Returns:
            Decimal: The ROE percentage, rounded to two decimal places.
        """
        equity = self.total_equity
        
        if equity <= Decimal("0"):
            return None
        
        return round((self.net_income / equity) * 100, 2)
    
    @property
    def roic(self) -> Decimal | None:
        """
        Calculates the Return on Invested Capital (ROIC) using net income over the sum of debt and equity.

        Returns:
            Decimal: The ROIC percentage, rounded to two decimal places.
        """
        invested_capital = self.total_debt + self.total_equity
        
        if invested_capital <= Decimal("0"):
            return None
        
        return round((self.net_income / invested_capital) * 100, 2)
    
    @property
    def debt_to_equity(self) -> Decimal | None:
        """
        Calculates the debt-to-equity ratio, indicating the relative proportion of shareholder equity and debt used to finance assets.

        Returns:
            Decimal: The debt-to-equity ratio, rounded to two decimal places.
        """
        equity = self.total_equity
        
        if equity <= Decimal("0"):
            return None
        
        return round(self.total_debt / equity, 2)
    
    @property
    def market_cap(self) -> Decimal:
        """
        Calculates the Market Capitalization based on year-end price and shares outstanding.
        
        Returns:
            Decimal: The total market value of the company's outstanding shares.
        """
        return self.year_end_price * self.shares_outstanding

    @property
    def pe_ratio(self) -> Decimal | None:
        """
        Calculates the Price-to-Earnings (P/E) Ratio.
        
        Returns:
            Decimal | None: The P/E ratio rounded to two decimal places, or None if net income is zero or negative.
        """
        if self.net_income <= Decimal("0"):
            return None
        return round(self.market_cap / self.net_income, 2)

    @property
    def pb_ratio(self) -> Decimal | None:
        """
        Calculates the Price-to-Book (P/B) Ratio.
        
        Returns:
            Decimal | None: The P/B ratio rounded to two decimal places, or None if total equity is zero or negative.
        """
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round(self.market_cap / equity, 2)

    @property
    def ps_ratio(self) -> Decimal | None:
        """
        Calculates the Price-to-Sales (P/S) Ratio.
        
        Returns:
            Decimal | None: The P/S ratio rounded to two decimal places, or None if revenue is zero or negative.
        """
        if self.revenue <= Decimal("0"):
            return None
        return round(self.market_cap / self.revenue, 2)

    @property
    def fcf_yield(self) -> Decimal | None:
        """
        Calculates the Free Cash Flow Yield as a percentage.
        
        Returns:
            Decimal | None: The FCF yield percentage rounded to two decimal places, or None if market cap is zero.
        """
        if self.market_cap == Decimal("0"):
            return None
        fcf = self.operating_cash_flow - self.capital_expenditures
        return round((fcf / self.market_cap) * 100, 2)
    
@dataclass(frozen=True)
class CompanyProfile:
    """
    Represents the company and company's business model details
    
    Attributes:
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
    business_description: str
    company_history: str
    ceo_name: str
    ceo_ownership: Decimal
    major_shareholders: Dict[str, Decimal]
    revenue_model: str
    strategy: str
    products_services: Dict[str, str]
    competitive_advantage: str
    competitors: Dict[str, str]
    management_insights: str
    risk_factors: Dict[str, str]
    historical_context_crises: str
    
    def __post_init__(self):
        if self.ceo_ownership < 0 or self.ceo_ownership > 100:
            raise ValueError(f"Domain Error: CEO ownership must be between 0 and 100%. Got {self.ceo_ownership}")
    
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