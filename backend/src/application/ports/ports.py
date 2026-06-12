from abc import ABC, abstractmethod
from typing import List, Dict, Any
from domain.entities.entities import Price, FinancialYear, FinancialQuarter, Ticker, CompanyProfile, IndustrySectorDynamics, EarningsReport

class QuantitativeDataPort(ABC):
    """
    Interface for fetching quantitative data, including current price and fundamental financial data.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve both current stock price and comprehensive financial data for a given stock ticker symbol.
    """
    @abstractmethod
    async def get_stock_current_price(self, symbol: str) -> Price:
        """
        Fetches the current stock price for a given ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the price.
            
        Returns:
            Price: Domain Entity containing the current price and currency.
        """
        pass
    
    @abstractmethod
    async def get_historical_prices(self, symbol: str) -> Dict[str, Price]:
        """
        Fetches the historical stock prices for a given ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the historical prices.
            
        Returns:
            Dict[str, Price]: Dictionary containing the historical prices by key.
        """
        pass
    
    @abstractmethod
    async def get_stock_fundamental_data(self, symbol: str) -> List[FinancialYear]:
        """
        Fetches the fundamental financial data for a given stock ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the fundamental data.
            
        Returns:
            List[FinancialYear]: List containing the fundamental data for each Financial Year.
        """
        pass
    
    @abstractmethod
    async def get_ticker_info(self, symbol: str) -> Ticker:
        """
        Fetches only the basic metadata for a ticker (Name, Sector, Industry).
        
        Args:
            symbol (str): The stock ticker symbol to fetch the ticker data.
            
        Returns:
            Ticker: Domain Entity containing the ticker data
        """
        pass

    @abstractmethod
    async def get_stock_quarterly_data(self, symbol: str) -> List[FinancialQuarter]:
        """
        Fetches the fundamental financial data for a given stock ticker symbol on a quarterly basis.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the fundamental data.
            
        Returns:
            List[FinancialQuarter]: List containing the fundamental data for each Financial Quarter.
        """
        pass
    
class PerformanceDataPort(ABC):
    """
    Interface for fetching historical performance charts.
    """
    @abstractmethod
    async def get_historical_performance_chart(self, symbols: List[str], period: str = "5y") -> List[Dict]:
        """
        Fetches historical performance data for multiple symbols to compare them.
        """
        pass

class OwnershipDataPort(ABC):
    """
    Interface for fetching major institutional shareholders.
    """
    @abstractmethod
    async def get_major_shareholders(self, symbol: str) -> Dict[str, float]:
        """
        Fetches the major institutional shareholders and their ownership percentage.
        
        Args:
            symbol (str): The stock ticker symbol.
            
        Returns:
            Dict[str, float]: Dictionary mapping shareholder name to their ownership percentage (e.g. {"Vanguard": 7.8}).
        """
        pass

class SearchDataPort(ABC):
    """
    Interface for searching tickers.
    """
    @abstractmethod
    async def search_tickers(self, query: str) -> List[Dict[str, str]]:
        """
        Searches for tickers matching the query.
        
        Args:
            query (str): The search term.
            
        Returns:
            List[Dict[str, str]]: A list of dictionaries containing symbol, name, and exchange.
        """
        pass

class TrendingDataPort(ABC):
    """
    Interface for fetching trending tickers by sector or industry.
    """
    @abstractmethod
    async def get_trending_by_sector(self, sector_key: str) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def get_trending_by_industry(self, industry_key: str) -> List[Dict[str, Any]]:
        pass


    
class QualitativeDataPort(ABC):
    """
    Interface for fetching qualitative data, including business explanation, revenue models etc.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve all data needed for qualitative analysis.
    """
    @abstractmethod
    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
        """
        Fetches the qualitative data for a given stock ticker symbol.
        
        Args:
            symbol (str): The ticker symbol to be analysed
            language (str): Target language for the analysis
            context (str): Contextual financial data to ground the analysis and prevent hallucination
            
        Returns:
            CompanyProfile: Domain Entity containing the qualitative data of the business
        """
        pass

class EarningsReportPort(ABC):
    """
    Interface for fetching earnings report data, including revenue growth, management tone etc.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve all data needed for earnings report analysis.
    """
    @abstractmethod
    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en") -> EarningsReport:
        """
        Analyses the earnings report of a company for a specific fiscal period (either a year or a quarter)
        
        Args:
            symbol (str): The stock ticker symbol of the company
            pdf_file_path (str): The path to the PDF file to be analysed
            
        Returns:
            EarningsReport: Domain Entity containing the data given the PDF file
        """
        pass

class SectorIndustrialDataPort(ABC):   
    @abstractmethod
    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
        """
        Analyses the specific sector and industry dynamics.
        
        Args:
            sector (str): The sector to be analysed
            industry (str): The industry to be analysed
        
        Returns:
            IndustrySectorDynamics: Domain Entity containing the data given the sector and industry
        """
        pass

class TranslationPort(ABC):
    """
    Interface for translating raw JSON data via an LLM or Translation API.
    """
    @abstractmethod
    async def translate_json(self, data: dict, target_language: str) -> dict:
        """
        Translates the string values of a JSON dictionary to the target language, preserving keys and structure.
        """
        pass
        
    @abstractmethod
    async def translate_text(self, text: str, target_language: str) -> str:
        """
        Translates a plain string to the target language.
        """
        pass