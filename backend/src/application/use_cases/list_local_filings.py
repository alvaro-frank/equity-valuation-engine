import os
import time
from application.dtos.core import LocalFilingListResult, LocalFilingDTO
from application.ports.document_port import DocumentPort

CACHE_LIFETIME_SECONDS = 24 * 60 * 60  # 24 hours

class ListLocalFilingsUseCase:
    """
    Service responsible for listing locally cached SEC filings for a given ticker.
    If the cache is empty or expired, it automatically fetches the latest filings from the SEC.
    """
    def __init__(self, document_port: DocumentPort):
        self.document_port = document_port

    async def execute(self, ticker: str) -> LocalFilingListResult:
        """
        Retrieves the list of available 10-K and 10-Q filings from the local cache.
        If empty or older than 24 hours, fetches new filings.
        """
        filings_data = await self.document_port.list_local_sec_filings(ticker)
        
        needs_fetch = False
        if not filings_data:
            needs_fetch = True
        else:
            try:
                most_recent_file = max([f["id"] for f in filings_data], key=os.path.getmtime)
                file_age = time.time() - os.path.getmtime(most_recent_file)
                if file_age > CACHE_LIFETIME_SECONDS:
                    needs_fetch = True
            except Exception:
                needs_fetch = True
                
        if needs_fetch:
            try:
                # Fetch the latest 10-K and 10-Q filings
                await self.document_port.get_latest_sec_filings(ticker, "10-K", limit=2)
                await self.document_port.get_latest_sec_filings(ticker, "10-Q", limit=4)
                
                # Re-list after fetching
                filings_data = await self.document_port.list_local_sec_filings(ticker)
            except Exception as e:
                # Silently handle failures (e.g. rate limits or non-US tickers)
                print(f"Error fetching SEC filings for {ticker}: {e}")
        
        dtos = [
            LocalFilingDTO(
                id=f["id"],
                form_type=f["form_type"],
                period=f["period"],
                accession_number=f["accession_number"]
            )
            for f in filings_data
        ]
        
        return LocalFilingListResult(filings=dtos)
