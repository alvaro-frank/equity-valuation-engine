import pytest
import json

from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from infrastructure.adapters.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.adapters.gemini_adapter import GeminiAdapter
from application.dtos.dtos import SectorIndustrialValuationResult

class TestSectorIndustrialIntegrationFlow:

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
                    "Symbol": "NVDA", 
                    "Name": "NVIDIA Corporation", 
                    "Sector": "TECHNOLOGY", 
                    "Industry": "SEMICONDUCTORS"
                }
            mock_response.raise_for_status.return_value = None
            return mock_response

        session.get.side_effect = side_effect
        return session

    @pytest.fixture
    def mock_gemini_client(self, mocker):
        client = mocker.MagicMock()
        mock_response = client.models.generate_content.return_value
        
        json_ficticio = {
            "sector": "TECHNOLOGY",
            "industry": "SEMICONDUCTORS",
            "rivalry_among_competitors": [
                {"factor": "High", "analysis": "Intense competition with AMD and Intel"}
            ],
            "bargaining_power_of_suppliers": [
                {"factor": "Low", "analysis": "TSMC is key but NVIDIA has scale"}
            ],
            "bargaining_power_of_customers": [
                {"factor": "Medium", "analysis": "Cloud providers are large but dependent"}
            ],
            "threat_of_new_entrants": [
                {"factor": "Very High", "analysis": "Extreme R&D costs and patents"}
            ],
            "threat_of_obsolescence": [
                {"factor": "Low", "analysis": "GPU dominance in AI training"}
            ],
            "economic_sensitivity": "Cyclical but AI driven",
            "interest_rate_exposure": "Medium"
        }
        mock_response.text = json.dumps(json_ficticio)
        return client

    def test_full_sector_industrial_flow(self, mock_session, mock_gemini_client):
        quant_adapter = AlphaVantageAdapter(api_key="TEST_KEY", session=mock_session)
        sector_adapter = GeminiAdapter(client=mock_gemini_client)
        
        use_case = SectorIndustrialValuationUseCase(
            quant_port=quant_adapter,
            sector_industrial_port=sector_adapter
        )

        result = use_case.evaluate_industry_by_ticker("NVDA")

        assert isinstance(result, SectorIndustrialValuationResult)
        assert result.ticker.symbol == "NVDA"
        assert result.ticker.industry == "SEMICONDUCTORS"
        assert result.sector == "TECHNOLOGY"
        assert "TSMC" in result.bargaining_power_of_suppliers["Low"]
        assert result.economic_sensitivity == "Cyclical but AI driven"