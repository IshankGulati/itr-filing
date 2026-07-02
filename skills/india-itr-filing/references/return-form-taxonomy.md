# Return Form Taxonomy

## Contents

1. First-pass taxpayer classification
2. Likely ITR form by case type
3. Full-support versus triage support
4. Common form-specific triggers

## 1. First-pass taxpayer classification

Start here before gathering detailed documents.

### Individual

- likely forms:
  - `ITR-1`
  - `ITR-2`
  - `ITR-3`
  - `ITR-4`

### HUF

- likely forms:
  - `ITR-2`
  - `ITR-3`
  - `ITR-4`

### Firm, LLP, cooperative, estate, business trust, investment fund, many non-company entities

- likely form:
  - `ITR-5`

### Company not claiming section 11 exemption

- likely form:
  - `ITR-6`

### Charitable or religious trusts, political parties, universities, certain exempt entities, and similar cases under section `139(4A)/(4B)/(4C)/(4D)`

- likely form:
  - `ITR-7`

Use the official taxpayer-type pages in [official-links.md](official-links.md) instead of memory when deciding.

## 2. Likely ITR form by case type

### `ITR-1`

Usually consider only when the case is clearly simple and resident-individual only.

Working cues:

- resident individual
- total income within the current `ITR-1` ceiling
- no business or profession
- agricultural income within the current `ITR-1` limit
- no foreign assets or income
- no carry-forward losses
- no director or unlisted-share complication

For the current AY, verify the official page for the exact scope. Current AY material can change details such as number of house properties or whether limited `112A` long-term capital gains are still allowed inside `ITR-1`.

Always confirm against the current official page and current AY utility material because edge eligibility can change.

### `ITR-2`

Usually consider when:

- taxpayer is an individual or HUF
- there is no business or profession income
- the case is too complex for `ITR-1`

Typical triggers:

- capital gains
- agricultural income beyond `ITR-1` simplicity
- foreign assets or foreign income
- multiple complexity flags
- carry-forward loss
- HUF without business or profession income

### `ITR-3`

Usually consider when:

- taxpayer is an individual or HUF
- there is income from business or profession
- the case is not eligible for simplified presumptive `ITR-4`

Typical triggers:

- proprietorship business
- freelance or professional income where simplified presumptive treatment is not being used or not clearly available
- business plus capital gains
- business plus foreign assets or income

### `ITR-4`

Usually consider only when:

- taxpayer is resident eligible person
- total income within the current `ITR-4` ceiling
- presumptive sections like `44AD`, `44ADA`, or `44AE` clearly apply
- agricultural income stays within the current `ITR-4` limit
- no disqualifying complexity flags appear

Do not force `ITR-4` just because a person has consulting income. Confirm presumptive fit, current-law thresholds, digital-receipt conditions, and disqualifiers.

### `ITR-5`, `ITR-6`, `ITR-7`

Use these for triage and collection when the taxpayer is outside the normal individual or HUF path. This skill should still help classify the case and gather documents, but do not assume the same final mapping logic as `ITR-1/2/3/4`.

## 3. Full-support versus triage support

### Full-support target in this skill

- `ITR-1`
- `ITR-2`
- `ITR-3`
- `ITR-4`

### Triage-first target in this skill

- `ITR-5`
- `ITR-6`
- `ITR-7`

For triage-first cases:

- identify the likely form
- collect the relevant source documents
- identify additional statutory forms
- organize workpapers
- state clearly what further extension is needed for JSON generation

## 4. Common form-specific triggers

### Move away from `ITR-1` quickly when you see:

- taxpayer is a `HUF`
- total income beyond the current `ITR-1` ceiling
- business or profession income
- agricultural income above the current `ITR-1` limit
- foreign assets, foreign signing authority, or foreign-source income
- carry-forward or brought-forward loss
- director status
- unlisted shares
- substantial capital-gains complexity

### Move away from `ITR-4` quickly when you see:

- total income beyond the current `ITR-4` ceiling
- clear business or profession complexity outside presumptive treatment
- agricultural income beyond the current `ITR-4` limit
- foreign assets or foreign-source income
- carry-forward loss
- short-term capital-gains complexity
- special-rate or unusual income

### Move toward `ITR-3` when you see:

- professional receipts
- proprietorship books
- business audit forms
- GST-ledger style source data
- `Form 10-IEA` regime decisions linked to business or profession
