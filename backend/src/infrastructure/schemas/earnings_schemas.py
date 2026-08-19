from pydantic import BaseModel, Field
from typing import List, Optional


class CapitalAllocationSchema(BaseModel):
    """
    Represents the capital allocation of the company.
    """

    infrastructure_assessment: str

class RiskDeconstructionSchema(BaseModel):
    """
    Represents the risk deconstruction of the company.
    """
    macro_risks: List[str]
    internal_risks: List[str]

class SourceCitation(BaseModel):
    """
    A specific citation source.
    """
    citation_number: int
    source_name: Optional[str] = None
    source_text: str

class EarningsReportSchema(BaseModel):
    """
    Schema for earnings report analysis focused on Value Investing.
    """
    period_end_date: str
    capital_allocation: CapitalAllocationSchema
    forward_guidance: str
    moat_trajectory_status: str
    moat_trajectory_description: str
    risk_deconstruction: RiskDeconstructionSchema
    bottom_line: str
    sources: List[SourceCitation] = Field(
        ..., 
        description="List of numerical citations used in the text and their source document section or page"
    )
