from controllers.quantitative_valuation_controller import QuantitativeValuationController
from controllers.qualitative_valuation_controller import QualitativeValuationController

def main():
    ticker = "MSFT"
    
    # 1. Quantitative Analysis
    quant_controller = QuantitativeValuationController()
    quant_controller.run(ticker, years=10)
    
    # Qualitative Analysis
    qual_controller = QualitativeValuationController()
    qual_controller.run(ticker)

if __name__ == "__main__":
    main()