# Contributing

Keep changes aligned with the skill's two core constraints:

- Default to a filing workpaper pack. Only add draft `ITR` JSON behavior when the current-`AY` utility, schema, and validation workflow are actually available and actually used.
- Keep simple cases simple. Do not add broker-, foreign-, or advanced-schedule scaffolding to every path by default.

## Contribution Rules

- Verify tax-law wording, thresholds, and portal behavior against current official Income Tax Department sources for the active `AY`.
- Keep references harness-neutral. The workflow belongs in `SKILL.md`; harness metadata in `agents/` should stay additive.
- Add provider-specific knowledge as a new focused reference instead of rewriting the base skill around one broker, fund platform, or employer equity tool.
- Prefer manifest-first intake, explicit blockers, and schedule-level traceability over opaque summary outputs.

## Local Checks

Run the bootstrap smoke tests before opening a change:

```bash
python3 skills/india-itr-filing/scripts/test_bootstrap_case.py
```
