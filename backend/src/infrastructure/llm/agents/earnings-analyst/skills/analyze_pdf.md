---
name: analyze_pdf
description: Skill for extracting data from a raw PDF Earnings Report.
---

--- PDF ANALYSIS DIRECTIVES ---
You have been provided with the full text of an Earnings Report PDF (e.g. 10-Q or 10-K).

CRITICAL TEMPORAL SCOPE:
- If the document is a quarterly report (10-Q), you MUST extract financial figures (Revenue, Margins, Cash Flows, CapEx) exclusively from the isolated 'Three Months Ended' column. NEVER extract the 'Six Months Ended', 'Nine Months Ended' or 'Year-to-Date' cumulative columns.
- If the document is an annual report (10-K), extract the full fiscal year figures.

Because this is a raw PDF text extraction:
1. You MUST generate the `core_performance` object by carefully locating the Consolidated Statement of Operations / Income Statement.
2. Ensure you extract strict GAAP metrics (Revenue, Operating Income for margin, Net Income for margin) and NEVER "Adjusted" Non-GAAP versions.
3. Locate the Consolidated Statement of Cash Flows for Operating Cash Flow and Capital Expenditures.
4. Be diligent in matching the correct column for the target period.
5. For qualitative fields, extract evidence from the Management's Discussion and Analysis (MD&A) section.
6. Narrative First, Citations Last: Generate your narrative analysis and append inline citations like [1]. Once you finish the narrative, populate the `sources` array at the end of the JSON with the extracted exact quotes that correspond to your numbers.
7. Financial Reality Check: Management narratives are often overly optimistic. You MUST anchor the 'moat_trajectory_status' and 'moat_trajectory_description' on hard financial data. If gross margins are compressing or revenue is declining, the moat is fundamentally NOT 'EXPANDING', regardless of management's claims about new technologies or market share. A declining financial profile implies a 'SHRINKING' or 'STABLE' moat.
8. Comprehensive Risks: Ensure you extract AT LEAST 3 macro/external risks and AT LEAST 3 internal/execution risks from the MD&A and Risk Factors sections.
9. Skepticism & Execution Check: Actively look for contradictions in the MD&A. Compare the tone of the narrative with the actual margin and revenue execution in the consolidated statements. If management blames "macro headwinds" while competitors are growing, explicitly state it as an internal execution risk.
10. JSON Formatting Integrity: CRITICAL: NEVER use double quotes (") inside any extracted text string. Always replace them with single quotes (') to avoid breaking the JSON schema formatting.
