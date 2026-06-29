from application.dtos.core import LocalFilingListResult
from application.ports.filing_repository_port import FilingRepositoryPort

class ListCompanyFilingsUseCase:
    """
    Service responsible for listing locally cached SEC filings for a given ticker.
    The FilingRepositoryPort handles fetching and caching transparently.
    """
    def __init__(self, filing_repository_port: FilingRepositoryPort):
        self.filing_repository_port = filing_repository_port

    async def execute(self, ticker: str) -> LocalFilingListResult:
        """
        Retrieves the list of available 10-K and 10-Q filings.
        """
        filings = await self.filing_repository_port.get_available_filings(ticker)
        return LocalFilingListResult(filings=filings)
