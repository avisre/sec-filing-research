# Completed checks — 26 October 2026

- Detailed observation keys: unique; 852,416 observations, 5,608 securities.
- Reconciliation: all 5,608 security summaries and all 304 metric aggregates agree with the frozen detailed records.
- Population: CIK omissions and repeated issuers counted; one-ticker-per-CIK sensitivity included.
- Annual denominator: filled + partial + missing equals eligible rows; excluded rows separately accounted for.
- Sample: exactly six cases in each of five disjoint strata; deterministic selection; no replacements; 30 supplemental statuses match frozen labels.
- Source verification: 27 numeric facts and three narrative/reporting-basis checks across 21 original SEC documents. Source hashes matched. The AAC annual target remains unresolved.
- PDF: 11 pages, selectable text, all 30 case IDs, 21 distinct original-filing links and one tracked product link. All 11 pages visually inspected for clipping, overlap, broken tables and unreadable text; passed.
- Public artifact screen: private paths, customer contacts, credential patterns and production connection strings absent in the screened exports and PDF.
- Publication authorization: the owner authorized publishing the prepared research and companion materials on 26 October 2026. No customer acquisition results are claimed.

Run `python3 scripts/analyze.py` and `python3 scripts/validate_package.py` to reproduce analytical checks. Run verify_filings.py with an existing cache for source checks. Automated checks cannot certify the author's accounting judgments; retain the stated caveats.
