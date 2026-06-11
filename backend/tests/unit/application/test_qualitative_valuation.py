import pytest
from decimal import Decimal

from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from domain.entities.entities import Ticker, CompanyProfile
from application.dtos.dtos import QualitativeValuationResult

class TestQualitativeValuationUseCase:

    @pytest.fixture
    def mock_qual_adapter(self, mocker):
        mock = mocker.MagicMock()
        mock.analyse_company = mocker.AsyncMock()
        return mock

    @pytest.fixture
    def mock_quant_adapter(self, mocker):
        mock = mocker.MagicMock()
        mock.get_ticker_info = mocker.AsyncMock()
        return mock

    @pytest.fixture
    def use_case(self, mock_qual_adapter, mock_quant_adapter):
        return QualitativeValuationUseCase(
            adapter=mock_qual_adapter, 
            quant_adapter=mock_quant_adapter
        )

    @pytest.mark.anyio
    async def test_analyse_ticker_happy_path(self, use_case, mock_qual_adapter, mock_quant_adapter):
        mock_quant_adapter.get_ticker_info.return_value = Ticker(
            symbol="MSFT", name="Microsoft", sector="Tech", industry="Software"
        )
        
        mock_qual_adapter.analyse_company.return_value = CompanyProfile(
            business_description="Tech giant",
            company_history="Founded 1975",
            key_executives=[{"name": "Satya Nadella", "title": "CEO", "ownership": Decimal("0.15")}],
            major_shareholders={"Vanguard": Decimal("8.5")},
            revenue_model="Cloud",
            strategy="AI",
            products_services={"Azure": "Cloud"},
            competitive_advantage="Moat",
            competitors={"AWS": "Cloud"},
            management_insights="Strong",
            risk_factors={"Risk": "Desc"},
            historical_context_crises="None",
            moat_trajectory="Expanding",
            moat_sources={"intangible_assets": 4, "switching_costs": 3, "network_effect": 5, "cost_advantage": 2, "efficient_scale": 1},
            quality_pillars={"management_quality": 4, "business_model_resilience": 5, "pricing_power": 4, "innovation_and_growth": 3, "tam_expansion": 4}
        )

        result = await use_case.analyse_ticker("MSFT")

        assert isinstance(result, QualitativeValuationResult)
        assert result.ticker.symbol == "MSFT"
        assert result.key_executives[0]["name"] == "Satya Nadella"
        
        mock_quant_adapter.get_ticker_info.assert_called_once_with("MSFT")
        mock_qual_adapter.analyse_company.assert_called_once_with(symbol="MSFT")

    @pytest.mark.anyio
    async def test_analyse_ticker_propagates_adapter_errors(self, use_case, mock_quant_adapter):
        mock_quant_adapter.get_ticker_info.side_effect = ConnectionError("API Limit")

        with pytest.raises(ConnectionError, match="API Limit"):
            await use_case.analyse_ticker("MSFT")