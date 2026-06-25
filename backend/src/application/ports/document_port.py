from abc import ABC, abstractmethod
from typing import List

class DocumentPort(ABC):
    """
    Interface for extracting unstructured documents (like SEC filings)
    """

    @abstractmethod
    async def get_latest_sec_filings(self, ticker: str, form_type: str, limit: int = 1) -> List[str]:
        """
        Fetches the latest SEC filings of a given form type for a ticker.
        
        Args:
            ticker: The company ticker symbol (e.g., MSFT)
            form_type: The SEC form type (e.g., '10-K', '10-Q')
            limit: Maximum number of filings to retrieve
            
        Returns:
            A list of strings, where each string is the path to the downloaded/extracted filing file.
        """
        pass

    @abstractmethod
    async def list_local_sec_filings(self, ticker: str) -> List[dict]:
        """
        Lists available SEC filings in the local cache.
        Returns a list of dictionaries with id, form_type, period, and accession_number.
        """
        pass
