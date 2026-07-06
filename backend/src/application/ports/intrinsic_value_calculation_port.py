from typing import Dict, Any
from abc import ABC, abstractmethod
from domain.entities.dcf import DCFAssumptions

class IntrinsicValueCalculationPort(ABC):
    """
    Port interface for an adapter capable of deducing Discounted Cash Flow (DCF) assumptions.
    
    This abstracts away the underlying LLM (e.g., Gemini, Groq, OpenRouter) and ensures
    the application layer receives the strictly formatted assumptions needed for valuation.
    """
    
    @abstractmethod
    async def deduce_dcf_assumptions(
        self, 
        ticker: str, 
        company_profile: Dict[str, Any], 
        quant_data: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, DCFAssumptions]:
        """
        Deduces realistic growth rates and discount rates for Bear, Fair, and Bull scenarios.
        
        Args:
            ticker (str): The stock ticker symbol.
            company_profile (Dict[str, Any]): Qualitative data, moat trajectory, and business model description.
            quant_data (Dict[str, Any]): Historical quantitative metrics (FCF trends, margins).
            
        Returns:
            Dict[str, DCFAssumptions]: A dictionary containing DCFAssumptions for 'bear', 'fair', and 'bull' scenarios.
        """
        pass
        
    # TODO (Production Blueprint): Prompt Segmentation (Micro-Agents)
    # @abstractmethod
    # async def _deduce_bear_assumptions(self, ticker: str, context: dict) -> DCFAssumptions: ...
    # @abstractmethod
    # async def _deduce_fair_assumptions(self, ticker: str, context: dict) -> DCFAssumptions: ...
    # @abstractmethod
    # async def _deduce_bull_assumptions(self, ticker: str, context: dict) -> DCFAssumptions: ...
