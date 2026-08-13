from abc import ABC, abstractmethod
from typing import List, Dict, Any
from domain.entities import Price, LiveQuote, FinancialYear, FinancialQuarter, Ticker

class QuantitativeDataPort(ABC):
    """
    Interface for fetching quantitative data, including current price and fundamental financial data.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve both current stock price and comprehensive financial data for a given stock ticker symbol.
    """
    @abstractmethod
    async def get_stock_current_price(self, symbol: str) -> LiveQuote:
        """
        Fetches the current stock price and live quote for a given ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the price.
            
        Returns:
            LiveQuote: Domain Entity containing the current price, change, and live support flag.
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
        
        Args:
            symbols (List[str]): List of stock ticker symbols.
            period (str): The time period for the performance data.
            
        Returns:
            List[Dict]: List of dictionaries containing the performance data.
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
