import pytest
import json
from decimal import Decimal

from domain.entities.entities import CompanyProfile, IndustrySectorDynamics
from infrastructure.adapters.gemini_adapter import GeminiAdapter

class TestGeminiAdapter:

    @pytest.fixture(autouse=True)
    def mock_sleep(self, mocker):
        mocker.patch("time.sleep", return_value=None)

    @pytest.fixture
    def mock_client(self, mocker):
        return mocker.MagicMock()

    @pytest.fixture
    def adapter(self, mock_client):
        return GeminiAdapter(client=mock_client)

    def test_analyse_company_happy_path(self, adapter, mock_client):
        mock_response = mock_client.models.generate_content.return_value
        
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
            "risk_factors": [{"title": "Regulation", "description": "Antitrust scrutiny"}],
            "historical_context_crises": "Survived dot-com bubble"
        }
        mock_response.text = json.dumps(json_ficticio)

        profile = adapter.analyse_company("MSFT")

        assert isinstance(profile, CompanyProfile)
        assert profile.ceo_name == "Satya Nadella"
        assert profile.ceo_ownership == Decimal("0.15")
        assert profile.major_shareholders["Vanguard"] == Decimal("8.5")
        assert profile.products_services["Azure"] == "Cloud platform"
        assert profile.competitors["AWS"] == "Cloud"
        
        mock_client.models.generate_content.assert_called_once()

    def test_analyse_industry_happy_path(self, adapter, mock_client):
        mock_response = mock_client.models.generate_content.return_value
        json_ficticio = {
            "sector": "TECHNOLOGY",
            "industry": "SOFTWARE",
            "rivalry_among_competitors": [{"factor": "Intensity", "analysis": "High"}],
            "bargaining_power_of_suppliers": [{"factor": "Suppliers", "analysis": "Low"}],
            "bargaining_power_of_customers": [{"factor": "Customers", "analysis": "Medium"}],
            "threat_of_new_entrants": [{"factor": "Barriers", "analysis": "High due to scale"}],
            "threat_of_obsolescence": [{"factor": "Tech Shift", "analysis": "Constant threat"}],
            "economic_sensitivity": "Cyclical",
            "interest_rate_exposure": "High impact on valuations"
        }
        mock_response.text = json.dumps(json_ficticio)

        industry_dynamics = adapter.analyse_industry("TECHNOLOGY", "SOFTWARE")

        assert isinstance(industry_dynamics, IndustrySectorDynamics)
        assert industry_dynamics.sector == "TECHNOLOGY"
        assert industry_dynamics.rivalry_among_competitors["Intensity"] == "High"
        mock_client.models.generate_content.assert_called_once()

    def test_analyse_company_handles_api_failure(self, adapter, mock_client):
        mock_client.models.generate_content.side_effect = Exception("Gemini server is down 503")

        with pytest.raises(ConnectionError, match="Gemini|Connection Error"):
            adapter.analyse_company("MSFT")
            
        assert mock_client.models.generate_content.call_count == 1