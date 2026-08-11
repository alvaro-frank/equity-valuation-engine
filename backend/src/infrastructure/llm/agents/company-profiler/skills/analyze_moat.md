---
name: analyze_moat
description: Analyzes the competitive advantage, competitors, moat trajectory, and quality pillars.
---

REQUIRED JSON STRUCTURE:
Return ONLY a valid JSON object following this exact schema:
{
    "competitive_advantage": "Deep 4-5 sentence analysis defending the existence, strength, and durability of the Moat. Explicitly anchor the analysis in ROIC, gross margins, or market share metrics.",
    "competitors": [
        { "name": "Competitor 1 Name", "ticker": "AAPL", "overlap": "Detailed 2-3 sentence analysis of direct overlap and competitive threat..." },
        { "name": "Competitor 2 Name", "ticker": "MSFT", "overlap": "Detailed 2-3 sentence analysis..." },
        { "name": "Competitor 3 Name", "ticker": "PRIVATE", "overlap": "Detailed 2-3 sentence analysis..." }
    ],
    "moat_trajectory_status": "EXPANDING/STABLE/SHRINKING",
    "moat_trajectory_description": "Detailed 2-3 sentence analysis of why the competitive advantage trajectory is shifting. Mention recent news.",
    "moat_sources": {
        "intangible_assets": 1,
        "switching_costs": 1,
        "network_effect": 1,
        "cost_advantage": 1,
        "efficient_scale": 1
    },
    "quality_pillars": {
        "management_quality": 1,
        "business_model_resilience": 1,
        "pricing_power": 1,
        "innovation_and_growth": 1,
        "tam_expansion": 1
    }
}
Do not include any markdown formatting outside the JSON, preamble, or conversational text. Return only the raw JSON.
