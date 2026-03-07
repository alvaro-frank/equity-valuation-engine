import pytest
from decimal import Decimal
from domain.entities.entities import (
    Price, 
    FinancialYear, 
    CompanyProfile, 
    MetricPoint, 
    QuantitativeAnalysis
)

class TestPriceEntity:
    def test_valid_price_creation(self):
        price = Price(amount=Decimal("150.50"), currency="EUR")
        
        assert price.amount == Decimal("150.50")
        assert price.currency == "EUR"

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price amount cannot be negative"):
            Price(amount=Decimal("-10.00"))

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
        }

    def test_valid_financial_year_creation(self, valid_financial_year_data):
        fy = FinancialYear(**valid_financial_year_data)
        
        assert fy.shares_outstanding == Decimal("100")

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

class TestCompanyProfileEntity:
    @pytest.fixture
    def valid_profile_data(self):
        return {
            "business_description": "Tech company",
            "company_history": "Founded in 1976",
            "ceo_name": "Tim Cook",
            "ceo_ownership": Decimal("0.5"),
            "major_shareholders": {"Vanguard": Decimal("8.0")},
            "revenue_model": "Hardware and Services",
            "strategy": "Innovation",
            "products_services": {"iPhone": "Smartphone"},
            "competitive_advantage": "Brand loyalty",
            "competitors": {"Samsung": "Hardware"},
            "management_insights": "Good",
            "risk_factors": {"Supply Chain": "Dependence on Asia"},
            "historical_context_crises": "Survived 2008 crisis"
        }

    @pytest.mark.parametrize("ownership", [
        Decimal("0"),   
        Decimal("50"),   
        Decimal("100")     
    ])
    def test_valid_ceo_ownership_boundaries(self, valid_profile_data, ownership):
        data = valid_profile_data.copy()
        data["ceo_ownership"] = ownership
        profile = CompanyProfile(**data)
        assert profile.ceo_ownership == ownership

    @pytest.mark.parametrize("invalid_ownership", [
        Decimal("-0.1"),  
        Decimal("100.1"),  
        Decimal("-50")     
    ])
    def test_invalid_ceo_ownership_raises_error(self, valid_profile_data, invalid_ownership):
        data = valid_profile_data.copy()
        data["ceo_ownership"] = invalid_ownership
        with pytest.raises(ValueError, match="CEO ownership must be between 0 and 100%"):
            CompanyProfile(**data)

class TestQuantitativeAnalysis:
    def test_calculate_cagr_happy_path(self):
        points = [
            MetricPoint(date="2023", value=Decimal("121")),
            MetricPoint(date="2022", value=Decimal("110")),
            MetricPoint(date="2021", value=Decimal("100")),
        ]
        
        analysis = QuantitativeAnalysis.create_analysis("Revenue", points)
        
        assert analysis.cagr == Decimal("10.00")

    def test_cagr_fails_gracefully_with_insufficient_data(self):
        points = [MetricPoint(date="2023", value=Decimal("100"))]
        
        analysis = QuantitativeAnalysis.create_analysis("Revenue", points)
        
        assert analysis.cagr is None 

    @pytest.mark.parametrize("recent_val, old_val", [
        (Decimal("100"), Decimal("-50")),
        (Decimal("-20"), Decimal("100")), 
        (Decimal("100"), Decimal("0")),  
    ])
    def test_cagr_fails_gracefully_with_invalid_values(self, recent_val, old_val):
        points = [
            MetricPoint(date="2023", value=recent_val),
            MetricPoint(date="2022", value=Decimal("50")),
            MetricPoint(date="2021", value=old_val),
        ]
        
        analysis = QuantitativeAnalysis.create_analysis("Net Income", points)
        
        assert analysis.cagr is None 