import pytest
import json
from decimal import Decimal

from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from infrastructure.adapters.output.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.adapters.output.gemini_adapter import GeminiAdapter

class TestEarningsIntegrationFlow:

    @pytest.fixture(autouse=True)
    def mock_sleep(self, mocker):
        mocker.patch("infrastructure.adapters.output.alpha_vantage_adapter.asyncio.sleep", return_value=None)
        mocker.patch("infrastructure.adapters.output.gemini_adapter.os.path.exists", return_value=False)
        mocker.patch("infrastructure.adapters.output.gemini_adapter.os.makedirs", return_value=None)
        mocker.patch("builtins.open", mocker.mock_open())

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
        client.aio.files = mocker.MagicMock()
        client.aio.files.upload = mocker.AsyncMock()
        
        mock_response = client.aio.models.generate_content.return_value
        
        json_ficticio = {
            "ticker": "MSFT",
            "period_end_date": "2026-03-31",
            "core_performance": {
                "adjusted_revenue": {"amount": 50000.0, "yoy_growth": 15.0},
                "adjusted_eps": {"amount": 5.0, "yoy_growth": 10.0},
                "adjusted_ebitda_margin": {"amount": 40.0, "yoy_growth": 2.0},
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
        mock_response.text = json.dumps(json_ficticio)
        return client

    @pytest.mark.anyio
    async def test_full_earnings_report_flow(self, mock_session, mock_gemini_client, tmp_path):
        quant_adapter = AlphaVantageAdapter(api_key="TEST_KEY", client=mock_session)
        quant_adapter.cache_dir = str(tmp_path)
        qual_adapter = GeminiAdapter(client=mock_gemini_client)
        qual_adapter.cache_dir = str(tmp_path)
        
        use_case = EarningsReportUseCase(
            adapter=qual_adapter, 
            quant_adapter=quant_adapter
        )

        result = await use_case.analyse_earnings_report("MSFT", "dummy.pdf")

        assert result.ticker.symbol == "MSFT"
        assert result.ticker.name == "Microsoft Corporation"
        assert result.period_end_date == "2026-03-31"
        assert result.core_performance.adjusted_revenue.amount == Decimal("50000")
        assert result.capital_allocation.infrastructure_assessment == "Accelerating"
        assert result.risk_deconstruction.macro_risks[0] == "Interest rates"
