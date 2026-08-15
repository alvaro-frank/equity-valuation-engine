import os
from typing import List, Dict, Optional
from loguru import logger
import traceback
from bs4 import BeautifulSoup

from application.ports.filing_repository_port import FilingRepositoryPort
from application.dtos import LocalFilingDTO, StructuredFilingDTO

try:
    from edgar import Company, set_identity
    import edgar
except ImportError:
    pass

class SECAdapter(FilingRepositoryPort):
    def __init__(self, cache_dir: str = ".llm_cache"):
        self.cache_dir = cache_dir
        
        # Load user agent from environment variable as per production plan
        # We must set this before calling any edgartools functions
        user_agent_email = os.getenv("SEC_API_EMAIL", "sec-bot@equity-valuation.com")
        # edgartools format for identity is usually "Name <email@example.com>"
        set_identity(f"EquityValuationEngine <{user_agent_email}>")
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _save_to_cache(self, ticker: str, data: dict):
        import json
        target_dir = os.path.join(self.cache_dir, ticker.upper(), "filings")
        os.makedirs(target_dir, exist_ok=True)
        cache_path = os.path.join(target_dir, f"sec_structured_{ticker.upper()}.json")
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.warning(f"Failed to cache SEC structured data for {ticker}: {e}")


    def _get_from_cache(self, ticker: str) -> Optional[dict]:
        import json
        cache_path = os.path.join(self.cache_dir, ticker.upper(), "filings", f"sec_structured_{ticker.upper()}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read SEC cache for {ticker}: {e}")
        return None

    async def get_structured_filings(self, ticker: str) -> StructuredFilingDTO:
        logger.info(f"[SECAdapter] Attempting Dual-Path extraction for {ticker}...")
        
        try:
            company = Company(ticker)
            
            # 1. Fetch indices (very fast, uses edgartools internal sqlite cache)
            tenk_filings = company.get_filings(form="10-K").head(2)
            tenq_filings = company.get_filings(form="10-Q").head(5)
            
            latest_k_date = tenk_filings[0].filing_date if len(tenk_filings) > 0 else None
            latest_q_date = tenq_filings[0].filing_date if len(tenq_filings) > 0 else None
            
            # 2. Check if our local JSON cache is up-to-date
            cached_data = self._get_from_cache(ticker)
            if cached_data:
                cache_keys = str(cached_data.keys())
                has_latest_k = latest_k_date and str(latest_k_date) in cache_keys
                has_latest_q = latest_q_date and str(latest_q_date) in cache_keys
                
                if (not latest_k_date or has_latest_k) and (not latest_q_date or has_latest_q):
                    logger.info(f"[SECAdapter] Cache hit! SEC filings for {ticker} are up-to-date. Skipping parsing.")
                    return StructuredFilingDTO(is_exact_match=True, exact_sections=cached_data)
            
            # 3. Cache Miss or Outdated: Selectively parse only the 3 required documents
            logger.info(f"[SECAdapter] Cache miss or outdated. Parsing SEC documents for {ticker}...")
            exact_sections = {}
            target_filings = []
            
            if len(tenk_filings) > 0:
                target_filings.append(("10-K", tenk_filings[0]))
            if len(tenq_filings) > 0:
                target_filings.append(("10-Q", tenq_filings[0]))
            if len(tenq_filings) > 3:
                target_filings.append(("10-Q", tenq_filings[3]))
                
            for doc_type, filing in target_filings:
                try:
                    obj = filing.obj()
                    if hasattr(obj, 'items'):
                        for item_key in obj.items:
                            exact_sections[f"{doc_type}_{filing.filing_date}_{item_key.upper()}"] = obj[item_key]
                except Exception as e:
                    logger.warning(f"Failed to parse {doc_type} for {ticker}: {e}")
            
            # Check if we successfully extracted the core items we need to consider Path 1 a success
            has_core_k = any("ITEM 1" in k for k in exact_sections.keys())
            has_core_q = any("ITEM 2" in k for k in exact_sections.keys()) if len(tenq_filings) > 0 else True
            
            if has_core_k and has_core_q:
                logger.info(f"[SECAdapter] Path 1 (Fast Path) Succeeded for {ticker}. All items extracted generically.")
                
                # Cache it locally so it's visible in the context folder
                self._save_to_cache(ticker, exact_sections)
                
                return StructuredFilingDTO(
                    is_exact_match=True,
                    exact_sections=exact_sections
                )
            else:
                logger.warning(f"[SECAdapter] Path 1 failed for {ticker}. Edgartools could not cleanly parse all sections.")
                raise Exception("Missing explicit sections.")
                
        except Exception as e:
            logger.warning(f"[SECAdapter] Attempting Path 2 (Fallback) for {ticker} due to: {e}")
            
            try:
                # Path 2 Fallback: Download the raw HTML and parse it for the LLM
                company = Company(ticker)
                latest_filings = company.get_filings(form=["10-K", "10-Q"]).head(3)
                
                markdown_parts = []
                for f in latest_filings:
                    try:
                        import sec_parser as sp
                        html = f.html()
                        elements = sp.Edgar10QParser().parse(html)
                        tree = sp.TreeBuilder().build(elements)
                        markdown_parts.append(f"--- Document: {f.form} ---\n{str(tree)[:150000]}")
                    except ImportError:
                        # Fallback to BeautifulSoup clean if sec-parser fails
                        html_content = f.html()
                        if html_content:
                            soup = BeautifulSoup(html_content, 'html.parser')
                            for element in soup(["script", "style", "head", "ix:header", "xbrli:context", "xbrli:unit"]):
                                element.extract()
                            clean_text = soup.get_text(separator=' ', strip=True)
                            # Truncate to 150k chars per document
                            markdown_parts.append(f"--- Document: {f.form} ---\n{clean_text[:150000]}\n")
                
                return StructuredFilingDTO(
                    is_exact_match=False,
                    markdown_content="\n".join(markdown_parts)
                )
                
            except Exception as e2:
                logger.error(f"[SECAdapter] Both Path 1 and Path 2 failed for {ticker}: {traceback.format_exc()}")
                # Return empty to allow pipeline to continue with quantitative data only
                return StructuredFilingDTO(is_exact_match=False, markdown_content="")
