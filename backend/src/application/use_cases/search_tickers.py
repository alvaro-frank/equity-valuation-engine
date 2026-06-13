from application.ports.ports import SearchDataPort
from application.dtos.dtos import TickerSearchResult, TickerSearchDTO

class SearchTickersUseCase:
    """
    Service responsible for searching tickers matching a specific query.
    """
    def __init__(self, search_port: SearchDataPort):
        self.search_port = search_port

    async def execute(self, query: str) -> TickerSearchResult:
        """
        Searches for tickers matching the query.
        
        Args:
            query (str): The search term.
            
        Returns:
            TickerSearchResult: DTO containing the search results.
        """
        results = await self.search_port.search_tickers(query)
        
        dto_results = [
            TickerSearchDTO(
                symbol=r["symbol"],
                name=r["name"],
                exchange=r.get("exchange", "")
            )
            for r in results
        ]
        
        return TickerSearchResult(results=dto_results)
