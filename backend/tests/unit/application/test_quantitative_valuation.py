import pytest
from decimal import Decimal

from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from domain.entities.entities import Ticker, FinancialYear
from application.dtos.dtos import QuantitativeValuationResult

class TestQuantitativeValuationUseCase:

    @pytest.fixture
    def mock_quant_adapter(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def use_case(self, mock_quant_adapter):
        return QuantitativeValuationUseCase(adapter=mock_quant_adapter)

    def test_evaluate_ticker_happy_path(self, use_case, mock_quant_adapter):
        mock_quant_adapter.get_ticker_info.return_value = Ticker(
            symbol="AAPL", name="Apple", sector="Tech", industry="Hardware"
        )

        fy_recent = FinancialYear(
            fiscal_date_ending="2023-12-31", revenue=Decimal("110"), ebitda=Decimal("0"),
            gross_profit=Decimal("0"), operating_income=Decimal("0"), net_income=Decimal("0"), 
            operating_cash_flow=Decimal("0"), capital_expenditures=Decimal("0"), 
            shares_outstanding=Decimal("10"), short_term_debt=Decimal("0"), 
            long_term_debt=Decimal("0"), total_debt=Decimal("0"), total_assets=Decimal("100"),
            total_liabilities=Decimal("0"), cash_and_equivalents=Decimal("0")
        )
        fy_old = FinancialYear(
            fiscal_date_ending="2022-12-31", revenue=Decimal("100"), ebitda=Decimal("0"),
            gross_profit=Decimal("0"), operating_income=Decimal("0"), net_income=Decimal("0"), 
            operating_cash_flow=Decimal("0"), capital_expenditures=Decimal("0"), 
            shares_outstanding=Decimal("10"), short_term_debt=Decimal("0"), 
            long_term_debt=Decimal("0"), total_debt=Decimal("0"), total_assets=Decimal("100"),
            total_liabilities=Decimal("0"), cash_and_equivalents=Decimal("0")
        )

        mock_quant_adapter.get_stock_fundamental_data.return_value = [fy_recent, fy_old]

        result = use_case.evaluate_ticker("AAPL", years=2)

        assert isinstance(result, QuantitativeValuationResult)
        assert result.ticker.symbol == "AAPL"
        
        assert "revenue" in result.metrics
        assert len(result.metrics["revenue"].yearly_data) == 2
        
        assert result.metrics["revenue"].cagr == Decimal("10.00")

        mock_quant_adapter.get_ticker_info.assert_called_once_with("AAPL")
        mock_quant_adapter.get_stock_fundamental_data.assert_called_once_with("AAPL")

    def test_calculate_cagr_happy_path(self):
        values = [Decimal("121"), Decimal("110"), Decimal("100")]
        cagr = QuantitativeValuationUseCase.calculate_cagr(values)
        assert cagr == Decimal("10.00")

    def test_cagr_returns_none_with_insufficient_data(self):
        values = [Decimal("100")]
        cagr = QuantitativeValuationUseCase.calculate_cagr(values)
        assert cagr is None 

    @pytest.mark.parametrize("recent_val, old_val", [
        (Decimal("100"), Decimal("-50")),
        (Decimal("-20"), Decimal("100")), 
        (Decimal("100"), Decimal("0")),  
    ])
    def test_cagr_returns_none_with_invalid_values(self, recent_val, old_val):
        values = [recent_val, Decimal("50"), old_val]
        cagr = QuantitativeValuationUseCase.calculate_cagr(values)
        assert cagr is None