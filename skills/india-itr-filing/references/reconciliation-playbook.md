# Reconciliation Playbook

## Contents

1. Recommended order of work
2. Lessons from prior complex cases
3. Working principles
4. Definition of done

## 1. Recommended order of work

Use this order unless the user explicitly needs a narrower slice first.

1. Profile the taxpayer and infer the likely ITR form.
2. Classify return mode and likely schedule family.
3. Build a document manifest, not a giant generic request list.
4. Reconcile `AIS`, `TIS`, `26AS`, TDS, and taxes-paid anchors.
5. Reconcile salary or pension if present.
6. Reconcile house-property items if present.
7. Reconcile business or profession if present.
8. Reconcile capital gains and investment income.
9. Reconstruct foreign income and capital gains only when the profile requires it.
10. Pull prior-year filed-return evidence for carry-forward claims if needed.
11. Compare regimes or optimization scenarios only after the above.
12. Mark the case as filing-ready only after open questions are reduced to non-material items.

## 2. Lessons from prior complex cases

These patterns tend to create avoidable delay and should be handled early.

### Reconciliation before optimization

`26AS`, `AIS`, and `TIS` surfaced taxable interest, dividends, and TDS entries that were broader than broker-only or bank-only views. The right move was to reconcile these first instead of debating tax strategy too early.

### Prior-year filed return beats raw broker memory

A foreign-broker loss summary suggested one carry-forward number, but the filed ITR JSON and CPC intimation supported a different usable `CFL` figure. When carry-forward matters, use the filed-return trail, not a platform summary.

### Foreign broker tax buckets are not filing-ready

The broker's own short-term and long-term buckets were not enough for Indian filing. The case needed lot-level reconstruction, an explicit matching method, and a separate INR conversion step.

### FX method must be documented, not implied

The case improved only after the FX source and the chosen Rule-115 or other official working method were written down in a standalone note with dated rates and sources.

### Keep "directional" and "filing-ready" separate

The working produced useful scenario estimates before all blockers were closed, but only because the documents clearly labeled what was provisional and what was not ready to file.

## 3. Working principles

- Reconcile tax credits and taxable receipts before calculating tax.
- Keep simple cases simple; do not expand the document list unless the profile requires it.
- Keep every meaningful assumption visible.
- Prefer portal or filed-return evidence over memory and screenshots when they conflict.
- Treat `26AS` as the anchor for tax-credit visibility, and use `AIS` or `TIS` as broader information feeds that still need reconciliation.
- Treat unexplained income lines as classification work, not as automatic taxable additions.
- Treat `VDA`, agricultural income, and foreign schedules as their own classification problems, not as leftovers to be stuffed into generic buckets.
- Separate cash-flow truth from tax characterization.
- Prefer a narrow list of explicit blockers over vague uncertainty.

## 4. Definition of done

Call the case filing-ready only when all of the following are true:

- likely ITR form is identified and justified
- all major income buckets are tied to source documents
- TDS, TCS, advance tax, and FTC support are mapped
- capital gains are classified in a defensible way
- carry-forward losses rely on filed-return evidence
- the output target is clear, especially whether the result is a manual-entry workpaper pack or a schema-tested draft JSON
- open questions are either resolved or clearly immaterial
- the final note states what is still assumption-driven, if anything
