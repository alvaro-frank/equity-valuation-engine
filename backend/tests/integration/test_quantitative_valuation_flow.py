import pytest
from decimal import Decimal

from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from infrastructure.adapters.alpha_vantage_adapter import AlphaVantageAdapter

class TestQuantitativeIntegrationFlow:

    @pytest.fixture(autouse=True)
    def mock_sleep(self, mocker):
        mocker.patch("time.sleep", return_value=None)

    @pytest.fixture
    def mock_session(self, mocker):
        session = mocker.MagicMock()

        def side_effect(url, params, **kwargs):
            mock_response = mocker.MagicMock()
            
            if params.get("function") == "OVERVIEW":
                mock_response.json.return_value = {
                    "Symbol": "AAPL", 
                    "Name": "Apple Inc", 
                    "Sector": "TECHNOLOGY", 
                    "Industry": "CONSUMER ELECTRONICS"
                }
            elif params.get("function") == "GLOBAL_QUOTE":
                mock_response.json.return_value = {
                    "Global Quote": {
                        "01. symbol": "AAPL",
                        "05. price": "150.00"
                    }
                }
            elif params.get("function") == "INCOME_STATEMENT":
                mock_response.json.return_value = {
                    "annualReports": [{
                        "fiscalDateEnding": "2023-12-31",
                        "totalRevenue": "383285000000",
                        "ebitda": "125820000000",
                        "grossProfit": "169148000000",
                        "operatingIncome": "114301000000",
                        "netIncome": "96995000000"
                    }]
                }
            elif params.get("function") == "BALANCE_SHEET":
                mock_response.json.return_value = {
                    "annualReports": [{
                        "fiscalDateEnding": "2023-12-31",
                        "commonStockSharesOutstanding": "15550061000",
                        "shortTermDebt": "15807000000",
                        "longTermDebt": "95281000000",
                        "totalAssets": "352583000000",
                        "totalLiabilities": "290437000000",
                        "cashAndCashEquivalentsAtCarryingValue": "29965000000"
                    }]
                }
            elif params.get("function") == "CASH_FLOW":
                mock_response.json.return_value = {
                    "annualReports": [{
                        "fiscalDateEnding": "2023-12-31",
                        "operatingCashflow": "110543000000",
                        "capitalExpenditures": "10959000000"
                    }]
                }
                
            mock_response.raise_for_status.return_value = None
            return mock_response

        session.get.side_effect = side_effect
        return session

    def test_full_quantitative_valuation_flow(self, mock_session):
        adapter = AlphaVantageAdapter(api_key="INTEGRATION_TEST_KEY", session=mock_session)
        use_case = QuantitativeValuationUseCase(adapter=adapter)

        result = use_case.evaluate_ticker("AAPL", years=1)

        assert result.ticker.symbol == "AAPL"
        assert result.ticker.sector == "TECHNOLOGY"
        
        assert "revenue" in result.metrics
        assert result.metrics["revenue"].yearly_data[0].value == Decimal("383285000000")
        
        assert "total debt" in result.metrics
        expected_total_debt = Decimal("15807000000") + Decimal("95281000000")
        assert result.metrics["total debt"].yearly_data[0].value == expected_total_debt