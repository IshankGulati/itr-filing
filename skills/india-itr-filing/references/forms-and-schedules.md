# Forms And Schedules

## Contents

1. Keep these categories separate
2. Common supporting documents
3. Common additional statutory forms
4. Common schedule candidates by head

## 1. Keep these categories separate

Do not mix these up while profiling the case.

- return form:
  - `ITR-1` to `ITR-7`
- return mode:
  - original
  - belated
  - revised
  - updated
- supporting source documents:
  - `Form 16`
  - `Form 16A`
  - `AIS`
  - `TIS`
  - `26AS`
  - broker reports
  - loan certificates
- additional statutory forms:
  - `Form 10E`
  - `Form 10-IEA`
  - `Form 67`
  - `Form 3CA-3CD`
  - `Form 3CB-3CD`
  - `Form 3CEB`
- schedules inside the return or utility:
  - `CG`
  - `OS`
  - `HP`
  - `BP`
  - `VDA`
  - `EI`
  - `VI-A`
  - `SI`
  - `AL`
  - `FA`
  - `FSI`
  - `TR`
  - TDS schedules
  - `TCS`
  - `IT`
  - `BFLA`
  - `CYLA`
  - `CFL`
  - `SPI`
  - `PTI`
  - `AMT`
  - `AMTC`

## 2. Common supporting documents

### Salary or pension

- `Form 16`
- employer payroll summary
- payslips
- pension statement
- `AIS`
- `TIS`
- `26AS`

### House property

- loan interest certificate
- municipal-tax receipts
- rent receipts
- purchase or sale deed when relevant
- `Form 26QB` and `Form 16B` when property `TDS` applies
- stamp-duty valuation support where section `50C` risk exists

### Business or profession

- invoices
- receipt ledger
- books or accounting export
- bank trail
- `Form 16A`
- `AIS`
- `26AS`

### Capital gains and investment income

- broker capital-gains report
- tax P&L
- mutual-fund capital-gains statement
- CAS
- contract notes
- dividend and interest statements
- exchange or wallet export for `VDA` if relevant

### Foreign assets or income

- foreign broker annual statement
- transaction export
- withholding report
- prior-year foreign-schedule support

### Agricultural or exempt income

- land records or crop-sale support where relevant
- agricultural-income computations
- exempt-income support for `EI` classification where relevant

## 3. Common additional statutory forms

Use these only when the profile says they matter.

- `Form 10E`
  - relief claim for salary arrears or similar cases
- `Form 10-IEA`
  - business or profession cases where regime option history matters
- `Form 67`
  - foreign tax credit support
- `Form 3CA-3CD` or `Form 3CB-3CD`
  - tax-audit cases
- `Form 3CEB`
  - transfer-pricing cases

Always confirm the current AY instructions and portal workflow before treating any additional form as complete.
Do not reuse old listed-equity rate assumptions blindly. For current AY listed-equity, `112A`, and `111A` cases, confirm current official utility or instructions before computing tax.

## 4. Common schedule candidates by head

These are working labels to help organize the case before final JSON mapping.

### Salary or pension

- salary schedule
- TDS salary schedule

### House property

- `HP`

### Business or profession

- `BP`
- profit and loss or balance-sheet support where the chosen utility requires it

### Capital gains

- `CG`
- `VDA` for virtual digital assets
- `BFLA`
- `CYLA`
- `CFL`

### Other sources

- `OS`
- `TCS`
- `IT`

### Deductions and reliefs

- `VI-A`

### Agricultural or exempt income

- `EI`

### Special-rate or threshold-driven items

- `SI`
- `AL` when the current `AY` thresholds are crossed

Keep `SI` separate from `SPI`: `SI` is the special-rate income schedule, while `SPI` remains the clubbing or specified-person schedule.

### Foreign assets or income

- `FA`
- `FSI`
- `TR`

### Credits, clubbing, and pass-through

- TDS on salary
- TDS on other income
- `SPI`
- `PTI`

### Advanced or niche items

- `AMT`
- `AMTC`

If a case is only a tax estimate, the schedule list can stay provisional. If the case is targeting a utility draft or portal-entry pack, the schedule list must become explicit before the final handoff.
If the case is targeting a portal-entry pack, schedule-level prose is not enough. The handoff should also include explicit field-level answers for branch-driving questions and row-ready data for portal tables such as unlisted shares, capital gains, director-company disclosures, and foreign assets when those sections are in scope.
Do not collapse `VDA` into normal capital gains or other sources. Treat it as a dedicated special-rate area and confirm current-law restrictions on deductions, set-off, and carry-forward before computing it.
