import os
import time
import json
import asyncio
import httpx
from loguru import logger

import pandas as pd
from decimal import Decimal
from typing import Dict, Optional, List
from dotenv import load_dotenv

from domain.entities import Price, LiveQuote, FinancialYear, FinancialQuarter, Ticker
from domain.entities.earnings import EarningsCallTranscript
from application.ports.core_financial_ports import QuantitativeDataPort, OwnershipDataPort, PerformanceDataPort, TranscriptDataPort
from application.ports.discovery_ports import SearchDataPort
from application.exceptions.exceptions import TickerNotFoundError, RateLimitExceededError, ConfigurationError, ExternalServiceError
from infrastructure.config.settings import settings
from infrastructure.mappers.alphavantage_mapper import map_to_financial_years, map_to_financial_quarters, calculate_ttm_year

load_dotenv()

class AlphaVantageAdapter(QuantitativeDataPort, OwnershipDataPort, PerformanceDataPort, SearchDataPort, TranscriptDataPort):
    """
    Adapter for fetching stock data from the Alpha Vantage API. Implements the QuantitativeDataPort interface.
    This adapter handles both current price and fundamental financial data retrieval, with built-in caching and error handling.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None, client: Optional[httpx.AsyncClient] = None):
        """
        Initializes the adapter, setting up the API key and cache directory.
        
        Args:
            api_key (Optional[str]): The API key for Alpha Vantage. If not provided,
        """
        if not api_key:
            raise ConfigurationError("Alpha Vantage API Key is required")
        
        self.api_key = api_key.strip()
        self.client = client
        self._in_flight_requests: Dict[str, asyncio.Task] = {}

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.cache_dir = os.path.join(base_dir, '.alpha_vantage_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_ttl_for_function(self, function: str) -> float:
        """
        Returns the appropriate Time-To-Live (TTL) in seconds for a given Alpha Vantage API function.
        """
        if function == "GLOBAL_QUOTE":
            return 86400.0  # 2 minutes for live quotes
        elif function == "INSTITUTIONAL_HOLDINGS":
            return 604800.0  # 7 days (1 week) for institutional holdings
        elif function == "EARNINGS_CALL_TRANSCRIPT":
            return 2592000.0 # 30 days for historical transcripts
        else:
            return 86400.0  # 24 hours for all other endpoints (Financials, Overview, Monthly Time Series)

    async def _get_data(self, function: str, symbol: str, **kwargs) -> Dict:
        """
        Internal method to fetch data from the Alpha Vantage API for a given function and stock symbol.
        Handles rate limiting, caching, and API errors gracefully.
        
        Args:
            function (str): The Alpha Vantage API function to call (e.g., "OVERVIEW", "INCOME_STATEMENT").
            symbol (str): The stock ticker symbol to fetch data for.
            **kwargs: Extra query parameters for the API.
            
        Returns:
            dict: The JSON response from the Alpha Vantage API as a dictionary.
        """
        ticker_cache_dir = os.path.join(self.cache_dir, symbol.upper())
        os.makedirs(ticker_cache_dir, exist_ok=True)
        
        # Build cache filename with optional suffix based on kwargs
        suffix = ""
        if "year" in kwargs and "quarter" in kwargs:
            suffix = f"_{kwargs['year']}_Q{kwargs['quarter']}"
            
        cache_filename = f"{function}{suffix}.json"
        cache_path = os.path.join(ticker_cache_dir, cache_filename)

        ttl_seconds = self._get_ttl_for_function(function)

        if os.path.exists(cache_path):
            file_age_seconds = time.time() - os.path.getmtime(cache_path)
            if file_age_seconds < ttl_seconds:
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    pass

        # In-flight request deduplication
        if cache_filename in self._in_flight_requests:
            return await self._in_flight_requests[cache_filename]
            
        # Create a new task and store it
        task = asyncio.create_task(self._fetch_and_cache(function, symbol, cache_path, **kwargs))
        self._in_flight_requests[cache_filename] = task
        try:
            return await task
        finally:
            self._in_flight_requests.pop(cache_filename, None)
            
    async def _fetch_and_cache(self, function: str, symbol: str, cache_path: str, **kwargs) -> Dict:
        params = {
            "function": function
        }
        
        if function == "SYMBOL_SEARCH":
            params["keywords"] = symbol
        else:
            params["symbol"] = symbol
            
        params.update(kwargs)
        
        # Alpha Vantage expects quarter="2024Q1" for transcripts, not year=2024 & quarter=1
        if function == "EARNINGS_CALL_TRANSCRIPT" and "year" in params and "quarter" in params:
            params["quarter"] = f"{params['year']}Q{params['quarter']}"
            del params["year"]
            
        # VERY IMPORTANT: Alpha Vantage has a bug where the 'demo' key fails for EARNINGS_CALL_TRANSCRIPT
        # if 'apikey' is not the LAST parameter in the query string.
        # Python 3.7+ preserves dict insertion order, and httpx preserves it in the URL.
        params["apikey"] = self.api_key
            
        max_retries = 3
        
        for attempt in range(max_retries):
            try:                
                if self.client:
                    response = await self.client.get(self.BASE_URL, params=params, timeout=15)
                else:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(self.BASE_URL, params=params, timeout=15)
                response.raise_for_status()
            except httpx.HTTPError as e:
                if attempt == max_retries - 1:
                    raise ExternalServiceError(f"Connection Error after {max_retries} attempts: {e}")
                await asyncio.sleep(2 ** attempt)
                continue
                
            data = response.json()
            
            if "Information" in data:
                if attempt == max_retries - 1:
                    raise RateLimitExceededError(f"Rate Limit (Speed) Exceeded after {max_retries} attempts: {data['Information']}")
                # Exponential backoff for rate limits: 1s, 2s, 4s...
                await asyncio.sleep(2 ** attempt)
                continue
                
            if "Note" in data:
                 raise RateLimitExceededError("Rate Limit (Daily): 25 requests/day reached.")
                 
            if "Error Message" in data:
                raise TickerNotFoundError(f"API Error: {data['Error Message']}")
            
            try:
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            except Exception:
                pass
                
            return data

    async def get_stock_current_price(self, symbol: str) -> LiveQuote:
        """
        Fetches the current stock price and quote for the given symbol using Alpha Vantage.
        
        Args:
            symbol (str): The stock ticker symbol (e.g., "AAPL").
            
        Returns:
            LiveQuote: An object containing the current price, change, and live support flag.
        """
        data = await self._get_data("GLOBAL_QUOTE", symbol)
        
        if not data or "Global Quote" not in data or not data["Global Quote"]:
            raise TickerNotFoundError(f"Price data not found for {symbol}")
            
        quote = data["Global Quote"]
        try:
            amount_str = quote.get("05. price")
            if not amount_str:
                raise ValueError("Price field missing")
            amount = Decimal(str(amount_str))
            
            change = None
            change_str = quote.get("09. change")
            if change_str and change_str not in ["None", "-"]:
                change = Decimal(str(change_str))
                
            change_percent = None
            change_percent_str = quote.get("10. change percent")
            if change_percent_str and "%" in change_percent_str:
                change_percent = Decimal(change_percent_str.replace("%", ""))
            
            return LiveQuote(
                amount=amount, 
                currency="USD",
                change=change,
                change_percent=change_percent,
                is_live_supported=settings.alpha_vantage_enable_live_polling
            )
        except Exception as e:
            raise TickerNotFoundError(f"Error parsing price data: {e}")
    
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
        data = await self._get_data("TIME_SERIES_MONTHLY_ADJUSTED", symbol)
        time_series = data.get("Monthly Adjusted Time Series", {})
        
        historical_prices = {}
        for date_str, metrics in time_series.items():
            year_month = date_str[:7]
            close_price = metrics.get("5. adjusted close")
            
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
            
        Returns:
            List[FinancialYear]: List containing the fundamental stock data for each Financial Year.
        """
        income_task = self._get_data("INCOME_STATEMENT", symbol)
        balance_task = self._get_data("BALANCE_SHEET", symbol)
        cash_task = self._get_data("CASH_FLOW", symbol)
        prices_task = self.get_historical_prices(symbol)
        
        income_stmt, balance_sheet, cash_flow, historical_prices = await asyncio.gather(
            income_task, balance_task, cash_task, prices_task
        )

        income_data = income_stmt.get("annualReports", [])
        balance_data = balance_sheet.get("annualReports", [])
        cash_data = cash_flow.get("annualReports", [])
        
        financial_years = map_to_financial_years(income_data, balance_data, cash_data, historical_prices)
        
        # Calculate TTM and prepend it
        income_q = income_stmt.get("quarterlyReports", [])
        balance_q = balance_sheet.get("quarterlyReports", [])
        cash_q = cash_flow.get("quarterlyReports", [])
        
        ttm_year = calculate_ttm_year(income_q, balance_q, cash_q)
        if ttm_year:
            financial_years.insert(0, ttm_year)
            
        return financial_years
        
    async def get_ticker_info(self, symbol: str) -> Ticker:
        """
        Fetches metadata for a ticker, including qualitative analysis context metrics.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the ticker data.
            
        Returns:
            Ticker: Domain Entity containing the ticker data
        """
        # Fetch OVERVIEW and GLOBAL_QUOTE concurrently
        overview_task = self._get_data("OVERVIEW", symbol)
        quote_task = self._get_data("GLOBAL_QUOTE", symbol)
        data, quote_data = await asyncio.gather(overview_task, quote_task)
        
        if not data or "Symbol" not in data:
            raise TickerNotFoundError(f"Ticker information not found for {symbol}")
            
        mc_raw = data.get("MarketCapitalization")
        pe_raw = data.get("PERatio")
        fpe_raw = data.get("ForwardPE")
        
        market_cap = Decimal(mc_raw) if mc_raw and mc_raw != "None" else None
        pe_ratio = Decimal(pe_raw) if pe_raw and pe_raw != "None" else None
        
        try:
            forward_pe = Decimal(fpe_raw) if fpe_raw and fpe_raw not in ["None", "-"] else None
        except Exception:
            forward_pe = None
            
        # Qualitative Context Fields from OVERVIEW
        def parse_dec(val):
            return Decimal(str(val)) if val and str(val) not in ["None", "-", ""] else None
            
        business_description = data.get("Description")
        profit_margins = parse_dec(data.get("ProfitMargin"))
        revenue_growth = parse_dec(data.get("QuarterlyRevenueGrowthYOY"))
        beta = parse_dec(data.get("Beta"))
        
        # Qualitative Context Fields from GLOBAL_QUOTE
        current_price = None
        regular_market_change = None
        regular_market_change_percent = None
        
        quote = quote_data.get("Global Quote", {}) if quote_data else {}
        if quote:
            current_price = parse_dec(quote.get("05. price"))
            regular_market_change = parse_dec(quote.get("09. change"))
            
            rmcp_raw = quote.get("10. change percent")
            if rmcp_raw and "%" in str(rmcp_raw):
                rmcp_raw = str(rmcp_raw).replace("%", "")
            regular_market_change_percent = parse_dec(rmcp_raw)
            
        def slugify(text: str) -> Optional[str]:
            if not text or text == "Unknown" or text == "None":
                return None
            import re
            t = text.lower()
            t = t.replace("&", "and")
            t = re.sub(r'[^a-z0-9]+', '-', t)
            return t.strip('-')
            
        sector_str = data.get("Sector", "Unknown")
        industry_str = data.get("Industry", "Unknown")
            
        return Ticker(
            symbol=data.get("Symbol", symbol),
            name=data.get("Name"),
            sector=sector_str,
            sector_key=slugify(sector_str),
            industry=industry_str,
            industry_key=slugify(industry_str),
            market_cap=market_cap,
            pe_ratio=pe_ratio,
            forward_pe=forward_pe,
            business_description=business_description,
            profit_margins=profit_margins,
            revenue_growth=revenue_growth,
            beta=beta,
            current_price=current_price,
            regular_market_change=regular_market_change,
            regular_market_change_percent=regular_market_change_percent
        )

    async def get_major_shareholders(self, symbol: str) -> Dict[str, float]:
        """
        Fetches the major institutional shareholders and their ownership percentage using Alpha Vantage.
        
        Args:
            symbol (str): The stock ticker symbol.
            
        Returns:
            Dict[str, float]: Dictionary mapping shareholder name to their ownership percentage.
        """
        try:
            holdings_task = self._get_data("INSTITUTIONAL_HOLDINGS", symbol)
            overview_task = self._get_data("OVERVIEW", symbol)
            
            holdings_data, overview_data = await asyncio.gather(holdings_task, overview_task)
            
            if not holdings_data or "holdings" not in holdings_data:
                return {}
                
            shares_outstanding_raw = overview_data.get("SharesOutstanding")
            if not shares_outstanding_raw or shares_outstanding_raw == "None":
                return {}
                
            shares_outstanding = float(shares_outstanding_raw)
            if shares_outstanding <= 0:
                return {}
                
            holdings = holdings_data.get("holdings", [])[:5]
            
            result = {}
            for holding in holdings:
                holder_name = holding.get("holder_name")
                shares_held_raw = holding.get("shares_held")
                
                if holder_name and shares_held_raw:
                    try:
                        shares_held = float(shares_held_raw)
                        percentage = (shares_held / shares_outstanding) * 100
                        result[str(holder_name)] = round(percentage, 2)
                    except ValueError:
                        continue
                        
            return result
        except Exception as e:
            print(f"Failed to fetch major shareholders for {symbol}: {e}")
            return {}

    async def get_earnings_call_transcript(self, ticker: str, year: int, quarter: int) -> Optional[EarningsCallTranscript]:
        """
        Fetches the earnings call transcript for a given stock symbol, year, and quarter.
        """
        try:
            from domain.entities.earnings import EarningsCallTranscript, TranscriptStatement
            from datetime import datetime
            
            # Alpha Vantage API expects quarter in format like "2024Q1" or year/quarter params.
            # Using standard year/quarter kwargs based on the API docs. 
            # Note: We pass them to _get_data so the cache filename generates correctly (e.g. _2024_Q1)
            data = await self._get_data("EARNINGS_CALL_TRANSCRIPT", ticker, year=year, quarter=quarter)
            
            if not data or "transcript" not in data:
                logger.error(f"DEBUG GET_DATA RESULT for {ticker} {year}Q{quarter}: {data}")
                return None
                
            # The structure returned by Alpha Vantage might vary. Let's gracefully parse it.
            # Usually it returns a 'transcript' array of objects with speaker and content.
            raw_transcripts = data.get("transcript", [])
            date_str = data.get("date")
            transcript_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
            
            statements = []
            for item in raw_transcripts:
                speaker = item.get("speaker", "Unknown")
                title = item.get("title", "Unknown")
                content = item.get("content", item.get("text", ""))
                sentiment = item.get("sentiment")
                
                # Try to cast sentiment to float if it exists
                if sentiment is not None:
                    try:
                        sentiment = float(sentiment)
                    except ValueError:
                        sentiment = None
                        
                statements.append(TranscriptStatement(
                    speaker=speaker,
                    title=title,
                    content=content,
                    sentiment=sentiment
                ))
                
            return EarningsCallTranscript(
                ticker=ticker.upper(),
                quarter=quarter,
                year=year,
                date=transcript_date,
                transcripts=statements
            )
        except Exception as e:
            logger.error(f"Failed to fetch earnings call transcript for {ticker} Q{quarter} {year}: {e}")
            return None

    async def search_tickers(self, query: str) -> List[Dict[str, str]]:
        """
        Searches for tickers matching the query using Alpha Vantage SYMBOL_SEARCH.
        
        Args:
            query (str): The search term.
            
        Returns:
            List[Dict[str, str]]: A list of dictionaries containing symbol, name, and exchange.
        """
        try:
            data = await self._get_data("SYMBOL_SEARCH", query)
            matches = data.get("bestMatches", [])
            
            results = []
            for match in matches:
                results.append({
                    "symbol": match.get("1. symbol", ""),
                    "name": match.get("2. name", ""),
                    "exchange": match.get("4. region", "")
                })
            return results
        except Exception as e:
            print(f"Error searching tickers for {query}: {e}")
            return []

    async def get_historical_performance_chart(self, tickers: List[str], period: str = "5y") -> List[Dict]:
        """
        Fetches historical weekly closing prices for multiple tickers and normalizes them 
        into a percentage return from day 1, replicating the behavior of YFinance for Sector Performance.

        Args:
            tickers (List[str]): A list of stock/ETF ticker symbols.
            period (str): The time period for which to fetch data (ignored here as we use TIME_SERIES_MONTHLY).

        Returns:
            List[Dict]: [{'date': '2020-01-01', 'SMH': 0.0, 'SPY': 0.0}, ...]
        """
        try:
            tasks = [self._get_data("TIME_SERIES_MONTHLY_ADJUSTED", ticker) for ticker in tickers]
            responses = await asyncio.gather(*tasks)
            
            # Extract closing prices per ticker per date
            # time_series structure: {"2024-05-10": {"5. adjusted close": "123.45"}, ...}
            ticker_series = {}
            all_dates = set()
            
            for ticker, data in zip(tickers, responses):
                ts = data.get("Monthly Adjusted Time Series", {})
                series = {}
                for date_str, metrics in ts.items():
                    close_val = metrics.get("5. adjusted close")
                    if close_val:
                        series[date_str] = float(close_val)
                        all_dates.add(date_str)
                ticker_series[ticker] = series
                
            if not all_dates:
                return []
                
            # Sort dates chronologically
            sorted_dates = sorted(list(all_dates))
            
            # Limit to 5 years (5 * 12 months = 60 data points)
            if period == "5y":
                sorted_dates = sorted_dates[-60:]
                
            # Build DataFrame-like structure
            df_dict = {"date": sorted_dates}
            for ticker in tickers:
                series = ticker_series.get(ticker, {})
                # Fill missing dates with previous values
                ticker_vals = []
                last_val = None
                for d in sorted_dates:
                    val = series.get(d)
                    if val is not None:
                        last_val = val
                    ticker_vals.append(last_val)
                df_dict[ticker] = ticker_vals
                
            df = pd.DataFrame(df_dict)
            df = df.set_index("date")
            df = df.dropna(how='all').ffill().bfill()
            
            if df.empty:
                return []
                
            # Normalize to percentage return
            returns = ((df / df.iloc[0]) - 1) * 100
            
            result = []
            for date, row in returns.iterrows():
                point = {"date": date}
                for ticker in tickers:
                    val = row.get(ticker)
                    point[ticker] = float(val) if pd.notna(val) else 0.0
                result.append(point)
                
            return result
        except Exception as e:
            print(f"Error fetching performance for {tickers}: {e}")
            return []



    async def get_stock_quarterly_data(self, symbol: str) -> List[FinancialQuarter]:
        """
        Fetches the fundamental financial data for a given stock ticker symbol from Alpha Vantage.
        Uses the quarterlyReports array.
        
        Args:
            symbol (str): The stock ticker symbol to fetch fundamental data for.
            
        Returns:
            List[FinancialQuarter]: List containing the fundamental stock data for each Financial Quarter.
        """
        income_task = self._get_data("INCOME_STATEMENT", symbol)
        balance_task = self._get_data("BALANCE_SHEET", symbol)
        cash_task = self._get_data("CASH_FLOW", symbol)
        prices_task = self.get_historical_prices(symbol)
        
        income_stmt, balance_sheet, cash_flow, historical_prices = await asyncio.gather(
            income_task, balance_task, cash_task, prices_task
        )

        income_data = income_stmt.get("quarterlyReports", [])
        balance_data = balance_sheet.get("quarterlyReports", [])
        cash_data = cash_flow.get("quarterlyReports", [])
        
        financial_quarters = map_to_financial_quarters(income_data, balance_data, cash_data, historical_prices)
        return financial_quarters[:12]