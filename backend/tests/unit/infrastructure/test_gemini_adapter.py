import pytest
import json
from decimal import Decimal

from domain.entities.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport
from infrastructure.adapters.output.gemini_adapter import GeminiAdapter

class TestGeminiAdapter:

    @pytest.fixture(autouse=True)
    def mock_sleep(self, mocker):
        mocker.patch("time.sleep", return_value=None)

    @pytest.fixture
    def mock_client(self, mocker):
        mock = mocker.MagicMock()
        mock.aio = mocker.MagicMock()
        mock.aio.models = mocker.MagicMock()
        mock.aio.models.generate_content = mocker.AsyncMock()
        mock.aio.files = mocker.MagicMock()
        mock.aio.files.upload = mocker.AsyncMock()
        mock.aio.files.get = mocker.AsyncMock()
        return mock

    @pytest.fixture
    def adapter(self, mock_client, tmp_path):
        adapter = GeminiAdapter(client=mock_client)
        adapter.cache_dir = str(tmp_path)
        return adapter

    @pytest.mark.anyio
    async def test_analyse_company_happy_path(self, adapter, mock_client):
        mock_response = mock_client.aio.models.generate_content.return_value
        
        json_ficticio = {
            "business_description": "Tech giant",
            "company_history": "Founded in 1975",
            "key_executives": [{"name": "Satya Nadella", "title": "CEO", "ownership": 0.15}],
            "revenue_model": "Software and Cloud",
            "strategy": "AI First",
            "products_services": [{"name": "Azure", "description": "Cloud platform"}],
            "competitive_advantage": "Ecosystem lock-in",
            "competitors": [{"name": "AWS", "overlap": "Cloud"}],
            "management_insights": "Strong execution",
            "risk_factors": [{"title": "Regulation", "description": "Antitrust scrutiny"}],
            "historical_context_crises": "Survived dot-com bubble",
            "moat_trajectory": "Expanding",
            "moat_sources": {"intangible_assets": 4, "switching_costs": 5, "network_effect": 5, "cost_advantage": 3, "efficient_scale": 2},
            "quality_pillars": {"management_quality": 4, "business_model_resilience": 5, "pricing_power": 4, "innovation_and_growth": 4, "tam_expansion": 4}
        }
        mock_response.text = json.dumps(json_ficticio)

        profile = await adapter.analyse_company("MSFT")

        assert isinstance(profile, CompanyProfile)
        assert profile.key_executives[0]["name"] == "Satya Nadella"
        assert profile.key_executives[0]["ownership"] == 0.15
        assert profile.products_services["Azure"] == "Cloud platform"
        assert profile.competitors["AWS"] == "Cloud"
        
        mock_client.aio.models.generate_content.assert_called_once()

    @pytest.mark.anyio
    async def test_analyse_industry_happy_path(self, adapter, mock_client):
        mock_response = mock_client.aio.models.generate_content.return_value
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

        industry_dynamics = await adapter.analyse_industry("TECHNOLOGY", "SOFTWARE")

        assert isinstance(industry_dynamics, IndustrySectorDynamics)
        assert industry_dynamics.sector == "TECHNOLOGY"
        assert industry_dynamics.rivalry_among_competitors["Intensity"] == "High"
        mock_client.aio.models.generate_content.assert_called_once()

    @pytest.mark.anyio
    async def test_analyse_company_handles_api_failure(self, adapter, mock_client):
        mock_client.aio.models.generate_content.side_effect = Exception("Gemini server is down 503")

        with pytest.raises(ConnectionError, match="Gemini|Connection Error"):
            await adapter.analyse_company("MSFT")
            
        assert mock_client.aio.models.generate_content.call_count == 1

    @pytest.mark.anyio
    async def test_analyse_earnings_report_happy_path(self, adapter, mock_client, mocker):
        mocker.patch("infrastructure.adapters.output.gemini_adapter.os.path.exists", return_value=False)
        mocker.patch("infrastructure.adapters.output.gemini_adapter.os.makedirs", return_value=None)
        
        mock_response = mock_client.aio.models.generate_content.return_value
        
        json_earnings = {
            "ticker": "MSFT",
            "period_end_date": "2026-03-31",
            "core_performance": {
                "adjusted_revenue": {"amount": 50000.0, "yoy_growth": 15.0},
                "adjusted_eps": {"amount": 5.0, "yoy_growth": 10.0},
                "adjusted_gross_margin": {"amount": 60.0, "yoy_growth": 1.0},
                "adjusted_operating_margin": {"amount": 40.0, "yoy_growth": 2.0},
                "adjusted_net_margin": {"amount": 30.0, "yoy_growth": 1.0},
                "free_cash_flow": {"amount": 15000.0, "yoy_growth": 5.0}
            },
            "capital_allocation": {
                "share_buybacks": 2000.0,
                "dividends": 1000.0,
                "capex_rd": 5000.0,
                "infrastructure_assessment": "Accelerating"
            },
            "forward_guidance": "Raise",
            "moat_trajectory": "Expanding",
            "risk_deconstruction": {
                "macro_risks": ["Interest rates"],
                "internal_risks": ["Execution delay"]
            },
            "bottom_line": "Excellent execution."
        }
        mock_response.text = json.dumps(json_earnings)

        mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data=b"dummy pdf content"))

        report = await adapter.analyse_earnings_report("MSFT", "dummy_pdf.pdf")

        assert isinstance(report, EarningsReport)
        assert report.period_end_date == "2026-03-31"
        assert report.core_performance.adjusted_revenue.amount == Decimal("50000.0")
        assert report.core_performance.adjusted_revenue.yoy_growth == Decimal("15.0")
        assert report.capital_allocation.share_buybacks == Decimal("2000.0")
        assert report.forward_guidance == "Raise"
        assert "Interest rates" in report.risk_deconstruction.macro_risks
        
        mock_client.aio.models.generate_content.assert_called_once()
        mock_client.aio.files.upload.assert_called_once()

    @pytest.mark.anyio
    async def test_analyse_earnings_report_handles_api_failure(self, adapter, mock_client, mocker):
        mocker.patch("infrastructure.adapters.output.gemini_adapter.os.path.exists", return_value=False)
        mocker.patch("builtins.open", mocker.mock_open(read_data=b"dummy pdf content"))
        mock_client.aio.models.generate_content.side_effect = Exception("Gemini server is down 503")

        with pytest.raises(ConnectionError, match="Connection Error"):
            await adapter.analyse_earnings_report("MSFT", "dummy_pdf.pdf")
            
        assert mock_client.aio.models.generate_content.call_count == 1