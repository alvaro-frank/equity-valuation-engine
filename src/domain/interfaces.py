from abc import ABC, abstractmethod

from services.dtos import PriceDTO, StockDataDTO

class StockDataProvider(ABC):
    @abstractmethod
    def get_stock_current_price(self, symbol: str) -> PriceDTO:
        pass
    
    @abstractmethod
    def get_stock_fundamental_data(self, symbol: str) -> StockDataDTO:
        pass