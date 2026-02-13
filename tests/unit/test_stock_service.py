import pytest
from decimal import Decimal
from unittest.mock import Mock

from domain.interfaces import StockDataProvider
from domain.stock_market import Stock, Price, Ticker
from services.stock_service import StockService

def test_analyse_stock_success_flow():
    mock_provider = Mock(spec=StockDataProvider)
    
    ticker_name = "IBM"
    fake_ticker = Ticker(symbol=ticker_name)
    fake_price = Price(Decimal("200.0"), "USD")
    fake_stock = Stock(
        ticker=fake_ticker, 
        price=fake_price
    )
    
    mock_provider.get_stock_fundamental_data.return_value = fake_stock

    service = StockService(data_provider=mock_provider)

    dto = service.analyse_stock(ticker_name)

    assert dto.symbol == ticker_name
    assert dto.price == Decimal("200.0")
    
    mock_provider.get_stock_fundamental_data.assert_called_once()

def test_analyse_stock_handles_provider_error():
    mock_provider = Mock(spec=StockDataProvider)
    
    mock_provider.get_stock_fundamental_data.side_effect = ConnectionError("API Down")
    
    service = StockService(data_provider=mock_provider)
    
    with pytest.raises(ConnectionError):
        service.analyse_stock("FAIL")