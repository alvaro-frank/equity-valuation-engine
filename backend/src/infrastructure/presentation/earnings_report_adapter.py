from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.dtos.dtos import EarningsReportResult

class EarningsReportAdapter:
    """
    Controller responsible for orchestrating the earnings report valuation process performing analysis using the EarningsReportUseCase.
    """
    def __init__(self, service: EarningsReportUseCase):
        """
        Initializes the controller with an injected EarningsReportUseCase.
        
        Args:
            service (EarningsReportUseCase): The service to handle the valuation logic.
        """
        self.service = service

    async def run(self, ticker_symbol: str, pdf_file_path: str):
        """
        Main method to run the earnings report valuation process.
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            pdf_file_path (str): The path to the PDF file.
        """
        try:
            dto = await self.service.analyse_earnings_report(ticker_symbol, pdf_file_path)
            self._display_results(dto)
        except Exception as e:
            print(f"Error analyzing earnings report: {e}")

    def _display_results(self, result: EarningsReportResult):
        """
        Nicely formats and prints the earnings report valuation results to the console.
        
        Args:
            result (EarningsReportResult): The result of the earnings report analysis to display.
        """
        print(f"\n{'='*80}")
        print(f"VALUE INVESTING EARNINGS ANALYSIS: {result.ticker.name} ({result.ticker.symbol})")
        print(f"Period Ended: {result.period_end_date}")
        print(f"{'='*80}")
        
        print(f"\n[1] CORE PERFORMANCE (Non-GAAP):")
        print(f"  - Adjusted Revenue: {result.core_performance.adjusted_revenue.amount:,.2f} (YoY: {result.core_performance.adjusted_revenue.yoy_growth:+.2f}%)")
        print(f"  - Adjusted EPS: {result.core_performance.adjusted_eps.amount:,.2f} (YoY: {result.core_performance.adjusted_eps.yoy_growth:+.2f}%)")
        print(f"  - Adj EBITDA Margin: {result.core_performance.adjusted_ebitda_margin.amount:,.2f} (YoY: {result.core_performance.adjusted_ebitda_margin.yoy_growth:+.2f}%)")
        print(f"  - Free Cash Flow: {result.core_performance.free_cash_flow.amount:,.2f} (YoY: {result.core_performance.free_cash_flow.yoy_growth:+.2f}%)")
        
        print(f"\n[2] CAPITAL ALLOCATION:")
        print(f"  - Share Buybacks: {result.capital_allocation.share_buybacks:,.2f}")
        print(f"  - Dividends: {result.capital_allocation.dividends:,.2f}")
        print(f"  - CapEx/R&D: {result.capital_allocation.capex_rd:,.2f}")
        print(f"  - Infrastructure Assessment: {result.capital_allocation.infrastructure_assessment}")
        
        print(f"\n[3] FORWARD GUIDANCE:")
        print(f"  {result.forward_guidance}")
        
        print(f"\n[4] MOAT TRAJECTORY:")
        print(f"  {result.moat_trajectory}")
        
        print(f"\n[5] RISK DECONSTRUCTION:")
        print(f"  External/Macro Risks:")
        for r in result.risk_deconstruction.macro_risks:
            print(f"   - {r}")
        print(f"  Internal/Execution Risks:")
        for r in result.risk_deconstruction.internal_risks:
            print(f"   - {r}")
            
        print(f"\n[!] THE BOTTOM LINE:")
        print(f"  {result.bottom_line}")
        
        print(f"\n{'='*80}\n")