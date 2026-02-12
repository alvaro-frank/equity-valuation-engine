from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional

class StockDataDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    symbol: str = Field(..., description="Ticker symbol")
    price: Decimal = Field(..., description="Current market price")
    currency: str = Field(..., description="Currency of the price (e.g., USD)")
    eps: Decimal = Field(..., description="Earnings Per Share (Trailing)")
    pe_ratio: Optional[Decimal] = Field(None, description="Price-to-Earnings Ratio. None if EPS is zero or data is unavailable.")