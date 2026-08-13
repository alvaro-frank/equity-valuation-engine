from abc import ABC, abstractmethod
from typing import List
from application.dtos import LocalFilingDTO, StructuredFilingDTO

class FilingRepositoryPort(ABC):
    """
    Interface for managing SEC filings.
    Abstracts away whether they are fetched from the web or from local cache.
    """


    @abstractmethod
    async def get_structured_filings(self, ticker: str) -> 'StructuredFilingDTO':
        """
        Retrieves SEC filings (10-K and 10-Q) for the Qualitative RAG Analysis.
        Returns a StructuredFilingDTO which contains either exact programmatic sections
        extracted via edgartools (Fast Path), or markdown content via sec-parser (Fallback Path).
        
        Args:
            ticker: The company ticker symbol.
            
        Returns:
            A StructuredFilingDTO instance.
        """
        pass
