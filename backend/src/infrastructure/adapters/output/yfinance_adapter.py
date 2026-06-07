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
            
            business_description = info.get("longBusinessDescription")
            
            profit_margins_raw = info.get("profitMargins")
            profit_margins = Decimal(str(profit_margins_raw)) if profit_margins_raw is not None and not pd.isna(profit_margins_raw) else None
            
            revenue_growth_raw = info.get("revenueGrowth")
            revenue_growth = Decimal(str(revenue_growth_raw)) if revenue_growth_raw is not None and not pd.isna(revenue_growth_raw) else None
            
            company_officers = info.get("companyOfficers", [])
            
            return Ticker(
                symbol=info.get("symbol", symbol),
                name=info.get("longName", info.get("shortName", "")),
                sector=info.get("sector", "Unknown"),
                sector_key=info.get("sectorKey"),
                industry=info.get("industry", "Unknown"),
                industry_key=info.get("industryKey"),
                market_cap=market_cap,
                pe_ratio=pe_ratio,
                forward_pe=forward_pe,
                regular_market_change=regular_market_change,
                regular_market_change_percent=regular_market_change_percent,
                business_description=business_description,
                profit_margins=profit_margins,
                revenue_growth=revenue_growth,
                company_officers=company_officers
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
            
            quarterly_financials = await asyncio.to_thread(lambda: ticker.quarterly_financials)
            quarterly_balance_sheet = await asyncio.to_thread(lambda: ticker.quarterly_balance_sheet)
            quarterly_cashflow = await asyncio.to_thread(lambda: ticker.quarterly_cashflow)
            
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
                    # Bank Fallback: If they have Interest Expense and Interest Income, they are a bank
                    interest_expense = get_val(financials, 'Interest Expense')
                    interest_income = get_val(financials, 'Interest Income')
                    if interest_expense > Decimal("0") and interest_income > Decimal("0"):
                        # For banks, yfinance 'Total Revenue' is actually Net Revenue.
                        # We add back Interest Expense to get true Gross Revenue
                        gross_profit = revenue
                        revenue = revenue + interest_expense
                    else:
                        policy_benefits = get_val(financials, 'Net Policyholder Benefits And Claims')
                        if policy_benefits > Decimal("0"):
                            gross_profit = revenue - policy_benefits
                        else:
                            # Fallback for Service Companies (100% Gross Margin if no COGS)
                            gross_profit = revenue
                        
                operating_income = get_val(financials, 'Operating Income')
                if operating_income == Decimal("0"):
                    operating_income = get_val(financials, 'Pretax Income')
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
                        comp_date = pd.to_datetime(date).tz_localize(None)
                        valid_prices = price_hist[price_hist.index.tz_localize(None) <= comp_date]
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
            latest_annual_date = financials.columns[0] if not financials.empty else None
            latest_quarterly_date = quarterly_financials.columns[0] if not quarterly_financials.empty else None

            if latest_quarterly_date and latest_annual_date and latest_quarterly_date > latest_annual_date:
                if len(quarterly_financials.columns) >= 4 and len(quarterly_cashflow.columns) >= 4:
                    q_dates = quarterly_financials.columns[:4]
                    q_cf_dates = quarterly_cashflow.columns[:4]

                    def get_ttm_val(df, dates, key):
                        if df.empty or key not in df.index:
                            return Decimal("0")
                        total = Decimal("0")
                        for d in dates:
                            if d in df.columns:
                                val = df.loc[key, d]
                                if not pd.isna(val):
                                    total += Decimal(str(val))
                        return total
                    
                    def get_latest_q_val(df, key):
                        if df.empty or key not in df.index:
                            return Decimal("0")
                        d = df.columns[0]
                        val = df.loc[key, d]
                        if pd.isna(val):
                            return Decimal("0")
                        return Decimal(str(val))

                    ttm_revenue = get_ttm_val(quarterly_financials, q_dates, 'Total Revenue')
                    if ttm_revenue > Decimal("0"):
                        ttm_gross_profit = get_ttm_val(quarterly_financials, q_dates, 'Gross Profit')
                        if ttm_gross_profit == Decimal("0"):
                            ttm_gross_profit = ttm_revenue
                        
                        ttm_operating_income = get_ttm_val(quarterly_financials, q_dates, 'Operating Income')
                        if ttm_operating_income == Decimal("0"):
                            ttm_operating_income = get_ttm_val(quarterly_financials, q_dates, 'Pretax Income')
                        
                        ttm_net_income = get_ttm_val(quarterly_financials, q_dates, 'Net Income')
                        if ttm_net_income == Decimal("0"):
                            ttm_net_income = get_ttm_val(quarterly_financials, q_dates, 'Net Income Common Stockholders')

                        ttm_ebitda = get_ttm_val(quarterly_financials, q_dates, 'EBITDA')
                        if ttm_ebitda == Decimal("0"):
                            ttm_ebitda = ttm_operating_income + get_ttm_val(quarterly_cashflow, q_cf_dates, 'Depreciation And Amortization')
                        
                        ttm_operating_cash_flow = get_ttm_val(quarterly_cashflow, q_cf_dates, 'Operating Cash Flow')
                        ttm_capital_expenditures = get_ttm_val(quarterly_cashflow, q_cf_dates, 'Capital Expenditure')
                        
                        ttm_total_assets = get_latest_q_val(quarterly_balance_sheet, 'Total Assets')
                        ttm_total_liabilities = get_latest_q_val(quarterly_balance_sheet, 'Total Liabilities Net Minority Interest')
                        ttm_total_debt = get_latest_q_val(quarterly_balance_sheet, 'Total Debt')
                        ttm_short_term_debt = get_latest_q_val(quarterly_balance_sheet, 'Current Debt')
                        ttm_long_term_debt = get_latest_q_val(quarterly_balance_sheet, 'Long Term Debt')
                        ttm_cash_and_equivalents = get_latest_q_val(quarterly_balance_sheet, 'Cash And Cash Equivalents')
                        
                        ttm_shares_outstanding = get_latest_q_val(quarterly_financials, 'Basic Average Shares')
                        if ttm_shares_outstanding == Decimal("0"):
                            ttm_shares_outstanding = get_latest_q_val(quarterly_financials, 'Diluted Average Shares')
                        
                        ttm_shares_outstanding = max(ttm_shares_outstanding, Decimal("0"))
                        ttm_total_assets = max(ttm_total_assets, Decimal("0"))
                        ttm_total_debt = max(ttm_total_debt, Decimal("0"))

                        years_data.append(FinancialYear(
                            fiscal_date_ending="TTM",
                            revenue=ttm_revenue,
                            ebitda=ttm_ebitda,
                            gross_profit=ttm_gross_profit,
                            operating_income=ttm_operating_income,
                            net_income=ttm_net_income,
                            operating_cash_flow=ttm_operating_cash_flow,
                            capital_expenditures=ttm_capital_expenditures,
                            shares_outstanding=ttm_shares_outstanding,
                            short_term_debt=ttm_short_term_debt,
                            long_term_debt=ttm_long_term_debt,
                            total_debt=ttm_total_debt,
                            total_assets=ttm_total_assets,
                            total_liabilities=ttm_total_liabilities,
                            cash_and_equivalents=ttm_cash_and_equivalents,
                            year_end_price=Decimal("0")
                        ))
            
            sorted_years = sorted([y for y in years_data if y.fiscal_date_ending != "TTM"], key=lambda x: x.fiscal_date_ending)
            ttm_year = next((y for y in years_data if y.fiscal_date_ending == "TTM"), None)
            if ttm_year:
                sorted_years.append(ttm_year)
                
            return sorted_years
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
                    # Bank Fallback
                    interest_expense = get_val(financials, 'Interest Expense')
                    interest_income = get_val(financials, 'Interest Income')
                    if interest_expense > Decimal("0") and interest_income > Decimal("0"):
                        gross_profit = revenue
                        revenue = revenue + interest_expense
                    else:
                        policy_benefits = get_val(financials, 'Net Policyholder Benefits And Claims')
                        if policy_benefits > Decimal("0"):
                            gross_profit = revenue - policy_benefits
                        else:
                            # Fallback for Service Companies
                            gross_profit = revenue
                        
                operating_income = get_val(financials, 'Operating Income')
                if operating_income == Decimal("0"):
                    operating_income = get_val(financials, 'Pretax Income')
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
                        comp_date = pd.to_datetime(date).tz_localize(None)
                        valid_prices = price_hist[price_hist.index.tz_localize(None) <= comp_date]
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

    async def get_trending_by_sector(self, sector_key: str) -> List[Dict]:
        """
        Fetches the top trending companies for a given sector using yfinance.
        """
        try:
            sector = await asyncio.to_thread(yf.Sector, sector_key)
            top_companies = await asyncio.to_thread(lambda: sector.top_companies)
            
            if top_companies is None or top_companies.empty:
                return []
            
            results = []
            for symbol, row in top_companies.iterrows():
                results.append({
                    "symbol": str(symbol),
                    "name": str(row.get("name", "")),
                    "rating": str(row.get("rating", "")) if pd.notna(row.get("rating")) else None,
                    "weight": float(row.get("market weight", 0.0)) if pd.notna(row.get("market weight")) else None
                })
            return results
        except Exception as e:
            print(f"Error fetching trending sector {sector_key}: {e}")
            return []

    async def get_trending_by_industry(self, industry_key: str) -> List[Dict]:
        """
        Fetches the top trending companies for a given industry using yfinance.
        """
        try:
            industry = await asyncio.to_thread(yf.Industry, industry_key)
            top_companies = await asyncio.to_thread(lambda: industry.top_companies)
            
            if top_companies is None or top_companies.empty:
                return []
            
            results = []
            for symbol, row in top_companies.iterrows():
                results.append({
                    "symbol": str(symbol),
                    "name": str(row.get("name", "")),
                    "rating": str(row.get("rating", "")) if pd.notna(row.get("rating")) else None,
                    "weight": float(row.get("market weight", 0.0)) if pd.notna(row.get("market weight")) else None
                })
            return results
        except Exception as e:
            print(f"Error fetching trending industry {industry_key}: {e}")
            return []
