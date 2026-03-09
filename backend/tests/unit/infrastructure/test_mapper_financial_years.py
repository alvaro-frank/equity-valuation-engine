import pytest
from decimal import Decimal

from domain.entities.entities import Price, FinancialYear
from infrastructure.mappers.mapper_financial_years import parse_decimal, map_to_financial_years

class TestParseDecimal:
    
    @pytest.mark.parametrize("valid_input, expected_output", [
        ("150.50", Decimal("150.50")), 
        (100, Decimal("100")),        
        (10.5, Decimal("10.5")),     
        ("0", Decimal("0")),           
    ])
    def test_parse_decimal_valid_inputs(self, valid_input, expected_output):
        result = parse_decimal(valid_input, "test_field")
        
        assert result == expected_output
        assert isinstance(result, Decimal)

    @pytest.mark.parametrize("missing_input", [
        None,
        "None",
        "",
    ])
    def test_parse_decimal_handles_missing_data_as_zero(self, missing_input):
        result = parse_decimal(missing_input, "test_field")
        
        assert result == Decimal("0")

    @pytest.mark.parametrize("corrupted_input", [
        "N/A",           
        "ERROR",         
        {"value": 10},  
        [1, 2, 3],       
    ])
    def test_parse_decimal_fails_fast_on_corrupted_data(self, corrupted_input):
        with pytest.raises(ValueError, match="Data Integrity Error"):
            parse_decimal(corrupted_input, "test_field")


class TestMapToFinancialYears:

    @pytest.fixture
    def mock_income(self):
        return [{"fiscalDateEnding": "2023-12-31", "totalRevenue": "1000", "netIncome": "200"}]

    @pytest.fixture
    def mock_balance(self):
        return [{"fiscalDateEnding": "2023-12-31", "totalAssets": "5000", "totalLiabilities": "2000", "commonStockSharesOutstanding": "100"}]

    @pytest.fixture
    def mock_cash(self):
        return [{"fiscalDateEnding": "2023-12-31", "operatingCashflow": "300", "capitalExpenditures": "50"}]

    @pytest.fixture
    def mock_prices(self):
        return {"2023-12": Price(amount=Decimal("150.50"), currency="USD")}

    def test_map_to_financial_years_happy_path(self, mock_income, mock_balance, mock_cash, mock_prices):
        years = map_to_financial_years(mock_income, mock_balance, mock_cash, mock_prices)
        
        assert len(years) == 1
        assert isinstance(years[0], FinancialYear)
        assert years[0].fiscal_date_ending == "2023-12-31"
        assert years[0].revenue == Decimal("1000")
        assert years[0].total_assets == Decimal("5000")
        assert years[0].operating_cash_flow == Decimal("300")
        assert years[0].year_end_price == Decimal("150.50")

    def test_map_to_financial_years_missing_price_defaults_to_zero(self, mock_income, mock_balance, mock_cash):
        empty_prices = {}
        years = map_to_financial_years(mock_income, mock_balance, mock_cash, empty_prices)
        
        assert len(years) == 1
        assert years[0].year_end_price == Decimal("0")

    def test_map_to_financial_years_missing_balance_sheet(self, mock_income, mock_cash, mock_prices):
        empty_balance = []
        with pytest.raises(ValueError, match="Missing data on date: 2023-12-31"):
            map_to_financial_years(mock_income, empty_balance, mock_cash, mock_prices)

    def test_map_to_financial_years_skips_missing_fiscal_date(self, mock_balance, mock_cash, mock_prices):
        invalid_income = [{"totalRevenue": "1000"}] 
        years = map_to_financial_years(invalid_income, mock_balance, mock_cash, mock_prices)
        
        assert len(years) == 0