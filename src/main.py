from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from services.stock_service import StockService

def main():
    print("--- EQUITY VALUATION ENGINE ---")
    
    try:
        adapter = AlphaVantageAdapter()
        service = StockService(data_provider=adapter)
        
        symbol_input = input("Ticker (ex: MSFT, AAPL): ").strip()
        
        print(f"Analysing {symbol_input}...")
        result = service.analyse_stock(symbol_input)
        
        print(f"\nREPORT: {result.symbol}")
        print(f"Price: {result.price} {result.currency}")
        print(f"EPS:   {result.eps}")
        if result.pe_ratio:
            print(f"P/E:   {result.pe_ratio:.2f}")
        else:
            print("P/E:   N/A")

    except ConnectionError as e:
        print(f"\n[LIMIT]: {e}")
    except Exception as e:
        print(f"\n[ERROR]: {e}")

if __name__ == "__main__":
    main()