from domain.entities import CompanyProfile
from application.ports.llm_analysis_ports import QualitativeDataPort
from application.ports.core_financial_ports import QuantitativeDataPort, OwnershipDataPort
from application.dtos import TickerResult, QualitativeValuationResult
from dataclasses import asdict
import dataclasses
import datetime
import logging
from loguru import logger

class QualitativeValuationUseCase:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in an entity Ticker, analyses the quality, moat and background of a business, and returns a DTO containing all information about the Qualitative data of the business.
    """
    def __init__(self, adapter: QualitativeDataPort, quant_adapter: QuantitativeDataPort, ownership_adapter: OwnershipDataPort, translator=None, filing_repository_port=None):
        """
        Initializes the QualitativeValuationUseCase with the GeminiAdapter for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter
        self.ownership_adapter = ownership_adapter
        self.translator = translator
        self.filing_repository_port = filing_repository_port
        
    async def analyse_ticker(self, ticker_symbol: str, language: str = "en", period: str = None) -> QualitativeValuationResult:
        """
        Fetches the ticker information, such as business name, sector and industry
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            language (str): Target language for the analysis
            
        Returns:
            QualitativeValuationResult: a DTO containing all information about the Qualitative data of the business.
        """
        logger.info(f"[QualitativeValuationUseCase] Qualitative Analysis requested for {ticker_symbol} (Lang: {language})")
        ticker_info = await self.quant_adapter.get_ticker_info(ticker_symbol)
        
        context_parts = []
        
        context_parts.append(f"Current Date: {datetime.date.today()}")
        
        if getattr(ticker_info, 'business_description', None):
            context_parts.append(f"Business Description: {ticker_info.business_description}")
            
        if getattr(ticker_info, 'market_cap', None):
            mc = float(ticker_info.market_cap)
            if mc >= 1e12:
                mc_str = f"${mc/1e12:.2f} Trillion"
            elif mc >= 1e9:
                mc_str = f"${mc/1e9:.2f} Billion"
            else:
                mc_str = f"${mc:,.0f}"
            context_parts.append(f"Current Market Cap: {mc_str}")
            
        if getattr(ticker_info, 'current_price', None):
            context_parts.append(f"Current Stock Price: ${float(ticker_info.current_price):.2f}")
            
        if getattr(ticker_info, 'profit_margins', None) is not None:
            context_parts.append(f"Profit Margins: {float(ticker_info.profit_margins)*100:.2f}%")
        if getattr(ticker_info, 'revenue_growth', None) is not None:
            context_parts.append(f"Revenue Growth: {float(ticker_info.revenue_growth)*100:.2f}%")
            
        if getattr(ticker_info, 'pe_ratio', None) is not None:
            context_parts.append(f"Current P/E Ratio: {float(ticker_info.pe_ratio):.2f}")
            
        if getattr(ticker_info, 'forward_pe', None) is not None:
            context_parts.append(f"Forward P/E Ratio: {float(ticker_info.forward_pe):.2f}")
            
        if getattr(ticker_info, 'regular_market_change_percent', None) is not None:
            context_parts.append(f"Today's Market Change: {float(ticker_info.regular_market_change_percent):.2f}%")
        
        officers = getattr(ticker_info, 'company_officers', [])
        if officers:
            officers_str = ", ".join([f"{o.get('name')} ({o.get('title')})" for o in officers[:10]])
            context_parts.append(f"Current Key Executives/Officers: {officers_str}")
            
        # Inject Major Shareholders
        major_shareholders = await self.ownership_adapter.get_major_shareholders(ticker_info.symbol)
        if major_shareholders:
            sh_str = ", ".join([f"{k} ({v:.2f}%)" for k, v in list(major_shareholders.items())[:5]])
            context_parts.append(f"Top Institutional Shareholders: {sh_str}")
            
        # Fetch Deep Fundamentals for ROIC, FCF, Debt
        financials = await self.quant_adapter.get_stock_fundamental_data(ticker_symbol)
        if financials:
            latest_year = financials[0]
            if getattr(latest_year, 'roic', None) is not None:
                context_parts.append(f"Latest Year ROIC: {float(latest_year.roic):.2f}%")
            if getattr(latest_year, 'roe', None) is not None:
                context_parts.append(f"Latest Year ROE: {float(latest_year.roe):.2f}%")
            
            # Format large numbers
            def fmt_currency(val):
                v = float(val)
                if abs(v) >= 1e12: return f"${v/1e12:.2f}T"
                elif abs(v) >= 1e9: return f"${v/1e9:.2f}B"
                elif abs(v) >= 1e6: return f"${v/1e6:.2f}M"
                return f"${v:,.0f}"
                
            if getattr(latest_year, 'free_cash_flow', None) is not None:
                context_parts.append(f"Latest Year Free Cash Flow: {fmt_currency(latest_year.free_cash_flow)}")
            if getattr(latest_year, 'capital_expenditures', None) is not None:
                context_parts.append(f"Latest Year CapEx: {fmt_currency(latest_year.capital_expenditures)}")
            if getattr(latest_year, 'total_debt', None) is not None:
                context_parts.append(f"Latest Year Total Debt: {fmt_currency(latest_year.total_debt)}")
            if getattr(latest_year, 'cash_and_equivalents', None) is not None:
                context_parts.append(f"Latest Year Cash on Hand: {fmt_currency(latest_year.cash_and_equivalents)}")
            
        context_str = "\n".join(context_parts)
        
        logger.info(f"[QualitativeValuationUseCase] Real-world Context built successfully for {ticker_symbol}.")
        
        # --- RAG INTEGRATION (SEC EDGAR FILINGS) ---
        structured_filings = None
        if self.filing_repository_port:
            try:
                structured_filings = await self.filing_repository_port.get_structured_filings(ticker_symbol)
                logger.info(f"[QualitativeValuationUseCase] SEC RAG structured context extracted for {ticker_symbol}. Exact Match: {structured_filings.is_exact_match}")
            except Exception as e:
                logger.error(f"[UseCase-Error] RAG injection failed for {ticker_symbol}: {e}")
        
        logger.info(f"[QualitativeValuationUseCase] Dispatching request to LLM Orchestrator...")
        qual_data: CompanyProfile = await self.adapter.analyse_company(
            symbol=ticker_info.symbol,
            language=language,
            context=context_str,
            structured_filings=structured_filings
        )
        
        ticker_dto = TickerResult(
            symbol=ticker_info.symbol,
            name=ticker_info.name,
            sector=ticker_info.sector,
            sector_key=ticker_info.sector_key,
            industry=ticker_info.industry,
            industry_key=ticker_info.industry_key
        )

        # Inject the business description directly from yfinance
        if getattr(ticker_info, 'business_description', None):
            desc = ticker_info.business_description
            if language != "en" and getattr(self, 'translator', None):
                try:
                    desc = await self.translator.translate_text(desc, language)
                except Exception as e:
                    logging.warning(f"Failed to translate business description: {e}")
            qual_data = dataclasses.replace(qual_data, business_description=desc)
            
        qual_data_dict = asdict(qual_data)
        if "major_shareholders" in qual_data_dict:
            del qual_data_dict["major_shareholders"]
            
        result_dto = QualitativeValuationResult(
            ticker=ticker_dto,
            major_shareholders=major_shareholders,
            **qual_data_dict
        )
            
        return result_dto