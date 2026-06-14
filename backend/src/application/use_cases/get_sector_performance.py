import logging
from application.ports.ports import QuantitativeDataPort, PerformanceDataPort
from application.dtos.dtos import SectorPerformanceResult

SECTOR_ETF_MAP = {
    "technology": "XLK",
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

INDUSTRY_ETF_MAP = {
    "biotechnology": "IBB",
    "banks-regional": "KRE",
    "software-application": "IGV",
    "software-infrastructure": "IGV",
    "asset-management": "KCE",
    "medical-devices": "IHI",
    "capital-markets": "KCE",
    "aerospace-defense": "ITA",
    "aerospace-&-defense": "ITA",
    "drug-manufacturers-general": "PPH",
    "drug-manufacturers-specialty-generic": "PPH",
    "oil-gas-e-p": "XOP",
    "internet-content-information": "FDN",
    "semiconductors": "SMH",
    "semiconductor-equipment-materials": "SMH",
    "packaged-foods": "PBJ",
    "grocery-stores": "PBJ",
    "medical-instruments-supplies": "IHI",
    "oil-gas-midstream": "AMLP",
    "auto-manufacturers": "CARZ",
    "auto-parts": "CARZ",
    "telecom-services": "IYZ",
    "communication-equipment": "IGN",
    "gold": "GDX",
    "engineering-construction": "PAVE",
    "restaurants": "PEJ",
    "leisure": "PEJ",
    "medical-care-facilities": "IHF",
    "healthcare-plans": "IHF",
    "other-industrial-metals-mining": "XME",
    "oil-gas-equipment-services": "XES",
    "specialty-retail": "XRT",
    "apparel-retail": "XRT",
    "internet-retail": "XRT",
    "entertainment": "PEJ",
    "travel-services": "PEJ",
    "insurance-property-casualty": "KIE",
    "insurance-life": "KIE",
    "insurance-specialty": "KIE",
    "insurance-diversified": "KIE",
    "reit-mortgage": "REM",
    "credit-services": "IPAY",
    "financial-data-stock-exchanges": "IAI",
    "marine-shipping": "IYT",
    "integrated-freight-logistics": "IYT",
    "trucking": "IYT",
    "railroads": "IYT",
    "building-products-equipment": "ITB",
    "residential-construction": "ITB",
    "electronic-gaming-multimedia": "HERO",
    "utilities-renewable": "ICLN",
    "solar": "TAN",
    "reit-residential": "REZ",
    "steel": "SLX",
    "banks-diversified": "KBE",
    "farm-products": "MOO",
    "agricultural-inputs": "MOO",
    "oil-gas-refining-marketing": "CRAK",
    "airlines": "JETS",
    "chemicals": "VAW",
    "specialty-chemicals": "VAW",
    "resorts-casinos": "BJK",
    "gambling": "BJK",
    "utilities-regulated-water": "CGW",
    "uranium": "URA"
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

        # 2. Map to ETFs
        sector_etf = SECTOR_ETF_MAP.get(sector, "SPY")
        industry_etf = INDUSTRY_ETF_MAP.get(industry, None)
        benchmark_ticker = "SPY"
        
        # Build the list of tickers to fetch uniquely
        tickers_set = {benchmark_ticker, sector_etf, ticker}
        if industry_etf:
            tickers_set.add(industry_etf)
            
        tickers_to_fetch = list(tickers_set)

        # 3. Fetch historical performance data (last 5 years)
        chart_data = await self.performance_port.get_historical_performance_chart(tickers_to_fetch, period="5y")

        return SectorPerformanceResult(
            company_ticker=ticker,
            sector=sector,
            industry=industry,
            benchmark_ticker=benchmark_ticker,
            sector_etf=sector_etf,
            industry_etf=industry_etf if industry_etf != sector_etf else None,
            chart_data=chart_data
        )
