from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from domain.exceptions.exceptions import DomainValidationError

@dataclass(frozen=True)
class BaseFinancialPeriod:
    """
    Base class representing the financial data for a specific fiscal period.
    Contains all shared metrics and properties between Years and Quarters.
    
    Attributes:
        fiscal_date_ending (str): The end date of the fiscal period.
        revenue (Decimal): Total revenue for the period.
        ebitda (Decimal): Earnings Before Interest, Taxes, Depreciation, and Amortization.
        gross_profit (Decimal): Gross profit for the period.
        operating_income (Decimal): Operating income for the period.
        net_income (Decimal): Net income for the period.
        operating_cash_flow (Decimal): Cash flow from operations.
        capital_expenditures (Decimal): Capital expenditures for the period.
        shares_outstanding (Decimal): Total shares outstanding during the period.
        short_term_debt (Decimal): Short-term debt at the end of the period.
        long_term_debt (Decimal): Long-term debt at the end of the period.
        total_debt (Decimal): Total debt at the end of the period.
        accounts_payable (Decimal): Accounts payable at the end of the period.
        current_liabilities (Decimal): Current liabilities at the end of the period.
        total_liabilities (Decimal): Total liabilities at the end of the period.
        cash_and_equivalents (Decimal): Cash and cash equivalents at the end of the period.
        accounts_receivable (Decimal): Accounts receivable at the end of the period.
        inventory (Decimal): Inventory value at the end of the period.
        current_assets (Decimal): Current assets at the end of the period.
        net_ppe (Decimal): Net property, plant, and equipment at the end of the period.
        intangible_assets (Decimal): Intangible assets at the end of the period.
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
    
    interest_expense: Decimal | None = None
    income_tax_expense: Decimal | None = None
    income_before_tax: Decimal | None = None
    beta: Decimal | None = None
    
    def __post_init__(self):
        if self.shares_outstanding < 0:
            raise DomainValidationError(f"Shares outstanding cannot be negative. Got {self.shares_outstanding}")
        if self.total_assets < 0:
            raise DomainValidationError(f"Total assets cannot be negative. Got {self.total_assets}")
        if self.total_debt < 0:
            raise DomainValidationError(f"Total debt cannot be negative. Got {self.total_debt}")

    @property
    def period_end_price(self) -> Decimal:
        """To be implemented by subclasses"""
        raise NotImplementedError

    @property
    def total_equity(self) -> Decimal:
        """Calculates total equity as total assets minus total liabilities."""
        return self.total_assets - self.total_liabilities

    @property
    def gross_margin(self) -> Decimal | None:
        """Calculates gross margin as (gross profit / revenue) * 100."""
        if self.revenue == Decimal("0"):
            return None
        return round((self.gross_profit / self.revenue) * 100, 2)

    @property
    def operating_margin(self) -> Decimal | None:
        """Calculates operating margin as (operating income / revenue) * 100."""
        if self.revenue == Decimal("0"):
            return None
        return round((self.operating_income / self.revenue) * 100, 2)

    @property
    def net_margin(self) -> Decimal | None:
        """Calculates net margin as (net income / revenue) * 100."""
        if self.revenue == Decimal("0"):
            return None
        return round((self.net_income / self.revenue) * 100, 2)

    @property
    def roe(self) -> Decimal | None:
        """Calculates Return on Equity (ROE) as (net income / total equity) * 100."""
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round((self.net_income / equity) * 100, 2)

    @property
    def roic(self) -> Decimal | None:
        """Calculates Return on Invested Capital (ROIC) as (net income / invested capital) * 100."""
        invested_capital = self.total_debt + self.total_equity
        if invested_capital <= Decimal("0"):
            return None
        return round((self.net_income / invested_capital) * 100, 2)

    @property
    def debt_to_equity(self) -> Decimal | None:
        """Calculates Debt-to-Equity ratio as total debt divided by total equity."""
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round(self.total_debt / equity, 2)

    @property
    def market_cap(self) -> Decimal:
        """Calculates market capitalization as shares outstanding multiplied by the period end price."""
        return self.shares_outstanding * self.period_end_price

    @property
    def tax_rate(self) -> Decimal:
        """Calculates effective tax rate, defaulting to 21% if missing or invalid."""
        if self.income_before_tax and self.income_before_tax > Decimal("0") and self.income_tax_expense:
            return round(self.income_tax_expense / self.income_before_tax, 4)
        return Decimal("0.21")

    @property
    def cost_of_debt(self) -> Decimal:
        """Calculates cost of debt, defaulting to 5% if missing or invalid."""
        if self.total_debt > Decimal("0") and self.interest_expense:
            return round(self.interest_expense / self.total_debt, 4)
        return Decimal("0.05")

    @property
    def historical_wacc(self) -> Decimal | None:
        """
        Calculates Historical WACC based on CAPM.
        Ke = R_f + Beta * ERP (where R_f = 4.2%, ERP = 5.0%)
        Kd = Cost of Debt (from interest_expense / total_debt)
        """
        equity_val = self.market_cap
        debt_val = self.total_debt
        total_val = equity_val + debt_val
        
        if total_val <= Decimal("0"):
            return None
            
        weight_equity = equity_val / total_val
        weight_debt = debt_val / total_val
        
        # Industry standard long-term assumptions
        risk_free_rate = Decimal("0.042")
        market_premium = Decimal("0.050")
        
        company_beta = self.beta if self.beta is not None else Decimal("1.0")
        cost_of_equity = risk_free_rate + (company_beta * market_premium)
        
        wacc = (weight_equity * cost_of_equity) + (weight_debt * self.cost_of_debt * (Decimal("1.0") - self.tax_rate))
        return round(wacc * Decimal("100"), 2)

    @property
    def pe_ratio(self) -> Decimal | None:
        """Calculates Price-to-Earnings (P/E) ratio as market capitalization divided by net income."""
        if self.net_income <= Decimal("0"):
            return None
        return round(self.market_cap / self.net_income, 2)

    @property
    def current_ratio(self) -> Decimal | None:
        """Calculates current ratio as current assets divided by current liabilities."""
        if self.current_liabilities <= Decimal("0"):
            return None
        return round(self.current_assets / self.current_liabilities, 2)

    @property
    def enterprise_value(self) -> Decimal:
        """Calculates enterprise value as market capitalization plus total debt minus cash and equivalents."""
        return self.market_cap + self.total_debt - self.cash_and_equivalents

    @property
    def ev_to_ebitda(self) -> Decimal | None:
        """Calculates EV/EBITDA ratio as enterprise value divided by EBITDA."""
        if self.ebitda <= Decimal("0"):
            return None
        return round(self.enterprise_value / self.ebitda, 2)

    @property
    def debt_to_ebitda(self) -> Decimal | None:
        """Calculates Debt-to-EBITDA ratio as total debt divided by EBITDA."""
        if self.ebitda <= Decimal("0"):
            return None
        return round(self.total_debt / self.ebitda, 2)

    @property
    def pb_ratio(self) -> Decimal | None:
        """Calculates Price-to-Book (P/B) ratio as market capitalization divided by total equity."""
        equity = self.total_equity
        if equity <= Decimal("0"):
            return None
        return round(self.market_cap / equity, 2)

    @property
    def ps_ratio(self) -> Decimal | None:
        """Calculates Price-to-Sales (P/S) ratio as market capitalization divided by revenue."""
        if self.revenue <= Decimal("0"):
            return None
        return round(self.market_cap / self.revenue, 2)

    @property
    def free_cash_flow(self) -> Decimal:
        """Calculates free cash flow as operating cash flow minus capital expenditures."""
        return self.operating_cash_flow - abs(self.capital_expenditures)

    @property
    def fcf_yield(self) -> Decimal | None:
        """Calculates free cash flow yield as (free cash flow / market capitalization) * 100."""
        if self.market_cap == Decimal("0"):
            return None
        fcf = self.operating_cash_flow - abs(self.capital_expenditures)
        return round((fcf / self.market_cap) * 100, 2)

    @property
    def eps(self) -> Decimal | None:
        """Calculates earnings per share (EPS) as net income divided by shares outstanding."""
        if self.shares_outstanding == Decimal("0"):
            return None
        return round(self.net_income / self.shares_outstanding, 2)

@dataclass(frozen=True)
class FinancialYear(BaseFinancialPeriod):
    """
    Represents the financial data for a specific fiscal year.
    
    Attributes:
        year_end_price (Decimal): The stock price at the end of the fiscal year.
    """
    year_end_price: Decimal = Decimal("0")

    @property
    def period_end_price(self) -> Decimal:
        return self.year_end_price

@dataclass(frozen=True)
class FinancialQuarter(BaseFinancialPeriod):
    """
    Represents the financial data for a specific fiscal quarter.
    
    Attributes:
        quarter_end_price (Decimal): The stock price at the end of the fiscal quarter.
    """
    quarter_end_price: Decimal = Decimal("0")

    @property
    def period_end_price(self) -> Decimal:
        """Returns the stock price at the end of the fiscal quarter."""
        return self.quarter_end_price

    @property
    def roic(self) -> Decimal | None:
        """Calculates Return on Invested Capital (ROIC) as (NOPAT / invested capital) * 100."""
        invested_capital = self.total_assets - self.total_liabilities + self.short_term_debt + self.long_term_debt - self.cash_and_equivalents
        if invested_capital == Decimal("0"):
            return None
        nopat = self.operating_income * Decimal("0.8") # Assumes 20% tax rate
        return round((nopat / invested_capital) * 100, 2)
