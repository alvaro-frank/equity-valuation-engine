import os
import time
import requests_cache
from datetime import timedelta
from decimal import Decimal
from typing import List, Optional
from dotenv import load_dotenv

from domain.interfaces import StockDataProvider
from domain.stock_market import FinancialYear, Stock, Ticker, Price

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
        
    def _parse_decimal(self, value: str) -> Decimal:
        if not value or value == "None":
            return Decimal("0")
        return Decimal(value)
    
    def _map_to_financial_years(self, income_list, balance_list, cash_list) -> List[FinancialYear]:
        years = []

        for income_report in income_list:
            fiscal_date = income_report.get("fiscalDateEnding")
            
            balance_report = next((b for b in balance_list if b.get("fiscalDateEnding") == fiscal_date), {})
            cash_report = next((c for c in cash_list if c.get("fiscalDateEnding") == fiscal_date), {})
            
            st_debt = self._parse_decimal(balance_report.get("shortTermDebt", "0"))
            lt_debt = self._parse_decimal(balance_report.get("longTermDebt", "0"))
            total_debt_calculated = st_debt + lt_debt
            
            year_data = FinancialYear(
                fiscal_date_ending=fiscal_date,
                revenue=self._parse_decimal(income_report.get("totalRevenue", "0")),
                net_income=self._parse_decimal(income_report.get("netIncome", "0")),
                ebitda=self._parse_decimal(income_report.get("ebitda", "0")),
                operating_cash_flow=self._parse_decimal(cash_report.get("operatingCashflow", "0")),
                capital_expenditures=self._parse_decimal(cash_report.get("capitalExpenditures", "0")),
                total_assets=self._parse_decimal(balance_report.get("totalAssets", "0")),
                total_liabilities=self._parse_decimal(balance_report.get("totalLiabilities", "0")),
                cash_and_equivalents=self._parse_decimal(balance_report.get("cashAndCashEquivalentsAtCarryingValue", "0")),
                total_debt=total_debt_calculated,
                shares_outstanding=self._parse_decimal(balance_report.get("commonStockSharesOutstanding", "0"))
            )
            
            years.append(year_data)
        
        return years

    def get_stock_current_price(self, ticker: Ticker) -> Price:
        data = self._get_data("GLOBAL_QUOTE", ticker.symbol)
        quote = data.get("Global Quote")
        
        if not quote:
            raise ValueError(f"Price data not found for {ticker.symbol}")
            
        price_str = quote.get("05. price")
        return Price(amount=Decimal(price_str), currency="USD")  

    def get_stock_fundamental_data(self, ticker: Ticker) -> Stock:
        overview = self._get_data("OVERVIEW", ticker.symbol)
        updated_ticker = Ticker(
            symbol=ticker.symbol,
            name=overview.get("Name", ""),
            sector=overview.get("Sector", "Unknown"),
            industry=overview.get("Industry", "Unknown")
        )
        
        if not overview:
            raise ValueError(f"No fundamental data for {ticker.symbol}")
        
        income_data = self._get_data("INCOME_STATEMENT", ticker.symbol).get("annualReports", [])
        balance_data = self._get_data("BALANCE_SHEET", ticker.symbol).get("annualReports", [])
        cash_data = self._get_data("CASH_FLOW", ticker.symbol).get("annualReports", [])

        financial_years = self._map_to_financial_years(income_data, balance_data, cash_data)

        price_obj = self.get_stock_current_price(updated_ticker)

        return Stock(
            ticker=updated_ticker,
            price=price_obj,
            financial_years=financial_years
        )