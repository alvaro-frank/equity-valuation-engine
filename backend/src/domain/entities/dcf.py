from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional
from domain.exceptions.exceptions import DomainValidationError

@dataclass(frozen=True)
class DCFAssumptions:
    """
    Represents the mathematical levers (growth rates and discount rate) and the narrative 
    justification for a specific DCF scenario, as deduced by the Valuation Engine/LLM.
    
    Attributes:
        fcf_growth_1_to_5 (Decimal): Projected free cash flow growth rate for years 1 to 5 (e.g., 0.15 for 15%).
        fcf_growth_6_to_10 (Decimal): Projected free cash flow growth rate for years 6 to 10 (e.g., 0.10 for 10%).
        wacc (Decimal): Weighted Average Cost of Capital (discount rate) (e.g., 0.085 for 8.5%).
        terminal_growth_rate (Decimal): Perpetual growth rate after year 10 (e.g., 0.025 for 2.5%).
        justification (str): Analytical narrative justifying these specific rates based on the company's moat and macro environment.
    """
    fcf_growth_1_to_5: Decimal
    fcf_growth_6_to_10: Decimal
    wacc: Decimal
    terminal_growth_rate: Decimal
    justification: str
    
    def __post_init__(self):
        if self.wacc <= 0:
            raise DomainValidationError("WACC must be strictly positive.")
        if self.wacc <= self.terminal_growth_rate:
            raise DomainValidationError("WACC must be greater than terminal growth rate to calculate Terminal Value.")

@dataclass
class DCFScenario:
    """
    Rich Domain Model representing a single DCF scenario (e.g., Bear, Fair, Bull).
    It encapsulates the Base Metrics, the Assumptions, and performs the rigorous mathematical 
    calculation of projected Free Cash Flows, Terminal Value, and Intrinsic Value.
    
    Attributes:
        scenario_name (str): Name of the scenario (Bear, Fair, Bull).
        assumptions (DCFAssumptions): The growth and discount rates to apply.
        base_fcf (Decimal): The Trailing Twelve Months (TTM) Free Cash Flow.
        shares_outstanding (Decimal): The current number of shares outstanding.
        net_cash (Decimal): The company's total cash minus total debt.
        
        # Calculated automatically
        projected_fcfs (List[Decimal]): The projected FCFs for years 1 to 10.
        terminal_value (Decimal): The Gordon Growth Model terminal value at year 10.
        intrinsic_value_per_share (Decimal): The final calculated fair value per share.
    """
    scenario_name: str
    assumptions: DCFAssumptions
    base_fcf: Decimal
    shares_outstanding: Decimal
    net_cash: Decimal
    
    projected_fcfs: List[Decimal] = field(init=False)
    terminal_value: Decimal = field(init=False)
    intrinsic_value_per_share: Decimal = field(init=False)
    
    def __post_init__(self):
        if self.shares_outstanding <= 0:
            raise DomainValidationError("Shares outstanding must be positive to calculate intrinsic value.")
        
        # 1. Project FCFs for 10 years
        fcfs = []
        current_fcf = self.base_fcf
        
        # Years 1-5
        for _ in range(5):
            current_fcf = current_fcf * (Decimal("1") + self.assumptions.fcf_growth_1_to_5)
            fcfs.append(current_fcf)
            
        # Years 6-10
        for _ in range(5):
            current_fcf = current_fcf * (Decimal("1") + self.assumptions.fcf_growth_6_to_10)
            fcfs.append(current_fcf)
            
        self.projected_fcfs = fcfs
        
        # 2. Calculate Terminal Value (Gordon Growth)
        # TV = FCF_10 * (1 + g) / (WACC - g)
        fcf_10 = self.projected_fcfs[-1]
        g = self.assumptions.terminal_growth_rate
        wacc = self.assumptions.wacc
        
        self.terminal_value = (fcf_10 * (Decimal("1") + g)) / (wacc - g)
        
        # 3. Discount FCFs and TV to Present Value (PV)
        pv_fcfs = Decimal("0")
        for i, fcf in enumerate(self.projected_fcfs, start=1):
            pv_fcfs += fcf / ((Decimal("1") + wacc) ** i)
            
        pv_tv = self.terminal_value / ((Decimal("1") + wacc) ** 10)
        
        # 4. Calculate Intrinsic Value per Share
        enterprise_value = pv_fcfs + pv_tv
        equity_value = enterprise_value + self.net_cash
        self.intrinsic_value_per_share = round(equity_value / self.shares_outstanding, 2)


@dataclass(frozen=True)
class DCFValuation:
    """
    Aggregate entity representing the complete DCF Valuation for a company.
    
    Attributes:
        base_fcf_ttm (Decimal): Historical anchor FCF.
        shares_outstanding (Decimal): Historical anchor shares.
        net_cash (Decimal): Historical anchor net cash.
        scenarios (Dict[str, DCFScenario]): Dictionary of evaluated scenarios keyed by name (e.g. 'fair', 'bear').
    """
    base_fcf_ttm: Decimal
    shares_outstanding: Decimal
    net_cash: Decimal
    scenarios: Dict[str, DCFScenario] = field(default_factory=dict)
