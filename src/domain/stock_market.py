from decimal import Decimal
from dataclasses import dataclass

@dataclass(frozen=True)
class Price:
    amount: Decimal
    currency: str = "USD"
        
    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"
 
@dataclass(frozen=True)
class Ticker:
    symbol: str
        
    def __str__(self):
        return self.symbol

@dataclass
class Stock:
    ticker: Ticker
    price: Price
    earnings_per_share: Decimal
    
    @property    
    def pe_ratio(self) -> Decimal:
        if self.earnings_per_share == Decimal("0"):
            raise ValueError("Earnings cannot be zero for P/E calculation")
        
        return self.price.amount / self.earnings_per_share
    
if __name__ == "__main__":
    apple_price = Price(amount=Decimal("150.00"), currency="USD")
    apple_ticker = Ticker(symbol="AAPL")
    
    apple_stock = Stock(ticker=apple_ticker, 
                        price=apple_price, 
                        earnings_per_share=Decimal("5.00"))
    
    print(f"Stock: {apple_stock.ticker}, Price: {apple_stock.price}, P/E Ratio: {apple_stock.pe_ratio:.2f}")
        