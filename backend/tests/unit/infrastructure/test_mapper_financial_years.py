import pytest
from decimal import Decimal
from infrastructure.mappers.mapper_financial_years import parse_decimal

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