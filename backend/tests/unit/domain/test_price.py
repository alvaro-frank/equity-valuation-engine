import pytest
from decimal import Decimal
from domain.entities.entities import Price

class TestPriceEntity:
    def test_valid_price_creation(self):
        price = Price(amount=Decimal("150.50"), currency="EUR")
        
        assert price.amount == Decimal("150.50")
        assert price.currency == "EUR"

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price amount cannot be negative"):
            Price(amount=Decimal("-10.00"))