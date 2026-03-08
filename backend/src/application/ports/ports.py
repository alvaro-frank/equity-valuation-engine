from abc import ABC, abstractmethod
from typing import List
from domain.entities.entities import Price, FinancialYear, Ticker, CompanyProfile, IndustrySectorDynamics

class QuantitativeDataPort(ABC):
    """
    Interface for fetching quantitative data, including current price and fundamental financial data.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve both current stock price and comprehensive financial data for a given stock ticker symbol.
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
    def get_stock_fundamental_data(self, symbol: str) -> List[FinancialYear]:
        """
        Fetches the fundamental financial data for a given stock ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the fundamental data.
            
        Returns:
            List[FinancialYear]: List containing the fundamental data for each Financial Year.
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
    
class QualitativeDataPort(ABC):
    """
    Interface for fetching qualitative data, including business explanation, revenue models etc.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve all data needed for qualitative analysis.
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

class SectorIndustrialDataPort(ABC):   
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