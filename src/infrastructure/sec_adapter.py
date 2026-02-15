import requests
from decimal import Decimal
from typing import List, Dict, Optional
from services.dtos import PriceDTO, TickerDTO, FinancialYearDTO, StockDataDTO

class SECAdapter:
    USER_AGENT = "Alvaro Franco alvarojf96@hotmail.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self._cik_map = self._load_cik_map()

    def _load_cik_map(self) -> Dict[str, str]:
        url = "https://www.sec.gov/files/company_tickers.json"
        try:
            response = self.session.get(url)
            return {v['ticker']: str(v['cik_str']).zfill(10) for k, v in response.json().items()}
        except: return {}

    def _get_value(self, facts: dict, tag_list: List[str]) -> Dict[str, Decimal]:
        for tag in tag_list:
            data = facts.get('facts', {}).get('us-gaap', {}).get(tag, {})
            if not data: data = facts.get('facts', {}).get('dei', {}).get(tag, {})
            if not data: continue

            units = data.get('units', {}).get('USD', []) or data.get('units', {}).get('shares', [])
            extracted = {}
            for e in units:
                if e.get('form') == '10-K' or e.get('fp') == 'FY':
                    extracted[e['end']] = Decimal(str(e['val']))
            
            if extracted: return extracted
        return {}

    def _find_closest_value(self, data_map: Dict[str, Decimal], target_date: str) -> Decimal:
        if target_date in data_map:
            return data_map[target_date]
        
        target_month = target_date[:7]
        for date, value in data_map.items():
            if date.startswith(target_month):
                return value
        return Decimal("0")

    def get_stock_fundamental_data(self, symbol: str) -> StockDataDTO:
        cik = self._cik_map.get(symbol.upper())
        if not cik: raise ValueError(f"CIK not found for symbol: {symbol}")

        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        facts = self.session.get(url).json()
        
        rev_tags = [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "Revenues", 
            "SalesRevenueNet",
            "RevenueFromContractWithCustomerExcludingRequiredCashDividends"
        ]
        inc_tags = ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]
        gross_tags = ["GrossProfit", "GrossProfitLoss"]
        
        rev_map = self._get_value(facts, rev_tags)
        inc_map = self._get_value(facts, inc_tags)
        gross_map = self._get_value(facts, gross_tags)
        
        available_dates = sorted(inc_map.keys(), reverse=True)
        financial_years_dto = []

        for date in available_dates[:5]:
            revenue = self._find_closest_value(rev_map, date)
            gross_profit = self._find_closest_value(gross_map, date)
            net_income = inc_map[date]

            financial_years_dto.append(FinancialYearDTO(
                fiscal_date_ending=date,
                revenue=revenue,
                net_income=net_income,
                ebitda=Decimal("0"),
                gross_profit=gross_profit,
                operating_income=Decimal("0"),
                operating_cash_flow=Decimal("0"),
                capital_expenditures=Decimal("0"),
                shares_outstanding=Decimal("0"),
                short_term_debt=Decimal("0"),
                long_term_debt=Decimal("0"),
                total_debt=Decimal("0"),
                total_assets=Decimal("0"),
                total_liabilities=Decimal("0"),
                cash_and_equivalents=Decimal("0")
            ))

        return StockDataDTO(
            ticker=TickerDTO(symbol=symbol.upper(), name=facts.get('entityName', symbol)),
            price=PriceDTO(amount=Decimal("0"), currency="USD"),
            financial_years=financial_years_dto
        )