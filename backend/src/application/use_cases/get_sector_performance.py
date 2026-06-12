import logging
from application.ports.ports import QuantitativeDataPort, PerformanceDataPort
from application.dtos.dtos import SectorPerformanceResult

SECTOR_ETF_MAP = {
    "technology": "XLK",
    "software-infrastructure": "IGV",
    "semiconductors": "SMH",
    "healthcare": "XLV",
    "financial-services": "XLF",
    "consumer-cyclical": "XLY",
    "industrials": "XLI",
    "energy": "XLE",
    "utilities": "XLU",
    "real-estate": "XLRE",
    "basic-materials": "XLB",
    "consumer-defensive": "XLP",
    "communication-services": "XLC"
}


class GetSectorPerformanceUseCase:
    """
    Use case for fetching the relative performance of a company's sector 
    compared to the S&P 500 (SPY).
    """
    def __init__(self, quant_port: QuantitativeDataPort, performance_port: PerformanceDataPort):
        self.quant_port = quant_port
        self.performance_port = performance_port

    async def execute(self, ticker: str) -> SectorPerformanceResult:
        # 1. Fetch basic info to determine sector/industry
        try:
            ticker_info = await self.quant_port.get_ticker_info(ticker)
            sector = ticker_info.sector_key or ticker_info.sector or ""
            industry = ticker_info.industry_key or ticker_info.industry or ""
            
            sector = sector.lower().replace(" ", "-")
            industry = industry.lower().replace(" ", "-")
        except Exception as e:
            logging.warning(f"Failed to get sector info for {ticker}: {e}")
            sector = ""
            industry = ""

        # 2. Map to ETF
        # Try industry first for more precision, then fallback to sector
        etf_ticker = SECTOR_ETF_MAP.get(industry, SECTOR_ETF_MAP.get(sector, "SPY"))
        
        # If we couldn't find a mapping, fallback to QQQ vs SPY as a generic tech/market comparison
        benchmark_ticker = "SPY"
        if etf_ticker == benchmark_ticker:
            etf_ticker = "QQQ"
            
        tickers_to_fetch = [etf_ticker, benchmark_ticker]

        # 3. Fetch historical performance data (last 5 years)
        chart_data = await self.performance_port.get_historical_performance_chart(tickers_to_fetch, period="5y")

        return SectorPerformanceResult(
            sector=sector,
            industry=industry,
            benchmark_ticker="SPY",
            etf_ticker=etf_ticker,
            chart_data=chart_data
        )
