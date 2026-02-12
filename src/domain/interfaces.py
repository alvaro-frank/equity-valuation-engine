from abc import ABC, abstractmethod

from domain.stock_market import Ticker, Stock, Price

class StockDataProvider(ABC):
    @abstractmethod
    def get_stock_current_price(self, ticker: Ticker) -> Price:
        pass
    
    @abstractmethod
    def get_stock_fundamental_data(self, ticker: Ticker) -> Stock:
        pass