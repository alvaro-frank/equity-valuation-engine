from abc import ABC, abstractmethod

from domain.entities import Price, Stock, Ticker, CompanyProfile, IndustrySectorDynamics

class QuantitativeDataProvider(ABC):
    """
    Interface for fetching quantitative data, including current price and fundamental financial data.
    This interface defines the contract for any data provider implementation, ensuring that they provide methods to retrieve both current stock price and comprehensive financial data for a given stock ticker symbol.
    """
    @abstractmethod
    def get_stock_current_price(self, symbol: str) -> Price:
        """
        Fetches the current stock price for a given ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the price.
            
        Returns:
            Price: Domain Entity containing the current price and currency.
        """
        pass
    
    @abstractmethod
    def get_stock_fundamental_data(self, symbol: str) -> Stock:
        """
        Fetches the fundamental financial data for a given stock ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the fundamental data.
            
        Returns:
            Stock: Domain Entity containing the stock's fundamental data, including financial years.
        """
        pass
    
    @abstractmethod
    def get_ticker_info(self, symbol: str) -> Ticker:
        """
        Fetches only the basic metadata for a ticker (Name, Sector, Industry).
        
        Args:
            symbol (str): The stock ticker symbol to fetch the ticker data.
            
        Returns:
            Ticker: Domain Entity containing the ticker data
        """
        pass
    
class QualitativeDataProvider(ABC):
    """
    Interface for fetching qualitative data, including business explanation, revenue models etc.
    This interface defines the contract for any data provider implementation, ensuring that they provide methods to retrieve all data needed for qualitative analysis.
    """
    @abstractmethod
    def analyse_company(self, symbol: str) -> CompanyProfile:
        """
        Fetches the qualitative data for a given stock ticker symbol.
        
        Args:
            symbol (str): The ticker symbol to be analysed
            
        Returns:
            CompanyProfile: Domain Entity containing the qualitative data of the business
        """
        pass
    
    @abstractmethod
    def analyse_industry(self, sector: str, industry: str) -> IndustrySectorDynamics:
        """
        Analyses the specific sector and industry dynamics.
        
        Args:
            sector (str): The sector to be analysed
            industry (str): The industry to be analysed
        
        Returns:
            IndustrySectorDynamics: Domain Entity containing the data given the sector and industry
        """
        pass