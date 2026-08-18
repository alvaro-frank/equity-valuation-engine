---
name: extract_business
description: Extracts the core business model, history, products, and strategy of a company.
---

REQUIRED JSON STRUCTURE:
Return ONLY a valid JSON object following this exact schema:
{
    "sources": [
        { "citation_id": "1", "source_name": "Latest 10-K", "exact_quote": "Exact quote from document here" },
        { "citation_id": "2", "source_name": "Q3 Earnings Call", "exact_quote": "Exact quote here" }
    ],
    "company_history": "Key milestones from foundation to present, heavily emphasizing the strategic shifts of the last 3 years with precise dates. Use citations [1].",
    "key_executives": [
        { "name": "Name A", "title": "CHIEF EXECUTIVE OFFICER" },
        { "name": "Name B", "title": "CHIEF FINANCIAL OFFICER" },
        { "name": "Name C", "title": "PRESIDENT & CHIEF INVESTMENT OFFICER" },
        { "name": "Name D", "title": "CHIEF TECHNOLOGY OFFICER" }
    ],
    "revenue_model": "Highly detailed explanation (3-4 sentences) of all major revenue streams, pricing power, and monetization strategy. Must include recent revenue breakdown percentages and margin or growth metrics if available.",
    "strategy": "Core strategic focus and future outlook, anchored in recent management commentary (e.g. latest earnings call).",
    "products_services": [
        { "name": "Product/Service 1", "description": "Comprehensive 2-3 sentence description explaining the utility, market fit, and strategic importance, including recent traction data." },
        { "name": "Product/Service 2", "description": "Comprehensive 2-3 sentence description..." },
        { "name": "Product/Service 3", "description": "Comprehensive 2-3 sentence description..." }
    ]
}

Do not include any markdown formatting outside the JSON, preamble, or conversational text. Return only the raw JSON.

SKILL-SPECIFIC INSTRUCTIONS:
- Source Fact-Extraction First: You MUST extract and define all 'sources' first at the top of the JSON. Then, use those exact citation IDs (e.g. [1]) to reference the evidence in the narrative sections.
- Quantitative Anchors: Whenever analyzing the 'revenue_model', you MUST explicitly cite structural financial metrics if available (e.g., Gross Margins, Operating Margins, ROIC, or FCF generation) to prove the qualitative thesis.
- Executives: Extract the CEO and CFO. Then, from the provided real-world context, extract the next 1 or 2 most senior/relevant officers. Do NOT invent roles. Clean the titles by keeping only the role, removing company names. Convert titles to UPPERCASE.
