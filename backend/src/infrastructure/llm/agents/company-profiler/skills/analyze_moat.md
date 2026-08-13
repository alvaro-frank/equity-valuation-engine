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

SKILL-SPECIFIC INSTRUCTIONS:
- Quantitative Anchors: Whenever analyzing the 'competitive_advantage', you MUST explicitly cite structural financial metrics if available (e.g., Gross Margins, Operating Margins, ROIC, or FCF generation) to prove the qualitative thesis. A moat without margin or ROIC expansion is not a moat.
- Independent Scoring: You MUST independently evaluate and assign a score from 1 to 5 for EACH 'moat_sources' and 'quality_pillars' metric based on the SPECIFIC company being analyzed. DO NOT copy the arbitrary numbers from the JSON example.
- Competitors: Enforce exactly ONE single company per item, providing its official stock ticker (use "PRIVATE" if unlisted). The 'overlap' must explicitly detail where they compete and quantify the competitor's threat.
- Moat Definitions:
  * Intangible Assets: Patents, brands, or regulatory licenses.
  * Switching Costs: The cost for a customer to change to a competitor.
  * Network Effect: The value of the service increases as more people use it.
  * Cost Advantage: Can the company produce goods/services at a structurally lower cost than peers?
  * Efficient Scale: Does the market only support one or a few players economically?

QUALITY EXAMPLES (follow this tone and depth):
GOOD competitive_advantage: "Apple's ecosystem creates a powerful flywheel: high switching costs from iCloud lock-in, iOS app investments, and seamless hardware-software integration drive 93% retention rates. The Services segment, growing at 14% YoY in Q3 2023, monetizes this captive base with 78% gross margins, creating a durable revenue stream less vulnerable to hardware cycles."
BAD competitive_advantage: "Apple has a strong brand and makes popular products that people like to buy."
