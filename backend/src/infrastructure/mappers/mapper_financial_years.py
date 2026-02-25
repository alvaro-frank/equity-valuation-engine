from decimal import Decimal
from typing import List, Dict, Any

from domain.entities import FinancialYear

def parse_decimal(value: str) -> Decimal:
        """
        Safely parses a string value to Decimal, returning 0 if the value is None or invalid.
        
        Args:
            value (str): The string value to parse.
            
        Raises:
            ValueError: If the value cannot be parsed to a Decimal and is not None or "None".
            
        Returns:
            Decimal: The parsed decimal value, or 0 if the input is invalid.
        """
        if value is None or value == "None" or value == "":
            return Decimal("0")
        try:
            return Decimal(value)
        except Exception:
            return Decimal("0")

def map_to_financial_years(income_list: List[Dict[str, Any]], balance_list: List[Dict[str, Any]], cash_list: List[Dict[str, Any]]) -> List[FinancialYear]:
        """
        Merges financial reports from three different accounting statements based on their fiscal ending date.

        This function iterates through the income statements and attempts to find matching
        balance sheet and cash flow reports for the same date. It ensures that data integrity
        is maintained by validating that all three reports exist for a given year.

        Args:
            income_list (List[Dict]): List of dictionaries representing yearly Income Statements.
            balance_list (List[Dict]): List of dictionaries representing yearly Balance Sheets.
            cash_list (List[Dict]): List of dictionaries representing yearly Cash Flow Statements.

        Raises:
            ValueError: If a corresponding Balance Sheet or Cash Flow report is missing for a 
                        date found in the Income Statements.

        Returns:
            List[FinancialYear]: A list of domain entities containing consolidated financial data.
        """
        balance_map = {report.get("fiscalDateEnding"): report for report in balance_list}
        cash_map = {report.get("fiscalDateEnding"): report for report in cash_list}
    
        years = []

        for income_report in income_list:
            fiscal_date = income_report.get("fiscalDateEnding")
            if not fiscal_date:
                continue
            
            balance_report = balance_map.get(fiscal_date)
            cash_report = cash_map.get(fiscal_date)
            
            if not balance_report or not cash_report:
                raise ValueError(
                    f"Missing data on date: {fiscal_date}. "
                    f"Balance: {'OK' if balance_report else 'MISSING'}, "
                    f"CashFlow: {'OK' if cash_report else 'MISSING'}"
                )
            
            year_data = FinancialYear(
                fiscal_date_ending=fiscal_date,
                # Revenue and Earnings
                revenue=parse_decimal(income_report.get("totalRevenue", "0")),
                ebitda=parse_decimal(income_report.get("ebitda", "0")),
                # Gross Profit and Operating Income
                gross_profit=parse_decimal(income_report.get("grossProfit", "0")),
                operating_income=parse_decimal(income_report.get("operatingIncome", "0")),
                # Net Income
                net_income=parse_decimal(income_report.get("netIncome", "0")),
                #Cash Flow
                operating_cash_flow=parse_decimal(cash_report.get("operatingCashflow", "0")),
                capital_expenditures=parse_decimal(cash_report.get("capitalExpenditures", "0")),
                # Shares Outstanding
                shares_outstanding=parse_decimal(balance_report.get("commonStockSharesOutstanding", "0")),
                # Debt
                short_term_debt=parse_decimal(balance_report.get("shortTermDebt")),
                long_term_debt=parse_decimal(balance_report.get("longTermDebt")),
                total_debt=parse_decimal(balance_report.get("shortTermDebt", "0")) + 
                        parse_decimal(balance_report.get("longTermDebt", "0")),
                # Assets and Liabilities
                total_assets=parse_decimal(balance_report.get("totalAssets", "0")),
                total_liabilities=parse_decimal(balance_report.get("totalLiabilities", "0")),
                cash_and_equivalents=parse_decimal(balance_report.get("cashAndCashEquivalentsAtCarryingValue", "0")),
            )
            
            years.append(year_data)
        
        return years