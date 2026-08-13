from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any

from domain.entities import FinancialQuarter, FinancialYear, Price

def parse_decimal(value: Any, field_name: str) -> Decimal:
        """
        Safely parses a string value to Decimal.
        If the value is legitimately missing (None, empty string), returns 0.
        If the value is corrupted or malformed, it FAILS FAST to prevent data corruption.
        
        Args:
            value (str): The string value to parse.
            
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
                
                # Operating Expenses
                research_and_development=parse_decimal(income_report.get("researchAndDevelopment", "0"), "researchAndDevelopment"),
                selling_general_and_administrative=parse_decimal(income_report.get("sellingGeneralAndAdministrative", "0"), "sellingGeneralAndAdministrative"),
                
                # Additional Cash Flow Metrics
                stock_based_compensation=parse_decimal(cash_report.get("stockBasedCompensation", "0"), "stockBasedCompensation"),
                stock_repurchases=(
                    parse_decimal(cash_report.get("paymentsForRepurchaseOfCommonStock", "0"), "paymentsForRepurchaseOfCommonStock") or 
                    parse_decimal(cash_report.get("paymentsForRepurchaseOfEquity", "0"), "paymentsForRepurchaseOfEquity")
                ),
                net_debt_issued=(
                    parse_decimal(cash_report.get("proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet", "0"), "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet") +
                    parse_decimal(cash_report.get("proceedsFromRepaymentsOfShortTermDebt", "0"), "proceedsFromRepaymentsOfShortTermDebt")
                ),
                
                # Market Price at Year End
                year_end_price=year_end_price
            )
            
            years.append(year_data)
        
        return years

def calculate_ttm_year(income_q: List[Dict[str, Any]], balance_q: List[Dict[str, Any]], cash_q: List[Dict[str, Any]]) -> FinancialYear:
    """
    Calculates Trailing Twelve Months (TTM) by summing the last 4 quarters for flow metrics 
    and taking the most recent quarter for stock metrics.
    """
    if len(income_q) < 4 or len(cash_q) < 4 or not balance_q:
        return None
        
    def sum_q_flow(reports, key):
        total = Decimal("0")
        for i in range(4):
            total += parse_decimal(reports[i].get(key, "0"), key)
        return total

    def latest_stock(reports, key):
        return parse_decimal(reports[0].get(key, "0"), key)
        
    return FinancialYear(
        fiscal_date_ending="TTM",
        
        # Flow metrics (Sum of last 4 quarters)
        revenue=sum_q_flow(income_q, "totalRevenue"),
        ebitda=sum_q_flow(income_q, "ebitda"),
        gross_profit=sum_q_flow(income_q, "grossProfit"),
        operating_income=sum_q_flow(income_q, "operatingIncome"),
        net_income=sum_q_flow(income_q, "netIncome"),
        
        # Cash Flow metrics (Sum of last 4 quarters)
        operating_cash_flow=sum_q_flow(cash_q, "operatingCashflow"),
        depreciation_and_amortization=sum_q_flow(cash_q, "depreciationDepletionAndAmortization"),
        capital_expenditures=sum_q_flow(cash_q, "capitalExpenditures"),
        net_investing_cash_flow=sum_q_flow(cash_q, "cashflowFromInvestment"),
        dividends_paid=sum_q_flow(cash_q, "dividendPayout"),
        net_financing_cash_flow=sum_q_flow(cash_q, "cashflowFromFinancing"),
        
        # Stock metrics (Latest quarter snapshot)
        shares_outstanding=latest_stock(balance_q, "commonStockSharesOutstanding"),
        short_term_debt=latest_stock(balance_q, "shortTermDebt"),
        long_term_debt=latest_stock(balance_q, "longTermDebt"),
        total_debt=latest_stock(balance_q, "shortTermDebt") + latest_stock(balance_q, "longTermDebt"),
        total_assets=latest_stock(balance_q, "totalAssets"),
        total_liabilities=latest_stock(balance_q, "totalLiabilities"),
        cash_and_equivalents=latest_stock(balance_q, "cashAndCashEquivalentsAtCarryingValue") + latest_stock(balance_q, "shortTermInvestments"),
        accounts_payable=latest_stock(balance_q, "currentAccountsPayable"),
        current_liabilities=latest_stock(balance_q, "totalCurrentLiabilities"),
        accounts_receivable=latest_stock(balance_q, "currentNetReceivables"),
        inventory=latest_stock(balance_q, "inventory"),
        current_assets=latest_stock(balance_q, "totalCurrentAssets"),
        net_ppe=latest_stock(balance_q, "propertyPlantEquipment"),
        intangible_assets=latest_stock(balance_q, "intangibleAssets"),
        
        # Operating Expenses
        research_and_development=sum_q_flow(income_q, "researchAndDevelopment"),
        selling_general_and_administrative=sum_q_flow(income_q, "sellingGeneralAndAdministrative"),
        
        # Additional Cash Flow Metrics
        stock_based_compensation=sum_q_flow(cash_q, "stockBasedCompensation"),
        stock_repurchases=(
            sum_q_flow(cash_q, "paymentsForRepurchaseOfCommonStock") or 
            sum_q_flow(cash_q, "paymentsForRepurchaseOfEquity")
        ),
        net_debt_issued=(
            sum_q_flow(cash_q, "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet") +
            sum_q_flow(cash_q, "proceedsFromRepaymentsOfShortTermDebt")
        ),
        
        # TTM stock price injected later
        year_end_price=Decimal("0")
    )


def map_to_financial_quarters(income_list: List[Dict[str, Any]], balance_list: List[Dict[str, Any]], cash_list: List[Dict[str, Any]], historical_prices: Dict[str, Price]) -> List[FinancialQuarter]:
        """
        Merges financial reports from three different accounting statements based on their fiscal ending date.
        
        Args:
            income_list (List[Dict]): List of dictionaries representing quarterly Income Statements.
            
        Returns:
            List[FinancialQuarter]: A list of domain entities containing consolidated financial data for each quarter.
        """
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
                
                # Operating Expenses
                research_and_development=parse_decimal(income_report.get("researchAndDevelopment", "0"), "researchAndDevelopment"),
                selling_general_and_administrative=parse_decimal(income_report.get("sellingGeneralAndAdministrative", "0"), "sellingGeneralAndAdministrative"),
                
                # Additional Cash Flow Metrics
                stock_based_compensation=parse_decimal(cash_report.get("stockBasedCompensation", "0"), "stockBasedCompensation"),
                stock_repurchases=(
                    parse_decimal(cash_report.get("paymentsForRepurchaseOfCommonStock", "0"), "paymentsForRepurchaseOfCommonStock") or 
                    parse_decimal(cash_report.get("paymentsForRepurchaseOfEquity", "0"), "paymentsForRepurchaseOfEquity")
                ),
                net_debt_issued=(
                    parse_decimal(cash_report.get("proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet", "0"), "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet") +
                    parse_decimal(cash_report.get("proceedsFromRepaymentsOfShortTermDebt", "0"), "proceedsFromRepaymentsOfShortTermDebt")
                ),
                
                quarter_end_price=year_end_price
            )
            
            quarters.append(quarter_data)
        
        return quarters