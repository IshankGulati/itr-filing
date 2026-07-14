# Portal Draft Filling

## Contents

1. When to offer it
2. Readiness gate
3. Prefill-diff workflow
4. Pause and resume choreography
5. Expected branch effects
6. Human-only boundaries

## 1. When to offer it

Offer live portal drafting only after the calculation workpapers are ready and only when the user explicitly wants help entering the prepared return into the Income Tax portal draft.

Use a direct confirmation such as:

`Do you want me to enter your prepared return data into the Income Tax portal draft in your browser? I will not log in, complete OTP or 2FA, submit, e-verify, or pay.`

Do not offer it as the default first move.
Do not jump into browser work while major classification or reconciliation blockers remain.

## 2. Readiness gate

Before any live portal work:

- `outputs/filing-readiness.md` must explicitly say the case is ready for manual portal or utility entry
- `outputs/filing-readiness.md` must also record:
  - schedule selection audit complete
  - visible schedules classified
  - stale selections resolved
  - upload packet readiness
- `profile.yaml` must capture `execution_mode`, `portal_fill_status`, `preferred_browser`, `login_state`, `human_only_steps`, `last_completed_portal_section`, and `persona_modules`
- `outputs/portal-field-map.yaml` must exist and answer the branch-driving questions explicitly; the checker accepts either JSON-compatible or normal YAML syntax in that file
- `outputs/portal-field-map.yaml > metadata` must also record `active_persona_modules`, `selection_audit_complete`, and `upload_packets`
- `outputs/schedule_inventory.yaml` must exist and classify every selected or visible screen with `selected`, `visible`, `applicable`, `screen_mode`, `why_selected`, `deselect_if_possible`, and `evidence`
- `schedule_map.md` must mark in-scope schedules as `filing_ready` or `portal_ready`
- `outputs/review_only_schedules.md` must exist so derived screens do not become first-pass manual-entry targets
- `outputs/portal-entry-plan.md` must describe the order of entry after the schedule-selection audit
- `outputs/portal-session-log.md` must exist before the live session starts and must be kept current once work is in progress
- `outputs/upload_packets/` must exist when the scaffold promises an upload path, even if the packet is still `scaffold_only`

If any of the above is missing, stop and finish the packet instead of improvising through the browser.

## 3. Prefill-diff workflow

Inspect the portal's prefilled state before editing anything substantial.

First do a selection audit:

- compare the portal chooser against the active persona modules
- identify screens that are selected but not actually applicable
- deselect what the portal allows
- classify anything still visible as `manual_input`, `review_only`, `auto_derived`, `mandatory_visible_zero_confirm`, `not_applicable_visible`, or `blocked`

This matters most in `ITR-3` no-books cases where the portal can still surface business-heavy screens that do not deserve regular-books treatment.

Record the comparison in `outputs/portal-prefill-diff.md`:

- what the portal already shows
- what the workpaper pack says
- whether the action is `keep`, `update`, `add`, or `deselect`
- which source document or workpaper supports the decision

Treat portal prefill as a starting point, not as authoritative truth.
If the portal already contains a validated bank account, prior disclosure row, or imported TDS line, record that fact and edit only if it conflicts with the source-of-truth workpapers.

## 4. Pause and resume choreography

Use `outputs/portal-session-log.md` during the live session.

At every pause, record:

- current page
- sections completed
- rows added or edited
- the exact last checkpoint
- the next checkpoint
- the reason for the pause

Update `profile.yaml` so `portal_fill_status` and `last_completed_portal_section` stay current.
If the browser session is interrupted, resume from the session log instead of re-deriving progress from memory.

## 5. Expected branch effects

Some portal sections appear or disappear based on earlier answers. Treat this as expected behavior unless it conflicts with the prepared packet.

Common branch drivers include:

- presumptive route versus regular business schedules
- audit applicability
- transfer-pricing applicability
- director-company disclosure
- partner status
- foreign assets or signing authority
- foreign tax credit
- unlisted shares

If a section disappears after one of these answers changes, do not assume the portal is broken. First check whether the branch effect is consistent with the packet.

For `professional_44ada_no_books` cases, do not let `ITR-3` business routing trick you into treating:

- Manufacturing Account
- Trading Account
- `OI`
- `UD`
- `AL`
- `AMTC`

as substantive manual work unless the case actually proves they belong.

## 6. Human-only boundaries

The live portal phase stops before any of the following:

- login
- OTP or `2FA`
- final submit
- `e-Verify`
- tax payment

Even when the user is already logged in, do not cross those boundaries.
The goal is to prepare the draft accurately and leave the final legally meaningful actions with the human.
