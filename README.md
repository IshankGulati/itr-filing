# india-itr-filing

`india-itr-filing` is an agent skill for profiling Indian income-tax return cases, collecting only the documents that matter, reconciling income head by head, and producing a filing workpaper pack for the current assessment year.

The default deliverable is a workpaper pack, not an upload-ready JSON. A draft `ITR` JSON is a secondary artifact that should only be produced when the current-`AY` utility, schema, and validation workflow are actually available and actually used.

## Scope

- Supports adaptive intake for `ITR-1` through `ITR-4`.
- Triage-first support for `ITR-5` through `ITR-7`.
- Covers resident, `RNOR`, and non-resident Indian taxpayers, including foreign assets, foreign income, foreign tax credit, deductions, and carry-forward losses.

## Safety

This repository is not tax advice. Treat it as an agent workflow and workpaper scaffold, then verify all filing positions, thresholds, utility behavior, and portal navigation against current official Income Tax Department sources for the active `AY`.

## Current Capabilities

- Profiles an Indian tax case first, then infers the likely `ITR` form, return mode, regime posture, and schedule candidates before asking for documents.
- Supports adaptive intake for `ITR-1` through `ITR-4`, and triage-first workpaper preparation for `ITR-5` through `ITR-7`.
- Builds a filing workpaper pack around `profile.yaml`, `document_manifest.csv`, `schedule_map.md`, `itr_working.md`, `itr_line_by_line.md`, `open_questions.md`, `case_learnings.md`, and `outputs/filing-readiness.md`.
- Keeps document collection targeted instead of generic, including support for scattered local files through a manifest-driven workflow.
- Covers reconciliation across salary, house property, business or profession, capital gains, other sources, deductions, taxes paid, and carry-forward dependencies.
- Handles foreign-broker and foreign-asset cases by guiding lot reconstruction, FX-method documentation, and downstream `FA` / `FSI` / `TR` / `Form 67` workpapers when relevant.
- Includes local tooling to bootstrap a case workspace and to detect drift between documented schedule ids and the skill's `schedule_candidates` enum.

## What To Expect

- The primary output is a filing workpaper pack, not an upload-ready return by default.
- A draft `ITR` JSON is a secondary artifact and should only be expected when the current-`AY` utility, schema, and validation workflow are actually available and actually used.
- The skill is intentionally conservative: it should ask only for documents that matter to the profiled case, and it may stop at explicit blockers or open questions when records are incomplete.
- Foreign-income and capital-gains support is designed for Indian taxpayers with overseas holdings or income; it is not a non-Indian return-preparation engine.
- This repository helps structure and document the work. Users should still expect final verification against current official portal instructions, form help, schema behavior, and law for the active `AY`.

## Foreign Capital Gains And FX Helpers

When foreign capital gains need INR conversion support, first reuse any reliable local `rule115`, `ttbr`, or `sbi_tt` workpapers already present in the workspace. If a fresh historical `SBI TT` lookup is needed, the repo [skbly7/sbi-tt-rates-historical](https://github.com/skbly7/sbi-tt-rates-historical) can be used as a helper source for historical TT rates while reconstructing foreign capital gains.

Treat that repo as an operational aid, not as a substitute for documenting the chosen Rule-115 or other FX method, relevant date logic, and current-law basis for the case.

## Installing

The skill lives at [skills/india-itr-filing](skills/india-itr-filing), self-contained under a folder named after the skill. Both Claude Code and Codex CLI discover skills by scanning a `skills/` directory for `SKILL.md` files, so install by copying (or symlinking) that folder into the right place. A skill folder is not effective one level too deep — the path must end in `.../india-itr-filing/SKILL.md`.

### Claude Code

Personal install (all projects on this machine):

```bash
mkdir -p ~/.claude/skills
cp -R skills/india-itr-filing ~/.claude/skills/india-itr-filing
```

Project-scoped install (only this repo):

```bash
mkdir -p .claude/skills
cp -R skills/india-itr-filing .claude/skills/india-itr-filing
```

Restart Claude Code, then run `/skills` to confirm `india-itr-filing` loaded.

### Codex CLI

Personal install:

```bash
mkdir -p ~/.codex/skills
cp -R skills/india-itr-filing ~/.codex/skills/india-itr-filing
```

Project-scoped install:

```bash
mkdir -p .codex/skills
cp -R skills/india-itr-filing .codex/skills/india-itr-filing
```

Codex detects new skills automatically; restart Codex if it doesn't appear. Verify with `ls ~/.codex/skills` and `head ~/.codex/skills/india-itr-filing/SKILL.md`.

## Using the skill

In Claude Code, invoke it directly:

```
/india-itr-filing
```

or describe the task and let Claude pick it up automatically (Claude matches the request against the skill's `description` in [SKILL.md](skills/india-itr-filing/SKILL.md)), e.g. "Use the india-itr-filing skill to help me file my ITR for FY 2025-26."

In Codex CLI, reference it with the `$` prefix, matching [agents/openai.yaml](skills/india-itr-filing/agents/openai.yaml):

```
Use $india-itr-filing to profile this tax case, gather only the needed documents, build a filing workpaper pack, and create a draft ITR JSON only when the current AY utility, schema, and validation workflow are actually available and actually used.
```

Either way, the skill drives an adaptive intake: it profiles the taxpayer, requests only the documents that matter for the case, and produces a filing workpaper pack rather than jumping straight to a JSON draft. See [Bootstrap Examples](#bootstrap-examples) below to scaffold a local case workspace before or during a session.

## Repository Layout

- [skills/india-itr-filing/SKILL.md](skills/india-itr-filing/SKILL.md) contains the main workflow.
- [skills/india-itr-filing/references](skills/india-itr-filing/references) contains focused reference notes for intake, forms, schedules, document retrieval, broker exports, and foreign-income handling.
- [skills/india-itr-filing/scripts/bootstrap_case.py](skills/india-itr-filing/scripts/bootstrap_case.py) bootstraps a local case workspace.
- [skills/india-itr-filing/scripts/check_schedule_consistency.py](skills/india-itr-filing/scripts/check_schedule_consistency.py) checks that the skill's documented schedule ids stay aligned with [references/forms-and-schedules.md](skills/india-itr-filing/references/forms-and-schedules.md).
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

Check schedule-doc consistency after changing schedule ids or schedule reference docs:

```bash
python3 skills/india-itr-filing/scripts/test_check_schedule_consistency.py
```

## Contributors

Contributors should keep the core skill generic and extend it additively.

- To add a broker or investment platform, extend [skills/india-itr-filing/references/broker-playbooks.md](skills/india-itr-filing/references/broker-playbooks.md) with a focused mini-playbook covering where reports live, which exports matter, preferred formats, known quirks, and the minimum artifact set needed for Indian-tax reconstruction.
- To add another modular component, prefer a new focused file under [skills/india-itr-filing/references](skills/india-itr-filing/references) when the addition is guidance, or a reusable script under [skills/india-itr-filing/scripts](skills/india-itr-filing/scripts) when the addition is operational tooling that can help across cases.
- Keep the workflow logic in [skills/india-itr-filing/SKILL.md](skills/india-itr-filing/SKILL.md) harness-neutral. Put harness-specific behavior only in [skills/india-itr-filing/agents](skills/india-itr-filing/agents).
- Update tests and docs together when you change scaffold outputs, schedule enums, or reference structure. At minimum, run `python3 skills/india-itr-filing/scripts/test_bootstrap_case.py` and `python3 skills/india-itr-filing/scripts/test_check_schedule_consistency.py`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the compact maintainer checklist.
