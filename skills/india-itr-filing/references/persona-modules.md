# Persona Modules

## Contents

1. Why persona modules exist
2. Composition rules
3. Seed module catalog
4. Target composite persona

## 1. Why persona modules exist

Use persona modules to keep portal preparation adaptive and fast.

The skill already profiles the filer at a high level, but portal work now needs a second layer:

- which modules are active for this case
- which schedules they pull into scope
- which portal screens stay manual
- which portal screens stay review-only, auto-derived, or zero-confirm
- which stale selections should be removed before live entry

Do not treat `ITR-3` as a single business persona. A salary-plus-`44ADA` no-books professional with Indian and foreign investments is not the same as a regular-books business filer.

## 2. Composition rules

- Keep `schedule_candidates` high-level in `profile.yaml` and `schedule_map.md`.
- Record active modules in `profile.yaml > persona_modules`.
- Use `outputs/schedule_inventory.yaml` for screen-level truth.
- Compose modules additively. A case can activate salary, `44ADA`, domestic capital gains, foreign assets, FTC, and disclosure modules at the same time.
- When two modules touch the same screen, prefer the stricter portal policy.
  - Example: if one module makes a screen manual and another marks it review-only, verify the real branch driver before downgrading it.
- A screen can be `selected` or `visible` without being substantively `applicable`.

## 3. Seed module catalog

### `salary_basic`

- triggers:
  - salary or pension income
- likely impact:
  - keeps salary screens in scope across `ITR-1`, `ITR-2`, or `ITR-3`
- common schedules:
  - salary
  - TDS salary when actually relevant
- common portal treatment:
  - `Schedule Salary` stays manual

### `professional_44ada_no_books`

- triggers:
  - professional receipts returned on a presumptive `44ADA` basis
  - no regular books path
- likely impact:
  - often pushes the case into `ITR-3` while still keeping business screens on a fast path
- common schedules:
  - `BP`
- common stale cleanup:
  - `Part A - Manufacturing Account`
  - `Part A - Trading Account`
  - `Part A - OI`
  - `Schedule UD`
- common portal treatment:
  - `BP` stays manual
  - Balance Sheet and `P&L` are often mandatory-visible but zero-confirm
  - `Part B-TI`, `Part B-TTI`, `Tax Paid`, `SI`, `CYLA`, `BFLA`, and conditional `CFL` stay review-heavy or derived

### `domestic_cap_gains`

- triggers:
  - domestic broker or mutual-fund gains
- likely impact:
  - keeps `CG` in scope and often activates downstream special-rate or set-off review
- common schedules:
  - `CG`
  - `SI`
  - `CYLA`
  - `BFLA`
  - `CFL`

### `domestic_112a`

- triggers:
  - listed equity or equity-oriented fund `LTCG` under `112A`
- likely impact:
  - extends `CG` handling with row-heavy `112A` work
- common schedules:
  - `CG`
  - `SI`
- common portal treatment:
  - `Schedule 112A` stays substantive
  - upload support is scaffold-only until a real template is available

### `domestic_other_sources`

- triggers:
  - domestic interest, dividend, or similar receipts
- likely impact:
  - keeps `OS` in scope and may activate TDS-on-other-income review
- common schedules:
  - `OS`
  - TDS other

### `foreign_assets`

- triggers:
  - foreign holdings or signing-authority answers
- likely impact:
  - activates `FA`
- common schedules:
  - `FA`

### `foreign_income`

- triggers:
  - foreign dividends, interest, or other foreign-source income
- likely impact:
  - activates `FSI`
- common schedules:
  - `FSI`

### `foreign_tax_credit`

- triggers:
  - foreign withholding or FTC claim
- likely impact:
  - activates `TR` and `Form 67` coordination
- common schedules:
  - `TR`
- common stale cleanup:
  - `AMTC` should stay out unless real AMT-credit history exists

### `prior_year_loss_setoff`

- triggers:
  - prior-year loss evidence
- likely impact:
  - activates `BFLA` and sometimes `CFL`
- common schedules:
  - `BFLA`
  - `CFL`

### `director_disclosure`

- triggers:
  - director-in-company flag
- likely impact:
  - activates Part A disclosure rows and often disqualifies simple return paths
- common portal treatment:
  - director-company rows stay manual

### `unlisted_equity_disclosure`

- triggers:
  - unlisted shares held at any time during the year
- likely impact:
  - activates row-level share disclosures and often disqualifies simple presumptive routing
- common stale cleanup:
  - `AL` is separate and should not be dragged in just because unlisted-equity rows exist
- common portal treatment:
  - unlisted-equity rows stay manual

## 4. Target composite persona

The first-class optimization target for this refactor is:

- resident individual
- salary
- `44ADA` no-books professional income
- domestic capital gains
- domestic other sources
- foreign assets
- foreign income
- foreign tax credit
- possible director or unlisted-equity disclosures

Recommended active module set:

- `salary_basic`
- `professional_44ada_no_books`
- `domestic_cap_gains`
- `domestic_112a` when actually relevant
- `domestic_other_sources`
- `foreign_assets`
- `foreign_income`
- `foreign_tax_credit`
- `prior_year_loss_setoff` when real prior-year losses exist
- `director_disclosure` when applicable
- `unlisted_equity_disclosure` when applicable

Use [portal-schedule-selection.md](portal-schedule-selection.md) for the screen policy and [itr3-44ada-no-books-playbook.md](itr3-44ada-no-books-playbook.md) for the live portal fast path.
