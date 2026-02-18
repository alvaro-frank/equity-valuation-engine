import os
import time
import requests_cache
from datetime import timedelta
from decimal import Decimal
from typing import List, Optional
from dotenv import load_dotenv

from domain.interfaces import QuantitativeDataProvider
from services.dtos import FinancialYearDTO, PriceDTO, QuantitativeDataDTO, TickerDTO

load_dotenv()

class AlphaVantageAdapter(QuantitativeDataProvider):
    """
    Adapter for fetching stock data from the Alpha Vantage API. Implements the QuantitativeDataProvider interface.
    This adapter handles both current price and fundamental financial data retrieval, with built-in caching and error handling.
    """
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
        
    def _parse_decimal(self, value: str) -> Decimal:
        """
        Safely parses a string value to Decimal, returning 0 if the value is None or invalid.
        
        Args:
            value (str): The string value to parse.
            
        Raises:
            ValueError: If the value cannot be parsed to a Decimal and is not None or "None".
            
        Returns:
            Decimal: The parsed decimal value, or 0 if the input is invalid.
        """
        if not value or value == "None":
            return Decimal("0")
        return Decimal(value)
    
    def _map_to_financial_years(self, income_list, balance_list, cash_list) -> List[FinancialYearDTO]:
        years = []

        for income_report in income_list:
            fiscal_date = income_report.get("fiscalDateEnding")
            
            balance_report = next((b for b in balance_list if b.get("fiscalDateEnding") == fiscal_date), {})
            cash_report = next((c for c in cash_list if c.get("fiscalDateEnding") == fiscal_date), {})
            
            st_debt = self._parse_decimal(balance_report.get("shortTermDebt", "0"))
            lt_debt = self._parse_decimal(balance_report.get("longTermDebt", "0"))
            total_debt_calculated = st_debt + lt_debt
            
            year_data = FinancialYearDTO(
                fiscal_date_ending=fiscal_date,
                # Revenue and Earnings
                revenue=self._parse_decimal(income_report.get("totalRevenue", "0")),
                ebitda=self._parse_decimal(income_report.get("ebitda", "0")),
                # Gross Profit and Operating Income
                gross_profit=self._parse_decimal(income_report.get("grossProfit", "0")),
                operating_income=self._parse_decimal(income_report.get("operatingIncome", "0")),
                # Net Income
                net_income=self._parse_decimal(income_report.get("netIncome", "0")),
                #Cash Flow
                operating_cash_flow=self._parse_decimal(cash_report.get("operatingCashflow", "0")),
                capital_expenditures=self._parse_decimal(cash_report.get("capitalExpenditures", "0")),
                # Shares Outstanding
                shares_outstanding=self._parse_decimal(balance_report.get("commonStockSharesOutstanding", "0")),
                # Debt
                short_term_debt=st_debt,
                long_term_debt=lt_debt,
                total_debt=total_debt_calculated,
                # Assets and Liabilities
                total_assets=self._parse_decimal(balance_report.get("totalAssets", "0")),
                total_liabilities=self._parse_decimal(balance_report.get("totalLiabilities", "0")),
                cash_and_equivalents=self._parse_decimal(balance_report.get("cashAndCashEquivalentsAtCarryingValue", "0")),
            )
            
            years.append(year_data)
        
        return years

    def get_stock_current_price(self, symbol: str) -> PriceDTO:
        """
        Fetches the current stock price for a given ticker symbol from the Alpha Vantage API.
        Handles API errors and rate limits gracefully.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the price for.
            
        Raises:
            ValueError: If the price data is not found for the given symbol or if the API returns an error message.
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            
        Returns:
            PriceDTO: A data transfer object containing the current price and currency.
        """
        data = self._get_data("GLOBAL_QUOTE", symbol)
        quote = data.get("Global Quote")
        
        if not quote:
            raise ValueError(f"Price data not found for {symbol}")
            
        price_str = quote.get("05. price")
        return PriceDTO(amount=Decimal(price_str), currency="USD")  

    def get_stock_fundamental_data(self, symbol: str) -> QuantitativeDataDTO:
        """
        Fetches the fundamental financial data for a given stock ticker symbol from the Alpha Vantage API.
        Handles API errors and rate limits gracefully, and maps the response to a QuantitativeDataDTO.
        
        Args:
            symbol (str): The stock ticker symbol to fetch fundamental data for.
            
        Raises:
            ValueError: If no fundamental data is available for the given symbol.
            ConnectionError: If there are issues connecting to the Alpha Vantage API or if rate limits are exceeded.
            
        Returns:
            QuantitativeDataDTO: A data transfer object containing the fundamental stock data.
        """
        overview = self._get_data("OVERVIEW", symbol)
        
        if not overview:
            raise ValueError(f"No fundamental data for {symbol}")
        
        updated_ticker = TickerDTO(
            symbol=symbol,
            name=overview.get("Name", ""),
            sector=overview.get("Sector", "Unknown"),
            industry=overview.get("Industry", "Unknown")
        )
        
        income_data = self._get_data("INCOME_STATEMENT", symbol).get("annualReports", [])
        balance_data = self._get_data("BALANCE_SHEET", symbol).get("annualReports", [])
        cash_data = self._get_data("CASH_FLOW", symbol).get("annualReports", [])

        financial_years = self._map_to_financial_years(income_data, balance_data, cash_data)

        price_obj = self.get_stock_current_price(symbol)

        return QuantitativeDataDTO(
            ticker=updated_ticker,
            price=price_obj,
            financial_years=financial_years
        )