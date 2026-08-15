from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
import os
import tempfile
import shutil
from typing import Optional
from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.use_cases.analyse_dcf_valuation import AnalyseDCFValuationUseCase
from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from application.use_cases.get_sector_performance import GetSectorPerformanceUseCase
from application.use_cases.get_earnings_call_transcript import GetEarningsCallTranscriptUseCase
from application.use_cases.get_available_filings import GetAvailableFilingsUseCase
from application.use_cases.search_tickers import SearchTickersUseCase

from application.exceptions.exceptions import (
    TickerNotFoundError,
    RateLimitExceededError,
    ConfigurationError,
    ExternalServiceError,
    LLMParsingError,
    InvalidDocumentFormatError,
    DataFetchError
)
from domain.exceptions.exceptions import DomainValidationError

from infrastructure.adapters.input.dependencies import (
    get_earnings_report_use_case,
    get_quantitative_use_case,
    get_qualitative_use_case,
    get_sector_use_case,
    get_sector_performance_use_case,
    get_transcript_use_case,
    get_dcf_use_case,
    get_search_tickers_use_case,
    get_quantitative_adapter,
    get_available_filings_use_case
)
from application.ports.core_financial_ports import QuantitativeDataPort
from pydantic import BaseModel
from loguru import logger

from application.dtos import (
    EarningsReportResult,
    QuantitativeValuationResult,
    QualitativeValuationResult,
    SectorIndustrialValuationResult,
    SectorPerformanceResult,
    TickerSearchResult,
    LocalFilingListResult,
    LiveQuoteResult,
    EarningsCallTranscriptResult
)

def handle_domain_error(e: Exception):
    """
    Maps domain exceptions to appropriate HTTP responses.
    """
    if isinstance(e, TickerNotFoundError):
        logger.warning(f"[Router-Error] Ticker not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    elif isinstance(e, RateLimitExceededError):
        logger.warning(f"[Router-Error] Rate Limit Exceeded: {e}")
        raise HTTPException(status_code=429, detail="rate_limit_exceeded")
    elif isinstance(e, (InvalidDocumentFormatError, DomainValidationError)):
        logger.warning(f"[Router-Error] Bad Request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    elif isinstance(e, (ExternalServiceError, DataFetchError, LLMParsingError)):
        logger.error(f"[Router-Error] Bad Gateway: {e}")
        raise HTTPException(status_code=502, detail=str(e))
    elif isinstance(e, ConfigurationError):
        logger.error(f"[Router-Error] Configuration Error: {e}")
        raise HTTPException(status_code=500, detail="Internal configuration error")
    
    logger.exception(f"[Router-Error] Unhandled Internal Error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")

router = APIRouter(
    prefix="/api/v1/valuation",
    tags=["Valuation"]
)

@router.get("/validate/{ticker}")
async def validate_ticker(
    ticker: str,
    adapter: QuantitativeDataPort = Depends(get_quantitative_adapter)
):
    """
    Validates if a ticker exists by quickly fetching its current price.
    Returns 200 OK with {"valid": true} if it exists, otherwise 404.
    """
    try:
        await adapter.get_stock_current_price(ticker.upper())
        return {"valid": True}
    except Exception as e:
        handle_domain_error(e)

@router.get("/search", response_model=TickerSearchResult)
async def search_ticker(
    q: str = Query(..., description="Search query for ticker or company name"),
    use_case: SearchTickersUseCase = Depends(get_search_tickers_use_case)
):
    """
    Searches for a ticker or company name.
    """
    if not q or len(q) < 1:
        return TickerSearchResult(results=[])
        
    try:
        return await use_case.execute(q)
    except Exception:
        # Silently fail for autocomplete
        return TickerSearchResult(results=[])

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
        raise InvalidDocumentFormatError("Only PDF files are supported.")
    try:
        # Create a temporary file to save the uploaded PDF
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, 'wb') as f:
            shutil.copyfileobj(file.file, f)
            
        result = await use_case.analyse_earnings_report(ticker.upper(), temp_path, language=lang)
        return result
    except Exception as e:
        handle_domain_error(e)
    finally:
        # Clean up the temporary file
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Error removing temporary file: {e}")



class LocalFilingRequest(BaseModel):
    file_path: str
    focus_period: Optional[str] = None

@router.get("/filings/{ticker}", response_model=LocalFilingListResult)
async def get_local_filings(
    ticker: str,
    use_case: GetAvailableFilingsUseCase = Depends(get_available_filings_use_case)
):
    """
    Returns a list of available historical financial quarters/years for the ticker,
    formatted as filings so the frontend can display them.
    """
    try:
        return await use_case.execute(ticker.upper())
    except Exception as e:
        handle_domain_error(e)

@router.post("/filings/{ticker}/analyse_local", response_model=EarningsReportResult)
async def analyse_local_filing(
    ticker: str,
    request: LocalFilingRequest,
    lang: str = Query("en", description="Language to generate the report in"),
    use_case: EarningsReportUseCase = Depends(get_earnings_report_use_case)
):
    """
    Analyses a locally cached SEC filing (txt or html) using the Gemini-powered model.
    """
    try:
        if not os.path.exists(request.file_path):
            raise InvalidDocumentFormatError(f"File not found: {request.file_path}")
            
        result = await use_case.analyse_earnings_report(ticker.upper(), request.file_path, language=lang, focus_period=request.focus_period)
        return result
    except Exception as e:
        handle_domain_error(e)

@router.get("/live-quote/{ticker}", response_model=LiveQuoteResult)
async def get_live_quote(
    ticker: str,
    adapter: QuantitativeDataPort = Depends(get_quantitative_adapter)
):
    """
    Fetches the live quote (price and change) for a ticker.
    Used for high-frequency polling when supported by the provider.
    """
    try:
        quote = await adapter.get_stock_current_price(ticker.upper())
        return LiveQuoteResult(
            amount=quote.amount,
            currency=quote.currency,
            change=quote.change,
            change_percent=quote.change_percent,
            is_live_supported=quote.is_live_supported
        )
    except Exception as e:
        handle_domain_error(e)

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
    logger.info(f"[Router] GET /quantitative/{ticker} initiated (years={years}).")
    try:
        result = await use_case.evaluate_ticker(ticker.upper(), years)
        return result
    except Exception as e:
        handle_domain_error(e)

@router.get("/qualitative/{ticker}", response_model=QualitativeValuationResult)
async def analyse_qualitative(
    ticker: str,
    lang: str = Query("en", description="Language to generate the report in"),
    period: str = Query(None, description="Specific period to analyze (e.g. Q3, Q4)"),
    use_case: QualitativeValuationUseCase = Depends(get_qualitative_use_case)
):
    """
    Generates a qualitative profile of the company, extracting the CEO, moat, competitors, etc.
    Returns a structured DTO representing the company profile.
    """
    logger.info(f"[Router] GET /qualitative/{ticker} initiated (lang={lang}).")
    try:
        result = await use_case.analyse_ticker(ticker.upper(), language=lang, period=period)
        return result
    except Exception as e:
        handle_domain_error(e)

@router.get("/dcf/{ticker}")
async def analyse_dcf(
    ticker: str,
    lang: str = Query("en", description="Language to generate the report in"),
    use_case: AnalyseDCFValuationUseCase = Depends(get_dcf_use_case)
):
    """
    Orchestrates the DCF Valuation process for a given ticker, returning intrinsic values and LLM assumptions.
    """
    try:
        # Pydantic will auto-serialize the domain entity DCFValuation
        result = await use_case.execute(ticker.upper(), language=lang)
        return result
    except Exception as e:
        handle_domain_error(e)

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
    except Exception as e:
        handle_domain_error(e)

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
    except Exception as e:
        handle_domain_error(e)

@router.get(
    "/{ticker}/transcripts",
    response_model=EarningsCallTranscriptResult,
    summary="Get Earnings Call Transcript",
    description="Fetches the earnings call transcript for a given stock ticker, year, and quarter.",
)
async def get_earnings_call_transcript(
    ticker: str,
    year: int = Query(..., description="The financial year (e.g., 2024)"),
    quarter: int = Query(..., description="The financial quarter (1, 2, 3, or 4)"),
    use_case: GetEarningsCallTranscriptUseCase = Depends(get_transcript_use_case)
):
    try:
        result = await use_case.execute(ticker=ticker.upper(), year=year, quarter=quarter)
        return result
    except Exception as e:
        handle_domain_error(e)
