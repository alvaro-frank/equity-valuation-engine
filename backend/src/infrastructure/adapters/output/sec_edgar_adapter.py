import os
import glob
import shutil
import re
from bs4 import BeautifulSoup
from typing import List
from sec_edgar_downloader import Downloader
from application.ports.filing_repository_port import FilingRepositoryPort
from application.dtos import LocalFilingDTO

class SECAdapter(FilingRepositoryPort):
    def __init__(self, cache_dir: str = ".llm_cache"):
        self.cache_dir = cache_dir
        self.dl = Downloader("EquityValuationEngine", "alvaro@example.com", self.cache_dir)
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _clean_html(self, html_content: str) -> str:
        """
        Removes HTML tags, scripts, and tables, keeping only readable text.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script, style, and metadata/XBRL elements that pollute the text
        for element in soup(["script", "style", "head", "ix:header", "xbrli:context", "xbrli:unit"]):
            element.extract()

        # Get text, strip whitespace
        text = soup.get_text(separator=' ', strip=True)
        return text

    async def _download_latest_sec_filings(self, ticker: str, form_type: str, limit: int = 1) -> List[str]:
        """
        Downloads SEC filings using sec-edgar-downloader, parses HTML,
        and saves as plain text in the cache directory.
        """
        # Download filing
        # Downloader creates structure: {cache_dir}/sec-edgar-filings/{ticker}/{form_type}/{accession_number}/full.txt
        self.dl.get(form_type, ticker, limit=limit, download_details=True)
        
        # Find downloaded files
        base_path = os.path.join(self.cache_dir, "sec-edgar-filings", ticker, form_type)
        if not os.path.exists(base_path):
            return []

        extracted_files = []
        
        # Find all primary-document.html or full.txt files
        # Actually, in sec-edgar-downloader v3, filings are downloaded as primary-document.html or full.txt
        # We search for .html or .txt inside the accession folders
        accession_folders = [f.path for f in os.scandir(base_path) if f.is_dir()]
        
        for folder in accession_folders:
            html_files = glob.glob(os.path.join(folder, "*.html"))
            txt_files = glob.glob(os.path.join(folder, "*.txt"))
            
            target_file = None
            if html_files:
                target_file = html_files[0]
            elif txt_files:
                target_file = txt_files[0]
                
            if target_file:
                with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # If HTML, clean it. Otherwise keep text.
                if target_file.endswith('.html') or '<html' in content[:1000].lower():
                    clean_text = self._clean_html(content)
                else:
                    clean_text = content
                    
                # Attempt to extract the report period from full-submission.txt metadata
                period_suffix = ""
                full_txt_path = os.path.join(folder, "full-submission.txt")
                if os.path.exists(full_txt_path):
                    try:
                        with open(full_txt_path, 'r', encoding='utf-8', errors='ignore') as ft:
                            header_content = ft.read(10000)
                            match = re.search(r'CONFORMED PERIOD OF REPORT:\s*(\d{8})', header_content)
                            if match:
                                date_str = match.group(1) # e.g. 20240930
                                year = int(date_str[:4])
                                month = int(date_str[4:6])
                                
                                fy_match = re.search(r'FISCAL YEAR END:\s*(\d{4})', header_content)
                                fy_end_month = 12
                                if fy_match:
                                    fy_end_month = int(fy_match.group(1)[:2])
                                    
                                fiscal_year = year
                                if month > fy_end_month:
                                    fiscal_year = year + 1
                                    
                                if "10-K" in form_type:
                                    period_suffix = f"_FY{fiscal_year}"
                                else:
                                    if month > fy_end_month:
                                        months_in = month - fy_end_month
                                    else:
                                        months_in = month + 12 - fy_end_month
                                        
                                    quarter = (months_in - 1) // 3 + 1
                                    period_suffix = f"_{fiscal_year}-Q{quarter}"
                    except Exception:
                        pass
                        
                # Save parsed text locally in {ticker}/filings/{form_type} folder for easy access
                accession_num = os.path.basename(folder)
                ticker_dir = os.path.join(self.cache_dir, ticker, "filings", form_type)
                if not os.path.exists(ticker_dir):
                    os.makedirs(ticker_dir)
                parsed_filename = os.path.join(ticker_dir, f"{ticker}_{form_type}{period_suffix}_{accession_num}.txt")
                
                with open(parsed_filename, 'w', encoding='utf-8') as f:
                    f.write(clean_text)
                    
                extracted_files.append(parsed_filename)
                
            # Remove the original heavy SEC accession directory to save space
            try:
                shutil.rmtree(folder)
            except Exception:
                pass
                
        # Aggressively clean up the entire sec-edgar-filings root folder to leave no traces
        sec_edgar_root = os.path.join(self.cache_dir, "sec-edgar-filings")
        try:
            if os.path.exists(sec_edgar_root):
                shutil.rmtree(sec_edgar_root)
        except Exception:
            pass
                
        return extracted_files

    def _list_local_sec_filings_internal(self, ticker: str) -> List[LocalFilingDTO]:
        filings = []
        base_dir = os.path.join(self.cache_dir, ticker.upper(), "filings")
        if not os.path.exists(base_dir):
            return filings
            
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".txt") and file.startswith(f"{ticker.upper()}_"):
                    match = re.match(r'^([A-Z0-9]+)_(10-K|10-Q)(_[A-Z0-9\-]+)_([0-9\-]+)\.txt$', file)
                    if match:
                        t, form_type, period_suffix, accession = match.groups()
                        period = period_suffix.lstrip('_')
                        filings.append(LocalFilingDTO(
                            id=os.path.join(root, file),
                            form_type=form_type,
                            period=period,
                            accession_number=accession
                        ))
        return sorted(filings, key=lambda x: x.period, reverse=True)

    async def get_available_filings(self, ticker: str) -> List[LocalFilingDTO]:
        import time
        import logging
        logger = logging.getLogger(__name__)
        
        cache_dir = os.path.join(self.cache_dir, ticker.upper(), "filings")
        
        need_download = True
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
            
            if file_count > 0 and (time.time() - most_recent_time) < 86400:
                logger.info(f"Cache for {ticker} is fresh (less than 24h old). Skipping SEC EDGAR extraction.")
                need_download = False
                
        if need_download:
            try:
                logger.info(f"Fetching latest 2 10-K filings for {ticker}...")
                await self._download_latest_sec_filings(ticker, "10-K", limit=2)
            except Exception as e:
                logger.error(f"Error fetching 10-K for {ticker}: {e}")
                
            try:
                logger.info(f"Fetching latest 5 10-Q filings for {ticker}...")
                await self._download_latest_sec_filings(ticker, "10-Q", limit=5)
            except Exception as e:
                logger.error(f"Error fetching 10-Q for {ticker}: {e}")
                
        return self._list_local_sec_filings_internal(ticker)

    async def get_filing_paths_for_rag(self, ticker: str, period: str = None) -> List[str]:
        # Ensure filings exist
        await self.get_available_filings(ticker)
        
        filings = self._list_local_sec_filings_internal(ticker)
        k_files = [f.id for f in filings if f.form_type == "10-K"]
        q_files = [f.id for f in filings if f.form_type == "10-Q"]
        
        files_to_inject = []
        is_q4 = (period and period.upper() == "Q4")
        
        if is_q4 or not q_files:
            files_to_inject.extend(k_files[:2])
        else:
            if k_files:
                files_to_inject.append(k_files[0])
            
            target_q = None
            if period:
                for qf in q_files:
                    if period.upper() in qf:
                        target_q = qf
                        break
            
            if not target_q and q_files:
                target_q = q_files[0]
                
            if target_q:
                files_to_inject.append(target_q)
                import re
                target_q_name = os.path.basename(target_q)
                match = re.search(r'([A-Z0-9]+)_10-Q_([0-9]{4})-Q([1-3])_', target_q_name)
                if match:
                    t, year, q_num = match.groups()
                    prev_year = str(int(year) - 1)
                    prev_q_str = f"{prev_year}-Q{q_num}"
                    for qf in q_files:
                        if prev_q_str in qf:
                            files_to_inject.append(qf)
                            break
                            
        return files_to_inject
