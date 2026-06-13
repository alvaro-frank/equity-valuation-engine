from typing import Optional
from application.ports.ports import TrendingDataPort
from application.dtos.dtos import TrendingTickerResult, TrendingTickerDTO

class GetTrendingTickersUseCase:
    """
    Service responsible for fetching trending tickers by sector or industry.
    """
    def __init__(self, trending_port: TrendingDataPort):
        self.trending_port = trending_port

    async def execute(self, sector_key: Optional[str] = None, industry_key: Optional[str] = None) -> TrendingTickerResult:
        """
        Fetches trending tickers by sector or industry.
        
        Args:
            sector_key (Optional[str]): The sector key.
            industry_key (Optional[str]): The industry key.
            
        Returns:
            TrendingTickerResult: DTO containing the trending tickers.
        """
        if industry_key:
            results = await self.trending_port.get_trending_by_industry(industry_key)
        elif sector_key:
            results = await self.trending_port.get_trending_by_sector(sector_key)
        else:
            raise ValueError("Either sector_key or industry_key must be provided")
            
        dto_results = [
            TrendingTickerDTO(
                symbol=r["symbol"],
                name=r["name"],
                rating=r.get("rating"),
                weight=r.get("weight")
            )
            for r in results
        ]
        
        return TrendingTickerResult(results=dto_results)
