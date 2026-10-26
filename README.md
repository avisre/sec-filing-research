# SEC filing verification checklist for AI research

A reusable prompt and worksheet for checking a financial answer against its source. Maintained by StockPortfolio.pro. This is a workflow template, not a published benchmark or a claim that any tool passed these checks.

## Start with a source

Use [SEC EDGAR](https://www.sec.gov/search-filings) to locate a company's filings. Identify the company, form, reporting period and filing date before extracting figures. You can use this checklist manually or with a filing-connected assistant.

## Reusable prompt

> Find [COMPANY]'s most recent filed 10-K. Return the SEC document URL, filing date and fiscal period end. Extract revenue and operating income for the latest two annual periods shown in that filing. Preserve units and identify the source statement or section. If a requested figure is unavailable, say so. Show any calculations separately, with formulas and source inputs. Do not fill gaps with estimates.

For a comparison, repeat for each company and identify mismatched periods or metric definitions before interpreting the result.

## Check the answer

1. Open the linked SEC document and confirm the company and form.
2. Record the reporting period separately from the filing date.
3. Locate each figure in the original statement or note.
4. Preserve the original metric label, units, sign and scope (company or segment).
5. Distinguish reported numbers from calculated ratios or changes.
6. Mark missing or unverified values explicitly.
7. Keep amendments or restatements visible when they affect the comparison.

## Worksheet

Use `filing-checklist.csv` for one row per metric and period. Empty fields are intentional. No company results or performance claims are supplied. Import into a spreadsheet if useful. Do not turn missing values into zero.

## Optional connection

StockPortfolio.pro provides SEC-filing research through Claude and ChatGPT. [Connection instructions and current access terms](https://www.stockportfolio.pro/connect?utm_source=referral&utm_medium=github&utm_campaign=filing_workflows_20261026&utm_content=github_filing_checklist).

This resource is published by the product's builder. The checklist can also be used with EDGAR directly.

## Research companion

[Published Zenodo report and data — DOI: 10.5281/zenodo.23657325](https://doi.org/10.5281/zenodo.23657325).

[Read the research report](research/financial-statement-coverage-audit.pdf): **Why Financial Statement Data Goes Missing: A Reproducible SEC Filing Coverage Audit** by Avinash Sreekumar, StockPortfolio.pro (26 October 2026).

The report examines a frozen product dataset and 30 original-filing cases, including unfavorable and unresolved findings. Coverage is not accuracy; the report is product-authored and not peer reviewed.

[Data and reproducibility instructions](research/README.md) · [All 30 case reviews](research/data/case-review.csv) · [Original SEC filing references](research/data/filing-references.csv)

## Reuse

Original guide, worksheet, report and analytical data: CC BY 4.0. Original research scripts: MIT. Third-party source rights are retained. See [licenses](LICENSE.md).
