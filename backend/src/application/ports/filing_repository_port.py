from abc import ABC, abstractmethod
from typing import List
from application.dtos import LocalFilingDTO

class FilingRepositoryPort(ABC):
    """
    Interface for managing SEC filings.
    Abstracts away whether they are fetched from the web or from local cache.
    """

    @abstractmethod
    async def get_available_filings(self, ticker: str) -> List[LocalFilingDTO]:
        """
        Retrieves the list of available SEC filings for a given ticker.
        If the cache is empty or outdated, this will automatically trigger an internal extraction.
        
        Args:
            ticker: The company ticker symbol.
            
        Returns:
            A list of LocalFilingDTO representing the available filings.
        """
        pass

    @abstractmethod
    async def get_filing_paths_for_rag(self, ticker: str, period: str = None) -> List[str]:
        """
        Retrieves the absolute file paths of the SEC filings needed for the Qualitative RAG Analysis.
        
        Args:
            ticker: The company ticker symbol.
            period: An optional specific period to focus on (e.g. 'Q3'). If None, the latest are used.
            
        Returns:
            A list of absolute file paths to the required .txt SEC filings.
        """
        pass
