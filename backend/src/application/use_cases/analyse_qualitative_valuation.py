from domain.entities.entities import CompanyProfile
from application.ports.ports import QualitativeDataPort, QuantitativeDataPort, OwnershipDataPort
from application.dtos.dtos import TickerResult, QualitativeValuationResult
from dataclasses import asdict
import dataclasses
import datetime
import logging

class QualitativeValuationUseCase:
    """
    Service responsible for performing stock qualitative valuation analysis based on the provided stock data.
    This service takes in an entity Ticker, analyses the quality, moat and background of a business, and returns a DTO containing all information about the Qualitative data of the business.
    """
    def __init__(self, adapter: QualitativeDataPort, quant_adapter: QuantitativeDataPort, ownership_adapter: OwnershipDataPort, translator=None):
        """
        Initializes the QualitativeValuationUseCase with the GeminiAdapter for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter
        self.ownership_adapter = ownership_adapter
        self.translator = translator
        
    async def analyse_ticker(self, ticker_symbol: str, language: str = "en") -> QualitativeValuationResult:
        """
        Fetches the ticker information, such as business name, sector and industry
        
        Args:
            ticker_symbol (str): The stock ticker symbol to analyse.
            
        Returns:
            QualitativeValuationResult: a DTO containing all information about the Qualitative data of the business.
        """
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
        
        officers = getattr(ticker_info, 'company_officers', [])
        if officers:
            officers_str = ", ".join([f"{o.get('name')} ({o.get('title')})" for o in officers[:10]])
            context_parts.append(f"Current Key Executives/Officers: {officers_str}")
            
        context_str = "\n".join(context_parts)
        
        qual_data: CompanyProfile = await self.adapter.analyse_company(
            symbol=ticker_info.symbol,
            language=language,
            context=context_str
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
            
        major_shareholders = await self.ownership_adapter.get_major_shareholders(ticker_info.symbol)

        return QualitativeValuationResult(
            ticker=ticker_dto,
            major_shareholders=major_shareholders,
            **qual_data_dict
        )