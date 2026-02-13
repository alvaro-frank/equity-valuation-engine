import os
import time
import requests_cache
from datetime import timedelta
from decimal import Decimal
from typing import List, Optional
from dotenv import load_dotenv

from domain.interfaces import StockDataProvider
from domain.stock_market import Stock, Ticker, Price

load_dotenv()

class AlphaVantageAdapter(StockDataProvider):
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None):
        raw_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not raw_key:
            raise ValueError("Alpha Vantage API Key not found in .env")
        
        self.api_key = raw_key.strip()

        self.session = requests_cache.CachedSession(
            'alpha_vantage_cache', 
            expire_after=timedelta(hours=24)
        )

    def _get_data(self, function: str, symbol: str) -> dict:
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key
        }
        try:
            time.sleep(1.5) 
            
            response = self.session.get(self.BASE_URL, params=params, timeout=15)
            data = response.json()
            
            if "Information" in data:
                raise ConnectionError(f"Rate Limit (Speed): {data['Information']}")
            
            if "Note" in data:
                 raise ConnectionError("Rate Limit (Daily): 25 requests/day reached.")
                 
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")
                
            return data
        except Exception as e:
            if isinstance(e, (ConnectionError, ValueError)):
                raise e
            raise ConnectionError(f"Alpha Vantage Connection Error: {e}")

    def get_stock_current_price(self, ticker: Ticker) -> Price:
        data = self._get_data("GLOBAL_QUOTE", ticker.symbol)
        quote = data.get("Global Quote")
        
        if not quote:
            raise ValueError(f"Price data not found for {ticker.symbol}")
            
        price_str = quote.get("05. price")
        return Price(amount=Decimal(price_str), currency="USD")

    def get_stock_fundamental_data(self, ticker: Ticker) -> Stock:
        overview = self._get_data("OVERVIEW", ticker.symbol)
        
        if not overview:
            raise ValueError(f"No fundamental data for {ticker.symbol}")

        price_obj = self.get_stock_current_price(ticker)

        return Stock(
            ticker=ticker,
            price=price_obj
        )