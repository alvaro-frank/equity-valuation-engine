from fastapi import APIRouter, Depends, HTTPException

from application.dtos.dtos import TrendingTickerResult
from application.use_cases.get_trending_tickers import GetTrendingTickersUseCase
from infrastructure.adapters.input.dependencies import get_trending_tickers_use_case

router = APIRouter(
    prefix="/api/v1/discovery",
    tags=["discovery"]
)

@router.get("/sector/{sector_key}/trending", response_model=TrendingTickerResult)
async def get_trending_sector(
    sector_key: str,
    use_case: GetTrendingTickersUseCase = Depends(get_trending_tickers_use_case)
):
    """
    Fetches the top trending companies for a specific sector.
    """
    try:
        return await use_case.execute(sector_key=sector_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/industry/{industry_key}/trending", response_model=TrendingTickerResult)
async def get_trending_industry(
    industry_key: str,
    use_case: GetTrendingTickersUseCase = Depends(get_trending_tickers_use_case)
):
    """
    Fetches the top trending companies for a specific industry.
    """
    try:
        return await use_case.execute(industry_key=industry_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
