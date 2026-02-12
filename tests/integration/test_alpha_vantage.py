import pytest

from decimal import Decimal
from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from domain.stock_market import Ticker, Price, Stock

@pytest.mark.integration
class TestAlphaVantageIntegration:
    """
    Test real interactions with the Alpha Vantage API to ensure our Adapter works correctly.
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Configures the Adapter with a real API key (from .env) and ensures the cache is used for repeated calls.
        """
        self.adapter = AlphaVantageAdapter()

    def test_real_price_fetch(self):
        """
        Test fetching the current price of a known stock (e.g., IBM) and verify it returns a valid Price object.
        """
        ticker = Ticker("IBM")
        
        result = self.adapter.get_stock_current_price(ticker)
        
        assert isinstance(result, Price)
        assert result.amount > 0
        assert result.currency == "USD"

    def test_real_fundamental_data_fetch(self):
        """
        Test fetching fundamental data for a known stock (e.g., AAPL) and verify it returns a valid Stock object with EPS.
        """
        ticker = Ticker("AAPL")
        
        result = self.adapter.get_stock_fundamental_data(ticker)
        
        assert isinstance(result, Stock)
        assert result.earnings_per_share is not None
        assert isinstance(result.earnings_per_share, Decimal)
        assert result.ticker.symbol == "AAPL"

    def test_invalid_ticker_error_handling(self):
        """
        Test that requesting data for an invalid ticker raises a ValueError.
        """
        ticker = Ticker("INVALID123")
        
        with pytest.raises(ValueError):
            self.adapter.get_stock_fundamental_data(ticker)