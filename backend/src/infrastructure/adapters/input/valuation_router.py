from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
import os

from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from application.use_cases.get_sector_performance import GetSectorPerformanceUseCase
from domain.exceptions import TickerNotFoundError, RateLimitExceededError

from infrastructure.adapters.input.dependencies import (
    get_earnings_report_use_case,
    get_quantitative_use_case,
    get_qualitative_use_case,
    get_sector_use_case,
    get_sector_performance_use_case
)

from application.dtos.dtos import (
    EarningsReportResult,
    QuantitativeValuationResult,
    QualitativeValuationResult,
    SectorIndustrialValuationResult,
    TickerSearchResponse,
    TickerSearchResult
)
import httpx

router = APIRouter(
    prefix="/api/v1/valuation",
    tags=["Valuation"]
)

@router.get("/search", response_model=TickerSearchResponse)
async def search_ticker(
    q: str = Query(..., description="Search query for ticker or company name")
):
    """
    Searches for a ticker or company name using Yahoo Finance autocomplete API.
    """
    if not q or len(q) < 1:
        return TickerSearchResponse(results=[])
        
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={q}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=5.0)
            
            if response.status_code != 200:
                return TickerSearchResponse(results=[])
                
            data = response.json()
            quotes = data.get("quotes", [])
            
            # Filter for Equity types and extract relevant fields
            results = []
            for quote in quotes:
                if quote.get("quoteType") == "EQUITY":
                    results.append(TickerSearchResult(
                        symbol=quote.get("symbol", ""),
                        name=quote.get("shortname", quote.get("longname", "")),
                        exchange=quote.get("exchDisp", "")
                    ))
                    if len(results) >= 6: # limit to 6 results
                        break
                        
            return TickerSearchResponse(results=results)
    except Exception as e:
        # Silently fail for autocomplete
        return TickerSearchResponse(results=[])

@router.post("/earnings/{ticker}", response_model=EarningsReportResult)
async def analyse_earnings_report(
    ticker: str,
    file: UploadFile = File(...),
    lang: str = Query("en", description="Language to generate the report in"),
    use_case: EarningsReportUseCase = Depends(get_earnings_report_use_case)
):
    """
    Analyses an Earnings Report (PDF) using the Gemini-powered Value Investing prompt.
    Returns a structured DTO with Core Performance, Capital Allocation, and Risk Deconstruction.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    import tempfile
    import shutil
    
    try:
        # Create a temporary file to save the uploaded PDF
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, 'wb') as f:
            shutil.copyfileobj(file.file, f)
            
        result = await use_case.analyse_earnings_report(ticker.upper(), temp_path, language=lang)
        return result
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "rate limit" in error_str or "quota" in error_str:
            raise HTTPException(status_code=429, detail="rate_limit_exceeded")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Error removing temporary file: {e}")

@router.get("/quantitative/{ticker}", response_model=QuantitativeValuationResult)
async def analyse_quantitative(
    ticker: str,
    years: int = Query(10, description="Number of years of historical data to retrieve"),
    use_case: QuantitativeValuationUseCase = Depends(get_quantitative_use_case)
):
    """
    Analyses the historical financial data of a given company.
    Returns a structured DTO with quantitative metrics and CAGRs.
    """
    try:
        result = await use_case.evaluate_ticker(ticker.upper(), years)
        return result
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "rate limit" in error_str or "quota" in error_str:
            raise HTTPException(status_code=429, detail="rate_limit_exceeded")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/qualitative/{ticker}", response_model=QualitativeValuationResult)
async def analyse_qualitative(
    ticker: str,
    lang: str = Query("en", description="Language to generate the report in"),
    use_case: QualitativeValuationUseCase = Depends(get_qualitative_use_case)
):
    """
    Generates a qualitative profile of the company, extracting the CEO, moat, competitors, etc.
    Returns a structured DTO representing the company profile.
    """
    try:
        result = await use_case.analyse_ticker(ticker.upper(), language=lang)
        return result
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "rate limit" in error_str or "quota" in error_str:
            raise HTTPException(status_code=429, detail="rate_limit_exceeded")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sector/{ticker}", response_model=SectorIndustrialValuationResult)
async def analyse_sector(
    ticker: str,
    lang: str = Query("en", description="Language to generate the report in"),
    use_case: SectorIndustrialValuationUseCase = Depends(get_sector_use_case)
):
    """
    Analyses the sector and industry dynamics (Porter's Five Forces, etc.) for a given ticker.
    Returns a structured DTO with the industry structural analysis.
    """
    try:
        result = await use_case.evaluate_industry_by_ticker(ticker.upper(), language=lang)
        return result
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "rate limit" in error_str or "quota" in error_str:
            raise HTTPException(status_code=429, detail="rate_limit_exceeded")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sector-performance/{ticker}")
async def get_sector_performance(
    ticker: str,
    use_case: GetSectorPerformanceUseCase = Depends(get_sector_performance_use_case)
):
    """
    Fetches the relative performance of a company's sector vs SPY over the last 5 years.
    Returns the normalized historical closing prices.
    """
    try:
        result = await use_case.execute(ticker.upper())
        return result
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
