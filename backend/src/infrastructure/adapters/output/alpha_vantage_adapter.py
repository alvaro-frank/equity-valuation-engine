import os
import time
import json
import asyncio
import httpx
from decimal import Decimal
from typing import Dict, Optional, List
from dotenv import load_dotenv

from domain.entities.entities import Price, FinancialYear, Ticker
from application.ports.ports import QuantitativeDataPort
from infrastructure.mappers.mapper_financial_years import map_to_financial_years

load_dotenv()

class AlphaVantageAdapter(QuantitativeDataPort):
    """
    Adapter for fetching stock data from the Alpha Vantage API. Implements the QuantitativeDataPort interface.
    This adapter handles both current price and fundamental financial data retrieval, with built-in caching and error handling.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None, client: Optional[httpx.AsyncClient] = None):
        """
        Initializes the adapter, setting up the API key and cache directory.
        """
        raw_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not raw_key:
            raise ValueError("Alpha Vantage API Key not found in .env")
        
        self.api_key = raw_key.strip()
        self.client = client

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.alpha_vantage_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    async def _get_data(self, function: str, symbol: str) -> Dict:
        """
        Internal method to fetch data from the Alpha Vantage API for a given function and stock symbol.
        Handles rate limiting, caching, and API errors gracefully.
        
        Args:
            function (str): The Alpha Vantage API function to call (e.g., "OVERVIEW", "INCOME_STATEMENT").
            symbol (str): The stock ticker symbol to fetch data for.
            
        Raises:
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            ValueError: If the API returns an error message or if the expected data is not found in the response.
            
        Returns:
            dict: The JSON response from the Alpha Vantage API as a dictionary.
        """
        cache_filename = f"{function}_{symbol.upper()}.json"
        cache_path = os.path.join(self.cache_dir, cache_filename)

        if os.path.exists(cache_path):
            file_age_seconds = time.time() - os.path.getmtime(cache_path)
            if file_age_seconds < 86400: # 24 hours
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    pass

        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key
        }
        try:
            await asyncio.sleep(1.5)
            
            if self.client:
                response = await self.client.get(self.BASE_URL, params=params, timeout=15)
            else:
                async with httpx.AsyncClient() as client:
                    response = await client.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
        except httpx.HTTPError as e: 
            raise ConnectionError(f"Connection Error: {e}")
        else:
            data = response.json()
            
            if "Information" in data:
                raise ConnectionError(f"Rate Limit (Speed): {data['Information']}")
            
            if "Note" in data:
                 raise ConnectionError("Rate Limit (Daily): 25 requests/day reached.")
                 
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")
            
            try:
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            except Exception:
                pass
                
            return data

    async def get_stock_current_price(self, symbol: str) -> Price:
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
        data = await self._get_data("GLOBAL_QUOTE", symbol)
        quote = data.get("Global Quote")
        
        if not quote:
            raise ValueError(f"Price data not found for {symbol}")
            
        price_str = quote.get("05. price")
        return Price(amount=Decimal(price_str), currency="USD")
    
    async def get_historical_prices(self, symbol: str) -> Dict[str, Price]:
        """
        Fetches and processes monthly historical closing prices for a given stock symbol.
        
        This method retrieves time-series data, extracts the monthly closing prices, 
        and maps them to their respective year and month.

        Args:
            symbol (str): The stock ticker symbol to retrieve historical data for.

        Returns:
            dict[str, Price]: A dictionary where keys are strings in 'YYYY-MM' format 
                              and values are Price objects containing the closing amount and currency.
        """
        data = await self._get_data("TIME_SERIES_MONTHLY", symbol)
        time_series = data.get("Monthly Time Series", {})
        
        historical_prices = {}
        for date_str, metrics in time_series.items():
            year_month = date_str[:7]
            close_price = metrics.get("4. close")
            
            if close_price:
                historical_prices[year_month] = Price(
                    amount=Decimal(close_price), 
                    currency="USD"
                )
                
        return historical_prices
        

    async def get_stock_fundamental_data(self, symbol: str) -> List[FinancialYear]:
        """
        Fetches the fundamental financial data for a given stock ticker symbol from the Alpha Vantage API.
        Handles API errors and rate limits gracefully, and maps the response to a List of Financial Year Domain Entities.
        
        Args:
            symbol (str): The stock ticker symbol to fetch fundamental data for.
            
        Raises:
            ValueError: If no fundamental data is available for the given symbol.
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            
        Returns:
            List[FinancialYear]: List containing the fundamental stock data for each Financial Year.
        """
        income_stmt = await self._get_data("INCOME_STATEMENT", symbol)
        balance_sheet = await self._get_data("BALANCE_SHEET", symbol)
        cash_flow = await self._get_data("CASH_FLOW", symbol)

        income_data = income_stmt.get("annualReports", [])
        balance_data = balance_sheet.get("annualReports", [])
        cash_data = cash_flow.get("annualReports", [])

        historical_prices = await self.get_historical_prices(symbol)
        
        financial_years = map_to_financial_years(income_data, balance_data, cash_data, historical_prices)
        return financial_years
        
    async def get_ticker_info(self, symbol: str) -> Ticker:
        """
        Fetches only the basic metadata for a ticker (Name, Sector, Industry).
        
        Args:
            symbol (str): The stock ticker symbol to fetch the ticker data.
            
        Returns:
            Ticker: Domain Entity containing the ticker data
        """
        data = await self._get_data("OVERVIEW", symbol)
        
        return Ticker(
            symbol=symbol,
            name=data.get("Name"),
            sector=data.get("Sector"),
            industry=data.get("Industry")
        )