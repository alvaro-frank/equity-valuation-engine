import os
import time
import requests_cache
import requests
from datetime import timedelta
from decimal import Decimal
from typing import Dict, Optional
from dotenv import load_dotenv

from domain.entities import Price, Stock, Ticker
from domain.ports import QuantitativeDataProvider
from infrastructure.mappers.mapper_financial_years import map_to_financial_years

load_dotenv()

class AlphaVantageAdapter(QuantitativeDataProvider):
    """
    Adapter for fetching stock data from the Alpha Vantage API. Implements the QuantitativeDataProvider interface.
    This adapter handles both current price and fundamental financial data retrieval, with built-in caching and error handling.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the adapter, setting up the API key and a 24-hour cache session.
        """
        raw_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not raw_key:
            raise ValueError("Alpha Vantage API Key not found in .env")
        
        self.api_key = raw_key.strip()

        self.session = requests_cache.CachedSession(
            'alpha_vantage_cache', 
            expire_after=timedelta(hours=24)
        )

    def _get_data(self, function: str, symbol: str) -> Dict:
        """
        Internal method to fetch data from the Alpha Vantage API for a given function and stock symbol.
        Handles rate limiting and API errors gracefully.
        
        Args:
            function (str): The Alpha Vantage API function to call (e.g., "OVERVIEW", "INCOME_STATEMENT").
            symbol (str): The stock ticker symbol to fetch data for.
            
        Raises:
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            ValueError: If the API returns an error message or if the expected data is not found in the response.
            
        Returns:
            dict: The JSON response from the Alpha Vantage API as a dictionary.
        """
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key
        }
        try:
            time.sleep(1.5) 
            
            response = self.session.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e: 
            raise ConnectionError(f"Connection Error: {e}")
        else:
            data = response.json()
            
            if "Information" in data:
                raise ConnectionError(f"Rate Limit (Speed): {data['Information']}")
            
            if "Note" in data:
                 raise ConnectionError("Rate Limit (Daily): 25 requests/day reached.")
                 
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")
                
            return data

    def get_stock_current_price(self, symbol: str) -> Price:
        """
        Fetches the current stock price for a given ticker symbol from the Alpha Vantage API.
        Handles API errors and rate limits gracefully.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the price for.
            
        Raises:
            ValueError: If the price data is not found for the given symbol or if the API returns an error message.
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            
        Returns:
            Price: Domain Entity containing the current price and currency.
        """
        data = self._get_data("GLOBAL_QUOTE", symbol)
        quote = data.get("Global Quote")
        
        if not quote:
            raise ValueError(f"Price data not found for {symbol}")
            
        price_str = quote.get("05. price")
        return Price(amount=Decimal(price_str), currency="USD")  

    def get_stock_fundamental_data(self, symbol: str) -> Stock:
        """
        Fetches the fundamental financial data for a given stock ticker symbol from the Alpha Vantage API.
        Handles API errors and rate limits gracefully, and maps the response to a Stock Entity.
        
        Args:
            symbol (str): The stock ticker symbol to fetch fundamental data for.
            
        Raises:
            ValueError: If no fundamental data is available for the given symbol.
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            
        Returns:
            Stock: Domain Entity containing the fundamental stock data.
        """
        overview = self._get_data("OVERVIEW", symbol)
        
        if not overview:
            raise ValueError(f"No fundamental data for {symbol}")
        
        updated_ticker = Ticker(
            symbol=symbol,
            name=overview.get("Name", ""),
            sector=overview.get("Sector", "Unknown"),
            industry=overview.get("Industry", "Unknown")
        )
        
        income_data = self._get_data("INCOME_STATEMENT", symbol).get("annualReports", [])
        balance_data = self._get_data("BALANCE_SHEET", symbol).get("annualReports", [])
        cash_data = self._get_data("CASH_FLOW", symbol).get("annualReports", [])

        financial_years = map_to_financial_years(income_data, balance_data, cash_data)

        price_obj = self.get_stock_current_price(symbol)

        return Stock(
            ticker=updated_ticker,
            price=price_obj,
            financial_years=financial_years
        )
        
    def get_ticker_info(self, symbol: str) -> Ticker:
        """
        Fetches only the basic metadata for a ticker (Name, Sector, Industry).
        
        Args:
            symbol (str): The stock ticker symbol to fetch the ticker data.
            
        Returns:
            Ticker: Domain Entity containing the ticker data
        """
        data = self._get_data("OVERVIEW", symbol)
        
        return Ticker(
            symbol=symbol,
            name=data.get("Name"),
            sector=data.get("Sector"),
            industry=data.get("Industry")
        )