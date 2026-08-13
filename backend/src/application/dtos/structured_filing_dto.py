from pydantic import BaseModel, Field
from typing import Dict, Optional

class StructuredFilingDTO(BaseModel):
    is_exact_match: bool = Field(..., description="True if edgartools successfully extracted sections directly.")
    exact_sections: Optional[Dict[str, str]] = Field(None, description="Dictionary containing 'business', 'risk_factors', and 'mda' sections. Present if is_exact_match is True.")
    markdown_content: Optional[str] = Field(None, description="Raw markdown content parsed by sec-parser for the fallback path. Present if is_exact_match is False.")
