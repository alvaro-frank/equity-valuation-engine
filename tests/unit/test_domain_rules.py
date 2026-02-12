import pytest

from decimal import Decimal
from domain.stock_market import Stock, Price, Ticker

def test_calculate_pe_ratio_correctly():
    ticker = Ticker(symbol="TEST")
    price = Price(amount=Decimal("100"), currency="USD")
    stock = Stock(ticker=ticker, price=price, earnings_per_share=Decimal("5"))
    
    result = stock.pe_ratio
    
    assert result == 20

def test_pe_ratio_is_none_when_eps_is_zero():
    ticker = Ticker(symbol="TEST")
    price = Price(amount=Decimal("100"), currency="USD")
    stock = Stock(ticker=ticker, price=price, earnings_per_share=Decimal("0"))
    
    with pytest.raises(ValueError) as excinfo:
        _ = stock.pe_ratio
    
    assert "Earnings cannot be zero" in str(excinfo.value)

def test_pe_ratio_handles_negative_earnings():
    ticker = Ticker(symbol="TEST")
    price = Price(amount=Decimal("100"), currency="USD")
    stock = Stock(ticker=ticker, price=price, earnings_per_share=Decimal("-5"))
    
    result = stock.pe_ratio
    
    assert result == -20