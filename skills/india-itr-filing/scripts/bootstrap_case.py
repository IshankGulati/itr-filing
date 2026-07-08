#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
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

EXECUTION_MODE_CHOICES = [
    "none",
    "utility_json",
    "portal_draft_fill",
    "utility_json_and_portal_draft_fill",
]

PORTAL_EXECUTION_MODES = {
    "portal_draft_fill",
    "utility_json_and_portal_draft_fill",
}

UTILITY_JSON_EXECUTION_MODES = {
    "utility_json",
    "utility_json_and_portal_draft_fill",
}

PORTAL_HUMAN_ONLY_STEPS = [
    "login",
    "otp_or_2fa",
    "final_submit",
    "e_verify",
    "tax_payment",
]

PORTAL_SCHEDULE_IDS = [
    "salary",
    "hp",
    "bp",
    "cg",
    "os",
    "vda",
    "ei",
    "via",
    "si",
    "al",
    "fa",
    "fsi",
    "tr",
    "tds_salary",
    "tds_other",
    "tcs",
    "it_paid",
    "bfla",
    "cyla",
    "cfl",
    "spi",
    "pti",
    "amt",
    "amtc",
]


PROFILE_TEMPLATE = """fy: {fy}
ay: {ay}
return_mode: unknown
filing_goal: {filing_goal}
execution_mode: {execution_mode}
portal_fill_status: not_offered
preferred_browser: unknown
login_state: unknown
human_only_steps:
  - login
  - otp_or_2fa
  - final_submit
  - e_verify
  - tax_payment
last_completed_portal_section: ""
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
- Execution mode:
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
- Portal draft readiness:
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
- Execution mode:
- Status vocabulary: `out_of_scope | provisional | filing_ready | portal_ready | blocked`

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
- Execution mode:
- Status vocabulary: `out_of_scope | provisional | filing_ready | portal_ready | blocked`

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

## Utility, JSON, or portal blockers

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
- Portal-only screenshots, copied labels, and prefill notes belong in `inputs/portal_anchors/` when live portal drafting is in scope.
"""


VALIDATION_NOTES_TEMPLATE = """# Validation Notes

- Current AY utility used:
- Schema used:
- Validation result:
- Draft status:
- Portal packet validated:
- Remaining blockers:
"""


FILING_READINESS_TEMPLATE = """# Filing Readiness

- Output target:
- Execution mode:
- Utility available for current AY:
- Draft JSON attempted:
- Ready for manual portal or utility entry:
- Portal fill readiness:
- Remaining blockers:
"""


PORTAL_ENTRY_PLAN_TEMPLATE = """# Portal Entry Plan

Last updated: {today}

Use this only after `outputs/filing-readiness.md` says the case is ready for manual
portal or utility entry and the user explicitly opted into live portal drafting.

## Default order

1. Prefill inspection
2. Part A and profile questions
3. Branch-driving questions
4. Income schedules
5. Taxes and credits
6. Foreign or advanced schedules if present
7. Bank and refund review
8. Preview stop point for human review

## Human-only boundaries

- Human logs in and completes any OTP or 2FA.
- Human performs final submit, `e-Verify`, and tax payment.
- Agent stops at preview or final review and does not click through the human-only steps.
"""


PORTAL_SESSION_LOG_TEMPLATE = """# Portal Session Log

Last updated: {today}

## Current state

- Current page:
- Completed sections:
- Rows entered:
- Last checkpoint:
- Next checkpoint:
- Pause reason:
"""


PORTAL_PREFILL_DIFF_TEMPLATE = """# Portal Prefill Diff

Last updated: {today}

Record portal-prepopulated values versus the workpaper source of truth before or during
live entry. Use action labels `keep`, `update`, or `add`.

| Section | Portal value | Workpaper value | Action | Source ref | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
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


def wants_portal_scaffold(execution_mode: str) -> bool:
    return execution_mode in PORTAL_EXECUTION_MODES


def wants_json_scaffold(filing_goal: str, execution_mode: str) -> bool:
    return (
        filing_goal == "json_draft_if_feasible"
        or execution_mode in UTILITY_JSON_EXECUTION_MODES
    )


def wants_filing_readiness(filing_goal: str, execution_mode: str) -> bool:
    return (
        filing_goal == "return_workpaper_pack"
        or wants_json_scaffold(filing_goal, execution_mode)
        or wants_portal_scaffold(execution_mode)
    )


def schedule_map_template(
    case_tier: str,
    filing_goal: str,
    execution_mode: str,
) -> str:
    if (
        case_tier == "simple"
        and not wants_json_scaffold(filing_goal, execution_mode)
    ):
        return LEAN_SCHEDULE_MAP_TEMPLATE
    return FULL_SCHEDULE_MAP_TEMPLATE


def input_subdirs(case_tier: str, filing_goal: str, execution_mode: str) -> list[str]:
    if (
        case_tier == "simple"
        and not wants_json_scaffold(filing_goal, execution_mode)
    ):
        subdirs = list(LEAN_INPUT_SUBDIRS)
    else:
        subdirs = list(INPUT_SUBDIRS)

    if wants_portal_scaffold(execution_mode) and "portal_anchors" not in subdirs:
        subdirs.append("portal_anchors")

    return subdirs


def portal_field_map_content(
    fy: str,
    ay: str,
    execution_mode: str,
) -> str:
    schedule_field_packets = {
        schedule_id: {
            "status": "",
            "summary": "",
            "source_refs": [],
        }
        for schedule_id in PORTAL_SCHEDULE_IDS
    }
    portal_field_map = {
        "metadata": {
            "fy": fy,
            "ay": ay,
            "likely_itr_form": "",
            "return_mode": "",
            "execution_mode": execution_mode,
            "portal_fill_status": "not_offered",
            "preferred_browser": "unknown",
            "login_state": "unknown",
            "last_completed_portal_section": "",
            "human_only_steps": PORTAL_HUMAN_ONLY_STEPS,
            "in_scope_schedules": [],
            "schedule_field_packets": schedule_field_packets,
        },
        "branch_questions": {
            "presumptive_route": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "audit_applicable": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "transfer_pricing_applicable": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "director_in_company": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "partner_in_firm_or_llp": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "foreign_assets_or_signing_authority": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "foreign_tax_credit_claimed": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "unlisted_shares_held": {
                "value": None,
                "source": "",
                "notes": "",
            },
            "refund_account_selected": {
                "value": None,
                "source": "",
                "notes": "",
            },
        },
        "part_a_general_information": {
            "filing_status": {
                "due_date": "",
                "filed_under": "",
                "revised_or_updated_path": "",
            },
            "taxpayer_profile": {
                "residential_status": "",
                "regime_position": "",
                "business_income_current_ay": None,
            },
            "audit_information": {
                "liable_44aa": None,
                "liable_44ab": None,
                "liable_92e": None,
            },
        },
        "bank_details": {
            "refund_account_choice": {
                "account_last4": "",
                "ifsc": "",
                "source": "",
                "status": "required",
            },
            "validated_accounts": [],
            "notes": "",
        },
        "table_rows": {
            "director_companies": [],
            "unlisted_equity_rows": [],
            "capital_gain_rows": [],
            "foreign_asset_rows": [],
        },
        "source_refs": [],
        "review_flags": [],
    }
    return json.dumps(portal_field_map, indent=2) + "\n"


def bootstrap_case(
    case_root: Path,
    fy: str,
    ay: str,
    overwrite: bool,
    case_tier: str,
    filing_goal: str,
    execution_mode: str,
) -> None:
    case_root.mkdir(parents=True, exist_ok=True)
    for relative_dir in BASE_CASE_DIRS:
        (case_root / relative_dir).mkdir(exist_ok=True)
    for relative_dir in input_subdirs(case_tier, filing_goal, execution_mode):
        (case_root / "inputs" / relative_dir).mkdir(exist_ok=True)

    today = date.today().isoformat()
    regime_position = default_regime_position(ay)

    write_text(
        case_root / "profile.yaml",
        PROFILE_TEMPLATE.format(
            fy=fy,
            ay=ay,
            filing_goal=filing_goal,
            execution_mode=execution_mode,
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
        schedule_map_template(case_tier, filing_goal, execution_mode).format(today=today),
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

    if wants_filing_readiness(filing_goal, execution_mode) or wants_json_scaffold(
        filing_goal,
        execution_mode,
    ):
        (case_root / "outputs").mkdir(exist_ok=True)

    if wants_json_scaffold(filing_goal, execution_mode):
        write_text(
            case_root / "outputs" / "itr-draft.json",
            JSON_TEMPLATE,
            overwrite,
        )
        write_text(
            case_root / "outputs" / "validation-notes.md",
            VALIDATION_NOTES_TEMPLATE,
            overwrite,
        )

    if wants_filing_readiness(filing_goal, execution_mode):
        write_text(
            case_root / "outputs" / "filing-readiness.md",
            FILING_READINESS_TEMPLATE,
            overwrite,
        )

    if wants_portal_scaffold(execution_mode):
        write_text(
            case_root / "outputs" / "portal-field-map.yaml",
            portal_field_map_content(fy, ay, execution_mode),
            overwrite,
        )
        write_text(
            case_root / "outputs" / "portal-entry-plan.md",
            PORTAL_ENTRY_PLAN_TEMPLATE.format(today=today),
            overwrite,
        )
        write_text(
            case_root / "outputs" / "portal-session-log.md",
            PORTAL_SESSION_LOG_TEMPLATE.format(today=today),
            overwrite,
        )
        write_text(
            case_root / "outputs" / "portal-prefill-diff.md",
            PORTAL_PREFILL_DIFF_TEMPLATE.format(today=today),
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
        "--execution-mode",
        choices=EXECUTION_MODE_CHOICES,
        default="none",
        help="Optional post-calculation execution support for utility JSON and/or portal draft filling",
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
        args.execution_mode,
    )


if __name__ == "__main__":
    main()
