from decimal import Decimal
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Price:
    amount: Decimal
    currency: str = "USD"
        
    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"
 
@dataclass(frozen=True)
class Ticker:
    symbol: str
    name: str = ""
    sector: str = "Unknown"
    industry: str = "Unknown"
        
    def __str__(self):
        return f"{self.symbol} - {self.name} ({self.sector}/{self.industry})"

@dataclass(frozen=True)
class FinancialYear:
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

@dataclass(frozen=True)
class Stock:
    ticker: Ticker
    price: Price
    financial_years: List[FinancialYear]
    
if __name__ == "__main__":
    apple_price = Price(amount=Decimal("150.00"), currency="USD")
    apple_ticker = Ticker(symbol="AAPL")
    
    apple_stock = Stock(ticker=apple_ticker, 
                        price=apple_price,
                        financial_years=[])
    
    print(f"Stock: {apple_stock.ticker}")
    print(f"Price: {apple_stock.price}")
    print(f"Financial Years: {len(apple_stock.financial_years)} years loaded.")  