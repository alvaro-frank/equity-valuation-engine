import requests
from decimal import Decimal
from domain.interfaces import StockDataProvider
from domain.stock_market import FinancialYear, Stock, Ticker, Price

class SECAdapter(StockDataProvider):
    USER_AGENT = "alvarojf96@hotmail.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self._cik_map = self._load_cik_map()

    def _load_cik_map(self):
        url = "https://www.sec.gov/files/company_tickers.json"
        return {v['ticker']: str(v['cik_str']).zfill(10) for k, v in self.session.get(url).json().items()}

    def _get_value(self, facts, tag_list):
        """Tenta várias tags US-GAAP e retorna um mapa {data: valor}."""
        for tag in tag_list:
            data = facts.get('facts', {}).get('us-gaap', {}).get(tag, {})
            if not data: data = facts.get('facts', {}).get('dei', {}).get(tag, {})
            if not data: continue

            units = data.get('units', {}).get('USD', []) or data.get('units', {}).get('shares', [])
            
            return {e['end']: Decimal(str(e['val'])) for e in units if e.get('fp') == 'FY'}
        return {}

    def get_stock_fundamental_data(self, ticker: Ticker) -> Stock:
        cik = self._cik_map.get(ticker.symbol)
        facts = self.session.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json").json()

        rev_tags = ["RevenueFromContractWithCustomerExcludingRequiredCashDividends", "Revenues", "SalesRevenueNet"]
        inc_tags = ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]
        share_tags = ["EntityCommonStockSharesOutstanding", "WeightedAverageNumberOfSharesOutstandingBasic"]

        revs = self._get_value(facts, rev_tags)
        incs = self._get_value(facts, inc_tags)
        shs = self._get_value(facts, share_tags)
        short = self._get_value(facts, ["DebtCurrent"])
        long = self._get_value(facts, ["LongTermDebtNoncurrent"])

        financial_years = []
        for date in sorted(incs.keys(), reverse=True)[:5]:
            total_debt = short.get(date, 0) + long.get(date, 0)
            financial_years.append(FinancialYear(
                fiscal_date_ending=date,
                revenue=revs.get(date, Decimal("0")),
                net_income=incs.get(date, Decimal("0")),
                ebitda=Decimal("0"), # Calcularemos depois
                operating_cash_flow=Decimal("0"), # Podes adicionar a tag se quiseres
                capital_expenditures=Decimal("0"),
                total_assets=Decimal("0"),
                total_liabilities=Decimal("0"),
                cash_and_equivalents=Decimal("0"),
                total_debt=total_debt,
                shares_outstanding=shs.get(date, Decimal("0"))
            ))

        return Stock(ticker=ticker, price=Price(Decimal("0")), financial_years=financial_years)

    def get_stock_current_price(self, ticker: Ticker) -> Price:
        return Price(Decimal("0"))