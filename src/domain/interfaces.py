from abc import ABC, abstractmethod

from services.dtos import PriceDTO, StockDataDTO

class StockDataProvider(ABC):
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
    def get_stock_fundamental_data(self, symbol: str) -> StockDataDTO:
        """
        Fetches the fundamental financial data for a given stock ticker symbol.
        
        Args:
            symbol (str): The stock ticker symbol to fetch the fundamental data for.
            
        Returns:
            StockDataDTO: A data transfer object containing the stock's fundamental data, including financial years.
        """
        pass