import pytest
from decimal import Decimal
from domain.entities.entities import CompanyProfile

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