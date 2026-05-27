import yfinance as yf
from decimal import Decimal
from typing import Dict, List, Optional
import asyncio
import pandas as pd
from datetime import datetime

from domain.entities.entities import Price, FinancialYear, FinancialQuarter, Ticker
from domain.exceptions import TickerNotFoundError, RateLimitExceededError
from application.ports.ports import QuantitativeDataPort, QuarterlyDataPort

class YfinanceAdapter(QuantitativeDataPort, QuarterlyDataPort):
    """
    Adapter for fetching stock data using the yfinance library.
    Implements QuantitativeDataPort and QuarterlyDataPort.
    """
    
    def __init__(self):
        # yfinance doesn't need API keys
        pass

    async def get_stock_current_price(self, symbol: str) -> Price:
        """
        Fetches the current stock price for the given symbol using yfinance.
        
        Args:
            symbol (str): The stock ticker symbol (e.g., "AAPL").
            
        Returns:
            Price: An object containing the current price and currency.
        """
        try:
            # Run yfinance blocking calls in a threadpool
            ticker = await asyncio.to_thread(yf.Ticker, symbol)
            fast_info = await asyncio.to_thread(lambda: ticker.fast_info)
            last_price = fast_info.get("lastPrice")
            
            if last_price is None or pd.isna(last_price):
                raise TickerNotFoundError(f"Price data not found for {symbol}")
                
            return Price(amount=Decimal(str(last_price)), currency="USD")
        except TickerNotFoundError:
            raise
        except Exception as e:
            raise TickerNotFoundError(f"Error fetching current price for {symbol}: {str(e)}")

    async def get_historical_prices(self, symbol: str) -> Dict[str, Price]:
        """
        Fetches historical monthly closing prices for the past 10 years for the given symbol using yfinance.
        
        Args:
            symbol (str): The stock ticker symbol (e.g., "AAPL").
            
        Returns:
            Dict[str, Price]: A dictionary mapping "YYYY-MM" to Price objects.
        """
        try:
            ticker = await asyncio.to_thread(yf.Ticker, symbol)
            hist = await asyncio.to_thread(ticker.history, period="10y", interval="1mo")
            
            if hist.empty:
                return {}
                
            historical_prices = {}
            for date, row in hist.iterrows():
                # Date is a Timestamp
                year_month = date.strftime("%Y-%m")
                close_price = row.get("Close")
                if pd.notna(close_price):
                    historical_prices[year_month] = Price(amount=Decimal(str(close_price)), currency="USD")
            
            return historical_prices
        except Exception:
            return {}

    async def get_ticker_info(self, symbol: str) -> Ticker:
        """
        Fetches information about the stock for the given symbol using yfinance.

        Args:
            symbol (str): The stock ticker symbol (e.g., "AAPL").

        Returns:
            Ticker: An object containing the ticker information.
        """
        try:
            ticker = await asyncio.to_thread(yf.Ticker, symbol)
            info = await asyncio.to_thread(lambda: ticker.info)
            
            if not info or "symbol" not in info:
                raise TickerNotFoundError(f"Ticker information not found for {symbol}")
                
            mc_raw = info.get("marketCap")
            pe_raw = info.get("trailingPE")
            fpe_raw = info.get("forwardPE")
            
            market_cap = Decimal(str(mc_raw)) if mc_raw and not pd.isna(mc_raw) else None
            pe_ratio = Decimal(str(pe_raw)) if pe_raw and not pd.isna(pe_raw) else None
            forward_pe = Decimal(str(fpe_raw)) if fpe_raw and not pd.isna(fpe_raw) else None
            
            rmc_raw = info.get("regularMarketChange")
            rmcp_raw = info.get("regularMarketChangePercent")
            regular_market_change = Decimal(str(rmc_raw)) if rmc_raw is not None and not pd.isna(rmc_raw) else None
            regular_market_change_percent = Decimal(str(rmcp_raw)) if rmcp_raw is not None and not pd.isna(rmcp_raw) else None
            
            return Ticker(
                symbol=info.get("symbol", symbol),
                name=info.get("longName", info.get("shortName", "")),
                sector=info.get("sector", "Unknown"),
                industry=info.get("industry", "Unknown"),
                market_cap=market_cap,
                pe_ratio=pe_ratio,
                forward_pe=forward_pe,
                regular_market_change=regular_market_change,
                regular_market_change_percent=regular_market_change_percent
            )
        except Exception as e:
            raise TickerNotFoundError(f"Error fetching info for {symbol}: {str(e)}")

    async def get_stock_fundamental_data(self, symbol: str) -> List[FinancialYear]:
        """
        Fetches historical financial data for the past 5 years for the given symbol using yfinance.
        
        Args:
            symbol (str): The stock ticker symbol (e.g., "AAPL").
            
        Returns:
            List[FinancialYear]: A list of FinancialYear objects containing the financial data for each year
        """
        try:
            ticker = await asyncio.to_thread(yf.Ticker, symbol)
            
            # Fetch all needed statements
            financials = await asyncio.to_thread(lambda: ticker.financials)
            balance_sheet = await asyncio.to_thread(lambda: ticker.balance_sheet)
            cashflow = await asyncio.to_thread(lambda: ticker.cashflow)
            
            if financials.empty:
                return []
                
            years_data = []
            
            # Columns are dates in descending order
            for date in financials.columns:
                date_str = date.strftime("%Y-%m-%d")
                
                def get_val(df, key):
                    if df.empty or date not in df.columns or key not in df.index:
                        return Decimal("0")
                    val = df.loc[key, date]
                    if pd.isna(val):
                        return Decimal("0")
                    return Decimal(str(val))
                    
                # Extract financials
                revenue = get_val(financials, 'Total Revenue')
                if revenue == Decimal("0"):
                    continue # Skip years with missing data (yfinance usually returns NaNs for the 5th year)
                    
                gross_profit = get_val(financials, 'Gross Profit')
                if gross_profit == Decimal("0"):
                    # Fallback for Service Companies (100% Gross Margin if no COGS)
                    gross_profit = revenue
                operating_income = get_val(financials, 'Operating Income')
                net_income = get_val(financials, 'Net Income')
                if net_income == Decimal("0"):
                    net_income = get_val(financials, 'Net Income Common Stockholders')
                if net_income == Decimal("0"):
                    net_income = get_val(financials, 'Net Income Including Noncontrolling Interests')
                ebitda = get_val(financials, 'EBITDA')
                if ebitda == Decimal("0"):
                    # Fallback for EBITDA
                    ebitda = operating_income + get_val(cashflow, 'Depreciation And Amortization')
                shares_outstanding = get_val(financials, 'Basic Average Shares')
                if shares_outstanding == Decimal("0"):
                    shares_outstanding = get_val(financials, 'Diluted Average Shares')
                
                # Extract balance sheet
                total_assets = get_val(balance_sheet, 'Total Assets')
                total_liabilities = get_val(balance_sheet, 'Total Liabilities Net Minority Interest')
                total_debt = get_val(balance_sheet, 'Total Debt')
                short_term_debt = get_val(balance_sheet, 'Current Debt')
                long_term_debt = get_val(balance_sheet, 'Long Term Debt')
                cash_and_equivalents = get_val(balance_sheet, 'Cash And Cash Equivalents')
                
                # Extract cashflow
                operating_cash_flow = get_val(cashflow, 'Operating Cash Flow')
                capital_expenditures = get_val(cashflow, 'Capital Expenditure')
                
                # Historical Price for year end
                year_end_price = Decimal("0")
                try:
                    hist_start = date - pd.Timedelta(days=5)
                    hist_end = date + pd.Timedelta(days=5)
                    price_hist = ticker.history(start=hist_start.strftime("%Y-%m-%d"), end=hist_end.strftime("%Y-%m-%d"))
                    if not price_hist.empty:
                        # Find the closest date before or on the fiscal date
                        valid_prices = price_hist[price_hist.index <= date]
                        if not valid_prices.empty:
                            close_val = valid_prices.iloc[-1]['Close']
                            if pd.notna(close_val):
                                year_end_price = Decimal(str(close_val))
                except:
                    pass

                # Sanitize values to prevent negative value errors in Domain
                shares_outstanding = max(shares_outstanding, Decimal("0"))
                total_assets = max(total_assets, Decimal("0"))
                total_debt = max(total_debt, Decimal("0"))

                years_data.append(FinancialYear(
                    fiscal_date_ending=date_str,
                    revenue=revenue,
                    ebitda=ebitda,
                    gross_profit=gross_profit,
                    operating_income=operating_income,
                    net_income=net_income,
                    operating_cash_flow=operating_cash_flow,
                    capital_expenditures=capital_expenditures,
                    shares_outstanding=shares_outstanding,
                    short_term_debt=short_term_debt,
                    long_term_debt=long_term_debt,
                    total_debt=total_debt,
                    total_assets=total_assets,
                    total_liabilities=total_liabilities,
                    cash_and_equivalents=cash_and_equivalents,
                    year_end_price=year_end_price
                ))
            
            return sorted(years_data, key=lambda x: x.fiscal_date_ending)
        except Exception as e:
            raise Exception(f"Failed to fetch fundamental data from yfinance: {str(e)}")

    async def get_stock_quarterly_data(self, symbol: str) -> List[FinancialQuarter]:
        """
        Fetches historical financial data for the past 5 years on a quarterly basis for the given symbol using yfinance.
        
        Args:
            symbol (str): The stock ticker symbol (e.g., "AAPL").
            
        Returns:
            List[FinancialQuarter]: A list of FinancialQuarter objects containing the financial data for each quarter
        """
        try:
            ticker = await asyncio.to_thread(yf.Ticker, symbol)
            
            # Fetch all needed statements
            financials = await asyncio.to_thread(lambda: ticker.quarterly_financials)
            balance_sheet = await asyncio.to_thread(lambda: ticker.quarterly_balance_sheet)
            cashflow = await asyncio.to_thread(lambda: ticker.quarterly_cashflow)
            
            if financials.empty:
                return []
                
            quarters_data = []
            
            # Columns are dates in descending order
            for date in financials.columns:
                date_str = date.strftime("%Y-%m-%d")
                
                def get_val(df, key):
                    if df.empty or date not in df.columns or key not in df.index:
                        return Decimal("0")
                    val = df.loc[key, date]
                    if pd.isna(val):
                        return Decimal("0")
                    return Decimal(str(val))
                    
                # Extract financials
                revenue = get_val(financials, 'Total Revenue')
                if revenue == Decimal("0"):
                    continue # Skip quarters with missing data
                    
                gross_profit = get_val(financials, 'Gross Profit')
                if gross_profit == Decimal("0"):
                    # Fallback for Service Companies
                    gross_profit = revenue
                operating_income = get_val(financials, 'Operating Income')
                net_income = get_val(financials, 'Net Income')
                if net_income == Decimal("0"):
                    net_income = get_val(financials, 'Net Income Common Stockholders')
                if net_income == Decimal("0"):
                    net_income = get_val(financials, 'Net Income Including Noncontrolling Interests')
                ebitda = get_val(financials, 'EBITDA')
                if ebitda == Decimal("0"):
                    # Fallback for EBITDA
                    ebitda = operating_income + get_val(cashflow, 'Depreciation And Amortization')
                shares_outstanding = get_val(financials, 'Basic Average Shares')
                if shares_outstanding == Decimal("0"):
                    shares_outstanding = get_val(financials, 'Diluted Average Shares')
                
                # Extract balance sheet
                total_assets = get_val(balance_sheet, 'Total Assets')
                total_liabilities = get_val(balance_sheet, 'Total Liabilities Net Minority Interest')
                total_debt = get_val(balance_sheet, 'Total Debt')
                short_term_debt = get_val(balance_sheet, 'Current Debt')
                long_term_debt = get_val(balance_sheet, 'Long Term Debt')
                cash_and_equivalents = get_val(balance_sheet, 'Cash And Cash Equivalents')
                
                # Extract cashflow
                operating_cash_flow = get_val(cashflow, 'Operating Cash Flow')
                capital_expenditures = get_val(cashflow, 'Capital Expenditure')
                
                # Historical Price for quarter end
                quarter_end_price = Decimal("0")
                try:
                    hist_start = date - pd.Timedelta(days=5)
                    hist_end = date + pd.Timedelta(days=5)
                    price_hist = ticker.history(start=hist_start.strftime("%Y-%m-%d"), end=hist_end.strftime("%Y-%m-%d"))
                    if not price_hist.empty:
                        # Find the closest date before or on the fiscal date
                        valid_prices = price_hist[price_hist.index <= date]
                        if not valid_prices.empty:
                            close_val = valid_prices.iloc[-1]['Close']
                            if pd.notna(close_val):
                                quarter_end_price = Decimal(str(close_val))
                except:
                    pass

                # Sanitize values to prevent negative value errors in Domain
                shares_outstanding = max(shares_outstanding, Decimal("0"))
                total_assets = max(total_assets, Decimal("0"))
                total_debt = max(total_debt, Decimal("0"))

                quarters_data.append(FinancialQuarter(
                    fiscal_date_ending=date_str,
                    revenue=revenue,
                    ebitda=ebitda,
                    gross_profit=gross_profit,
                    operating_income=operating_income,
                    net_income=net_income,
                    operating_cash_flow=operating_cash_flow,
                    capital_expenditures=capital_expenditures,
                    shares_outstanding=shares_outstanding,
                    short_term_debt=short_term_debt,
                    long_term_debt=long_term_debt,
                    total_debt=total_debt,
                    total_assets=total_assets,
                    total_liabilities=total_liabilities,
                    cash_and_equivalents=cash_and_equivalents,
                    year_end_price=quarter_end_price
                ))
            
            return sorted(quarters_data, key=lambda x: x.fiscal_date_ending)
        except Exception as e:
            raise Exception(f"Failed to fetch quarterly data from yfinance: {str(e)}")
