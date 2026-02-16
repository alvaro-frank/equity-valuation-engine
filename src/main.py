import sys
from controllers.valuation_controller import ValuationController

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "MSFT"
    
    controller = ValuationController()
    controller.run(ticker, years=10)