# Why Financial Statement Data Goes Missing: A Reproducible SEC Filing Coverage Audit

Avinash Sreekumar | StockPortfolio.pro

Research report, version 1.0 | 26 October 2026 | Not peer reviewed

## Abstract

A missing cell in a financial-data interface is not a diagnosis. We analyze a frozen StockPortfolio.pro audit covering 5,608 listed securities and 852,416 presentation-row observations across annual and quarterly panels. After the original exclusion rules, 394,799 annual observations remain: 220,665 (55.9%) are filled across available periods, 34,429 (8.7%) are partial, and 139,705 (35.4%) are missing throughout. These are measures of presentation coverage, not financial accuracy. Thirty deterministically selected cases are reviewed using 21 original SEC documents and filing-history metadata. The cases illustrate reporting-period differences, later-filing comparatives, dimensional contexts, narrative disclosure, and mismatches between accounting labels. One annual target remains unadjudicated because no annual filing is identified. The package reproduces the descriptive statistics and scoped filing checks; it does not reproduce the entire historical extraction pipeline. No competitor comparison or investment-performance claim is made.

## 1. Research question and scope

When a financial-data table is blank, what can its coverage diagnostics actually establish? This report examines one product dataset and the interpretation of its missing-row labels. It does not estimate the completeness of SEC EDGAR, rank financial-data vendors, or measure the accuracy of an AI model.

The distinction matters because structured data and the original document are different representations. SEC documentation describes Company Facts as an aggregation across submissions of facts from non-custom taxonomies that apply to the entire filing entity. The original filing can also contain custom concepts, dimensional disclosures and prose. A search limited to selected structured tags cannot establish that the filing contains no relevant disclosure. [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

Inline XBRL allows financial facts and their contexts to be inspected within the original human-readable document. We use those documents to check selected amounts, periods, units, signs and dimensions. [SEC Inline XBRL overview](https://www.sec.gov/structureddata/osd-inline-xbrl.html)

## 2. Data and methods

### 2.1 Snapshot and provenance

The detailed audit comprises 12 recovered shard files. Its companion completeness index records generation at 2026-10-25 14:20:34 UTC; the security index records 2026-10-25 14:05:03 UTC. Inputs were frozen on 26 October 2026. These timestamps identify the audit and index snapshots, not a guarantee that every issuer filed or was refreshed on that date.

All 5,608 security-level summary records and all 304 row-level aggregate records reconcile exactly to the recovered detailed observations. No duplicate security–statement–basis–metric keys were found. Input checksums and the sanitized detailed export accompany the report. An older narrative summary describes a different population and row definition; its before/after claims are not reused here.

The population follows the product index’s stock classification, including its possible classification errors. It contains 4,185 records in the original regular-reporter tier and 1,423 in its other-stock tier. These are product rules, not independently certified regulatory categories. Foreign issuers, different share classes and recently listed entities are not assumed comparable.

### 2.2 Unit, periods and denominators

One observation is a security × statement × basis × presentation row. It summarizes a row across up to five available annual records or eight available quarterly records. It is not one financial fact or one cell. Annual and quarterly records are analyzed separately; their statuses are not added into a single quality score.

A row is filled if every available period has a non-null value, partial if some do, and missing if none do or if there are no statement records. A row with one available period can therefore be filled. Missing years are not inserted to create a fixed five-year panel. Zero is a present value; null remains missing. The case-period supplement documents the selected rows’ available dates and values, but is not a complete census of all panel dates.

The original exclusion rules remove 27,097 annual observations marked not applicable, 1,884 with per-share data withheld, and 2,428 blank by formula design: 31,409 in total. Subtracting these from 426,208 raw annual observations yields 394,799 eligible observations. Exclusions are conditional product rules, including industry rules; they are not independently proven accounting requirements. Changing them changes the denominator.

### 2.3 Reported, calculated and relabelled rows

The presentation mixes reported inputs with formulas and aliases. Gross, operating and net margins and the effective tax rate are calculated ratios. The EBITDA row adds operating income and depreciation/amortization; the EBIT row aliases operating income. The other-operating-expenses row is a residual. Some totals and cash-plus-investment rows use fallback arithmetic. A filled row therefore does not prove that its exact displayed metric was filed as a standalone line.

Original values, calculated results and presentation labels must be distinguished. The case review flags scope and label differences even when the numerical input is present. No unverified value is repaired, imputed or substituted in this study.

### 2.4 Duplicate issuers

The 5,608 securities map to 5,525 known CIKs, with nine securities lacking a CIK. Sixty-two CIKs occur on more than one security, covering 136 securities. There are 74 additional securities beyond one ticker per known CIK. These are repeated issuer exposures, not duplicate observation keys.

As a sensitivity analysis, retaining the lexicographically first ticker per CIK and treating missing-CIK securities separately leaves 5,534 records. Annual filled coverage becomes 55.8276%, compared with 55.8930% in the security-weighted analysis. This small difference is specific to this snapshot; neither weighting is an accuracy measure.

### 2.5 Case selection and validation

The sample was fixed before filing review. It contains six cases in each of five disjoint groups: filled rows; partial rows excluding mapped/alternative-tag reasons; mapped-tag gaps; alternative-tag gaps; and hidden rows with apparent missing-data reasons. Within each group, observations were ordered by ticker, metric and statement using ascending Unicode order, retaining the first six distinct CIKs. Missing CIKs would be keyed by ticker. Issuers may recur across groups.

The resulting sample is lexically concentrated and deliberately explanatory. It is neither random nor representative, so it cannot support an error rate or population-level causal attribution. No case was replaced because its evidence was inconvenient or incomplete.

The review inspected 21 original SEC documents. It checked 27 numeric receipts by element ID, tag, reporting dates, unit, scale/sign and dimensions, plus three narrative or reporting-basis cases. Primary annual filings were examined first. Where a diagnostic pointed to a later filing’s comparative balance, that later document was also inspected and kept distinct. Supplemental local row projections matched all 30 frozen statuses, but historical values were not exhaustively audited.

## 3. Descriptive results

### 3.1 Annual presentation coverage

| Statement | Eligible rows | Filled | Partial | Missing |
| --- | --- | --- | --- | --- |
| Income | 123,560 | 74,132 (60.0%) | 8,293 (6.7%) | 41,135 (33.3%) |
| Balance sheet | 159,720 | 87,318 (54.7%) | 17,296 (10.8%) | 55,106 (34.5%) |
| Cash flow | 111,519 | 59,215 (53.1%) | 8,840 (7.9%) | 43,464 (39.0%) |
| All three | 394,799 | 220,665 (55.9%) | 34,429 (8.7%) | 139,705 (35.4%) |

Percentages use each row’s eligible denominator and are rounded to one decimal place. Filled, partial and missing are mutually exclusive. The regular-reporter tier has 179,691 filled observations out of 295,058 (60.9%); the other-stock tier has 40,974 out of 99,741 (41.1%). Differences can reflect population and denominator rules as well as data availability. They do not establish that one group’s reported figures are more accurate.

Quarterly counts are supplied in results/coverage.csv with their own denominators. The paper focuses on annual case studies and makes no assumption that quarterly cash-flow records all represent standalone quarters.

### 3.2 Diagnostic labels describe search outcomes

The 174,134 annual observations that are partial or missing carry the following original diagnostic labels. Each observation receives one label, although a row can have several underlying issues across periods.

| Original diagnostic label | Annual rows | Interpretation |
| --- | --- | --- |
| not_reported | 108,650 | No matched fact in tested tag set |
| no_statement_rows | 25,230 | No rows in extracted statement panel |
| sec_has_alt_tag | 23,089 | Alternative-tag candidate |
| missing_unchecked | 14,480 | Missing; source match not checked |
| sec_has_mapped_tag | 1,389 | Mapped-tag candidate |
| no_sec_file | 1,296 | No verified issuer-data file |

The largest category, not_reported, means that the audit did not find a matching fact under its tested tags and matching rules. It is not a finding that the issuer failed to report the information. Likewise, a candidate tag can concern a different concept, a different filing version or a different scope. The labels are useful investigation leads, not established root causes.

## 4. What the original filings show

### 4.1 Coverage can be complete over a short history

AACI’s cash observation and AACO’s accumulated-deficit observation are filled even though the inspected panels each contain only one balance-sheet period. Both latest amounts are supported by their original filings. This confirms the coverage definition’s available-period behavior; it does not establish five-year completeness. [F05](https://www.sec.gov/Archives/edgar/data/2092897/000119312526117694/d107030d10k.htm) [F06](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm)

### 4.2 A structured blank can coexist with disclosure

AAL’s dataset has null dividend values for 2025 and 2024, while Item 5 expressly describes no cash dividend payments in those years. The filing is informative even though the structured row is blank. We retain the original nulls and record the narrative evidence separately. [F08](https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/aal-20251231.htm)

AAMI’s 2025 common-stock value is present as a zero in a context excluding consolidated funds. The missing unqualified dataset cell cannot be explained simply as non-disclosure; accepting the dimensional value requires a scope decision. [F10](https://www.sec.gov/Archives/edgar/data/1748824/000162828026012856/aami-20251231.htm)

### 4.3 Matching a tag does not settle the metric

AACG’s current-debt input uses a standard tag whose name suggests long-term debt’s current portion, but the filing labels the amount a short-term loan. Its alternative-tag candidate for other operating expenses is general and administrative expense, whereas the audited presentation row is a residual. Both illustrate why tag names cannot replace examination of the filed label and the target formula. [F04](https://www.sec.gov/Archives/edgar/data/1420529/000110465926037267/aacg-20251231x20f.htm)

AAME’s cash-flow line combines accounts payable and accrued expenses, while the product row names accounts payable alone. The numerical input is supported; equivalence of the narrower presentation label is not. [F09](https://www.sec.gov/Archives/edgar/data/8177/000114036126039933/ef20060652_10k.htm)

### 4.4 Later comparatives require separate provenance

All six selected mapped-tag cases were traced to later quarterly documents reporting comparative balances for annual period-end dates. This confirms the candidates in those cases; it does not show that the same tagged lines existed in the original annual filings. It also does not establish the upstream reason that the product left the rows blank.

ABBV illustrates the need to retain filing versions: the annual balance sheet shows USD 6.265 billion, whereas the later quarterly comparative shows USD 6.293 billion under the candidate tag. The cause of this difference was not established. ABNB’s annual note gives gross customer receivables and a reserve separately, while the later quarterly filing provides a net comparative. A calculated annual net and a directly tagged later comparative must not be silently conflated. [F17](https://www.sec.gov/Archives/edgar/data/1551152/000155115226000026/abbv-20260630.htm) [F19](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000027/abnb-20260630.htm)

### 4.5 A missing annual panel does not mean no statement exists

AACO’s original report contains a cash-flow statement covering the period from inception in November to the end of December 2025. Its annual extracted cash-flow panel is empty. That short duration lies outside the audit matcher’s 340–390-day annual window. The statement’s existence is verified; the exact upstream extraction cause and a capex value are not established. [F06](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm)

For AAC, no annual filing is identified in the frozen index or retrieved submissions history. The available quarterly report establishes a different basis and cannot adjudicate the selected annual target. The case remains in the sample as unresolved. [F03](https://www.sec.gov/Archives/edgar/data/2128115/000110465926095993/tmb-20260630x10q.htm)

## 5. Limitations and reproducibility

This is a single-product observational audit authored by the product’s founder. The coverage definition, stock classification, exclusions and row labels are product-specific. Their completeness does not certify accounting correctness. The census is security-weighted, includes repeated issuers, and contains no fixed five-year panel guarantee. The selected cases do not estimate prevalence or a population error rate.

The original data-quality labels are preserved, including their overbroad names. We do not infer cause merely from a later filing match. Quarterly comparatives can reflect different presentations or revisions. A missing source concept does not imply zero; a present alternative does not establish metric equivalence. Some annual targets and older gaps remain unresolved. No independent second reviewer has adjudicated the cases.

The public package reproduces descriptive statistics and sample selection from the sanitized frozen observations. It provides scripts to recheck the scoped receipts against the original SEC documents, including hashes. It does not redistribute complete issuer filings, the original SEC bulk archive, or the product’s entire historical extraction environment. Therefore statistical reproduction and source-receipt verification are supported; end-to-end regeneration of the original audit from raw EDGAR is not claimed.

The supplemental sample values were projected from local issuer files during this review. They are useful for documenting available periods and nulls, but only the specifically cited facts and narrative checks were validated against originals. The report should not be read as validation of every historical number.

## 6. Conclusion

Financial-data coverage is a property of a particular representation, population and denominator. In this snapshot, about 56% of eligible annual presentation rows are filled across available periods. The case studies show that missingness can coexist with filed narrative, dimensional facts, combined categories, later comparatives or short-period statements. A practical audit should preserve those distinctions and trace proposed replacements to the original filing before treating a blank as either an error or a zero.

## Disclosure and reuse

Avinash Sreekumar is the founder of StockPortfolio.pro, the product whose dataset is examined, and has a commercial interest in the report’s visibility. This is a product-authored research report, not an independent vendor comparison or peer-reviewed publication. It includes adverse observations about the product’s labels and coverage. Software-assisted analysis and document preparation were used; the author is responsible for its interpretation.

Original prose and original analysis data are offered under CC BY 4.0. Original analysis scripts are offered under the MIT License. Third-party filing documents and SEC materials retain their applicable rights and are linked rather than redistributed in full. The dataset contains public issuer identifiers and research observations, not customer records.

Readers interested in the product can consult [StockPortfolio.pro connection instructions](https://www.stockportfolio.pro/connect?utm_source=referral&utm_medium=zenodo&utm_campaign=filing_workflows_20261026&utm_content=statement_coverage_paper).

## Appendix A. All 30 case reviews

The descriptions below report the scope actually checked. A confirmed receipt is not validation of every historical period or proof of a root cause. The machine-readable case-review.csv and fact-checks.csv preserve the identifiers, dates and receipts.

### filled-01 — A: Accounts payable

Snapshot: filled; diagnostic: none.

The 2025 accounts-payable value is USD 570 million in the original balance sheet. This confirms the latest observation, not every historical period. [F01](https://www.sec.gov/Archives/edgar/data/1090872/000109087225000087/a-20251031.htm)

### filled-02 — AA: Accounts payable

Snapshot: filled; diagnostic: none.

The 2025 trade-payables value is USD 1.938 billion. The latest observation matches the original filing. [F02](https://www.sec.gov/Archives/edgar/data/1675149/000119312526077167/aa-20251231.htm)

### filled-03 — AACG: Capital expenditure

Snapshot: filled; diagnostic: none.

The 2025 equipment-purchase outflow is CNY 1,281,220. The data uses a negative cash-outflow sign; the XBRL payment magnitude is positive. A separate USD convenience translation must not replace the CNY value. [F04](https://www.sec.gov/Archives/edgar/data/1420529/000110465926037267/aacg-20251231x20f.htm)

### filled-04 — AACI: Cash and cash equivalents

Snapshot: filled; diagnostic: none.

The filing reports cash of USD 4,347. Only one annual balance-sheet period is available; filled does not mean five years. The product label includes cash equivalents, while the filed line is cash. [F05](https://www.sec.gov/Archives/edgar/data/2092897/000119312526117694/d107030d10k.htm)

### filled-05 — AACO: Retained earnings

Snapshot: filled; diagnostic: none.

The 2025 accumulated deficit is USD 99,715, represented as negative retained earnings. Only one balance-sheet period is available. [F06](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm)

### filled-06 — AAL: Accounts payable

Snapshot: filled; diagnostic: none.

The 2025 accounts-payable value is USD 2.840 billion. The latest observation matches the original filing. [F08](https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/aal-20251231.htm)

### partial-01 — AA: Long-term investments

Snapshot: gappy; diagnostic: not_reported.

The filing shows noncurrent marketable securities of USD 1.397 billion for 2025 and an explicit tagged zero for 2024. These support the two populated cells; the missing older cells are not adjudicated. [F02](https://www.sec.gov/Archives/edgar/data/1675149/000119312526077167/aa-20251231.htm)

### partial-02 — AACG: Current maturities of long-term debt

Snapshot: gappy; diagnostic: not_reported.

The CNY 1 million 2025 amount appears under a short-term-loan label, despite using LongTermDebtCurrent. Mapping that tag directly to current maturities of long-term debt can misdescribe the filed item. [F04](https://www.sec.gov/Archives/edgar/data/1420529/000110465926037267/aacg-20251231x20f.htm)

### partial-03 — AAL: Dividends paid

Snapshot: gappy; diagnostic: not_reported.

Item 5 states that no cash dividends were paid in 2025 or 2024, while both cells are null in the dataset. A missing structured value does not imply the filing is silent; this review does not modify those nulls. [F08](https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/aal-20251231.htm)

### partial-04 — AAME: Change in accounts payable

Snapshot: gappy; diagnostic: not_reported.

The 2025 USD 5.5 million cash-flow change combines accounts payable and accrued expenses. The presentation label mentions accounts payable alone, so numerical presence does not establish a like-for-like metric. [F09](https://www.sec.gov/Archives/edgar/data/8177/000114036126039933/ef20060652_10k.htm)

### partial-05 — AAMI: Common stock

Snapshot: gappy; diagnostic: not_reported.

The 2025 common-stock value is tagged zero in a context excluding consolidated funds. That dimensional fact exists despite a null dataset cell. Whether it satisfies the intended entity scope remains unresolved. [F10](https://www.sec.gov/Archives/edgar/data/1748824/000162828026012856/aami-20251231.htm)

### partial-06 — AAON: Deferred tax assets

Snapshot: gappy; diagnostic: not_reported.

The balance sheet has a tagged zero for 2025 and USD 836,000 for 2024. These support the populated cells; they do not resolve the missing 2021 and 2022 cells. [F13](https://www.sec.gov/Archives/edgar/data/824142/000082414226000005/aaon-20251231.htm)

### mapped_tag_gap-01 — AACO: Total current liabilities

Snapshot: hidden; diagnostic: sec_has_mapped_tag.

A later 10-Q reports USD 465,990 of current liabilities for the 2025 comparison date. The annual filing labels that amount total liabilities. Same-date tag availability is not proof of an annual extraction error. [F07](https://www.sec.gov/Archives/edgar/data/2099906/000121390026087862/ea0300514-10q_abony1.htm)

Annual comparison source: [F06](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm).

### mapped_tag_gap-02 — AAOI: Deferred tax assets

Snapshot: hidden; diagnostic: sec_has_mapped_tag.

A later 10-Q reports USD 7.616 million of deferred income-tax assets for year-end 2025. The candidate is supported, but the precise annual mapping or extraction cause is not established. [F12](https://www.sec.gov/Archives/edgar/data/1158114/000143774926026278/aaoi20260630_10q.htm)

Annual comparison source: [F11](https://www.sec.gov/Archives/edgar/data/1158114/000143774926005875/aaoi20251231_10k.htm).

### mapped_tag_gap-03 — AAPL: Intangible assets

Snapshot: hidden; diagnostic: sec_has_mapped_tag.

A later 10-Q reports USD 13.301 billion of net intangible assets for the 2025 comparison date. It supports the tag candidate; it does not show that the same tagged line appeared in the annual filing. [F15](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm)

Annual comparison source: [F14](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm).

### mapped_tag_gap-04 — ABBV: Other current assets

Snapshot: hidden; diagnostic: sec_has_mapped_tag.

The later 10-Q shows USD 6.293 billion for the 2025 comparison date; the annual balance sheet shows USD 6.265 billion under a different tag. The cause of the difference is not established; automatic substitution would be unsafe. [F17](https://www.sec.gov/Archives/edgar/data/1551152/000155115226000026/abbv-20260630.htm)

Annual comparison source: [F16](https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm).

### mapped_tag_gap-05 — ABNB: Receivables

Snapshot: hidden; diagnostic: sec_has_mapped_tag.

The later 10-Q reports 2025 net customer receivables of USD 186 million. The annual note separately reports USD 225 million gross and USD 39 million reserve. Their difference is calculated, not a copied annual net tag. [F19](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000027/abnb-20260630.htm)

Annual comparison source: [F18](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm).

### mapped_tag_gap-06 — ACA: Treasury stock

Snapshot: gappy; diagnostic: sec_has_mapped_tag.

The later 10-Q explicitly tags 2025 treasury stock as zero. The annual equity table also displays a dash for that balance. This supports a candidate zero, not a rule that all missing values should become zero. [F21](https://www.sec.gov/Archives/edgar/data/1739445/000173944526000067/aca-20260331.htm)

Annual comparison source: [F20](https://www.sec.gov/Archives/edgar/data/1739445/000173944526000029/aca-20251231.htm).

### alternative_tag_gap-01 — A: Deferred tax assets

Snapshot: hidden; diagnostic: sec_has_alt_tag.

The filing reports a USD 380 million net deferred-tax balance for 2025. A net asset/liability concept is not automatically equivalent to the presentation row deferred tax assets. [F01](https://www.sec.gov/Archives/edgar/data/1090872/000109087225000087/a-20251031.htm)

### alternative_tag_gap-02 — AA: Intangible assets

Snapshot: hidden; diagnostic: sec_has_alt_tag.

The 2025 USD 34 million figure is net finite-lived intangible assets. Its scope must be checked before using it for a broader intangible-assets row. [F02](https://www.sec.gov/Archives/edgar/data/1675149/000119312526077167/aa-20251231.htm)

### alternative_tag_gap-03 — AACG: Other operating expenses

Snapshot: hidden; diagnostic: sec_has_alt_tag.

The candidate is CNY 78,767,406 of general and administrative expense. The audited presentation row is a residual of operating expenses after R&D and SG&A. These are different metrics. [F04](https://www.sec.gov/Archives/edgar/data/1420529/000110465926037267/aacg-20251231x20f.htm)

### alternative_tag_gap-04 — AACO: Accounts payable

Snapshot: hidden; diagnostic: sec_has_alt_tag.

The later 10-Q combines payables and accrued expenses at USD 33,875 for 2025. The annual filing describes accrued expenses. It does not establish a standalone trade-payables amount. [F07](https://www.sec.gov/Archives/edgar/data/2099906/000121390026087862/ea0300514-10q_abony1.htm)

Annual comparison source: [F06](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm).

### alternative_tag_gap-05 — AAL: Long-term debt

Snapshot: hidden; diagnostic: sec_has_alt_tag.

The 2025 USD 24.639 billion figure is long-term debt net of current maturities. The target row requires checking debt scope and lease treatment before accepting this alternative tag. [F08](https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/aal-20251231.htm)

### alternative_tag_gap-06 — AAME: Deferred tax assets

Snapshot: hidden; diagnostic: sec_has_alt_tag.

The tax note reports a 2025 net deferred-tax asset of USD 15.044 million. Gross-versus-net treatment remains a definition decision; tag presence alone does not resolve it. [F09](https://www.sec.gov/Archives/edgar/data/8177/000114036126039933/ef20060652_10k.htm)

### apparent_missing-01 — A: Cash & short-term investments

Snapshot: hidden; diagnostic: not_reported.

Cash and cash equivalents are reported at USD 1.789 billion in 2025. The combined cash-plus-short-term-investments row is null. A missing investment input cannot silently be treated as zero. [F01](https://www.sec.gov/Archives/edgar/data/1090872/000109087225000087/a-20251031.htm)

### apparent_missing-02 — AA: Cash & short-term investments

Snapshot: hidden; diagnostic: not_reported.

The 2025 cash balance is USD 1.597 billion. That component does not establish the value of the broader combined row or justify filling its missing input with zero. [F02](https://www.sec.gov/Archives/edgar/data/1675149/000119312526077167/aa-20251231.htm)

### apparent_missing-03 — AAC: Accounts payable

Snapshot: hidden; diagnostic: no_statement_rows.

No annual filing is identified in the frozen index or the retrieved submissions history. The available June 2026 10-Q is a different reporting basis. Annual accounts payable remains unadjudicated; the case is retained. [F03](https://www.sec.gov/Archives/edgar/data/2128115/000110465926095993/tmb-20260630x10q.htm)

### apparent_missing-04 — AACG: Accounts payable

Snapshot: hidden; diagnostic: not_reported.

The 2025 balance sheet combines accrued expenses and other payables at CNY 56,493,791. This is disclosure, but it does not establish a standalone trade-payables figure. [F04](https://www.sec.gov/Archives/edgar/data/1420529/000110465926037267/aacg-20251231x20f.htm)

### apparent_missing-05 — AACI: Accounts payable

Snapshot: hidden; diagnostic: not_reported.

The balance sheet separately reports accrued expenses of USD 32,031 and offering costs. These categories cannot simply be relabelled accounts payable. The target value remains unresolved. [F05](https://www.sec.gov/Archives/edgar/data/2092897/000119312526117694/d107030d10k.htm)

### apparent_missing-06 — AACO: Capital expenditure

Snapshot: hidden; diagnostic: no_statement_rows.

The original filing includes a cash-flow statement from inception on 13 November to 31 December 2025. The annual data panel has no rows. A short reporting period is outside the audit matcher’s 340–390-day annual window; capex is not established as zero. [F06](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm)

## Appendix B. Original filing references

All documents were retrieved on 26 October 2026. The accompanying reference table includes direct URLs, accessions and SHA-256 hashes. A quarterly filing’s report date is distinct from the annual comparative date of a selected fact.

- [F01: A 10-K](https://www.sec.gov/Archives/edgar/data/1090872/000109087225000087/a-20251031.htm); filed 2025-12-22; accession 0001090872-25-000087.

- [F02: AA 10-K](https://www.sec.gov/Archives/edgar/data/1675149/000119312526077167/aa-20251231.htm); filed 2026-02-26; accession 0001193125-26-077167.

- [F03: AAC 10-Q](https://www.sec.gov/Archives/edgar/data/2128115/000110465926095993/tmb-20260630x10q.htm); filed 2026-08-13; accession 0001104659-26-095993.

- [F04: AACG 20-F](https://www.sec.gov/Archives/edgar/data/1420529/000110465926037267/aacg-20251231x20f.htm); filed 2026-03-31; accession 0001104659-26-037267.

- [F05: AACI 10-K](https://www.sec.gov/Archives/edgar/data/2092897/000119312526117694/d107030d10k.htm); filed 2026-03-20; accession 0001193125-26-117694.

- [F06: AACO 10-K](https://www.sec.gov/Archives/edgar/data/2099906/000121390026035679/ea0282881-10k_abony1.htm); filed 2026-03-27; accession 0001213900-26-035679.

- [F07: AACO 10-Q](https://www.sec.gov/Archives/edgar/data/2099906/000121390026087862/ea0300514-10q_abony1.htm); filed 2026-08-11; accession 0001213900-26-087862.

- [F08: AAL 10-K](https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/aal-20251231.htm); filed 2026-02-18; accession 0000006201-26-000014.

- [F09: AAME 10-K](https://www.sec.gov/Archives/edgar/data/8177/000114036126039933/ef20060652_10k.htm); filed 2026-10-16; accession 0001140361-26-039933.

- [F10: AAMI 10-K](https://www.sec.gov/Archives/edgar/data/1748824/000162828026012856/aami-20251231.htm); filed 2026-02-27; accession 0001628280-26-012856.

- [F11: AAOI 10-K](https://www.sec.gov/Archives/edgar/data/1158114/000143774926005875/aaoi20251231_10k.htm); filed 2026-02-26; accession 0001437749-26-005875.

- [F12: AAOI 10-Q](https://www.sec.gov/Archives/edgar/data/1158114/000143774926026278/aaoi20260630_10q.htm); filed 2026-08-06; accession 0001437749-26-026278.

- [F13: AAON 10-K](https://www.sec.gov/Archives/edgar/data/824142/000082414226000005/aaon-20251231.htm); filed 2026-03-02; accession 0000824142-26-000005.

- [F14: AAPL 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm); filed 2025-10-31; accession 0000320193-25-000079.

- [F15: AAPL 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm); filed 2026-07-31; accession 0000320193-26-000020.

- [F16: ABBV 10-K](https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm); filed 2026-02-20; accession 0001551152-26-000008.

- [F17: ABBV 10-Q](https://www.sec.gov/Archives/edgar/data/1551152/000155115226000026/abbv-20260630.htm); filed 2026-08-03; accession 0001551152-26-000026.

- [F18: ABNB 10-K](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm); filed 2026-02-12; accession 0001559720-26-000004.

- [F19: ABNB 10-Q](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000027/abnb-20260630.htm); filed 2026-08-06; accession 0001559720-26-000027.

- [F20: ACA 10-K](https://www.sec.gov/Archives/edgar/data/1739445/000173944526000029/aca-20251231.htm); filed 2026-02-27; accession 0001739445-26-000029.

- [F21: ACA 10-Q](https://www.sec.gov/Archives/edgar/data/1739445/000173944526000067/aca-20260331.htm); filed 2026-05-01; accession 0001739445-26-000067.

Additional source: [AAC submissions history](https://data.sec.gov/submissions/CIK0002128115.json), retrieved 26 October 2026; the sanitized history and its provenance are included.
