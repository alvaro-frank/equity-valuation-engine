from fastapi import APIRouter, Depends, Query, HTTPException
import os

from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase

from infrastructure.adapters.input.dependencies import (
    get_earnings_report_use_case,
    get_quantitative_use_case,
    get_qualitative_use_case,
    get_sector_use_case
)

from application.dtos.dtos import (
    EarningsReportResult,
    QuantitativeValuationResult,
    QualitativeValuationResult,
    SectorIndustrialValuationResult
)

router = APIRouter(
    prefix="/api/v1/valuation",
    tags=["Valuation"]
)

@router.get("/earnings/{ticker}", response_model=EarningsReportResult)
def analyse_earnings_report(
    ticker: str,
    pdf_path: str = Query(..., description="Path to the Earnings Report PDF file"),
    use_case: EarningsReportUseCase = Depends(get_earnings_report_use_case)
):
    """
    Analyses an Earnings Report (PDF) using the Gemini-powered Value Investing prompt.
    Returns a structured DTO with Core Performance, Capital Allocation, and Risk Deconstruction.
    """
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail=f"PDF file not found at: {pdf_path}")
        
    try:
        result = use_case.analyse_earnings_report(ticker.upper(), pdf_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quantitative/{ticker}", response_model=QuantitativeValuationResult)
def analyse_quantitative(
    ticker: str,
    years: int = Query(10, description="Number of years of historical data to retrieve"),
    use_case: QuantitativeValuationUseCase = Depends(get_quantitative_use_case)
):
    """
    Analyses the historical financial data of a given company.
    Returns a structured DTO with quantitative metrics and CAGRs.
    """
    try:
        result = use_case.evaluate_ticker(ticker.upper(), years)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/qualitative/{ticker}", response_model=QualitativeValuationResult)
def analyse_qualitative(
    ticker: str,
    use_case: QualitativeValuationUseCase = Depends(get_qualitative_use_case)
):
    """
    Generates a qualitative profile of the company, extracting the CEO, moat, competitors, etc.
    Returns a structured DTO representing the company profile.
    """
    try:
        result = use_case.analyse_ticker(ticker.upper())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sector/{ticker}", response_model=SectorIndustrialValuationResult)
def analyse_sector(
    ticker: str,
    use_case: SectorIndustrialValuationUseCase = Depends(get_sector_use_case)
):
    """
    Analyses the sector and industry dynamics (Porter's Five Forces, etc.) for a given ticker.
    Returns a structured DTO with the industry structural analysis.
    """
    try:
        result = use_case.evaluate_industry_by_ticker(ticker.upper())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
