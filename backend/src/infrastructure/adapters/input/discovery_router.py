from fastapi import APIRouter, Depends, HTTPException
from typing import List

from application.dtos.dtos import TrendingTickersResponse, TrendingTickerDTO
from infrastructure.adapters.output.yfinance_adapter import YfinanceAdapter
from infrastructure.adapters.input.dependencies import get_yfinance_adapter

router = APIRouter(
    prefix="/api/v1/discovery",
    tags=["discovery"]
)

@router.get("/sector/{sector_key}/trending", response_model=TrendingTickersResponse)
async def get_trending_sector(
    sector_key: str,
    yfinance_adapter: YfinanceAdapter = Depends(get_yfinance_adapter)
):
    """
    Fetches the top trending companies for a specific sector.
    """
    try:
        results = await yfinance_adapter.get_trending_by_sector(sector_key)
        dtos = [TrendingTickerDTO(**r) for r in results]
        return TrendingTickersResponse(results=dtos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/industry/{industry_key}/trending", response_model=TrendingTickersResponse)
async def get_trending_industry(
    industry_key: str,
    yfinance_adapter: YfinanceAdapter = Depends(get_yfinance_adapter)
):
    """
    Fetches the top trending companies for a specific industry.
    """
    try:
        results = await yfinance_adapter.get_trending_by_industry(industry_key)
        dtos = [TrendingTickerDTO(**r) for r in results]
        return TrendingTickersResponse(results=dtos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
