from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from domain.stock_market import Ticker, Stock, Price

class StockDataProvider(ABC):
    @abstractmethod
    def get_stock_current_price(self, ticker: Ticker) -> Price:
        pass

    # --- A TUA VEZ DE COMPLETAR AQUI ---
    
    @abstractmethod
    def get_stock_fundamental_data(self, ticker: Ticker) -> Stock:
        pass

    @abstractmethod
    def search_tickers_by_name(self, query: str) -> List[Ticker]:
        pass