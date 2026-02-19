from infrastructure.gemini_adapter import GeminiAdapter
from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from services.qualitative_valuation_service import QualitativeValuationService
from services.quantitative_valuation_service import QuantitativeValuationService
from services.sector_valuation_service import SectorValuationService
from controllers.quantitative_valuation_controller import QuantitativeValuationController
from controllers.qualitative_valuation_controller import QualitativeValuationController
from controllers.sector_valuation_controller import SectorValuationController

def main():
    ticker = "NVDA"
    years_of_history = 10
    
    # Adapters
    alpha_vantage_adapter = AlphaVantageAdapter()
    gemini_adapter = GeminiAdapter()
    
    #Services
    sector_service = SectorValuationService(qual_provider=gemini_adapter, quant_provider=alpha_vantage_adapter)
    qual_service = QualitativeValuationService(adapter=gemini_adapter, quant_adapter=alpha_vantage_adapter)
    quant_service = QuantitativeValuationService(adapter=alpha_vantage_adapter)
    
    # Controllers
    sector_controller = SectorValuationController(sector_service)
    qual_controller = QualitativeValuationController(qual_service)
    quant_controller = QuantitativeValuationController(quant_service)
    
    print(f"{'='*80}")
    print(f"FULL INVESTMENT DOSSIER: {ticker}")
    print(f"{'='*80}")
    
    # Sector/Industry Analysis
    sector_controller.run(ticker)
    # Qualitative Analysis
    qual_controller.run(ticker)
    # Quantitative Analysis
    quant_controller.run(ticker, years=years_of_history)
    
    print(f"{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()