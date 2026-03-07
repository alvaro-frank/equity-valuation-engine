import pytest
from decimal import Decimal
from requests.exceptions import RequestException

from infrastructure.adapters.alpha_vantage_adapter import AlphaVantageAdapter
from domain.entities.entities import Price, Ticker

class TestAlphaVantageAdapter:
    
    @pytest.fixture(autouse=True)
    def mock_sleep(self, mocker):
        mocker.patch("infrastructure.adapters.alpha_vantage_adapter.time.sleep", return_value=None)

    @pytest.fixture
    def mock_session(self, mocker):
        return mocker.MagicMock()

    @pytest.fixture
    def adapter(self, mock_session):
        return AlphaVantageAdapter(api_key="TEST_API_KEY", session=mock_session)

    def test_get_ticker_info_happy_path(self, adapter, mock_session):
        mock_response = mock_session.get.return_value
        mock_response.json.return_value = {
            "Symbol": "MSFT",
            "Name": "Microsoft Corporation",
            "Sector": "TECHNOLOGY",
            "Industry": "SERVICES-PREPACKAGED SOFTWARE"
        }
        mock_response.raise_for_status.return_value = None

        ticker = adapter.get_ticker_info("MSFT")

        assert isinstance(ticker, Ticker)
        assert ticker.symbol == "MSFT"
        assert ticker.name == "Microsoft Corporation"
        
        mock_session.get.assert_called_once()
        _, called_kwargs = mock_session.get.call_args
        assert called_kwargs["params"]["function"] == "OVERVIEW"
        assert called_kwargs["params"]["symbol"] == "MSFT"
        assert called_kwargs["params"]["apikey"] == "TEST_API_KEY"

    def test_get_stock_current_price_happy_path(self, adapter, mock_session):
        mock_response = mock_session.get.return_value
        mock_response.json.return_value = {
            "Global Quote": {
                "01. symbol": "MSFT",
                "05. price": "415.50"
            }
        }
        
        price = adapter.get_stock_current_price("MSFT")
        
        assert isinstance(price, Price)
        assert price.amount == Decimal("415.50")
        assert price.currency == "USD"

    def test_get_data_handles_network_failure(self, adapter, mock_session):
        mock_session.get.side_effect = RequestException("Timeout error")
        
        with pytest.raises(ConnectionError, match="Connection Error: Timeout error"):
            adapter.get_ticker_info("MSFT")

    @pytest.mark.parametrize("api_error_response, expected_match", [
        ({"Information": "Rate limit exceeded..."}, "Rate Limit \(Speed\)"),
        ({"Note": "Daily limit reached..."}, "Rate Limit \(Daily\)"),
        ({"Error Message": "Invalid API call..."}, "API Error"),
    ])
    def test_get_data_handles_api_rate_limits_and_errors(self, adapter, mock_session, api_error_response, expected_match):
        mock_response = mock_session.get.return_value
        mock_response.json.return_value = api_error_response
        
        with pytest.raises(Exception, match=expected_match):
            adapter.get_ticker_info("MSFT")