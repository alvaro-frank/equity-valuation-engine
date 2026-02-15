from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional

class PriceDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    amount: Decimal = Field(..., description="Price amount")
    currency: str = Field(..., description="Currency of the price (e.g., USD)")
    
class TickerDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    symbol: str = Field(..., description="Ticker symbol")
    name: Optional[str] = Field(None, description="Company name")
    sector: Optional[str] = Field("Unknown", description="Sector of the company")
    industry: Optional[str] = Field("Unknown", description="Industry of the company")
    
class FinancialYearDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    fiscal_date_ending: str = Field(..., description="Fiscal year end date")
    
    revenue: Decimal = Field(..., description="Total revenue for the year")
    ebitda: Decimal = Field(..., description="EBITDA for the year")
    
    gross_profit: Decimal = Field(..., description="Gross profit for the year")
    operating_income: Decimal = Field(..., description="Operating income for the year")
    net_income: Decimal = Field(..., description="Net income for the year")
    
    operating_cash_flow: Decimal = Field(..., description="Operating cash flow for the year")
    capital_expenditures: Decimal = Field(..., description="Capital expenditures for the year")
    
    shares_outstanding: Decimal = Field(..., description="Shares outstanding at fiscal year end")
    
    short_term_debt: Decimal = Field(..., description="Short-term debt at fiscal year end")
    long_term_debt: Decimal = Field(..., description="Long-term debt at fiscal year end")
    total_debt: Decimal = Field(..., description="Total debt at fiscal year end")
    
    total_assets: Decimal = Field(..., description="Total assets at fiscal year end")
    total_liabilities: Decimal = Field(..., description="Total liabilities at fiscal year end")
    cash_and_equivalents: Decimal = Field(..., description="Cash and equivalents at fiscal year end")

class StockDataDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    ticker: TickerDTO = Field(..., description="Ticker information")
    price: PriceDTO = Field(..., description="Current stock price")
    financial_years: list[FinancialYearDTO] = Field(..., description="List of financial data for recent years")