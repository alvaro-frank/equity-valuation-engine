from infrastructure.gemini_adapter import GeminiAdapter
from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from services.qualitative_valuation_service import QualitativeValuationService
from services.quantitative_valuation_service import QuantitativeValuationService
from controllers.quantitative_valuation_controller import QuantitativeValuationController
from controllers.qualitative_valuation_controller import QualitativeValuationController

def main():
    ticker = "MSFT"
    
    # 1. Quantitative Analysis
    alpha_vantage_adapter = AlphaVantageAdapter()
    quant_service = QuantitativeValuationService(adapter=alpha_vantage_adapter)
    quant_controller = QuantitativeValuationController(quant_service)
    quant_controller.run(ticker, years=10)
    
    # Qualitative Analysis
    gemini_adapter = GeminiAdapter()
    qual_service = QualitativeValuationService(adapter=gemini_adapter)
    qual_controller = QualitativeValuationController(qual_service)
    qual_controller.run(ticker)

if __name__ == "__main__":
    main()