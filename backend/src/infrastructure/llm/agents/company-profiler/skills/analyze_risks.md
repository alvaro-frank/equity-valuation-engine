---
name: analyze_risks
description: Analyzes management insights, capital allocation, near term catalysts, and risk factors.
---

REQUIRED JSON STRUCTURE:
Return ONLY a valid JSON object following this exact schema:
{
    "sources": [
        { "citation_id": "1", "source_name": "Latest 10-K", "exact_quote": "Exact quote from document here" }
    ],
    "management_insights": "Synthesize the caliber, candor, and track record of management. Do they acknowledge mistakes? Are they overly promotional? Use citations [1].",
    "capital_allocation_strategy": "Detailed analysis of how management deploys Free Cash Flow: CapEx intensity, M&A track record, share buybacks, and dividend policy.",
    "near_term_catalysts": [
        { "event": "Catalyst 1 Name", "impact": "Detailed 2-3 sentence breakdown of how this upcoming event could positively or negatively re-rate the stock in the next 12-24 months." }
    ],
    "risk_factors": [
        { "title": "Risk 1 Title (e.g. Geopolitical)", "description": "Detailed 2-3 sentence breakdown of the risk impact and probability. Must include recent specific headwinds and quantifiable data." },
        { "title": "Risk 2 Title (e.g. Competitive)", "description": "Detailed 2-3 sentence breakdown..." },
        { "title": "Risk 3 Title (e.g. Internal)", "description": "Detailed 2-3 sentence breakdown..." },
        { "title": "Risk 4 Title (e.g. Macro)", "description": "Detailed 2-3 sentence breakdown..." }
    ],
    "historical_context_crises": "How the company navigated past major crises and recent macro challenges (e.g. 2022 inflation, recent industry downturns)."
}

Do not include any markdown formatting outside the JSON, preamble, or conversational text. Return only the raw JSON.

SKILL-SPECIFIC INSTRUCTIONS:
- Source Fact-Extraction First: You MUST extract and define all 'sources' first at the top of the JSON. Then, use those exact citation IDs (e.g. [1]) to reference the evidence in the narrative sections.
- Capital Allocation: When analyzing capital allocation, evaluate explicitly if management is repurchasing shares at a discount to intrinsic value or executing value-destructive M&A at peaks. Give precise dollar amounts.
- Comprehensive Risks: MUST provide a detailed list of at least 4 to 6 critical risk factors. Ensure these reflect CURRENT events and real recent news, with specific dates or numbers (e.g. "Q4 2023 supply chain disruption causing $200M impact").
