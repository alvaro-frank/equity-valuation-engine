from abc import ABC, abstractmethod
from domain.entities import CompanyProfile, IndustrySectorDynamics, EarningsReport

class QualitativeDataPort(ABC):
    """
    Interface for fetching qualitative data, including business explanation, revenue models etc.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve all data needed for qualitative analysis.
    """
    @abstractmethod
    async def analyse_company(self, symbol: str, language: str = "en", context: str = "") -> CompanyProfile:
        """
        Fetches the qualitative data for a given stock ticker symbol.
        
        Args:
            symbol (str): The ticker symbol to be analysed
            language (str): Target language for the analysis
            context (str): Contextual financial data to ground the analysis and prevent hallucination
            
        Returns:
            CompanyProfile: Domain Entity containing the qualitative data of the business
        """
        pass

class EarningsReportPort(ABC):
    """
    Interface for fetching earnings report data, including revenue growth, management tone etc.
    This interface defines the contract for any data port implementation, ensuring that they provide methods to retrieve all data needed for earnings report analysis.
    """
    @abstractmethod
    async def analyse_earnings_report(self, symbol: str, pdf_file_path: str, language: str = "en", focus_period: str = None) -> EarningsReport:
        """
        Analyses the earnings report of a company for a specific fiscal period (either a year or a quarter)
        
        Args:
            symbol (str): The stock ticker symbol of the company
            pdf_file_path (str): The path to the PDF file to be analysed
            language (str): Target language for the analysis
            
        Returns:
            EarningsReport: Domain Entity containing the data given the PDF file
        """
        pass

class SectorIndustrialDataPort(ABC):   
    @abstractmethod
    async def analyse_industry(self, sector: str, industry: str, language: str = "en") -> IndustrySectorDynamics:
        """
        Analyses the specific sector and industry dynamics.
        
        Args:
            sector (str): The sector to be analysed
            industry (str): The industry to be analysed
            language (str): Target language for the analysis
        
        Returns:
            IndustrySectorDynamics: Domain Entity containing the data given the sector and industry
        """
        pass
