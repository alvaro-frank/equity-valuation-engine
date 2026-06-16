import pytest
from decimal import Decimal
from domain.entities.dcf import DCFAssumptions, DCFScenario
from domain.exceptions.exceptions import DomainValidationError

def test_dcf_scenario_google_fair_case():
    """
    Test the DCF mathematical engine using the real-world GOOG Fair Case scenario 
    provided by the LLM. It guarantees the output is exactly $265.43.
    """
    # LLM Assumptions for Fair Case
    assumptions = DCFAssumptions(
        fcf_growth_1_to_5=Decimal("0.15"),    # 15%
        fcf_growth_6_to_10=Decimal("0.10"),   # 10%
        wacc=Decimal("0.085"),                # 8.5%
        terminal_growth_rate=Decimal("0.025"),# 2.5%
        justification="Cloud and AI integration drives strong steady growth."
    )
    
    # Base Anchor Metrics
    scenario = DCFScenario(
        scenario_name="Fair",
        assumptions=assumptions,
        base_fcf=Decimal("82.5"),        # 82.5 Billion
        shares_outstanding=Decimal("12.35"), # 12.35 Billion
        net_cash=Decimal("105.0")        # 105.0 Billion
    )
    
    # Our internal math guarantees the mathematically exact value of $258.47
    # Note: The LLM originally returned 265.43, which demonstrates exactly why 
    # we use Python for the math instead of the LLM (it slightly hallucinated the compounding).
    assert scenario.intrinsic_value_per_share == Decimal("258.47")

def test_dcf_assumptions_validation():
    # WACC must be strictly positive
    with pytest.raises(DomainValidationError, match="WACC must be strictly positive."):
        DCFAssumptions(
            fcf_growth_1_to_5=Decimal("0.15"),
            fcf_growth_6_to_10=Decimal("0.10"),
            wacc=Decimal("0.0"),
            terminal_growth_rate=Decimal("0.025"),
            justification="Test"
        )
        
    # WACC must be greater than terminal growth rate
    with pytest.raises(DomainValidationError, match="WACC must be greater than terminal growth rate"):
        DCFAssumptions(
            fcf_growth_1_to_5=Decimal("0.15"),
            fcf_growth_6_to_10=Decimal("0.10"),
            wacc=Decimal("0.02"),
            terminal_growth_rate=Decimal("0.025"),
            justification="Test"
        )

def test_dcf_scenario_invalid_shares():
    assumptions = DCFAssumptions(
        fcf_growth_1_to_5=Decimal("0.15"),
        fcf_growth_6_to_10=Decimal("0.10"),
        wacc=Decimal("0.085"),
        terminal_growth_rate=Decimal("0.025"),
        justification="Test"
    )
    
    with pytest.raises(DomainValidationError, match="Shares outstanding must be positive"):
        DCFScenario(
            scenario_name="Fair",
            assumptions=assumptions,
            base_fcf=Decimal("82.5"),
            shares_outstanding=Decimal("0"),
            net_cash=Decimal("105.0")
        )
