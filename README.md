# india-itr-filing

`india-itr-filing` is an agent skill for profiling Indian income-tax return cases, collecting only the documents that matter, reconciling income head by head, and producing a filing workpaper pack for the current assessment year.

The default deliverable is a workpaper pack, not an upload-ready JSON. A draft `ITR` JSON is a secondary artifact that should only be produced when the current-`AY` utility, schema, and validation workflow are actually available and actually used.

## Scope

- Supports adaptive intake for `ITR-1` through `ITR-4`.
- Triage-first support for `ITR-5` through `ITR-7`.
- Covers resident, `RNOR`, and non-resident Indian taxpayers, including foreign assets, foreign income, foreign tax credit, deductions, and carry-forward losses.

## Safety

This repository is not tax advice. Treat it as an agent workflow and workpaper scaffold, then verify all filing positions, thresholds, utility behavior, and portal navigation against current official Income Tax Department sources for the active `AY`.

## Repository Layout

- [skills/india-itr-filing/SKILL.md](skills/india-itr-filing/SKILL.md) contains the main workflow.
- [skills/india-itr-filing/references](skills/india-itr-filing/references) contains focused reference notes for intake, forms, schedules, document retrieval, broker exports, and foreign-income handling.
- [skills/india-itr-filing/scripts/bootstrap_case.py](skills/india-itr-filing/scripts/bootstrap_case.py) bootstraps a local case workspace.
- [skills/india-itr-filing/agents](skills/india-itr-filing/agents) contains additive harness metadata.

## Bootstrap Examples

Use a lean starter for a simple workpaper-first case:

```bash
python3 skills/india-itr-filing/scripts/bootstrap_case.py /tmp/itr-case \
  --fy FY_2025-26 \
  --ay "AY 2026-27" \
  --tier simple
```

Use the full scaffold when the case is complex or explicitly JSON-targeted:

```bash
python3 skills/india-itr-filing/scripts/bootstrap_case.py /tmp/itr-case \
  --fy FY_2025-26 \
  --ay "AY 2026-27" \
  --tier complex \
  --filing-goal json_draft_if_feasible
```

## Extending

Provider-specific knowledge should be added additively through `references/` instead of overfitting the core skill to one broker or platform. See [skills/india-itr-filing/references/broker-playbooks.md](skills/india-itr-filing/references/broker-playbooks.md) for the extension pattern.
