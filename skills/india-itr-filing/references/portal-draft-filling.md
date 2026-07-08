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
- `profile.yaml` must capture `execution_mode`, `portal_fill_status`, `preferred_browser`, `login_state`, `human_only_steps`, and `last_completed_portal_section`
- `outputs/portal-field-map.yaml` must exist and answer the branch-driving questions explicitly; the checker accepts either JSON-compatible or normal YAML syntax in that file
- `schedule_map.md` must mark in-scope schedules as `filing_ready` or `portal_ready`
- `outputs/portal-entry-plan.md` must describe the order of entry
- `outputs/portal-session-log.md` must exist before the live session starts and must be kept current once work is in progress

If any of the above is missing, stop and finish the packet instead of improvising through the browser.

## 3. Prefill-diff workflow

Inspect the portal's prefilled state before editing anything substantial.

Record the comparison in `outputs/portal-prefill-diff.md`:

- what the portal already shows
- what the workpaper pack says
- whether the action is `keep`, `update`, or `add`
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

## 6. Human-only boundaries

The live portal phase stops before any of the following:

- login
- OTP or `2FA`
- final submit
- `e-Verify`
- tax payment

Even when the user is already logged in, do not cross those boundaries.
The goal is to prepare the draft accurately and leave the final legally meaningful actions with the human.
