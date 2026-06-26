import asyncio
from decimal import Decimal
from typing import Dict, Any

from application.ports.core_financial_ports import QuantitativeDataPort
from application.ports.llm_analysis_ports import QualitativeDataPort
from application.ports.intrinsic_value_calculation_port import IntrinsicValueCalculationPort
from domain.entities.dcf import DCFAssumptions, DCFScenario, DCFValuation
from application.exceptions.exceptions import ExternalServiceError

class AnalyseDCFValuationUseCase:
    """
    Orchestrates the Discounted Cash Flow (DCF) valuation process.
    It fetches quantitative base data, fetches qualitative data for the moat context,
    invokes the LLM to deduce growth/discount rates, and instantiates the pure mathematical Domain Entities.
    """
    def __init__(
        self,
        quant_data_port: QuantitativeDataPort,
        qual_data_port: QualitativeDataPort,
        llm_port: IntrinsicValueCalculationPort
    ):
        self.quant_data_port = quant_data_port
        self.qual_data_port = qual_data_port
        self.llm_port = llm_port

    async def execute(self, ticker: str, language: str = "en") -> DCFValuation:
        """
        Executes the DCF valuation process for the given ticker.
        """
        # 1. Fetch Quantitative data first
        try:
            financial_years = await self.quant_data_port.get_stock_fundamental_data(ticker)
        except Exception as e:
            raise ExternalServiceError(f"Failed to fetch quantitative data for DCF: {str(e)}")

        if not financial_years:
            raise ExternalServiceError(f"No quantitative financial data available for {ticker} to perform DCF.")

        latest_year = financial_years[-1]

        # 2. Extract strictly mathematical base anchors
        base_fcf = latest_year.free_cash_flow
        shares_outstanding = latest_year.shares_outstanding
        net_cash = latest_year.cash_and_equivalents - latest_year.total_debt

        # 3. Short-circuit if base FCF is negative to save LLM calls
        if base_fcf < 0:
            dummy_assumptions = DCFAssumptions(
                fcf_growth_1_to_5=Decimal("0.0"),
                fcf_growth_6_to_10=Decimal("0.0"),
                wacc=Decimal("0.10"),
                terminal_growth_rate=Decimal("0.02"),
                justification="Company has negative Free Cash Flow. DCF Valuation is fundamentally incompatible."
            )
            scenarios = {
                "bear": DCFScenario("Bear", dummy_assumptions, base_fcf, shares_outstanding, net_cash),
                "fair": DCFScenario("Fair", dummy_assumptions, base_fcf, shares_outstanding, net_cash),
                "bull": DCFScenario("Bull", dummy_assumptions, base_fcf, shares_outstanding, net_cash),
            }
            return DCFValuation(
                base_fcf_ttm=base_fcf,
                shares_outstanding=shares_outstanding,
                net_cash=net_cash,
                scenarios=scenarios
            )

        # 4. Fetch Qualitative data
        try:
            company_profile_obj = await self.qual_data_port.analyse_company(ticker, language=language)
        except Exception as e:
            raise ExternalServiceError(f"Failed to fetch qualitative data for DCF: {str(e)}")

        # 3. Prepare Context for LLM
        # We build a historical FCF trend to ground the LLM's growth projections
        fcf_history = {}
        for year in financial_years[:5]:  # Last 5 years
            fcf_history[year.fiscal_date_ending] = {
                "revenue": float(year.revenue),
                "operating_margin": float(year.operating_margin) if year.operating_margin else None,
                "free_cash_flow": float(year.free_cash_flow)
            }

        quant_data_context = {
            "historical_financials": fcf_history,
            "current_base_fcf": float(base_fcf)
        }

        # Dump profile to dict for LLM context, focusing on moat
        profile_context = {
            "business_description": company_profile_obj.business_description,
            "competitive_advantage": company_profile_obj.competitive_advantage,
            "moat_trajectory": f"{company_profile_obj.moat_trajectory_status}. {company_profile_obj.moat_trajectory_description}",
            "risk_factors": company_profile_obj.risk_factors,
            "macro_exposure": "Derived from qualitative data"
        }

        # 4. Invoke LLM to deduce DCF Assumptions (Bear, Fair, Bull)
        # The LLM strictly provides rates, NO MATH.
        assumptions_map: Dict[str, DCFAssumptions] = await self.llm_port.deduce_dcf_assumptions(
            ticker=ticker,
            company_profile=profile_context,
            quant_data=quant_data_context,
            language=language
        )

        # 5. Instantiate the Rich Domain Models (Calculates intrinsic value automatically)
        scenarios = {}
        for scenario_name, assumptions in assumptions_map.items():
            scenarios[scenario_name] = DCFScenario(
                scenario_name=scenario_name.capitalize(),
                assumptions=assumptions,
                base_fcf=base_fcf,
                shares_outstanding=shares_outstanding,
                net_cash=net_cash
            )

        # 6. Return the aggregate root entity
        return DCFValuation(
            base_fcf_ttm=base_fcf,
            shares_outstanding=shares_outstanding,
            net_cash=net_cash,
            scenarios=scenarios
        )
