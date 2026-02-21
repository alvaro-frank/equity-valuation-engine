from decimal import Decimal
from dataclasses import dataclass
from typing import List

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

@dataclass(frozen=True)
class Stock:
    """
    Represents a stock with its ticker information, current price, and historical financial data.
    
    Attributes:
        ticker (Ticker): The ticker information of the stock.
        price (Price): The current price of the stock.
        financial_years (List[FinancialYear]): The list of financial years for the stock.
    """
    ticker: Ticker
    price: Price
    financial_years: List[FinancialYear]
    
    def calculate_cagr(self, field_name: str, num_years: int) -> Decimal:
        """Calculalates CAGR for a specific metric on the last X years.
        
        Args:
            field_name (str): Name of the metric
            num_years (int): Number of years to analyse
            
        Returns:
            cagr_val (Decimal): the calculated CAGR value
        """
        sorted_years = sorted(self.financial_years, key=lambda x: x.fiscal_date_ending)
        analysis_years = sorted_years[-num_years:]
        
        if len(analysis_years) < 2:
            return Decimal("0")

        begin_val = getattr(analysis_years[0], field_name, Decimal("0"))
        end_val = getattr(analysis_years[-1], field_name, Decimal("0"))
        t = len(analysis_years) - 1

        if begin_val > 0:
            ratio = float(end_val / begin_val)
            if ratio > 0:
                cagr_val = (pow(ratio, (1 / t)) - 1) * 100
                return Decimal(str(round(cagr_val, 2)))
        
        return Decimal("0")
    
if __name__ == "__main__":
    apple_price = Price(amount=Decimal("150.00"), currency="USD")
    apple_ticker = Ticker(symbol="AAPL")
    
    apple_stock = Stock(ticker=apple_ticker, 
                        price=apple_price,
                        financial_years=[])
    
    print(f"Stock: {apple_stock.ticker}")
    print(f"Price: {apple_stock.price}")
    print(f"Financial Years: {len(apple_stock.financial_years)} years loaded.")  