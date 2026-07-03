---
name: india-itr-filing
description: Profile an Indian income-tax return case, choose the likely ITR form, request only the relevant documents, guide the user to official or standard download sources, reconcile income head by head, and produce a filing workpaper pack for the current AY. When the current AY offline utility, schema, and validations are actually available and used, also produce a schema-tested ITR draft JSON. Use for Indian ITR work covering residents, non-residents, HUFs, business or profession cases, capital gains, mutual funds, broker statements, foreign investments held by Indian taxpayers, foreign assets or income, foreign tax credit, deductions, or carry-forward losses.
---

# India Itr Filing

## Overview

Start by profiling the taxpayer, not by asking for every possible document. Keep the workflow adaptive: simple salary-only cases should stay simple, while capital-gains, business, foreign-asset, or carry-forward-loss cases should expand only as needed.

The end goal is not just a tax estimate. The default end goal is a filing workpaper pack with a clear schedule map, source trail, and blocker list. Only promise a utility-compatible JSON draft when the current AY utility, schema, and validations are actually available and the case is materially complete.

Open each new engagement with a short persona and caution line such as: "I'm an AI tax consultant helping you structure this Indian ITR case. I can make mistakes, so we should verify final filing positions against current official sources before you file."

Infer from source documents before asking avoidable follow-up questions. When a question is still needed, ask it in plain English, explain why it matters, and state the current threshold or decision rule after checking the active-law source for the relevant `FY` or `AY` instead of naming only a section number.

## Scope

- Default full-support target:
  - `ITR-1`
  - `ITR-2`
  - `ITR-3`
  - `ITR-4`
- Triage-first target:
  - `ITR-5`
  - `ITR-6`
  - `ITR-7`

For `ITR-5/6/7`, this skill should still profile the user, identify the correct form family, collect the right documents, and prepare workpapers. Do not assume the same downstream mapping as a personal `ITR-1/2/3/4` case unless the user explicitly wants that extension.

Foreign scope in this skill is limited to Indian taxpayers who hold foreign investments or receive foreign income. This skill is not a generic multi-country tax engine and does not attempt to prepare non-Indian tax returns.

## Quick Start

1. Read [references/official-links.md](references/official-links.md).
2. Read [references/return-form-taxonomy.md](references/return-form-taxonomy.md).
3. Read [references/intake-checklist.md](references/intake-checklist.md).
4. Read [references/case-buckets.md](references/case-buckets.md) if you need a first-pass archetype for the user.
5. Read [references/forms-and-schedules.md](references/forms-and-schedules.md) before mapping work into a filing-ready JSON.
6. Read [references/broker-playbooks.md](references/broker-playbooks.md) when broker or platform-specific exports matter.
7. If a local workspace would help, run `scripts/bootstrap_case.py <case-root> --fy FY_2025-26 --ay "AY 2026-27" --tier simple` for a lean starter or switch `--tier` / `--filing-goal` when the case is more complex or JSON-targeted.
8. If the user already has files scattered across different folders, do not force a folder migration. Keep a manifest with absolute paths instead.

## Workflow

## 1. Profile the taxpayer first

Create or update `profile.yaml` before requesting documents.

Capture at least:

- `fy`
- `ay`
- `return_mode`
  - `original`
  - `belated`
  - `revised`
  - `updated`
- `filing_goal`
  - `return_workpaper_pack`
  - `json_draft_if_feasible`
  - `tax_estimate_only`
  - `document_collection_first`
- `case_tier`
  - `simple`
  - `moderate`
  - `complex`
- `taxpayer_type`
  - `individual`
  - `huf`
  - `firm_or_llp`
  - `company`
  - `aop_boi_trust_ajp`
- `residential_status`
  - `resident`
  - `rnor`
  - `non_resident`
  - `unknown`
- `likely_itr_form`
- `regime_position`
  - `default_new`
  - `consider_old`
  - `business_opt_out_involved`
  - `unknown`
- `compliance_flags`
  - `director_in_company`
  - `unlisted_equity_holder`
  - `foreign_signing_authority`
  - `foreign_tax_credit`
  - `audit_requirement`
  - `transfer_pricing`
- `income_heads`
  - `salary_or_pension`
  - `house_property`
  - `business_or_profession`
  - `presumptive_business_or_profession`
  - `capital_gains`
  - `other_sources`
  - `agricultural_income`
  - `foreign_income_or_assets`
  - `carry_forward_losses`
  - `special_rate_income`
- `investment_buckets`
  - `listed_equity_or_etf`
  - `mutual_funds`
  - `fno_or_intraday`
  - `bonds_or_debt`
  - `property`
  - `esop_rsu_espp`
  - `unlisted_shares`
  - `foreign_broker`
  - `vda`
- `schedule_candidates`
  - `salary`
  - `hp`
  - `bp`
  - `cg`
  - `os`
  - `vda`
  - `ei`
  - `via`
  - `si`
  - `al`
  - `fa`
  - `fsi`
  - `tr`
  - `tds_salary`
  - `tds_other`
  - `tcs`
  - `it_paid`
  - `bfla`
  - `cyla`
  - `cfl`
  - `spi`
  - `pti`
  - `amt`
  - `amtc`

Do not ask for broker exports, foreign schedules, or audit reports unless the profile says they matter.
Keep `si` separate from `spi`: `si` tracks special-rate income, while `spi` remains the clubbing or specified-person schedule.
If the user is unsure whether they need to file at all, verify current mandatory-filing triggers from official sources before collecting a large document pack.

## 2. Choose the likely ITR form

Use [references/return-form-taxonomy.md](references/return-form-taxonomy.md) and the official portal links behind it.

Working rule:

- `ITR-1` for very simple resident-individual cases only. For the current AY, confirm the official page for total-income ceiling, agricultural-income limit, house-property scope, and any limited `112A` capital-gains allowance.
- `ITR-2` when there is no business or profession income but there are capital gains, agricultural income beyond `ITR-1` simplicity, foreign assets, multiple complexity flags, or other `ITR-1` disqualifiers.
- `ITR-3` when there is business or profession income outside presumptive `ITR-4` simplicity.
- `ITR-4` only when presumptive eligibility clearly fits, the current AY thresholds and digital-receipt conditions are checked, and no disqualifying complexity is present.

Also distinguish the return mode:

- original or belated return
- revised return
- updated-return path

If `return_mode` is `updated`, treat it as a legally constrained path, not just another filing mode. Before proceeding, verify the current ITR-U rules from official sources and current utility material. An updated return is generally not available to reduce total tax liability, create or increase a refund, or convert the case into a loss return, and it usually carries additional-tax implications. Do not promise filing readiness until current-law eligibility and current utility support are confirmed.

If the official portal summary and another portal summary appear to conflict, do not hard-code the edge case. Cross-check the current AY download page, current schema, current validation rules, and current form instructions before finalizing.

## 3. Request only the relevant documents

Read [references/document-acquisition.md](references/document-acquisition.md).
Use [references/case-buckets.md](references/case-buckets.md) to keep the request matched to the user's archetype.

Build a tailored request pack from the profile:

- simple salary case:
  - `Form 16`
  - `AIS`
  - `TIS`
  - `26AS`
  - bank interest statements if applicable
- salary plus capital gains:
  - above plus broker or mutual-fund gain reports
- profession or business:
  - above plus invoices, receipts, bank trail, `Form 16A`, books, audit or presumptive support as relevant
- foreign or carry-forward case:
  - above plus foreign broker statements, transaction exports, withholding support, prior-year filed return evidence

If you bootstrap a local workspace, keep the next-request pack in `document_request.md` so the document ask stays tied to the current profile instead of turning into a generic checklist.
If a starter folder tree would help, keep it under `inputs/` with `salary`, `business`, `investments`, `foreign`, `prior_year`, and `portal_anchors`. Use `inputs/investments/` for both capital-gains artifacts and deduction proofs; do not split them into separate `capital_gains/` and `deductions/` folders unless the user explicitly asks.

If you hit a broker-export quirk, a portal navigation that drifted from the documented path, or any other operational surprise mid-case, log it in `case_learnings.md` as it happens rather than losing it. If the same quirk recurs across cases, promote it into [references/reconciliation-playbook.md](references/reconciliation-playbook.md)'s "Lessons from prior complex cases" section so future cases benefit without needing to rediscover it.

If the user asks where to get a document, point them to the relevant official or standard portal from [references/document-acquisition.md](references/document-acquisition.md).

## 4. Work with scattered files through a manifest

Do not assume the user has a perfect folder tree.

Maintain `document_manifest.csv` with:

- `head`
- `subhead`
- `source_name`
- `portal_or_provider`
- `required_for`
- `priority`
- `available`
- `path_or_link`
- `coverage`
- `status`
- `notes`

If the user already has a local directory structure they like, work with it. If not, bootstrap a neutral workspace and keep absolute paths in the manifest.

## 5. Reconcile head by head

Read [references/reconciliation-playbook.md](references/reconciliation-playbook.md).

Use this order unless a narrower request makes more sense:

1. taxpayer profile and likely form
2. return mode and likely schedule set
3. `AIS`, `TIS`, `26AS`, taxes paid, and TDS anchors
4. salary or pension
5. house property
6. business or profession
7. capital gains and investment income
8. other sources
9. deductions, reliefs, regime choice
10. foreign assets, foreign income, and foreign tax credit
11. carry-forward losses and prior-year dependencies

Keep every figure tagged as:

- `raw`
- `reconciled`
- `provisional`
- `filing_ready`

## 6. Handle foreign and FX work carefully

Read [references/foreign-income-capital-gains.md](references/foreign-income-capital-gains.md) whenever foreign brokers, foreign assets, foreign income, or foreign tax credit appear.
Read [references/broker-playbooks.md](references/broker-playbooks.md) when the user needs help locating exports from a broker or investment platform.

Before creating new FX workpapers:

- search the workspace for existing `rule115`, `ttbr`, `sbi_tt`, or similar files
- search any checked-in local helper outputs or workpapers before assuming a fresh lookup is needed
- reuse existing local workpapers where they are reliable and documented
- cite the exact local file used for the FX method
- if exact dated rates are available locally, use them before asking whether provisional precision is acceptable
- before presenting a detailed FX-converted gain as final, compare it against a rough independent estimate and re-check the method if the gap is unexpectedly large

Do not silently switch FX methods mid-case.
Do not assume the same FX method fits every foreign-income type or every treaty situation.
Do not present provisional FX precision as exact.

For a resident selling foreign shares, treat the INR conversion as a genuine fork, not a settled rule: per-leg conversion (mainstream, keeps rupee movement in the gain) and single-rate-on-net-gain give materially different figures. Name the method, cite the source, and when they diverge materially present both and let the user or their CA choose. Do not flip methods just because a prior tool or the user reported a different number, and do not treat a resident's rupee-depreciation gain as an error to remove. See [references/foreign-income-capital-gains.md](references/foreign-income-capital-gains.md) section 4.

`Schedule FA` is calendar-year and lists holdings, not this year's trades. Never read an `FA` line as a current-`FY` sale without cross-checking the transaction export and prior-year filed return; a platform `FA` draft can carry closed or stale positions. Treat a platform-vs-export mismatch as reconciliation work, not as a defect in the user's records.

## 7. Produce a filing package, and a JSON draft only when feasible

The default final artifact should be a filing workpaper pack that can support portal entry or utility entry for the current AY. When the official current AY offline utility, schema, and validations are available and actually used, add a schema-tested draft JSON as a secondary artifact.

Minimum output set:

- `profile.yaml`
- `document_manifest.csv`
- `schedule_map.md`
- `itr_working.md`
- `itr_line_by_line.md`
- `open_questions.md`
- `case_learnings.md`
- `outputs/filing-readiness.md`

Conditional JSON set, only when the current AY utility, schema, and validations were actually used:

- `outputs/itr-draft.json`
- `outputs/validation-notes.md`

Use the official downloads page, offline-utility manual, and current AY schema from [references/official-links.md](references/official-links.md) whenever the form family is `ITR-1/2/3/4`.

Only call `outputs/itr-draft.json` schema-tested when:

- the current AY utility or schema was actually accessed
- the current validation material was checked
- all material schedules in scope were populated or explicitly blocked
- `outputs/validation-notes.md` records what was validated and what was not

If a required schedule cannot be built because data is missing:

- stop short of inventing values
- mark the draft as blocked
- keep `open_questions.md` crisp and actionable

## Guardrails

- Prefer official Income Tax portal guidance over news articles, explainers, or forum posts.
  - Anti-pattern: "A tax-prep blog explains this clearly, so I'll cite it as the rule." Blogs and forums can lag or misstate a current-AY threshold; use them only to orient, then confirm against the official portal.
  - Anti-pattern: "The official page is verbose, so I'll rely on the forum summary instead of reading it." If the primary source is harder to parse, slow down and verify it; difficulty is not a license to replace it.
- Use third-party portals only as document-acquisition channels, not as tax-law authority.
  - Anti-pattern: "The broker portal's help page says this gain is long-term, so that's final." A download source is not a tax-law source, even when it sounds authoritative.
  - Anti-pattern: "This filing platform auto-classified the deduction, so I can treat its explanation as the governing rule." Software hints can help you navigate, but they do not replace the official law or portal instructions for the current AY.
- Do not assume a folder layout.
  - Anti-pattern: "Most users keep documents in a `Documents/Tax` folder, so I'll look there first without asking." Ask or check the manifest; do not guess a path convention onto someone else's files.
  - Anti-pattern: "I didn't find the PDF in the first likely folder, so the user probably doesn't have it." Missing from your guessed location is not missing from the case; update the manifest or ask for the actual path.
- Do not request every possible tax proof up front.
  - Anti-pattern: "I am not sure what matters yet, so I'll ask for salary proofs, all broker exports, foreign statements, audit reports, and property papers now just in case." Unknown scope is a reason to profile first, not to over-collect everything.
  - Anti-pattern: "Schedule `FA` might apply, so I should request foreign-broker exports from every filer before I know whether they hold foreign assets." Only ask for foreign or niche documents when the profile says those schedules are plausibly in scope.
- Do not trust broker tax buckets blindly for Indian capital-gains treatment.
  - Anti-pattern: "The broker's own short-term/long-term split looked reasonable, so I used it directly." Broker buckets are frequently built for a different tax jurisdiction or a different lot-matching method than Indian law requires; see [references/reconciliation-playbook.md](references/reconciliation-playbook.md) for a concrete case where this cost real rework.
  - Anti-pattern: "The platform already tagged everything as equity `LTCG` or `STCG`, so lot reconstruction would just duplicate work." A broker label can still be wrong for Indian filing; reconstruct or verify when the treatment matters.
- Do not treat a portal auto-fill as final truth without source reconciliation.
  - Anti-pattern: "The pre-filled AIS number matches roughly what I expected, so I'll keep it as-is." Roughly matching is not reconciled; trace it to a source document before accepting it.
  - Anti-pattern: "The portal imported the TDS line from `26AS`, so I do not need to compare it against the certificate or challan trail." Auto-fill is a starting point; reconciliation still requires source-level confirmation.
- Do not present an estimate as an upload-ready JSON.
  - Anti-pattern: "The numbers are provisional, but the JSON already validates against the schema, so I'll call it filing-ready." Schema validity is necessary, not sufficient; provisional figures still block a filing-ready label.
  - Anti-pattern: "The user only wants a directional answer, but I may as well hand over the JSON draft now because it looks complete enough." Directional guidance and filing artifacts are different deliverables; keep the estimate separate until blockers are closed.
- Do not promise a portal-uploadable file unless the current AY utility or schema has actually been used and validation status is recorded.
  - Anti-pattern: "Last AY's schema structure is probably still correct, so I don't need to re-check this AY's utility." Schemas and validation rules change between assessment years; confirm the current one every time, and record what was checked in `outputs/validation-notes.md`.
  - Anti-pattern: "The utility download page looked familiar a few months ago, so I can say this draft is uploadable without re-opening it." Familiarity is not current-year validation; confirm the exact AY utility and write down what was tested.

## References

- Read [references/official-links.md](references/official-links.md) for primary-source portal links.
- Read [references/return-form-taxonomy.md](references/return-form-taxonomy.md) for form selection and support boundaries.
- Read [references/intake-checklist.md](references/intake-checklist.md) for profiling questions and manifest-driven intake.
- Read [references/case-buckets.md](references/case-buckets.md) for first-pass user archetypes.
- Read [references/document-acquisition.md](references/document-acquisition.md) for common document download paths by income head.
- Read [references/forms-and-schedules.md](references/forms-and-schedules.md) for common statutory forms, source documents, and likely schedules.
- Read [references/broker-playbooks.md](references/broker-playbooks.md) for broker and platform export patterns and extension guidance.
- Read [references/reconciliation-playbook.md](references/reconciliation-playbook.md) for ordering, anti-patterns, and definition of done.
- Read [references/foreign-income-capital-gains.md](references/foreign-income-capital-gains.md) for lot reconstruction, FX, FTC, and prior-year loss handling.

## Scripts

- Run `scripts/bootstrap_case.py` to create a neutral case workspace with profile, manifest, workpaper, and request templates. Use `--tier simple|moderate|complex` and `--filing-goal return_workpaper_pack|json_draft_if_feasible|tax_estimate_only|document_collection_first` so simple cases stay lean and JSON scaffolding appears only when it is actually the goal.
- Run `scripts/check_schedule_consistency.py` after editing the `schedule_candidates` enum in this file or [references/forms-and-schedules.md](references/forms-and-schedules.md). It fails loudly if the two drift out of sync instead of leaving a stale or undocumented id in place.
