import pytest

from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from domain.entities.entities import Ticker, IndustrySectorDynamics
from application.dtos.dtos import SectorIndustrialValuationResult

class TestSectorIndustrialValuationUseCase:

    @pytest.fixture
    def mock_quant_port(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def mock_sector_port(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def use_case(self, mock_quant_port, mock_sector_port):
        return SectorIndustrialValuationUseCase(
            quant_port=mock_quant_port,
            sector_industrial_port=mock_sector_port
        )

    def test_evaluate_industry_by_ticker_happy_path(self, use_case, mock_quant_port, mock_sector_port):
        mock_quant_port.get_ticker_info.return_value = Ticker(
            symbol="TSLA", name="Tesla", sector="Consumer Cyclical", industry="Auto Manufacturers"
        )
        
        mock_sector_port.analyse_industry.return_value = IndustrySectorDynamics(
            sector="Consumer Cyclical",
            industry="Auto Manufacturers",
            rivalry_among_competitors={"Intensity": "High"},
            bargaining_power_of_suppliers={"Suppliers": "Medium"},
            bargaining_power_of_customers={"Customers": "Low"},
            threat_of_new_entrants={"Barriers": "High"},
            threat_of_obsolescence={"Tech": "High"},
            economic_sensitivity="High",
            interest_rate_exposure="High"
        )

        result = use_case.evaluate_industry_by_ticker("TSLA")

        assert isinstance(result, SectorIndustrialValuationResult)
        assert result.ticker.symbol == "TSLA"
        assert result.sector == "Consumer Cyclical"
        assert result.industry == "Auto Manufacturers"
        assert result.rivalry_among_competitors["Intensity"] == "High"

        mock_quant_port.get_ticker_info.assert_called_once_with("TSLA")
        mock_sector_port.analyse_industry.assert_called_once_with(
            sector="Consumer Cyclical", 
            industry="Auto Manufacturers"
        )

    def test_evaluate_industry_propagates_quant_error(self, use_case, mock_quant_port):
        mock_quant_port.get_ticker_info.side_effect = ConnectionError("API Down")

        with pytest.raises(ConnectionError, match="API Down"):
            use_case.evaluate_industry_by_ticker("TSLA")

    def test_evaluate_industry_propagates_sector_error(self, use_case, mock_quant_port, mock_sector_port):
        mock_quant_port.get_ticker_info.return_value = Ticker(
            symbol="TSLA", sector="Consumer Cyclical", industry="Auto Manufacturers"
        )
        mock_sector_port.analyse_industry.side_effect = ValueError("Parsing Error")

        with pytest.raises(ValueError, match="Parsing Error"):
            use_case.evaluate_industry_by_ticker("TSLA")