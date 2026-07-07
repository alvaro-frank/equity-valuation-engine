from decimal import Decimal
import pandas as pd
from typing import Optional

from domain.entities import FinancialYear, FinancialQuarter

def parse_financial_period(date_str: str, date, financials, balance_sheet, cashflow, ticker, is_quarter: bool = False):
    """
    Parses the financial data for a specific period (year or quarter) and returns a FinancialYear or FinancialQuarter object.
    
    Args:
        date_str (str): The date string in "YYYY-MM-DD" format.
        date: The pandas Timestamp object for the date.
        financials: The financials DataFrame from yfinance.
        balance_sheet: The balance sheet DataFrame from yfinance.
        cashflow: The cash flow DataFrame from yfinance.
        ticker: The yfinance Ticker object.
        is_quarter (bool): Whether the period is a quarter (True) or a year (False).
        
    Returns:
        FinancialYear or FinancialQuarter: The parsed financial data object for the period.
    """
    def get_val(df, key):
        if df.empty or date not in df.columns or key not in df.index:
            return Decimal("0")
        val = df.loc[key, date]
        if pd.isna(val):
            return Decimal("0")
        return Decimal(str(val))
        
    revenue = get_val(financials, 'Total Revenue')
    if revenue == Decimal("0"):
        return None # Skip missing data
        
    gross_profit = get_val(financials, 'Gross Profit')
    if gross_profit == Decimal("0"):
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
                gross_profit = revenue
                
    operating_income = get_val(financials, 'Operating Income')
    if operating_income == Decimal("0"):
        operating_income = get_val(financials, 'Pretax Income')
        
    interest_expense_direct = get_val(financials, 'Interest Expense')
    income_tax_expense = get_val(financials, 'Tax Provision')
    income_before_tax = get_val(financials, 'Pretax Income')
        
    net_income = get_val(financials, 'Net Income')
    if net_income == Decimal("0"):
        net_income = get_val(financials, 'Net Income Common Stockholders')
    if net_income == Decimal("0"):
        net_income = get_val(financials, 'Net Income Including Noncontrolling Interests')
    ebitda = get_val(financials, 'EBITDA')
    if ebitda == Decimal("0"):
        ebitda = operating_income + get_val(cashflow, 'Depreciation And Amortization')
    shares_outstanding = get_val(financials, 'Basic Average Shares')
    if shares_outstanding == Decimal("0"):
        shares_outstanding = get_val(financials, 'Diluted Average Shares')
    
    total_assets = get_val(balance_sheet, 'Total Assets')
    total_liabilities = get_val(balance_sheet, 'Total Liabilities Net Minority Interest')
    total_debt = get_val(balance_sheet, 'Total Debt')
    short_term_debt = get_val(balance_sheet, 'Current Debt')
    long_term_debt = get_val(balance_sheet, 'Long Term Debt')
    cash_and_equivalents = get_val(balance_sheet, 'Cash And Cash Equivalents')
    
    accounts_payable = get_val(balance_sheet, 'Accounts Payable')
    if accounts_payable == Decimal("0"):
        accounts_payable = get_val(balance_sheet, 'Payables')
    current_liabilities = get_val(balance_sheet, 'Current Liabilities')
    
    accounts_receivable = get_val(balance_sheet, 'Accounts Receivable')
    if accounts_receivable == Decimal("0"):
        accounts_receivable = get_val(balance_sheet, 'Receivables')
    inventory = get_val(balance_sheet, 'Inventory')
    current_assets = get_val(balance_sheet, 'Current Assets')
    net_ppe = get_val(balance_sheet, 'Net PPE')
    
    intangible_assets = get_val(balance_sheet, 'Goodwill And Other Intangible Assets')
    if intangible_assets == Decimal("0"):
        intangible_assets = get_val(balance_sheet, 'Other Intangible Assets') + get_val(balance_sheet, 'Goodwill')
    
    operating_cash_flow = get_val(cashflow, 'Operating Cash Flow')
    depreciation_and_amortization = get_val(cashflow, 'Depreciation And Amortization')
    stock_based_compensation = get_val(cashflow, 'Stock Based Compensation')
    capital_expenditures = get_val(cashflow, 'Capital Expenditure')
    net_investing_cash_flow = get_val(cashflow, 'Investing Cash Flow')
    dividends_paid = get_val(cashflow, 'Cash Dividends Paid')
    stock_repurchases = get_val(cashflow, 'Repurchase Of Capital Stock')
    net_debt_issued = get_val(cashflow, 'Net Issuance Payments Of Debt')
    net_financing_cash_flow = get_val(cashflow, 'Financing Cash Flow')
    
    period_end_price = Decimal("0")
    try:
        hist_start = date - pd.Timedelta(days=5)
        hist_end = date + pd.Timedelta(days=5)
        price_hist = ticker.history(start=hist_start.strftime("%Y-%m-%d"), end=hist_end.strftime("%Y-%m-%d"))
        if not price_hist.empty:
            comp_date = pd.to_datetime(date).tz_localize(None)
            valid_prices = price_hist[price_hist.index.tz_localize(None) <= comp_date]
            if not valid_prices.empty:
                close_val = valid_prices.iloc[-1]['Close']
                if pd.notna(close_val):
                    period_end_price = Decimal(str(close_val))
    except:
        pass

    shares_outstanding = max(shares_outstanding, Decimal("0"))
    total_assets = max(total_assets, Decimal("0"))
    total_debt = max(total_debt, Decimal("0"))

    base_args = dict(
        fiscal_date_ending=date_str,
        revenue=revenue,
        ebitda=ebitda,
        gross_profit=gross_profit,
        operating_income=operating_income,
        net_income=net_income,
        operating_cash_flow=operating_cash_flow,
        depreciation_and_amortization=depreciation_and_amortization,
        stock_based_compensation=stock_based_compensation,
        capital_expenditures=capital_expenditures,
        net_investing_cash_flow=net_investing_cash_flow,
        dividends_paid=dividends_paid,
        stock_repurchases=stock_repurchases,
        net_debt_issued=net_debt_issued,
        net_financing_cash_flow=net_financing_cash_flow,
        shares_outstanding=shares_outstanding,
        short_term_debt=short_term_debt,
        long_term_debt=long_term_debt,
        total_debt=total_debt,
        accounts_payable=accounts_payable,
        current_liabilities=current_liabilities,
        total_liabilities=total_liabilities,
        cash_and_equivalents=cash_and_equivalents,
        accounts_receivable=accounts_receivable,
        inventory=inventory,
        current_assets=current_assets,
        net_ppe=net_ppe,
        intangible_assets=intangible_assets,
        total_assets=total_assets,
        interest_expense=interest_expense_direct,
        income_tax_expense=income_tax_expense,
        income_before_tax=income_before_tax
    )
    
    if is_quarter:
        return FinancialQuarter(**base_args, quarter_end_price=period_end_price)
    else:
        return FinancialYear(**base_args, year_end_price=period_end_price)


