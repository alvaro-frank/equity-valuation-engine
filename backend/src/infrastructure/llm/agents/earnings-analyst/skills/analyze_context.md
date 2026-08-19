---
name: analyze_context
description: Skill for extracting data from a structured JSON containing Financials and Transcript.
---

--- STRUCTURED CONTEXT DIRECTIVES ---
You have been provided with a structured JSON context that contains three distinct sections:
1. `current_period_financials`: Contains pre-calculated and precise numerical values extracted directly from the official SEC financial statements for the target period.
2. `previous_period_financials`: Contains the financial data for the homologous period of the previous year. Use this to cross-reference with management's narrative.
3. `earnings_call_transcript`: Contains the verbatim Q&A and prepared remarks from the management's earnings call for this exact period.

Because this is a structured data extraction:
1. For all qualitative assessments (infrastructure_assessment, forward_guidance, moat_trajectory_description, risk_deconstruction, bottom_line), you MUST rely heavily on the `earnings_call_transcript`, `current_period_financials`, and `previous_period_financials` blocks.
2. The citations in your `sources` array MUST be extracted verbatim from the `earnings_call_transcript` block to prove your qualitative claims.
3. For the `bottom_line` specifically, you MUST start your paragraph by explicitly stating the mathematical YoY percentage changes between `current_period_financials` and `previous_period_financials` for Revenue, Net Income, and Gross Margin. Do not use generic words like "grew" or "declined" without the exact numbers. If revenue dropped, you must explicitly state the drop.
4. Narrative First, Citations Last: Generate your narrative analysis and append inline citations like [1]. Once you finish the narrative, populate the `sources` array at the end of the JSON with the extracted exact quotes. NEVER cite an analyst's question as a source. If you want to highlight a risk raised by an analyst, you MUST cite management's response, dodge, or acknowledgment of that issue.
5. Financial Reality Check: Management narratives are often overly optimistic. You MUST anchor the 'moat_trajectory_status' and 'moat_trajectory_description' on hard financial data from the context. If gross margins are compressing or revenue is declining, the moat is fundamentally NOT 'EXPANDING', regardless of management's claims about new technologies or market share. A declining financial profile implies a 'SHRINKING' or 'STABLE' moat.
6. Comprehensive Risks: When analyzing `risk_deconstruction`, look deeply into the Q&A section of the transcript where analysts press management. Extract AT LEAST 3 macro/external risks and AT LEAST 3 internal/execution risks.
7. Skepticism & Execution Check: Actively look for contradictions in the Q&A section where analysts press management. If executives dodge questions about margin compression or churn, explicitly state it as an execution risk. Do not accept corporate fluff.
8. JSON Formatting Integrity: CRITICAL: NEVER use double quotes (") inside any extracted text string. Always replace them with single quotes (') to avoid breaking the JSON schema formatting.
