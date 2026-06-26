from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SearchDataPort(ABC):
    """
    Interface for searching tickers.
    """
    @abstractmethod
    async def search_tickers(self, query: str) -> List[Dict[str, str]]:
        """
        Searches for tickers matching the query.
        
        Args:
            query (str): The search term.
            
        Returns:
            List[Dict[str, str]]: A list of dictionaries containing symbol, name, and exchange.
        """
        pass

class TrendingDataPort(ABC):
    """
    Interface for fetching trending tickers by sector or industry.
    """
    @abstractmethod
    async def get_trending_by_sector(self, sector_key: str) -> List[Dict[str, Any]]:
        """
        Fetches trending tickers by sector.
        
        Args:
            sector_key (str): The sector key.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing symbol, name, rating
        """
        pass
        
    @abstractmethod
    async def get_trending_by_industry(self, industry_key: str) -> List[Dict[str, Any]]:
        """
        Fetches trending tickers by industry.
        
        Args:
            industry_key (str): The industry key.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing symbol, name, rating
        """
        pass
