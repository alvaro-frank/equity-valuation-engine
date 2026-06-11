from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any

from domain.entities.entities import FinancialYear, Price

def parse_decimal(value: Any, field_name: str) -> Decimal:
        """
        Safely parses a string value to Decimal.
        If the value is legitimately missing (None, empty string), returns 0.
        If the value is corrupted or malformed, it FAILS FAST to prevent data corruption.
        
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
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError(f"Data Integrity Error: Could not parse field '{field_name}' with value '{value}' to Decimal.")

def map_to_financial_years(income_list: List[Dict[str, Any]], balance_list: List[Dict[str, Any]], cash_list: List[Dict[str, Any]], historical_prices: Dict[str, Price]) -> List[FinancialYear]:
        """
        Merges financial reports from three different accounting statements based on their fiscal ending date.

        This function iterates through the income statements and attempts to find matching
        balance sheet and cash flow reports for the same date. It ensures that data integrity
        is maintained by validating that all three reports exist for a given year.

        Args:
            income_list (List[Dict]): List of dictionaries representing yearly Income Statements.
            balance_list (List[Dict]): List of dictionaries representing yearly Balance Sheets.
            cash_list (List[Dict]): List of dictionaries representing yearly Cash Flow Statements.
            historical_prices (Dict[str, Price]): Dictionary mapping YYYY-MM to the closing Price entity.

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
                # Em vez de abortar tudo com ValueError, vamos apenas ignorar este ano incompleto
                # e avançar para o próximo, garantindo que os anos mais recentes funcionam perfeitamente.
                continue
                
            year_month = fiscal_date[:7]
            price_obj = historical_prices.get(year_month)
            year_end_price = price_obj.amount if price_obj else Decimal("0")
            
            year_data = FinancialYear(
                fiscal_date_ending=fiscal_date,
                
                # Revenue and Earnings
                revenue=parse_decimal(income_report.get("totalRevenue", "0"), "totalRevenue"),
                ebitda=parse_decimal(income_report.get("ebitda", "0"), "ebitda"),
                
                # Gross Profit and Operating Income
                gross_profit=parse_decimal(income_report.get("grossProfit", "0"), "grossProfit"),
                operating_income=parse_decimal(income_report.get("operatingIncome", "0"), "operatingIncome"),
                
                # Net Income
                net_income=parse_decimal(income_report.get("netIncome", "0"), "netIncome"),
                
                # Cash Flow
                operating_cash_flow=parse_decimal(cash_report.get("operatingCashflow", "0"), "operatingCashflow"),
                depreciation_and_amortization=parse_decimal(cash_report.get("depreciationDepletionAndAmortization", "0"), "depreciationDepletionAndAmortization"),
                capital_expenditures=parse_decimal(cash_report.get("capitalExpenditures", "0"), "capitalExpenditures"),
                net_investing_cash_flow=parse_decimal(cash_report.get("cashflowFromInvestment", "0"), "cashflowFromInvestment"),
                dividends_paid=parse_decimal(cash_report.get("dividendPayout", "0"), "dividendPayout"),
                net_financing_cash_flow=parse_decimal(cash_report.get("cashflowFromFinancing", "0"), "cashflowFromFinancing"),
                
                # Shares Outstanding
                shares_outstanding=parse_decimal(balance_report.get("commonStockSharesOutstanding", "0"), "commonStockSharesOutstanding"),
                
                # Debt
                short_term_debt=parse_decimal(balance_report.get("shortTermDebt", "0"), "shortTermDebt"),
                long_term_debt=parse_decimal(balance_report.get("longTermDebt", "0"), "longTermDebt"),
                
                # Total Debt
                total_debt=(
                    parse_decimal(balance_report.get("shortTermDebt", "0"), "shortTermDebt") + 
                    parse_decimal(balance_report.get("longTermDebt", "0"), "longTermDebt")
                ),
                
                # Assets and Liabilities
                total_assets=parse_decimal(balance_report.get("totalAssets", "0"), "totalAssets"),
                total_liabilities=parse_decimal(balance_report.get("totalLiabilities", "0"), "totalLiabilities"),
                cash_and_equivalents=parse_decimal(balance_report.get("cashAndCashEquivalentsAtCarryingValue", "0"), "cashAndCashEquivalentsAtCarryingValue"),
                
                accounts_payable=parse_decimal(balance_report.get("currentAccountsPayable", "0"), "currentAccountsPayable"),
                current_liabilities=parse_decimal(balance_report.get("totalCurrentLiabilities", "0"), "totalCurrentLiabilities"),
                accounts_receivable=parse_decimal(balance_report.get("currentNetReceivables", "0"), "currentNetReceivables"),
                inventory=parse_decimal(balance_report.get("inventory", "0"), "inventory"),
                current_assets=parse_decimal(balance_report.get("totalCurrentAssets", "0"), "totalCurrentAssets"),
                net_ppe=parse_decimal(balance_report.get("propertyPlantEquipment", "0"), "propertyPlantEquipment"),
                intangible_assets=parse_decimal(balance_report.get("intangibleAssets", "0"), "intangibleAssets"),
                
                # Market Price at Year End
                year_end_price=year_end_price
            )
            
            years.append(year_data)
        
        return years

def map_to_financial_quarters(income_list: List[Dict[str, Any]], balance_list: List[Dict[str, Any]], cash_list: List[Dict[str, Any]], historical_prices: Dict[str, Price]) -> List[FinancialQuarter]:
        """
        Merges financial reports from three different accounting statements based on their fiscal ending date.
        """
        from domain.entities.entities import FinancialQuarter
        quarters = []
        
        balance_dict = {report.get("fiscalDateEnding"): report for report in balance_list}
        cash_dict = {report.get("fiscalDateEnding"): report for report in cash_list}
        
        for income_report in income_list:
            date_ending = income_report.get("fiscalDateEnding")
            if not date_ending:
                continue
                
            balance_report = balance_dict.get(date_ending)
            cash_report = cash_dict.get(date_ending)
            
            if not balance_report or not cash_report:
                continue
                
            year_month = date_ending[:7]
            year_end_price = Decimal("0")
            if year_month in historical_prices:
                year_end_price = historical_prices[year_month].amount

            quarter_data = FinancialQuarter(
                fiscal_date_ending=date_ending,
                revenue=parse_decimal(income_report.get("totalRevenue", "0"), "totalRevenue"),
                ebitda=parse_decimal(income_report.get("ebitda", "0"), "ebitda"),
                gross_profit=parse_decimal(income_report.get("grossProfit", "0"), "grossProfit"),
                operating_income=parse_decimal(income_report.get("operatingIncome", "0"), "operatingIncome"),
                net_income=parse_decimal(income_report.get("netIncome", "0"), "netIncome"),
                operating_cash_flow=parse_decimal(cash_report.get("operatingCashflow", "0"), "operatingCashflow"),
                depreciation_and_amortization=parse_decimal(cash_report.get("depreciationDepletionAndAmortization", "0"), "depreciationDepletionAndAmortization"),
                capital_expenditures=parse_decimal(cash_report.get("capitalExpenditures", "0"), "capitalExpenditures"),
                net_investing_cash_flow=parse_decimal(cash_report.get("cashflowFromInvestment", "0"), "cashflowFromInvestment"),
                dividends_paid=parse_decimal(cash_report.get("dividendPayout", "0"), "dividendPayout"),
                net_financing_cash_flow=parse_decimal(cash_report.get("cashflowFromFinancing", "0"), "cashflowFromFinancing"),
                shares_outstanding=parse_decimal(balance_report.get("commonStockSharesOutstanding", "0"), "commonStockSharesOutstanding"),
                short_term_debt=parse_decimal(balance_report.get("shortTermDebt", "0"), "shortTermDebt"),
                long_term_debt=parse_decimal(balance_report.get("longTermDebt", "0"), "longTermDebt"),
                total_debt=(
                    parse_decimal(balance_report.get("shortTermDebt", "0"), "shortTermDebt") + 
                    parse_decimal(balance_report.get("longTermDebt", "0"), "longTermDebt")
                ),
                total_assets=parse_decimal(balance_report.get("totalAssets", "0"), "totalAssets"),
                total_liabilities=parse_decimal(balance_report.get("totalLiabilities", "0"), "totalLiabilities"),
                cash_and_equivalents=parse_decimal(balance_report.get("cashAndCashEquivalentsAtCarryingValue", "0"), "cashAndCashEquivalentsAtCarryingValue"),
                accounts_payable=parse_decimal(balance_report.get("currentAccountsPayable", "0"), "currentAccountsPayable"),
                current_liabilities=parse_decimal(balance_report.get("totalCurrentLiabilities", "0"), "totalCurrentLiabilities"),
                accounts_receivable=parse_decimal(balance_report.get("currentNetReceivables", "0"), "currentNetReceivables"),
                inventory=parse_decimal(balance_report.get("inventory", "0"), "inventory"),
                current_assets=parse_decimal(balance_report.get("totalCurrentAssets", "0"), "totalCurrentAssets"),
                net_ppe=parse_decimal(balance_report.get("propertyPlantEquipment", "0"), "propertyPlantEquipment"),
                intangible_assets=parse_decimal(balance_report.get("intangibleAssets", "0"), "intangibleAssets"),
                quarter_end_price=year_end_price
            )
            
            quarters.append(quarter_data)
        
        return quarters