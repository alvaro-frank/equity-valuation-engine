from application.use_cases.analyse_sector_industrial_valuation import SectorIndustrialValuationUseCase
from application.dtos.dtos import SectorValuationDTO
from dataclasses import asdict

class SectorValuationController:
    """
    Controller responsible for orchestrating the industry and sector valuation process.
    It delegates logic to the SectorIndustrialValuationUseCase and handles terminal presentation.
    """
    def __init__(self, service: SectorIndustrialValuationUseCase):
        """
        Initializes the controller with an injected SectorIndustrialValuationUseCase.
        
        Args:
            service (SectorIndustrialValuationUseCase): The service to handle industry analysis.
        """
        self.service = service

    def run(self, ticker_symbol: str):
        """
        Executes the industry analysis process for a given ticker symbol.

        Args:
            ticker_symbol (str): The stock ticker used to identify the industry.
            
        Returns:
            None: This method creates the SectorValuationDTO.
        """
        print(f"\nPerforming Industry Dynamics Analysis for {ticker_symbol}...")
        
        try:
            analysis_dto = self.service.evaluate_industry_by_ticker(ticker_symbol)
            self._display_industry_report(analysis_dto)

        except Exception as e:
            print(f"Industry analysis error: {e}")

    def _display_industry_report(self, analysis: SectorValuationDTO):
        """
        Formats and prints the structural industry analysis to the console.
        
        Args:
            analysis (SectorValuationDTO): The industry/sector valuation analysis to display.
            
        Returns:
            None: This method prints the results directly to the console.
        """
        print(f"\n{'='*75}")
        print(f"INDUSTRY STRUCTURAL ANALYSIS: {analysis.industry.upper()}")
        print(f"Sector: {analysis.sector} | Reference Ticker: {analysis.ticker.symbol}")
        print(f"{'='*75}")
        
        self._print_force_section("RIVALRY AMONG COMPETITORS", analysis.rivalry_among_competitors)
        self._print_force_section("BARGAINING POWER OF SUPPLIERS", analysis.bargaining_power_of_suppliers)
        self._print_force_section("BARGAINING POWER OF CUSTOMERS", analysis.bargaining_power_of_customers)
        self._print_force_section("THREAT OF NEW ENTRANTS", analysis.threat_of_new_entrants)
        self._print_force_section("THREAT OF OBSOLESCENCE", analysis.threat_of_obsolescence)
        
        print(f"\nMACROECONOMIC SENSITIVITY:")
        print(f"   - Economic Sensitivity: {analysis.economic_sensitivity}")
        print(f"   - Interest Rate Exposure: {analysis.interest_rate_exposure}")
        
        print(f"\n{'='*75}\n")

    def _print_force_section(self, title: str, force_dict: dict):
        """
        Helper to print dictionary-based analysis sections in a bulleted list format.
        
        Args:
            title (str): The name of the industry force or section.
            force_dict (dict): A dictionary where keys are factors and values are 
                               their corresponding qualitative descriptions.
                               
        Returns:
            None: Only helps to print the keys and values of the dict
        """
        print(f"\n{title}:")
        for factor, description in force_dict.items():
            print(f"   - {factor}: {description}")