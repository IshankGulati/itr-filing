# ITR-3 44ADA No-Books Playbook

## Contents

1. When this playbook applies
2. What this persona is not
3. Fast-path screen policy
4. Screens to deselect or challenge first
5. Practical portal route

## 1. When this playbook applies

Use this playbook when the filer is broadly:

- a resident individual
- carrying salary and/or professional income
- returning professional receipts on a presumptive `44ADA` basis
- not using a regular-books business path
- also carrying domestic investments, foreign holdings, or FTC complexity that pushes the case into `ITR-3`

This playbook is especially useful when `ITR-3` is being used because of disclosure or complexity flags, not because the filer genuinely has a normal books-driven business return.

## 2. What this persona is not

Do not mistake this persona for:

- a manufacturing or trading business
- a regular-books profit-and-loss and balance-sheet case
- an audit-driven business return unless facts actually prove it
- an AMT or AMTC case by default
- an `AL` case just because the portal surfaced the screen

The portal may still show business-heavy or threshold-heavy screens. That is a routing fact, not proof that those screens are substantively in scope.

## 3. Fast-path screen policy

Manual or substantive by default:

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

Mandatory-visible or review-heavy by default:

- `Part A - Balance Sheet`
- `Part A - P & L`
- `Part B-TI`
- `Part B-TTI`
- `Tax Paid`
- `Schedule SI`
- `Schedule CYLA`
- `Schedule BFLA`
- `Schedule CFL` only if recomputation truly leaves a carry-forward result

Selected but usually wrong unless proved otherwise:

- `Part A - Manufacturing Account`
- `Part A - Trading Account`
- `Part A - OI`
- `Schedule UD`
- `Schedule AL`
- `Schedule AMTC`
- `Schedule 80-IB`
- `Schedule 80-IE`

## 4. Screens to deselect or challenge first

Before entering figures:

1. audit the portal chooser
2. mark stale or suspicious screens in `outputs/schedule_inventory.yaml`
3. deselect what the portal allows
4. classify anything the portal keeps visible as:
   - `not_applicable_visible`
   - `mandatory_visible_zero_confirm`
   - `review_only`

Do not spend live-session time inside Manufacturing Account, Trading Account, or `OI` unless:

- audit is actually in scope
- a regular-books path is actually intended
- the portal forces visibility and there is no deselection path

## 5. Practical portal route

Recommended live-entry order:

1. prefill inspection and selection cleanup
2. Part A general facts and branch-driving answers
3. salary
4. `44ADA` `BP`
5. `CG` and `112A`
6. `OS`
7. TDS-on-other-income and other tax anchors
8. `BFLA`, `SI`, `CYLA`, `CFL`, `Part B-TI`, and `Part B-TTI` as review-heavy checkpoints
9. foreign schedules `FSI`, `TR`, and `FA`
10. director and unlisted-equity rows
11. bank-account review and preview stop

Stop at preview or final review. Human-only actions remain:

- login
- OTP or `2FA`
- submit
- `e-Verify`
- tax payment
