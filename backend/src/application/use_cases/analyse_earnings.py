import os
import json
from typing import Optional
from domain.entities import FinancialQuarter, FinancialYear
from application.ports.core_financial_ports import QuantitativeDataPort, TranscriptDataPort
from application.ports.llm_analysis_ports import QualitativeDataPort
from application.exceptions.exceptions import TickerNotFoundError

class AnalyseEarningsUseCase:
    """
    Use Case responsible for gathering the Earnings Call Transcript and the quantitative
    financial statements for a specific quarter, preparing the context, and delegating
    the analysis to the LLM.
    """
    def __init__(self, 
                 transcript_port: TranscriptDataPort, 
                 quant_port: QuantitativeDataPort,
                 llm_port: QualitativeDataPort = None):
        self.transcript_port = transcript_port
        self.quant_port = quant_port
        self.llm_port = llm_port

    async def execute(self, ticker: str, quarter_id: str) -> dict:
        """
        Executes the analysis for a given ticker and quarter_id (e.g., '2024Q1' or '2024').
        """
        is_annual = len(quarter_id) == 4
        
        if is_annual:
            year_val = int(quarter_id)
            quarter_val = 4 # Q4 transcript for annual
        else:
            if len(quarter_id) != 6 or quarter_id[4] != 'Q':
                raise ValueError(f"Invalid quarter_id format: {quarter_id}. Expected format: YYYYQX or YYYY")
            year_val = int(quarter_id[:4])
            quarter_val = int(quarter_id[5:])

        # 2. Fetch Transcript
        transcript_entity = await self.transcript_port.get_earnings_call_transcript(ticker, year_val, quarter_val)
        
        # 3. Fetch Financials
        target_financial = None
        previous_financial = None
        
        if is_annual:
            financial_years = await self.quant_port.get_stock_fundamental_data(ticker)
            if financial_years:
                for fy in financial_years:
                    if fy.fiscal_date_ending.startswith(str(year_val)):
                        target_financial = fy
                    elif fy.fiscal_date_ending.startswith(str(year_val - 1)):
                        previous_financial = fy
        else:
            financial_quarters = await self.quant_port.get_stock_quarterly_data(ticker)
            if financial_quarters:
                from collections import defaultdict
                quarters_by_year = defaultdict(list)
                
                for fq in financial_quarters:
                    year_str = fq.fiscal_date_ending[:4]
                    quarters_by_year[year_str].append(fq)
                    
                for year_str, q_list in quarters_by_year.items():
                    q_list.sort(key=lambda x: x.fiscal_date_ending)
                    for i, fq in enumerate(q_list):
                        mapped_id = f"{year_str}Q{i+1}"
                        if mapped_id == quarter_id:
                            target_financial = fq

            if target_financial:
                # Find the previous quarter by subtracting exactly 1 year from the target's fiscal date
                target_date = target_financial.fiscal_date_ending
                target_year = int(target_date[:4])
                target_month_day = target_date[4:]
                
                # Handle leap year edge case (Feb 29 -> Feb 28)
                if target_month_day == "-02-29":
                    target_month_day = "-02-28"
                    
                expected_prev_date = f"{target_year - 1}{target_month_day}"
                
                # We need to find the closest match or exact match.
                # First try exact match
                previous_financial = next((fq for fq in financial_quarters if fq.fiscal_date_ending == expected_prev_date), None)
                print(f"[DEBUG] expected_prev_date: {expected_prev_date}, Found exact: {previous_financial is not None}")
                
                # If not found, look for one within 10 days of the expected date
                if not previous_financial:
                    from datetime import datetime, timedelta
                    expected_dt = datetime.strptime(expected_prev_date, "%Y-%m-%d")
                    for fq in financial_quarters:
                        fq_dt = datetime.strptime(fq.fiscal_date_ending, "%Y-%m-%d")
                        if abs((fq_dt - expected_dt).days) <= 10:
                            previous_financial = fq
                            print(f"[DEBUG] Found approx: {fq.fiscal_date_ending}")
                            break

        if not transcript_entity and not target_financial:
            raise TickerNotFoundError(f"Neither transcript nor financial data found for {ticker} in {quarter_id}")

        # 4. Prepare Context
        context_data = {
            "current_period_financials": {},
            "previous_period_financials": {},
            "earnings_call_transcript": []
        }
        
        import dataclasses
        
        def format_financial(financial_entity):
            result = {}
            for field, value in dataclasses.asdict(financial_entity).items():
                if value is not None:
                    try:
                        formatted_val = f"{float(value):,.0f}" if isinstance(value, (int, float)) or hasattr(value, '__float__') else str(value)
                    except:
                        formatted_val = str(value)
                    
                    display_name = field.replace('_', ' ').title()
                    result[display_name] = formatted_val
            
            try:
                result["Total Equity"] = f"{float(financial_entity.total_equity):,.0f}"
            except:
                pass
            return result
        
        if target_financial:
            context_data["current_period_financials"] = format_financial(target_financial)
            
        if previous_financial:
            context_data["previous_period_financials"] = format_financial(previous_financial)

        if transcript_entity:
            for t in transcript_entity.transcripts:
                context_data["earnings_call_transcript"].append({
                    "speaker": t.speaker,
                    "title": t.title,
                    "content": t.content
                })
            
        full_context = json.dumps(context_data, indent=2)
        
        # 5. Save to Cache
        try:
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            cache_dir = os.path.join(backend_dir, ".llm_cache", ticker.upper(), "analysis", "context", "filings")
            os.makedirs(cache_dir, exist_ok=True)
            
            if is_annual:
                filename = f"FY{year_val}.json"
            else:
                filename = f"Q{quarter_val}{year_val}.json"
                
            cache_path = os.path.join(cache_dir, filename)
            with open(cache_path, 'w', encoding='utf-8') as f:
                f.write(full_context)
        except Exception as e:
            print(f"Error saving to cache: {e}")
        
        # 6. Call LLM
        if not self.llm_port:
            raise Exception("LLM Port not configured for AnalyseEarningsUseCase")
            
        er_result = await self.llm_port.analyse_earnings_from_context(
            symbol=ticker.upper(),
            context=full_context,
            language="en",
            focus_period=quarter_id
        )
        
        # 7. Get ticker info and build final DTO
        ticker_info = await self.quant_port.get_ticker_info(ticker.upper())
        import dataclasses
        from application.dtos import TickerResult, EarningsReportResult
        
        ticker_dto = TickerResult(
            symbol=ticker.upper(),
            name=ticker_info.name,
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )

        result_dict = dataclasses.asdict(er_result)

        # 8. Deterministic Mathematical Injection for Core Performance
        if target_financial:
            def to_float(val):
                try: return float(val) if val is not None else 0.0
                except: return 0.0
                
            rev = to_float(target_financial.revenue)
            net_inc = to_float(target_financial.net_income)
            shares = to_float(target_financial.shares_outstanding)
            gross = to_float(target_financial.gross_profit)
            op_inc = to_float(target_financial.operating_income)
            ocf = to_float(target_financial.operating_cash_flow)
            capex = to_float(target_financial.capital_expenditures)

            core_perf = result_dict.get("core_performance") or {}
            if rev > 0:
                core_perf["revenue"] = {"amount": rev / 1e9}  # Store in billions
                if shares > 0:
                    core_perf["eps"] = {"amount": net_inc / shares}
                core_perf["gross_margin"] = {"amount": (gross / rev) * 100}
                core_perf["operating_margin"] = {"amount": (op_inc / rev) * 100}
                core_perf["net_margin"] = {"amount": (net_inc / rev) * 100}
                core_perf["free_cash_flow"] = {"amount": (ocf - abs(capex)) / 1e9}
                
                # YoY calculations
                if previous_financial:
                    prev_rev = to_float(previous_financial.revenue)
                    prev_net_inc = to_float(previous_financial.net_income)
                    prev_shares = to_float(previous_financial.shares_outstanding)
                    prev_gross = to_float(previous_financial.gross_profit)
                    prev_op_inc = to_float(previous_financial.operating_income)
                    prev_ocf = to_float(previous_financial.operating_cash_flow)
                    prev_capex = to_float(previous_financial.capital_expenditures)
                    
                    if prev_rev != 0:
                        core_perf["revenue"]["yoy_growth"] = ((rev - prev_rev) / abs(prev_rev)) * 100
                        
                        prev_gross_margin = (prev_gross / prev_rev) * 100
                        core_perf["gross_margin"]["yoy_growth"] = core_perf["gross_margin"]["amount"] - prev_gross_margin
                        
                        prev_op_margin = (prev_op_inc / prev_rev) * 100
                        core_perf["operating_margin"]["yoy_growth"] = core_perf["operating_margin"]["amount"] - prev_op_margin
                        
                        prev_net_margin = (prev_net_inc / prev_rev) * 100
                        core_perf["net_margin"]["yoy_growth"] = core_perf["net_margin"]["amount"] - prev_net_margin
                    
                    if prev_shares > 0 and shares > 0:
                        eps = net_inc / shares
                        prev_eps = prev_net_inc / prev_shares
                        if prev_eps != 0:
                            core_perf["eps"]["yoy_growth"] = ((eps - prev_eps) / abs(prev_eps)) * 100
                    
                    prev_fcf = prev_ocf - abs(prev_capex)
                    fcf = ocf - abs(capex)
                    if prev_fcf != 0:
                        core_perf["free_cash_flow"]["yoy_growth"] = ((fcf - prev_fcf) / abs(prev_fcf)) * 100
            
            result_dict["core_performance"] = core_perf
            
            # Capital Allocation Injection
            cap_alloc = result_dict.get("capital_allocation", {})
            stock_rep = to_float(target_financial.stock_repurchases)
            div = to_float(target_financial.dividends_paid)
            rd = to_float(target_financial.research_and_development)
            
            # Convert to billions (and make positive since cash outflows are usually negative)
            cap_alloc["share_buybacks"] = abs(stock_rep) / 1e9 if stock_rep != 0 else 0.0
            cap_alloc["dividends"] = abs(div) / 1e9 if div != 0 else 0.0
            cap_alloc["capex_rd"] = (abs(capex) + abs(rd)) / 1e9 if (capex != 0 or rd != 0) else 0.0
            result_dict["capital_allocation"] = cap_alloc
            
        # 9. Inject Full Transcript
        if transcript_entity:
            result_dict["transcript"] = [
                {
                    "speaker": t.speaker,
                    "title": t.title,
                    "content": t.content
                }
                for t in transcript_entity.transcripts
            ]
        else:
            result_dict["transcript"] = None
            
        return EarningsReportResult(
            ticker=ticker_dto,
            **result_dict
        )
