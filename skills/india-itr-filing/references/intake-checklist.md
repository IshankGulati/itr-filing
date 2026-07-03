# Intake Checklist

## Contents

1. First questions
2. Follow-up question style
3. Profile dimensions
4. Simple versus complex case split
5. Filing-need triage
6. Manifest-first intake
7. Minimum starter artifacts

## 1. First questions

Ask these before asking for documents.

- Which `FY` and `AY` are we working on?
- Is this an `individual`, `HUF`, `firm/LLP`, `company`, or `trust/AOP/BOI` return?
- Is the taxpayer `resident`, `RNOR`, `non-resident`, or unsure?
- Is the user trying to file an original return, belated return, revised return, or updated return?
- Is the target output a filing workpaper pack, a schema-tested draft JSON if feasible, or only a tax estimate?
- If the user is unsure whether filing is mandatory, do we need to verify current filing triggers from official sources first?

## 2. Follow-up question style

Use these rules once the first-pass profile is on paper:

- Open the case with a short "AI tax consultant" persona and a brief warning that mistakes are possible and final positions must be verified before filing.
- Infer answers from the documents first when the evidence is already likely to be in `AIS`, `26AS`, broker statements, `Form 16A`, invoices, or books.
- When a question is still needed, use plain English, say why it matters, and state the current threshold or decision rule only after checking current official sources for the active `FY` or `AY`.
- If a threshold is not yet verified, say that you are checking it instead of pretending the section number itself is understandable.

Sample rewrites:

- Instead of `Is your freelance income run under 44ADA presumptive taxation, or regular books?`
  ask `For your freelance or professional income, are you using the simpler presumptive route where we use a standard profit percentage, or are you keeping normal books and claiming actual expenses? This tells me whether we stay in the presumptive lane or need full business schedules.`
- Instead of `Does your freelance turnover cross the 44AB audit threshold?`
  ask `Are your business or professional receipts anywhere near the current tax-audit trigger for your year? I will verify the exact threshold from current official sources before relying on it, because the rule can change with the facts.`
- Instead of `Did your foreign broker dividends have tax withheld abroad?`
  ask `Your broker dividend statement usually shows this. If you share it, I will infer it from the document; if not, tell me whether tax was withheld abroad on those dividends because that affects foreign-tax-credit and Form 67 work.`
- Instead of `Any house property or crypto/VDA holdings not mentioned yet?`
  ask `Is there any rental or house-property activity, or any crypto or VDA trading, that is not already visible in the documents?`

## 3. Profile dimensions

Use these to keep the request adaptive.

### Income heads

- salary or pension
- house property
- business or profession
- presumptive business or profession
- capital gains
- other sources
- agricultural income
- foreign income or assets
- carry-forward losses
- special-rate income

### Investment buckets

- listed equity or ETF
- mutual funds
- futures, options, or intraday
- bonds or debt products
- property
- ESOP, RSU, or ESPP
- unlisted shares
- foreign broker
- virtual digital assets

### Compliance flags

- director in company
- unlisted equity holder
- foreign asset or signing authority
- foreign tax credit
- audit requirement
- transfer pricing requirement
- regime opt-out or `Form 10-IEA` involvement

### Likely schedule candidates

Build an early schedule list and keep refining it.

- salary
- `HP`
- `BP`
- `CG`
- `OS`
- `VDA`
- `EI`
- `VI-A`
- `SI`
- `AL`
- `FA`
- `FSI`
- `TR`
- TDS on salary
- TDS on other income
- `TCS`
- advance tax or self-assessment tax
- `BFLA`
- `CYLA`
- `CFL`
- `SPI`
- `PTI`
- `AMT`
- `AMTC`

Keep `SI` separate from `SPI` while profiling. They are not interchangeable schedule labels.

## 4. Simple versus complex case split

### Usually simple

- resident individual
- likely `ITR-1`
- total income within the current `ITR-1` ceiling
- salary or pension
- routine bank interest
- agricultural income within `ITR-1` simplicity
- no foreign assets
- no carry-forward losses
- no business or profession

Ask for a minimal set only.

### Usually moderate

- likely `ITR-2`
- capital gains
- agricultural income beyond `ITR-1` simplicity
- multiple properties
- ESOP or RSU
- deductions or reliefs that need source proof

### Usually complex

- likely `ITR-3`, `ITR-5`, `ITR-6`, or `ITR-7`
- business or profession
- presumptive versus normal books decision
- foreign broker or foreign assets
- FTC
- prior-year losses
- audit or transfer pricing forms

## 5. Filing-need triage

If the user is unsure whether filing is required, verify current official triggers before doing deep collection work.

Common reasons this check matters:

- income near or below the basic exemption threshold
- foreign assets or foreign signing authority
- carry-forward loss intention
- high-value trigger conditions under the current law

If this check is unresolved, keep the case in `document_collection_first` or `tax_estimate_only` mode until the filing requirement is clearer.

## 6. Manifest-first intake

Do not require the user to move files into a specific folder tree.

Instead:

- create `document_manifest.csv`
- record absolute paths to local files
- record portal links when the user still needs to download a document
- record what each document is required for
- record a priority like `high`, `medium`, or `low`
- mark each required source as `missing`, `requested`, `received`, `reviewed`, or `normalized`

Use copying into a local workspace only when it actually helps.

## 7. Minimum starter artifacts

Create these immediately:

- `profile.yaml`
- `document_manifest.csv`
- `schedule_map.md`
- `itr_working.md`
- `itr_line_by_line.md`
- `open_questions.md`

For filing-targeted cases also create:

- `outputs/filing-readiness.md`

For JSON-targeted cases also create:

- `outputs/itr-draft.json`
- `outputs/validation-notes.md`
