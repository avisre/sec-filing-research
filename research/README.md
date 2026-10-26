# SEC filing coverage research package

**Why Financial Statement Data Goes Missing: A Reproducible SEC Filing Coverage Audit**  
Avinash Sreekumar · StockPortfolio.pro · version 1.0 · 26 October 2026

Research report, version 1.0. Not peer reviewed. See the hosting repository for publication links.

## Read

- `financial-statement-coverage-audit.pdf`: standalone research report, including all 30 case reviews and original-filing references.
- `paper.md`: editable report source.
- `data/case-review.csv`: scope, judgments, unresolved cases and direct filing links.
- `data/fact-checks.csv`: 27 numeric receipts with fact IDs, periods, units and dimensions.
- `data/filing-references.csv`: 21 original document URLs and hashes.

## Reproduce the statistics

Python 3.10 or newer; the analysis uses the standard library only. Tested with Python 3.14.4.

```sh
python3 scripts/analyze.py
```

This reads the frozen `data/row-observations.csv.gz`, recomputes all counts and percentages, reconciles the original security and row summaries, and regenerates deterministic case selection. Outputs go to `results/`. It does not call production services or change the product.

A small companion `analysis.ipynb` runs the same analysis and exposes the tables and case-review data. It contains no credentials or product installation dependency.

## Recheck original filings

Install `lxml` (tested 6.1.0), set `SEC_USER_AGENT` to your research name and contact, then:

```sh
python3 scripts/verify_filings.py --cache-dir ./filing-cache
```

The script downloads only the listed SEC documents, with spacing between requests, and verifies 27 numeric receipts plus three narrative/reporting-basis checks. Use `--offline` to recheck an existing cache. It fails rather than silently accepting changed source-document hashes. Full filings are not included in this package. A passing receipt does not settle accounting equivalence, older missing periods or the cause of a blank. AAC's annual target remains unresolved.

## Rebuild the PDF

Install `reportlab` (tested 5.0.0) and the DejaVu Serif/Sans fonts under `/usr/share/fonts/truetype/dejavu`, then:

```sh
python3 scripts/build_pdf.py
```

The renderer reads `paper.md`; edit that file to revise the report. It generates selectable text and clickable citations. The creation metadata is deterministic. `requirements.txt` pins the versions used for optional rendering and source checks; no dependencies are needed for statistics alone.

## Validate the package

```sh
python3 scripts/validate_package.py
```

This checks denominator identities, deterministic case membership, null/zero distinctions, the unresolved case, PDF text and links, and the public-artifact screen. See `QUALITY_CHECKS.md` for the completed visual review.

## Meaning and limits

An observation is a security × statement × basis × presentation row, not an individual reported fact. Filled means present in all available periods (up to five annual/eight quarterly), not necessarily five/eight periods. Zero and null are distinct. Excluded rows follow the original product rules. Labels such as `not_reported` and `sec_has_alt_tag` are diagnostics, not verified root causes.

Statistics and sample selection are reproducible from the frozen export. End-to-end historical extraction from EDGAR is not claimed reproducible: the full original bulk archive, all input snapshots and extraction environment are not distributed. The case-period values supplement documents a later read-only projection whose 30 statuses match the frozen labels; not every historical value was source-validated.

The original detailed export has 852,416 observations covering 5,608 securities. Public-source issuer identifiers are retained to allow duplicate-issuer checks. Customer information and private product configuration are excluded. See `data/source-metadata.json` for provenance and `SHA256SUMS` for package checksums.

## License and disclosure

Original prose and original analytical data: CC BY 4.0. Original scripts: MIT. Linked third-party filings retain their applicable rights. See `LICENSE.md`.

The author owns the product whose dataset is examined. This report is not an independent vendor ranking. Adverse findings and unresolved cases are retained. No claims are made about search ranking, AI citations, investment returns or customer acquisition results.
