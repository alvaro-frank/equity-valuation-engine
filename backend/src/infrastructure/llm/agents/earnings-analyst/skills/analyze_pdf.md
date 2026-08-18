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
