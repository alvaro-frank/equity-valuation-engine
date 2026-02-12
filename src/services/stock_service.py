from domain.interfaces import StockDataProvider
from domain.stock_market import Ticker
from services.dtos import StockDataDTO

class StockService:
    def __init__(self, data_provider: StockDataProvider):
        self.data_provider = data_provider
        
    def analyse_stock(self, ticker_symbol: str) -> dict:
        ticker = Ticker(symbol=ticker_symbol)
        stock_data = self.data_provider.get_stock_fundamental_data(ticker)
        
        try:
            pe_ratio = f"{stock_data.pe_ratio:.2f}"
        except ValueError as e:
            pe_ratio = None
        
        return StockDataDTO(
            symbol=stock_data.ticker.symbol,
            price=stock_data.price.amount,
            currency=stock_data.price.currency,
            eps=stock_data.earnings_per_share,
            pe_ratio=pe_ratio
        )