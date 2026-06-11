import pytest
from decimal import Decimal
from domain.entities.entities import CompanyProfile, MoatSources, QualityPillars

class TestCompanyProfileEntity:
    @pytest.fixture
    def valid_profile_data(self):
        return {
            "business_description": "Tech company",
            "company_history": "Founded in 1976",
            "key_executives": [{"name": "Tim Cook", "title": "CEO", "ownership": Decimal("0.5")}],
            "revenue_model": "Hardware and Services",
            "strategy": "Innovation",
            "products_services": {"iPhone": "Smartphone"},
            "competitive_advantage": "Brand loyalty",
            "competitors": {"Samsung": "Hardware"},
            "management_insights": "Good",
            "risk_factors": {"Supply Chain": "Dependence on Asia"},
            "historical_context_crises": "Survived 2008 crisis",
            "moat_trajectory": "Expanding",
            "moat_sources": MoatSources(**{"intangible_assets": 4, "switching_costs": 3, "network_effect": 5, "cost_advantage": 2, "efficient_scale": 1}),
            "quality_pillars": QualityPillars(**{"management_quality": 4, "business_model_resilience": 5, "pricing_power": 4, "innovation_and_growth": 3, "tam_expansion": 4})
        }

    @pytest.mark.parametrize("ownership", [
        Decimal("0"),   
        Decimal("50"),   
        Decimal("100")     
    ])
    def test_valid_ceo_ownership_boundaries(self, valid_profile_data, ownership):
        data = valid_profile_data.copy()
        data["key_executives"][0]["ownership"] = ownership
        profile = CompanyProfile(**data)
        assert profile.key_executives[0]["ownership"] == ownership

    @pytest.mark.parametrize("invalid_ownership", [
        Decimal("-0.1"),  
        Decimal("100.1"),  
        Decimal("-50")     
    ])
    def test_invalid_ceo_ownership_raises_error(self, valid_profile_data, invalid_ownership):
        data = valid_profile_data.copy()
        data["key_executives"][0]["ownership"] = invalid_ownership
        with pytest.raises(ValueError, match="Executive ownership must be between 0 and 100%"):
            CompanyProfile(**data)