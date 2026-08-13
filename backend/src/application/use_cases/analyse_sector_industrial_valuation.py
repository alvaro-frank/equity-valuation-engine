import logging
from typing import Optional
from application.ports.core_financial_ports import QuantitativeDataPort
from application.ports.llm_analysis_ports import SectorIndustrialDataPort
from application.ports.filing_repository_port import FilingRepositoryPort
from domain.entities import IndustrySectorDynamics
from application.dtos import TickerResult, SectorIndustrialValuationResult
from dataclasses import asdict

class SectorIndustrialValuationUseCase:
    """
    Service responsible for orchestrating the industry and sector analysis.
    It fetches sector metadata for a ticker and uses AI to perform a structural analysis.
    """
    def __init__(self, quant_port: QuantitativeDataPort, sector_industrial_port: SectorIndustrialDataPort, filing_repository_port: Optional[FilingRepositoryPort] = None):
        """
        Initializes the service with qualitative (AI), quantitative (Financial Data) ports, and optional filing repository for RAG.
        
        Args:
            quant_port (QuantitativeDataPort): Port for ticker and sector metadata.
            sector_industrial_port (SectorIndustrialDataPort): Port for AI industry analysis.
            filing_repository_port (FilingRepositoryPort, optional): Port to fetch SEC filings for RAG context.
        """
        self.quant_port = quant_port
        self.sector_industrial_port = sector_industrial_port
        self.filing_repository_port = filing_repository_port

    async def evaluate_industry_by_ticker(self, ticker_symbol: str, language: str = "en") -> SectorIndustrialValuationResult:
        """
        Main entry point to analyse an industry based on a specific company ticker.
        
        Args:
            ticker_symbol (str): The stock ticker to identify the sector and industry.
            language (str): Target language for the analysis
            
        Returns:
            SectorIndustrialValuationResult: a DTO containing all information about the Industry and Sector.
        """
        ticker_info = await self.quant_port.get_ticker_info(ticker_symbol)
        
        context_str = ""
        if self.filing_repository_port:
            try:
                # Fetch recent filings for sector analysis
                structured_filings = await self.filing_repository_port.get_structured_filings(ticker_symbol)
                
                if structured_filings:
                    if structured_filings.is_exact_match and structured_filings.exact_sections:
                        # Convert dict to string for the context
                        sections_str = "\n\n".join([f"--- {k} ---\n{v}" for k, v in structured_filings.exact_sections.items()])
                        context_str = f"\n\n--- RECENT SEC FILINGS ---\n{sections_str}\n=====================================\n"
                    elif structured_filings.markdown_content:
                        context_str = f"\n\n--- RECENT SEC FILINGS ---\n{structured_filings.markdown_content}\n=====================================\n"
            except Exception as e:
                logging.error(f"RAG injection failed for Sector Analysis: {e}")
        
        analysis: IndustrySectorDynamics = await self.sector_industrial_port.analyse_industry(
            sector=ticker_info.sector_key or ticker_info.sector,
            industry=ticker_info.industry_key or ticker_info.industry,
            language=language,
            ticker=ticker_info.symbol,
            context=context_str
        )
        
        ticker_dto = TickerResult(
            symbol=ticker_info.symbol,
            name=ticker_info.name,
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )
        
        return SectorIndustrialValuationResult(
            ticker=ticker_dto,
            **asdict(analysis)
        )