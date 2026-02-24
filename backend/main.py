from infrastructure.gemini_adapter import GeminiAdapter
from infrastructure.alpha_vantage_adapter import AlphaVantageAdapter
from use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from controllers.quantitative_valuation_controller import QuantitativeValuationController
from controllers.qualitative_valuation_controller import QualitativeValuationController
from controllers.sector_valuation_controller import SectorValuationController

def main():
    ticker = "MSFT"
    years_of_history = 10
    
    # Adapters
    alpha_vantage_adapter = AlphaVantageAdapter()
    gemini_adapter = GeminiAdapter()
    
    #Use Cases
    sector_service = SectorIndustrialValuationUseCase(qual_provider=gemini_adapter, quant_provider=alpha_vantage_adapter)
    qual_service = QualitativeValuationUseCase(adapter=gemini_adapter, quant_adapter=alpha_vantage_adapter)
    quant_service = QuantitativeValuationUseCase(adapter=alpha_vantage_adapter)
    
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