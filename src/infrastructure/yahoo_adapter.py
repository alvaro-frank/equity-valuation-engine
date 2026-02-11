import yfinance
from decimal import Decimal, InvalidOperation
from domain.interfaces import StockDataProvider
from domain.stock_market import Price, Ticker, Stock

class YahooFinanceAdapter(StockDataProvider):
    def get_stock_current_price(self, ticker: Ticker) -> Price:
        try:
            yf_ticker = yfinance.Ticker(ticker.symbol)
            
            info = yf_ticker.info
            
            raw_price = info.get('currentPrice')
            if raw_price is None:
                raise ValueError(f"Price not found for {ticker.symbol}")

            price_decimal = Decimal(str(raw_price))
            
            currency = info.get('currency', 'USD')
            
            return Price(amount=price_decimal, currency=currency)
            
        except (ValueError, InvalidOperation) as e:
            raise ValueError(f"Data error for {ticker.symbol}: {e}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance for {ticker.symbol}: {e}")
        
    def get_stock_fundamental_data(self, ticker: Ticker) -> Stock:
        try:
            yf_ticker = yfinance.Ticker(ticker.symbol)
            
            info = yf_ticker.info
            
            price = self.get_stock_current_price(ticker)
            
            raw_eps = info.get('trailingEps')
            if raw_eps is None:
                raise ValueError(f"EPS not found for {ticker.symbol}")

            eps_decimal = Decimal(str(raw_eps))
            
            return Stock(ticker=ticker, price=price, earnings_per_share=eps_decimal)
            
        except (ValueError, InvalidOperation) as e:
            raise ValueError(f"Data error for {ticker.symbol}: {e}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance for {ticker.symbol}: {e}")