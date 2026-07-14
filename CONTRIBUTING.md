# Contributing

Keep changes aligned with the skill's core constraints:

- Default to a filing workpaper pack. Only add draft `ITR` JSON behavior when the current-`AY` utility, schema, and validation workflow are actually available and actually used.
- Keep live portal drafting optional, user-approved, and stopped before human-only steps such as login, OTP or `2FA`, submit, `e-Verify`, and payment.
- Keep simple cases simple. Do not add broker-, foreign-, or advanced-schedule scaffolding to every path by default.
- Keep `schedule_candidates` high-level. Put portal-only screen logic in the persona-policy layer and `schedule_inventory.yaml`, not in the schedule enum.

## Contribution Rules

- Verify tax-law wording, thresholds, and portal behavior against current official Income Tax Department sources for the active `AY`.
- Keep references harness-neutral. The workflow belongs in `SKILL.md`; harness metadata in `agents/` should stay additive.
- Add provider-specific knowledge as a new focused reference instead of rewriting the base skill around one broker, fund platform, or employer equity tool.
- Prefer manifest-first intake, explicit blockers, and schedule-level traceability over opaque summary outputs.
- When portal behavior changes, update `scripts/persona_policy.py`, the relevant portal references, and the validator together so screen modes, stale-selection rules, and docs do not drift.

## Adding A Broker Or Platform

- Extend `skills/india-itr-filing/references/broker-playbooks.md` with a provider-specific mini-playbook instead of baking provider assumptions into the main workflow.
- Record the provider name, where reports are usually found, exact report names, preferred export formats, known field quirks, and which artifact set is sufficient for Indian-tax reconstruction.
- If the provider needs foreign-capital-gains support, document any reusable `Rule 115`, `SBI TT`, or lot-reconstruction assumptions explicitly instead of implying them from a spreadsheet.

## Adding Another Modular Component

- Use `references/` for durable guidance or playbooks.
- Use `scripts/` for reusable operational tooling such as validators, consistency checks, or workspace bootstrap helpers.
- Use `scripts/persona_policy.py` for shared persona-module logic, screen-mode defaults, and stale-selection policy instead of duplicating those rules across scripts.
- Touch `SKILL.md` only when the base workflow itself needs to change for all users, not just one provider or one edge case.
- Keep agent metadata additive in `agents/`.

## Local Checks

Run the bootstrap smoke tests before opening a change:

```bash
python3 skills/india-itr-filing/scripts/test_bootstrap_case.py
```

Run the schedule-consistency tests when changing schedule ids, schedule docs, or related workflow text:

```bash
python3 skills/india-itr-filing/scripts/test_check_schedule_consistency.py
```

Run the portal-packet tests when changing execution-mode logic, portal artifacts, or live-entry validation rules:

```bash
python3 skills/india-itr-filing/scripts/test_check_portal_packet.py
```

Run the persona-policy fixtures when changing module composition, starter screen inventory, or stale-selection defaults:

```bash
python3 skills/india-itr-filing/scripts/test_persona_policy.py
```
