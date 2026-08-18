import asyncio
from typing import List
from application.ports.core_financial_ports import QuantitativeDataPort
from application.dtos import LocalFilingDTO, LocalFilingListResult
from domain.entities import FinancialYear, FinancialQuarter

class GetAvailableFilingsUseCase:
    """
    Service responsible for retrieving available financial quarters and years from the data provider
    and formatting them as "filings" for the frontend to consume.
    """
    def __init__(self, quant_adapter: QuantitativeDataPort):
        """
        Initialises the GetAvailableFilingsUseCase with the quantitative adapter.
        """
        self.quant_adapter = quant_adapter

    async def execute(self, ticker_symbol: str) -> LocalFilingListResult:
        """
        Fetches the latest 3 financial years and latest 8 financial quarters for a company
        and maps them to LocalFilingDTO elements.
        
        Args:
            ticker_symbol (str): The stock ticker symbol.
            
        Returns:
            LocalFilingListResult: A list of available filings.
        """
        yearly_task = self.quant_adapter.get_stock_fundamental_data(ticker_symbol)
        quarterly_task = self.quant_adapter.get_stock_quarterly_data(ticker_symbol)
        
        financial_years, financial_quarters = await asyncio.gather(
            yearly_task, quarterly_task
        )
        
        filings = []
        
        # Add Top 3 Years
        if financial_years:
            valid_years = [y for y in financial_years if y.fiscal_date_ending != "TTM"]
            top_3_years = valid_years[:3]
            for fy in top_3_years:
                year_str = fy.fiscal_date_ending[:4]
                filings.append(
                    LocalFilingDTO(
                        id=year_str,
                        form_type="10-K",
                        period=fy.fiscal_date_ending,
                        accession_number=year_str,
                        focus_period="FY"
                    )
                )
                
        # Add Top 10 Quarters
        if financial_quarters:
            from collections import defaultdict
            quarters_by_year = defaultdict(list)
            
            for fq in financial_quarters:
                year_str = fq.fiscal_date_ending[:4]
                quarters_by_year[year_str].append(fq)
                
            quarter_dtos = []
            for year_str, q_list in quarters_by_year.items():
                q_list.sort(key=lambda x: x.fiscal_date_ending)
                for i, fq in enumerate(q_list):
                    quarter = f"Q{i+1}"
                    quarter_dtos.append(
                        LocalFilingDTO(
                            id=f"{year_str}{quarter}",
                            form_type="10-Q",
                            period=fq.fiscal_date_ending,
                            accession_number=year_str,
                            focus_period=quarter
                        )
                    )
                    
            quarter_dtos.sort(key=lambda x: x.period, reverse=True)
            filings.extend(quarter_dtos[:12])
                
        return LocalFilingListResult(filings=filings)
