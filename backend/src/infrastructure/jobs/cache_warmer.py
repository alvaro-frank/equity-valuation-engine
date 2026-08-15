import os
import sys
import json
import time
import asyncio
from datetime import datetime
from loguru import logger

# Add src directory to sys.path so we can import internal modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from infrastructure.adapters.output.alpha_vantage_adapter import AlphaVantageAdapter
from infrastructure.config.settings import settings

class CacheWarmer:
    """
    Background job designed to prefetch and warm up the Alpha Vantage cache.
    Intended to be run during off-peak hours (e.g., midnight) to ensure the system
    has fresh data for the upcoming trading day without exposing users to API latency.
    
    WARNING: This script is designed for Premium Alpha Vantage keys (75 req/min).
    Running this on a Free Tier key (25 req/day) will instantly exhaust the daily quota.
    """
    
    def __init__(self):
        self.adapter = AlphaVantageAdapter(api_key=settings.alpha_vantage_api_key)
        self.cache_dir = self.adapter.cache_dir
        # The endpoints that need to be maintained fresh
        self.endpoints = [
            "OVERVIEW",
            "BALANCE_SHEET",
            "CASH_FLOW",
            "INCOME_STATEMENT",
            "INSTITUTIONAL_HOLDINGS",
            "TIME_SERIES_MONTHLY"
        ]

    def _get_active_tickers(self) -> list[str]:
        """Scans the cache directory to find which tickers users have previously searched."""
        if not os.path.exists(self.cache_dir):
            logger.warning("Cache directory does not exist. No tickers to warm up.")
            return []
            
        tickers = []
        for item in os.listdir(self.cache_dir):
            item_path = os.path.join(self.cache_dir, item)
            # Tickers are stored as directories in the root of the cache (e.g., .alpha_vantage_cache/IBM/)
            if os.path.isdir(item_path):
                tickers.append(item.upper())
        return tickers

    async def warm_up(self):
        """
        Main execution loop.
        Iterates over all known tickers and their required endpoints.
        If a file is missing or older than its TTL, it fetches fresh data.
        Enforces a strict 1.0 second sleep to guarantee max 60 calls/minute,
        staying safely under the 75 calls/minute Premium limit.
        """
        tickers = self._get_active_tickers()
        logger.info(f"Starting Cache Warmer job for {len(tickers)} active tickers.")
        
        calls_made = 0
        
        for ticker in tickers:
            logger.info(f"Checking cache status for {ticker}...")
            
            for endpoint in self.endpoints:
                ttl = self.adapter._get_ttl_for_function(endpoint)
                file_path = os.path.join(self.cache_dir, ticker, f"{endpoint}.json")
                
                needs_update = False
                
                if not os.path.exists(file_path):
                    needs_update = True
                else:
                    age_seconds = time.time() - os.path.getmtime(file_path)
                    if age_seconds > ttl:
                        needs_update = True
                        
                if needs_update:
                    logger.info(f"  -> Refreshing {endpoint} for {ticker} (TTL expired or missing).")
                    try:
                        # The adapter itself will save to cache upon successful fetch
                        await self.adapter._get_data(endpoint, ticker)
                        calls_made += 1
                        
                        # STRICT PACING: Sleep 1.0 second to ensure we don't exceed 60 req/min
                        await asyncio.sleep(1.0)
                    except Exception as e:
                        logger.error(f"  -> Failed to refresh {endpoint} for {ticker}: {e}")
                else:
                    logger.debug(f"  -> {endpoint} is still fresh. Skipping.")
                    
        logger.info(f"Cache Warmer completed successfully. Total API calls made: {calls_made}.")

if __name__ == "__main__":
    warmer = CacheWarmer()
    asyncio.run(warmer.warm_up())
