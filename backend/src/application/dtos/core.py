from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, List

class TickerSearchDTO(BaseModel):
    """
    Data Transfer Object representing a search result for a stock ticker, including symbol, name, and exchange.
    """
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    exchange: str = Field(..., description="Exchange name")

class TickerSearchResult(BaseModel):
    """
    Data Transfer Object representing the results of a stock ticker search.
    """
    results: List[TickerSearchDTO] = Field(..., description="List of search results")

class TrendingTickerDTO(BaseModel):
    """
    Data Transfer Object representing a trending stock ticker, including symbol, name, and performance metrics.
    """
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    rating: Optional[str] = Field(None, description="Analyst rating")
    weight: Optional[float] = Field(None, description="Market weight in sector/industry")

class TrendingTickerResult(BaseModel):
    """
    Data Transfer Object representing the results of a trending stock ticker search.
    """
    results: List[TrendingTickerDTO] = Field(..., description="List of trending tickers")

class TickerResult(BaseModel):
    """
    Data Transfer Object representing the ticker information of a stock, including symbol, name, sector, and industry.
    """
    model_config = ConfigDict(frozen=True)
    
    symbol: str = Field(..., description="Ticker symbol")
    name: str = Field(..., description="Company name")
    sector: str = Field(..., description="Company sector")
    sector_key: Optional[str] = Field(None, description="yfinance sector key")
    industry: str = Field(..., description="Company industry")
    industry_key: Optional[str] = Field(None, description="yfinance industry key")
    market_cap: Optional[Decimal] = Field(None, description="Current market capitalization")
    pe_ratio: Optional[Decimal] = Field(None, description="Live Price-to-Earnings Ratio")
    forward_pe: Optional[Decimal] = Field(None, description="Forward Price-to-Earnings Ratio")
    current_price: Optional[Decimal] = Field(None, description="Live Stock Price")
    regular_market_change: Optional[Decimal] = Field(None, description="Live Market Price Change")
    regular_market_change_percent: Optional[Decimal] = Field(None, description="Live Market Price Change Percentage")

class LocalFilingDTO(BaseModel):
    """
    Data Transfer Object representing a cached SEC filing document.
    """
    id: str = Field(..., description="Unique identifier or file path for the document")
    form_type: str = Field(..., description="Type of filing (e.g. 10-K, 10-Q)")
    period: str = Field(..., description="Period string (e.g. FY2025, 2026-Q1)")
    accession_number: str = Field(..., description="SEC Accession Number")

class LocalFilingListResult(BaseModel):
    """
    Data Transfer Object representing a list of cached SEC filing documents.
    """
    filings: List[LocalFilingDTO] = Field(..., description="List of local filings")
