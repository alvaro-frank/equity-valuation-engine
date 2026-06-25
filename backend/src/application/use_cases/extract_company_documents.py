import logging
from typing import List, Dict
from application.ports.document_port import DocumentPort

logger = logging.getLogger(__name__)

class ExtractCompanyDocumentsUseCase:
    def __init__(self, document_port: DocumentPort):
        self.document_port = document_port

    async def execute(self, ticker: str, num_10k: int = 2, num_10q: int = 5) -> Dict[str, List[str]]:
        """
        Extracts recent 10-K and 10-Q filings for a ticker.
        """
        logger.info(f"Extracting company documents for {ticker}...")
        
        extracted_files = {
            "10-K": [],
            "10-Q": []
        }
        
        import os
        import time
        
        # Determine cache directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        cache_dir = os.path.join(base_dir, ".llm_cache", ticker.upper(), "filings")
        
        # TTL Check: Skip extraction if the most recent file in cache is younger than 24 hours
        if os.path.exists(cache_dir):
            most_recent_time = 0
            file_count = 0
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    if file.endswith(".txt"):
                        file_count += 1
                        file_path = os.path.join(root, file)
                        mtime = os.path.getmtime(file_path)
                        if mtime > most_recent_time:
                            most_recent_time = mtime
            
            # If we have files and the youngest is less than 24 hours (86400 seconds) old, skip download
            if file_count > 0 and (time.time() - most_recent_time) < 86400:
                logger.info(f"Cache for {ticker} is fresh (less than 24h old). Skipping SEC EDGAR extraction.")
                return extracted_files

        try:
            logger.info(f"Fetching latest {num_10k} 10-K filings...")
            extracted_10k = await self.document_port.get_latest_sec_filings(ticker, "10-K", limit=num_10k)
            extracted_files["10-K"] = extracted_10k
            logger.info(f"Successfully extracted {len(extracted_10k)} 10-K filings.")
        except Exception as e:
            logger.error(f"Error fetching 10-K for {ticker}: {e}")

        try:
            logger.info(f"Fetching latest {num_10q} 10-Q filings...")
            extracted_10q = await self.document_port.get_latest_sec_filings(ticker, "10-Q", limit=num_10q)
            extracted_files["10-Q"] = extracted_10q
            logger.info(f"Successfully extracted {len(extracted_10q)} 10-Q filings.")
        except Exception as e:
            logger.error(f"Error fetching 10-Q for {ticker}: {e}")

        return extracted_files
