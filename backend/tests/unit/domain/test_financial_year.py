import pytest
from decimal import Decimal
from domain.entities.entities import FinancialYear

class TestFinancialYearEntity:
    @pytest.fixture
    def valid_financial_year_data(self):
        return {
            "fiscal_date_ending": "2023-12-31",
            "revenue": Decimal("1000"),
            "ebitda": Decimal("200"),
            "gross_profit": Decimal("500"),
            "operating_income": Decimal("150"),
            "net_income": Decimal("100"),
            "operating_cash_flow": Decimal("120"),
            "capital_expenditures": Decimal("50"),
            "shares_outstanding": Decimal("100"),
            "short_term_debt": Decimal("20"),
            "long_term_debt": Decimal("80"),
            "total_debt": Decimal("100"),
            "total_assets": Decimal("500"),
            "total_liabilities": Decimal("300"),
            "cash_and_equivalents": Decimal("50"),
            "year_end_price": Decimal("10")
        }

    def test_valid_financial_year_creation(self, valid_financial_year_data):
        fy = FinancialYear(**valid_financial_year_data)
        
        assert fy.shares_outstanding == Decimal("100")
        assert fy.year_end_price == Decimal("10")

    @pytest.mark.parametrize("field, invalid_value", [
        ("shares_outstanding", Decimal("-1")),
        ("total_assets", Decimal("-100")),
        ("total_debt", Decimal("-50")),
    ])
    def test_financial_year_invariants(self, valid_financial_year_data, field, invalid_value):
        data = valid_financial_year_data.copy()
        data[field] = invalid_value
        
        with pytest.raises(ValueError, match="Domain Error"):
            FinancialYear(**data)
            
    def test_financial_ratios_calculation(self, valid_financial_year_data):
        fy = FinancialYear(**valid_financial_year_data)
        
        assert fy.total_equity == Decimal("200") 
        assert fy.gross_margin == Decimal("50.00") 
        assert fy.operating_margin == Decimal("15.00") 
        assert fy.net_margin == Decimal("10.00") 
        assert fy.roe == Decimal("50.00") 
        assert fy.roic == Decimal("33.33") 
        assert fy.debt_to_equity == Decimal("0.50") 
        
        assert fy.market_cap == Decimal("1000")
        assert fy.pe_ratio == Decimal("10.00")
        assert fy.pb_ratio == Decimal("5.00")
        assert fy.ps_ratio == Decimal("1.00")
        assert fy.fcf_yield == Decimal("7.00")

    @pytest.mark.parametrize("field_to_zero, property_to_check", [
        ("revenue", "gross_margin"),
        ("revenue", "operating_margin"),
        ("revenue", "net_margin"),
        ("revenue", "ps_ratio"),
    ])
    def test_margins_handle_zero_revenue(self, valid_financial_year_data, field_to_zero, property_to_check):
        data = valid_financial_year_data.copy()
        data[field_to_zero] = Decimal("0")
        fy = FinancialYear(**data)
        
        if property_to_check == "ps_ratio":
            assert getattr(fy, property_to_check) is None
        else:
            assert getattr(fy, property_to_check) == Decimal("0")

    def test_ratios_handle_zero_equity_and_capital(self, valid_financial_year_data):
        data = valid_financial_year_data.copy()
        data["total_assets"] = Decimal("300")
        data["total_liabilities"] = Decimal("300")
        data["total_debt"] = Decimal("0")
        
        fy = FinancialYear(**data)
        
        assert fy.total_equity == Decimal("0")
        assert fy.roe is None
        assert fy.roic is None
        assert fy.debt_to_equity is None
        assert fy.pb_ratio is None