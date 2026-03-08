import pytest
from decimal import Decimal
from domain.entities.entities import MetricPoint, QuantitativeAnalysis

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