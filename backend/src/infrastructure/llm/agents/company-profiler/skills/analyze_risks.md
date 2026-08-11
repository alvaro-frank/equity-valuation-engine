---
name: analyze_risks
description: Analyzes management insights, capital allocation, near term catalysts, and risk factors.
---

REQUIRED JSON STRUCTURE:
Return ONLY a valid JSON object following this exact schema:
{
    "management_insights": "Analysis of management quality, execution track record, and integrity.",
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
