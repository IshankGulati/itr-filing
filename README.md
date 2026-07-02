# india-itr-filing

`india-itr-filing` is an agent skill for profiling Indian income-tax return cases, collecting only the documents that matter, reconciling income head by head, and producing a filing workpaper pack for the current assessment year.

The default deliverable is a workpaper pack, not an upload-ready JSON. A draft `ITR` JSON is a secondary artifact that should only be produced when the current-`AY` utility, schema, and validation workflow are actually available and actually used.

## Scope

- Supports adaptive intake for `ITR-1` through `ITR-4`.
- Triage-first support for `ITR-5` through `ITR-7`.
- Covers resident, `RNOR`, and non-resident Indian taxpayers, including foreign assets, foreign income, foreign tax credit, deductions, and carry-forward losses.

## Safety

This repository is not tax advice. Treat it as an agent workflow and workpaper scaffold, then verify all filing positions, thresholds, utility behavior, and portal navigation against current official Income Tax Department sources for the active `AY`.

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
