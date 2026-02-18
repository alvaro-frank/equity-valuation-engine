from abc import ABC, abstractmethod

from services.dtos import PriceDTO, QuantitativeDataDTO

class StockDataProvider(ABC):
    """
    Interface for fetching stock data, including current price and fundamental financial data.
    This interface defines the contract for any data provider implementation, ensuring that they provide methods to retrieve both current stock price and comprehensive financial data for a given stock ticker symbol.
    """
    @abstractmethod
    def get_stock_current_price(self, symbol: str) -> PriceDTO:
        """
        Fetches the current stock price for a given ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the price for.
            
        Returns:
            PriceDTO: A data transfer object containing the current price and currency.
        """
        pass
    
    @abstractmethod
    def get_stock_fundamental_data(self, symbol: str) -> QuantitativeDataDTO:
        """
        Fetches the fundamental financial data for a given stock ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the fundamental data for.
            
        Returns:
            QuantitativeDataDTO: A data transfer object containing the stock's fundamental data, including financial years.
        """
        pass