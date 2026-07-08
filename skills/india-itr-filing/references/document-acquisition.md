# Document Acquisition

## Contents

1. Portal documents
2. Salary and pension
3. House property
4. Business or profession
5. Capital gains and investments
6. Other sources and deductions
7. Foreign assets and income
8. Plain-English follow-up asks
9. Practical guidance for scattered documents

## 1. Portal documents

These should be gathered early in almost every case.
Verify current portal labels and menu paths before quoting them as exact steps. If a label or deep link has moved, re-start from the portal home, help area, or downloads page.

### `26AS`

- Current common portal path:
  - `Login > e-File > Income Tax Return > View Form 26AS`
- Use for:
  - TDS or TCS visibility
  - taxes paid
  - reconciliation anchor

### `AIS`

- Current common portal path:
  - `Login > AIS`
- Use for:
  - broader income and transaction visibility
  - SFT information
  - demand or refund context
  - foreign-information flags

### `TIS`

- Current common portal path:
  - `Login > AIS > TIS`
- Use for:
  - cleaner summary view of income buckets alongside `AIS`
  - first-pass interest, dividend, and other-source reconciliation
  - spotting mismatches that need deeper `AIS` or document review

### Prior-year return artifacts

Common sources:

- e-Filing portal filed-return downloads
- previously saved JSON
- acknowledgement copy
- CPC intimation

Use for:

- carry-forward losses
- prior regime elections
- prior foreign schedules
- revised-return continuity
- updated-return or correction continuity

## 2. Salary and pension

### Common source documents

- `Form 16`
- employer payroll summary
- final payslips
- pension statement
- `AIS`
- `26AS`

### Common ways users obtain them

- employer HR or payroll portal
- employer finance team
- pension disbursing bank or pension portal

### Useful related forms

- `Form 12BB`
- `Form 10E`

## 3. House property

### Common source documents

- home loan interest certificate
- principal repayment certificate
- rent receipts
- rent agreement
- municipal tax receipts
- sale deed or purchase deed when property was transacted
- `Form 26QB` and `Form 16B` when buyer-side `TDS` applies
- stamp-duty valuation support when section `50C` risk exists

### Common ways users obtain them

- lender loan-account portal
- builder or registrar records
- personal records for rent and municipal taxes

Use only when the profile actually includes house-property income, loss, or related deduction claims.

## 4. Business or profession

### Common source documents

- invoices
- receipt ledger
- bank-credit trail
- `Form 16A`
- books or accounting export
- GST returns if relevant
- audit reports if applicable

### Common ways users obtain them

- billing system
- accounting software
- bank statements
- client-issued `Form 16A`

### Useful related forms

- `Form 10-IEA` for regime position in business or profession cases
- `Form 3CA-3CD`
- `Form 3CB-3CD`
- `Form 3CEB`

When clarifying presumptive treatment or audit risk:

- infer from invoices, books, `Form 16A`, and bank trail before asking a follow-up
- do not ask only `Does your turnover cross 44AB?`
- instead ask in plain English and say why it matters
- check the current official threshold or decision rule for the active `FY` or `AY` before quoting it back

## 5. Capital gains and investments

### Listed equity, ETF, F&O, intraday

Common source documents:

- broker capital-gains report
- tax P&L
- tradebook
- contract notes
- holding statement

Common ways users obtain them:

- broker back office
- annual tax reports from broker portal
- depository CAS or holding statement when the broker report is incomplete

### Mutual funds

Common source documents:

- capital-gains statement
- account statement
- consolidated account statement

Common ways users obtain them:

- MFCentral:
  - [https://www.mfcentral.com/](https://www.mfcentral.com/)
- CAMS:
  - [https://www.camsonline.com/](https://www.camsonline.com/)
- KFintech mutual fund investor services:
  - [https://mfs.kfintech.com/](https://mfs.kfintech.com/)
- fund-house portal
- depository CAS when relevant

### Property capital gains

Common source documents:

- purchase deed
- sale deed
- stamp-duty evidence
- official stamp-duty valuation where relevant
- improvement-cost evidence
- loan-closure evidence when relevant
- `Form 26QB`
- `Form 16B`

Review whether deeming-value provisions like section `50C` may matter before trusting sale consideration at face value.
If the property is business inventory rather than a capital asset, check whether section `43CA` style treatment is relevant instead of assuming the case belongs only in capital gains.

### ESOP, RSU, ESPP, unlisted shares

Common source documents:

- employer stock plan statements
- vesting reports
- sale confirmations
- broker statements
- payroll tax-withholding support
- valuation support when unlisted-share rules or section `50CA` issues may matter

### Virtual digital assets

Common source documents:

- exchange trade export
- transaction ledger
- wallet transfer history where relevant
- realized-gain report if available

Common ways users obtain them:

- exchange tax center
- full transaction CSV export
- wallet explorer or self-maintained ledger when exchange export is incomplete

Common working caution:

- do not map `VDA` into generic capital-gains treatment without verifying the dedicated current-law rules

### Foreign broker investments

Common source documents:

- annual activity statement
- transaction export
- dividend report
- interest report
- withholding-tax report
- prior-year opening-position statement

## 6. Other sources and deductions

### Interest and dividends

Common source documents:

- bank interest certificate
- FD interest certificate
- savings-account statements
- broker dividend statements
- EPF or provident-fund interest support when relevant
- `AIS`

### Deductions and reliefs

Common source documents:

- life insurance receipts
- PPF passbook or statement
- ELSS statement
- NPS transaction statement
- health insurance premium receipts
- donation receipts
- education-loan interest certificate

Gather these only if the user is actually testing or claiming the deduction.
If you are using the default starter scaffold, keep deduction proofs inside `inputs/investments/` with the related investment or tax-saving evidence instead of creating a separate `inputs/deductions/` folder.

## 7. Foreign assets and income

Common source documents:

- foreign broker annual statements
- transaction exports
- foreign tax withholding reports
- bank statements for foreign income receipts if relevant
- prior `FA`, `FSI`, `TR`, or `Form 67` workpapers if available

Read [broker-playbooks.md](broker-playbooks.md) for a reusable way to ask for the right exports even when the skill does not yet have a provider-specific mini-guide.

When FX conversion is needed:

- search the workspace for local `SBI TTBR` or `Rule 115` workpapers before creating new ones
- reuse existing documented local files where reliable
- check dividend and withholding reports before asking the user whether foreign tax was withheld

## 8. Plain-English follow-up asks

Use these patterns when a follow-up is still needed after inspecting available documents.

- `For your freelance or professional income, are you using the simpler presumptive route where we use a standard profit percentage, or are you keeping normal books and claiming actual expenses? This helps decide whether we stay in the simplified path or need full business schedules.`
- `Are your business or professional receipts anywhere near the current tax-audit trigger for your year? I will confirm the exact threshold from current official sources before relying on it, because that affects whether audit reports belong in the request pack.`
- `Your broker dividend statement usually shows this. Should I infer foreign tax withholding from that report, or do you already know that tax was withheld abroad on those dividends?`
- `Is there any rental or house-property activity, or any crypto or VDA trading, that is not already visible in the documents?`

## 9. Practical guidance for scattered documents

If a user has documents spread across many folders:

- do not require renaming or relocating everything
- capture the absolute path or download URL in `document_manifest.csv`
- mark what the document is required for and how urgent it is
- ask for only the next high-value missing document
- normalize data into local workpapers after review

If a starter scaffold helps and the user does not already have a preferred structure, keep it under `inputs/`:

- `inputs/salary/`
- `inputs/business/`
- `inputs/investments/` for capital-gains reports, mutual-fund statements, and deduction proofs
- `inputs/foreign/`
- `inputs/prior_year/`
- `inputs/portal_anchors/`

Use `inputs/portal_anchors/` specifically for portal-only observations gathered during live drafting:

- screenshots of portal states or warnings
- copied labels when the portal wording drifts from the documented path
- notes on validated bank accounts or refund-account choices
- snapshots of prefilled tables before editing
- page-specific resume notes for interrupted sessions
