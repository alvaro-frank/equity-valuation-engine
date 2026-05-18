import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.adapters.output.gemini_adapter import GeminiAdapter
from infrastructure.adapters.output.alpha_vantage_adapter import AlphaVantageAdapter
from application.use_cases.analyse_qualitative_valuation import QualitativeValuationUseCase
from application.use_cases.analyse_quantitative_valuation import QuantitativeValuationUseCase
from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from infrastructure.adapters.input.quantitative_valuation_adapter import QuantitativeValuationAdapter
from infrastructure.adapters.input.qualitative_valuation_adapter import QualitativeValuationAdapter
from infrastructure.adapters.input.sector_valuation_adapter import SectorValuationAdapter

def main():
    ticker = "MSFT"
    years_of_history = 10
    
    # Adapters
    alpha_vantage_adapter = AlphaVantageAdapter()
    gemini_adapter = GeminiAdapter()
    
    #Use Cases
    sector_service = SectorIndustrialValuationUseCase(quant_port=alpha_vantage_adapter, sector_industrial_port=gemini_adapter)
    qual_service = QualitativeValuationUseCase(adapter=gemini_adapter, quant_adapter=alpha_vantage_adapter)
    quant_service = QuantitativeValuationUseCase(adapter=alpha_vantage_adapter)
    
    # Controllers
    sector_controller = SectorValuationAdapter(sector_service)
    qual_controller = QualitativeValuationAdapter(qual_service)
    quant_controller = QuantitativeValuationAdapter(quant_service)
    
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