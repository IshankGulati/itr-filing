#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


BASE_CASE_DIRS = [
    "inputs",
    "workpapers",
]

INPUT_SUBDIRS = [
    "salary",
    "business",
    "investments",
    "foreign",
    "prior_year",
    "portal_anchors",
]

# A lean salary-style case should not spawn empty foreign/business/prior-year folders.
LEAN_INPUT_SUBDIRS = [
    "salary",
    "investments",
]


PROFILE_TEMPLATE = """fy: {fy}
ay: {ay}
return_mode: unknown
filing_goal: {filing_goal}
case_tier: {case_tier}
taxpayer_type: unknown
residential_status: unknown
likely_itr_form: unknown
regime_position: {regime_position}
compliance_flags:
  director_in_company: false
  unlisted_equity_holder: false
  foreign_signing_authority: false
  foreign_tax_credit: false
  audit_requirement: false
  transfer_pricing: false
income_heads:
  salary_or_pension: false
  house_property: false
  business_or_profession: false
  presumptive_business_or_profession: false
  capital_gains: false
  other_sources: false
  agricultural_income: false
  foreign_income_or_assets: false
  carry_forward_losses: false
  special_rate_income: false
investment_buckets:
  listed_equity_or_etf: false
  mutual_funds: false
  fno_or_intraday: false
  bonds_or_debt: false
  property: false
  esop_rsu_espp: false
  unlisted_shares: false
  foreign_broker: false
  vda: false
schedule_candidates: []
notes: []
"""


WORKING_TEMPLATE = """# {fy} ITR Working Note

Last updated: {today}

## Scope

- Return being prepared:
- Output target:
- Likely ITR form:
- Reason:

## Taxpayer profile

- Taxpayer type:
- Residential status:
- Regime position:

## Source overview

- `AIS`:
- `TIS`:
- `26AS`:
- Prior-year return support:

## Head-wise status

### Salary or pension

- 

### House property

- 

### Business or profession

- 

### Capital gains and investments

- 

### Other sources

- 

### Agricultural or exempt income (only if relevant)

- 

### Foreign income or assets (only if relevant)

- 

### Deductions and reliefs

- 

## Assumptions

- 

## Open blockers

- 

## Next steps

- 
"""


LINE_BY_LINE_TEMPLATE = """# {fy} ITR Line By Line

Last updated: {today}

## Status

- Filing readiness:
- JSON readiness:
- Main blocker:

## Income heads

### Salary or pension

- Source:
- Treatment:
- Caveat:

### House property

- Source:
- Treatment:
- Caveat:

### Business or profession

- Source:
- Treatment:
- Caveat:

### Capital gains and investments

- Source:
- Treatment:
- Caveat:

### Other sources

- Source:
- Treatment:
- Caveat:

### Agricultural or exempt income (only if relevant)

- Source:
- Treatment:
- Caveat:

### Foreign income or assets (only if relevant)

- Source:
- Treatment:
- Caveat:

### Deductions and reliefs

- Source:
- Treatment:
- Caveat:
"""


LEAN_SCHEDULE_MAP_TEMPLATE = """# Schedule Map

Last updated: {today}

## Likely return frame

- Return mode:
- Likely ITR form:
- Filing goal:

## Core schedule candidates

### Salary

- Source:
- Utility or portal-entry target:
- Status:

### House property (`HP`)

- Source:
- Utility or portal-entry target:
- Status:

### Business or profession (`BP`)

- Source:
- Utility or portal-entry target:
- Status:

### Capital gains (`CG`)

- Source:
- Utility or portal-entry target:
- Status:

### Other sources (`OS`)

- Source:
- Utility or portal-entry target:
- Status:

### Deductions and reliefs (`VI-A`)

- Source:
- Utility or portal-entry target:
- Status:

### Credits and taxes paid

- TDS on salary:
- TDS on other income:
- `TCS`:
- `IT`:

## Expand only if the profile requires it

- Add `VDA`, `SI`, `AL`, foreign schedules, or set-off schedules only when the case grows beyond simple salary or bank-interest scope.
"""


FULL_SCHEDULE_MAP_TEMPLATE = """# Schedule Map

Last updated: {today}

## Likely return frame

- Return mode:
- Likely ITR form:
- Filing goal:

## Schedule candidates

### Salary

- Source:
- Utility or portal-entry target:
- Status:

### House property (`HP`)

- Source:
- Utility or portal-entry target:
- Status:

### Business or profession (`BP`)

- Source:
- Utility or portal-entry target:
- Status:

### Capital gains (`CG`)

- Source:
- Utility or portal-entry target:
- Status:

### Other sources (`OS`)

- Source:
- Utility or portal-entry target:
- Status:

### Deductions and reliefs (`VI-A`)

- Source:
- Utility or portal-entry target:
- Status:

### Special-rate and threshold-driven sections

- `VDA`:
- `EI`:
- `SI`:
- `AL`:

### Credits and taxes paid

- TDS on salary:
- TDS on other income:
- `TCS`:
- `IT`:

### Foreign schedules

- `FA`:
- `FSI`:
- `TR`:

### Set-off and carry forward

- `BFLA`:
- `CYLA`:
- `CFL`:

### Other advanced schedules

- `SPI`:
- `PTI`:
- `AMT`:
- `AMTC`:
"""


CASE_LEARNINGS_TEMPLATE = """# Case Learnings

Last updated: {today}

Log operational quirks discovered while working this case: broker-export gotchas,
portal navigation that drifted from the documented path, schema surprises, anything
that would save time on a similar future case. This is scratch, not tax law — do not
record tax-treatment conclusions here.

If a learning generalizes beyond this one case (recurs across clients, brokers, or
AYs), promote it into the india-itr-filing skill's
references/reconciliation-playbook.md, "Lessons from prior complex cases" section,
instead of leaving it stuck in this file.

## Entries

-
"""


OPEN_QUESTIONS_TEMPLATE = """# Open Questions

Last updated: {today}

## Missing documents

- 

## Unresolved classifications

- 

## Rules to verify from official sources

- 

## Utility or JSON blockers

- 
"""


REQUEST_TEMPLATE = """# Document Request

Last updated: {today}

## Profile-driven request

Fill this only after `profile.yaml` is updated.

## Ask next for

- 

## Helpful download paths

- Verify current portal navigation before quoting menu labels. Portal steps and deep links drift across redesigns and `AY` rollovers.
- Portal home: https://www.incometax.gov.in/iec/foportal/
- Downloads page: https://www.incometax.gov.in/iec/foportal/downloads
- `26AS` current common path: Login > e-File > Income Tax Return > View Form 26AS
- `AIS` and `TIS` current common path: Login > AIS
- Offline utility manual: https://www.incometax.gov.in/iec/foportal/help/offline-utility
- Current AY utilities and schema: https://www.incometax.gov.in/iec/foportal/downloads
"""


JSON_TEMPLATE = """{
  "status": "not_started",
  "validation_status": "not_attempted",
  "notes": []
}
"""


MANIFEST_HEADERS = [
    "head",
    "subhead",
    "source_name",
    "portal_or_provider",
    "required_for",
    "priority",
    "available",
    "path_or_link",
    "coverage",
    "status",
    "notes",
]


def write_text(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def write_manifest(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(MANIFEST_HEADERS)


def default_regime_position(ay: str) -> str:
    digits = "".join(ch if ch.isdigit() else " " for ch in ay).split()
    if not digits:
        return "unknown"
    start_year = int(digits[0])
    if start_year >= 2024:
        return "default_new"
    return "unknown"


def wants_json_scaffold(filing_goal: str) -> bool:
    return filing_goal == "json_draft_if_feasible"


def wants_filing_readiness(case_tier: str, filing_goal: str) -> bool:
    # filing-readiness.md tracks readiness of the workpaper pack, so it belongs to any
    # filing-targeted goal regardless of tier. This keeps SKILL.md's minimum output set and
    # intake-checklist ("for filing-targeted cases") consistent with what the script produces.
    return filing_goal in {
        "return_workpaper_pack",
        "json_draft_if_feasible",
    }


def schedule_map_template(case_tier: str, filing_goal: str) -> str:
    if case_tier == "simple" and not wants_json_scaffold(filing_goal):
        return LEAN_SCHEDULE_MAP_TEMPLATE
    return FULL_SCHEDULE_MAP_TEMPLATE


def input_subdirs(case_tier: str, filing_goal: str) -> list[str]:
    if case_tier == "simple" and not wants_json_scaffold(filing_goal):
        return LEAN_INPUT_SUBDIRS
    return INPUT_SUBDIRS


def bootstrap_case(
    case_root: Path,
    fy: str,
    ay: str,
    overwrite: bool,
    case_tier: str,
    filing_goal: str,
) -> None:
    case_root.mkdir(parents=True, exist_ok=True)
    for relative_dir in BASE_CASE_DIRS:
        (case_root / relative_dir).mkdir(exist_ok=True)
    for relative_dir in input_subdirs(case_tier, filing_goal):
        (case_root / "inputs" / relative_dir).mkdir(exist_ok=True)

    today = date.today().isoformat()
    regime_position = default_regime_position(ay)

    write_text(
        case_root / "profile.yaml",
        PROFILE_TEMPLATE.format(
            fy=fy,
            ay=ay,
            filing_goal=filing_goal,
            case_tier=case_tier,
            regime_position=regime_position,
        ),
        overwrite,
    )
    write_manifest(case_root / "document_manifest.csv", overwrite)
    write_text(
        case_root / "document_request.md",
        REQUEST_TEMPLATE.format(today=today),
        overwrite,
    )
    write_text(
        case_root / "itr_working.md",
        WORKING_TEMPLATE.format(fy=fy, today=today),
        overwrite,
    )
    write_text(
        case_root / "itr_line_by_line.md",
        LINE_BY_LINE_TEMPLATE.format(fy=fy, today=today),
        overwrite,
    )
    write_text(
        case_root / "schedule_map.md",
        schedule_map_template(case_tier, filing_goal).format(today=today),
        overwrite,
    )
    write_text(
        case_root / "open_questions.md",
        OPEN_QUESTIONS_TEMPLATE.format(today=today),
        overwrite,
    )
    write_text(
        case_root / "case_learnings.md",
        CASE_LEARNINGS_TEMPLATE.format(today=today),
        overwrite,
    )

    if wants_filing_readiness(case_tier, filing_goal) or wants_json_scaffold(filing_goal):
        (case_root / "outputs").mkdir(exist_ok=True)

    if wants_json_scaffold(filing_goal):
        write_text(
            case_root / "outputs" / "itr-draft.json",
            JSON_TEMPLATE,
            overwrite,
        )
        write_text(
            case_root / "outputs" / "validation-notes.md",
            "# Validation Notes\n\n- Current AY utility used:\n- Schema used:\n- Validation result:\n- Draft status:\n- Remaining blockers:\n",
            overwrite,
        )

    if wants_filing_readiness(case_tier, filing_goal):
        write_text(
            case_root / "outputs" / "filing-readiness.md",
            "# Filing Readiness\n\n- Output target:\n- Utility available for current AY:\n- Draft JSON attempted:\n- Ready for manual portal or utility entry:\n- Remaining blockers:\n",
            overwrite,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a neutral workspace for an Indian ITR case.",
    )
    parser.add_argument("case_root", help="Path to the case workspace")
    parser.add_argument("--fy", required=True, help="Financial year label, e.g. FY_2025-26")
    parser.add_argument("--ay", required=True, help="Assessment year label, e.g. AY 2026-27")
    parser.add_argument(
        "--tier",
        choices=["simple", "moderate", "complex"],
        default="moderate",
        help="Case tier used to decide how much starter scaffolding to create",
    )
    parser.add_argument(
        "--filing-goal",
        choices=[
            "return_workpaper_pack",
            "json_draft_if_feasible",
            "tax_estimate_only",
            "document_collection_first",
        ],
        default="return_workpaper_pack",
        help="Primary deliverable goal for the scaffolded case",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite starter files if they already exist",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bootstrap_case(
        Path(args.case_root).expanduser(),
        args.fy,
        args.ay,
        args.overwrite,
        args.tier,
        args.filing_goal,
    )


if __name__ == "__main__":
    main()
