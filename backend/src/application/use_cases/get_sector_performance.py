from typing import Dict, Any
import asyncio
from application.ports.ports import QuantitativeDataPort

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
    def __init__(self, quant_port: QuantitativeDataPort):
        self.quant_port = quant_port

    async def execute(self, ticker: str) -> Dict[str, Any]:
        # 1. Fetch basic info to determine sector/industry
        try:
            ticker_info = await self.quant_port.get_ticker_info(ticker)
            sector = ticker_info.sector_key or ticker_info.sector or ""
            industry = ticker_info.industry_key or ticker_info.industry or ""
            
            sector = sector.lower().replace(" ", "-")
            industry = industry.lower().replace(" ", "-")
        except Exception as e:
            print(f"Failed to get sector info for {ticker}: {e}")
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
        chart_data = await self.quant_port.get_historical_performance_chart(tickers_to_fetch, period="5y")

        return {
            "sector": sector,
            "industry": industry,
            "etf_ticker": etf_ticker,
            "benchmark_ticker": benchmark_ticker,
            "chart_data": chart_data
        }
