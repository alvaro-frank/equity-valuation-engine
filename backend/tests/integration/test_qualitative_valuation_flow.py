import pytest
import json
from decimal import Decimal

from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from infrastructure.adapters.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.adapters.gemini_adapter import GeminiAdapter

class TestQualitativeIntegrationFlow:

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
                    "Symbol": "MSFT", 
                    "Name": "Microsoft Corporation", 
                    "Sector": "TECHNOLOGY", 
                    "Industry": "SOFTWARE"
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
            "business_description": "Tech giant",
            "company_history": "Founded in 1975",
            "ceo_name": "Satya Nadella",
            "ceo_ownership": 0.15,
            "major_shareholders": [{"name": "Vanguard", "ownership": 8.5}],
            "revenue_model": "Software and Cloud",
            "strategy": "AI First",
            "products_services": [{"name": "Azure", "description": "Cloud platform"}],
            "competitive_advantage": "Ecosystem lock-in",
            "competitors": [{"name": "AWS", "overlap": "Cloud"}],
            "management_insights": "Strong execution",
            "risk_factors": [{"title": "Regulation", "description": "Antitrust"}],
            "historical_context_crises": "Survived dot-com bubble"
        }
        mock_response.text = json.dumps(json_ficticio)
        return client

    def test_full_qualitative_valuation_flow(self, mock_session, mock_gemini_client):
        quant_adapter = AlphaVantageAdapter(api_key="TEST_KEY", session=mock_session)
        qual_adapter = GeminiAdapter(client=mock_gemini_client)
        
        use_case = QualitativeValuationUseCase(
            adapter=qual_adapter, 
            quant_adapter=quant_adapter
        )

        result = use_case.analyse_ticker("MSFT")

        assert result.ticker.symbol == "MSFT"
        assert result.ticker.name == "Microsoft Corporation"
        assert result.ceo_name == "Satya Nadella"
        assert result.ceo_ownership == Decimal("0.15")
        assert result.major_shareholders["Vanguard"] == Decimal("8.5")
        assert result.products_services["Azure"] == "Cloud platform"
        assert result.competitors["AWS"] == "Cloud"