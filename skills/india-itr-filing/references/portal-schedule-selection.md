# Portal Schedule Selection

## Contents

1. Four states to keep separate
2. Screen modes
3. Where each artifact belongs
4. Target persona policy
5. Stale-selection handling

## 1. Four states to keep separate

Portal work must separate these ideas:

- `selected`
  - the schedule or screen is currently selected in the portal chooser or draft
- `visible`
  - the portal still shows the screen after routing
- `applicable`
  - the screen is genuinely relevant to the filing position
- `manual`
  - a human or agent actually needs to enter or edit substantive values

Do not collapse these into one yes/no decision.

Examples:

- A screen can be `selected` and `visible` but not `applicable` if stale prefill kept it alive.
- A screen can be `visible` and `applicable` but not substantive manual work if the portal derives the numbers and only needs review.
- A screen can be `mandatory` in portal language without becoming a regular-books data-entry exercise.

## 2. Screen modes

Use these values in `outputs/schedule_inventory.yaml`:

- `manual_input`
  - substantive data entry or row editing is still required
- `review_only`
  - confirm derived or prefilled values rather than attacking it first
- `auto_derived`
  - figures should derive from upstream schedules and only need review
- `mandatory_visible_zero_confirm`
  - the portal shows the screen, but the practical path is usually zero-confirm or minimal review
- `not_applicable_visible`
  - the screen is visible due to stale selection or portal behavior and should be deselected if possible
- `blocked`
  - the screen cannot be completed yet because a real input is missing

## 3. Where each artifact belongs

- `profile.yaml`
  - active `persona_modules`
  - high-level `schedule_candidates`
- `schedule_map.md`
  - schedule readiness at a high level
- `outputs/schedule_inventory.yaml`
  - screen-by-screen truth, including `selected`, `visible`, `applicable`, `screen_mode`, `why_selected`, `deselect_if_possible`, and `evidence`
- `outputs/review_only_schedules.md`
  - quick human-readable list of derived or review-heavy screens
- `outputs/portal-entry-plan.md`
  - canonical route order for live entry after the screen inventory is classified

Keep portal-only screens such as `Part A - Manufacturing Account`, `Part A - Trading Account`, `Part B-TI`, and `Part B-TTI` out of `schedule_candidates`.

## 4. Target persona policy

Target persona:

- salary
- `44ADA` no-books professional income
- domestic investments and capital gains
- foreign assets or income
- FTC
- possible director or unlisted-equity disclosures

Default manual or substantive screens:

- `Schedule Salary`
- `Schedule BP`
- `Schedule CG`
- `Schedule 112A` when relevant
- `Schedule OS`
- `Schedule FSI`
- `Schedule TR`
- `Schedule FA`
- director-company rows
- unlisted-equity rows

Default mandatory-visible or review-heavy screens:

- `Part A - Balance Sheet`
- `Part A - P & L`
- `Part B-TI`
- `Part B-TTI`
- `Tax Paid`
- `Schedule SI`
- `Schedule CYLA`
- `Schedule BFLA`
- `Schedule CFL` only when recomputation truly keeps it alive

Default stale or must-deselect screens unless evidence proves otherwise:

- `Part A - Manufacturing Account`
- `Part A - Trading Account`
- `Part A - OI`
- `Schedule UD`
- `Schedule AL`
- `Schedule AMTC`
- `Schedule 80-IB`
- `Schedule 80-IE`
- other deduction sub-schedules not actually claimed

## 5. Stale-selection handling

Do a schedule-selection audit before live entry:

1. Compare the portal chooser against the composed persona modules.
2. Mark every selected or visible screen in `outputs/schedule_inventory.yaml`.
3. For each inapplicable screen, choose one of:
   - deselect
   - keep visible but `not_applicable_visible`
   - keep visible but `mandatory_visible_zero_confirm` when portal routing forces it
4. Record evidence when an apparently stale screen is actually valid for the case.

Do not call a case portal-ready while screens like `AL`, `AMTC`, `UD`, `80-IB`, or `80-IE` are still selected without explicit justification.
