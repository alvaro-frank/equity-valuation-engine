import pytest
import json
from decimal import Decimal

from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from infrastructure.adapters.output.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.adapters.output.gemini_adapter import GeminiAdapter

class TestQualitativeIntegrationFlow:

    @pytest.fixture(autouse=True)
    def mock_sleep(self, mocker):
        mocker.patch("infrastructure.adapters.output.alpha_vantage_adapter.asyncio.sleep", return_value=None)

    @pytest.fixture
    def mock_session(self, mocker):
        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock()

        async def side_effect(url, params, **kwargs):
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

        mock_client.get.side_effect = side_effect
        return mock_client

    @pytest.fixture
    def mock_gemini_client(self, mocker):
        client = mocker.MagicMock()
        client.aio = mocker.MagicMock()
        client.aio.models = mocker.MagicMock()
        client.aio.models.generate_content = mocker.AsyncMock()
        
        mock_response = client.aio.models.generate_content.return_value
        
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
            "risk_factors": [{"title": "Regulation", "description": "Antitrust"}],
            "historical_context_crises": "Survived dot-com bubble",
            "moat_trajectory": "Expanding",
            "moat_sources": {"intangible_assets": 4, "switching_costs": 5, "network_effect": 5, "cost_advantage": 3, "efficient_scale": 2},
            "quality_pillars": {"management_quality": 4, "business_model_resilience": 5, "pricing_power": 4, "innovation_and_growth": 4, "tam_expansion": 4}
        }
        mock_response.text = json.dumps(json_ficticio)
        return client

    @pytest.mark.anyio
    async def test_full_qualitative_valuation_flow(self, mock_session, mock_gemini_client, tmp_path):
        quant_adapter = AlphaVantageAdapter(api_key="TEST_KEY", client=mock_session)
        quant_adapter.cache_dir = str(tmp_path)
        qual_adapter = GeminiAdapter(client=mock_gemini_client)
        qual_adapter.cache_dir = str(tmp_path)
        
        use_case = QualitativeValuationUseCase(
            adapter=qual_adapter, 
            quant_adapter=quant_adapter
        )

        result = await use_case.analyse_ticker("MSFT")

        assert result.ticker.symbol == "MSFT"
        assert result.ticker.name == "Microsoft Corporation"
        assert result.key_executives[0]["name"] == "Satya Nadella"
        assert result.key_executives[0]["ownership"] == 0.15
        assert result.products_services["Azure"] == "Cloud platform"
        assert result.competitors["AWS"] == "Cloud"