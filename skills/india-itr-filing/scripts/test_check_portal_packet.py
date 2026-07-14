#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from persona_policy import starter_schedule_inventory


SCRIPT_PATH = Path(__file__).with_name("check_portal_packet.py")
SPEC = importlib.util.spec_from_file_location("check_portal_packet_module", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load portal-packet module from {SCRIPT_PATH}")

check_portal_packet_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_portal_packet_module)


def build_schedule_map(schedule_statuses: dict[str, str]) -> str:
    return f"""# Schedule Map

## Schedule candidates

### Salary

- Source:
- Utility or portal-entry target:
- Status: {schedule_statuses.get("salary", "")}

### House property (`HP`)

- Source:
- Utility or portal-entry target:
- Status: {schedule_statuses.get("hp", "")}

### Business or profession (`BP`)

- Source:
- Utility or portal-entry target:
- Status: {schedule_statuses.get("bp", "")}

### Capital gains (`CG`)

- Source:
- Utility or portal-entry target:
- Status: {schedule_statuses.get("cg", "")}

### Other sources (`OS`)

- Source:
- Utility or portal-entry target:
- Status: {schedule_statuses.get("os", "")}

### Deductions and reliefs (`VI-A`)

- Source:
- Utility or portal-entry target:
- Status: {schedule_statuses.get("via", "")}

### Special-rate and threshold-driven sections

- `VDA`: {schedule_statuses.get("vda", "")}
- `EI`: {schedule_statuses.get("ei", "")}
- `SI`: {schedule_statuses.get("si", "")}
- `AL`: {schedule_statuses.get("al", "")}

### Credits and taxes paid

- TDS on salary: {schedule_statuses.get("tds_salary", "")}
- TDS on other income: {schedule_statuses.get("tds_other", "")}
- `TCS`: {schedule_statuses.get("tcs", "")}
- `IT`: {schedule_statuses.get("it_paid", "")}

### Foreign schedules

- `FA`: {schedule_statuses.get("fa", "")}
- `FSI`: {schedule_statuses.get("fsi", "")}
- `TR`: {schedule_statuses.get("tr", "")}

### Set-off and carry forward

- `BFLA`: {schedule_statuses.get("bfla", "")}
- `CYLA`: {schedule_statuses.get("cyla", "")}
- `CFL`: {schedule_statuses.get("cfl", "")}

### Other advanced schedules

- `SPI`: {schedule_statuses.get("spi", "")}
- `PTI`: {schedule_statuses.get("pti", "")}
- `AMT`: {schedule_statuses.get("amt", "")}
- `AMTC`: {schedule_statuses.get("amtc", "")}
"""


def build_portal_packet() -> dict[str, object]:
    return {
        "metadata": {
            "active_persona_modules": [],
            "selection_audit_complete": True,
            "upload_packets": {
                "112a_csv": {
                    "status": "scaffold_only",
                    "template_path": "",
                    "notes": "fixture",
                }
            },
            "schedule_field_packets": {
                "salary": {"status": "ready", "summary": "", "source_refs": []},
                "cg": {"status": "ready", "summary": "", "source_refs": []},
            }
        },
        "branch_questions": {
            "presumptive_route": {"value": False},
            "audit_applicable": {"value": False},
            "transfer_pricing_applicable": {"value": False},
            "director_in_company": {"value": False},
            "partner_in_firm_or_llp": {"value": False},
            "foreign_assets_or_signing_authority": {"value": False},
            "foreign_tax_credit_claimed": {"value": False},
            "unlisted_shares_held": {"value": False},
            "refund_account_selected": {"value": True},
        },
        "part_a_general_information": {
            "filing_status": {},
            "taxpayer_profile": {},
            "audit_information": {},
        },
        "bank_details": {
            "refund_account_choice": {
                "account_last4": "0861",
                "ifsc": "ABCD0123456",
                "source": "portal",
                "status": "required",
            }
        },
        "table_rows": {
            "director_companies": [],
            "unlisted_equity_rows": [],
            "capital_gain_rows": [{"asset": "MF", "amount": 1}],
            "foreign_asset_rows": [],
        },
        "source_refs": [],
        "review_flags": [],
    }


def build_schedule_inventory() -> dict[str, object]:
    inventory = starter_schedule_inventory([])
    screens = inventory["screens"]
    assert isinstance(screens, dict)
    screens["Schedule Salary"]["related_schedule_ids"] = ["salary"]
    screens["Schedule CG"]["related_schedule_ids"] = ["cg"]
    return inventory


def write_case_fixture(
    case_root: Path,
    *,
    execution_mode: str = "portal_draft_fill",
    portal_fill_status: str = "accepted",
    likely_itr_form: str = "ITR-2",
    schedule_candidates: list[str] | None = None,
    persona_modules: list[str] | None = None,
    schedule_statuses: dict[str, str] | None = None,
    ready_for_entry: str = "yes",
    selection_audit_complete: str = "yes",
    visible_schedules_classified: str = "yes",
    stale_selections_resolved: str = "yes",
    upload_packet_readiness: str = "scaffold_only",
    portal_packet: dict[str, object] | None = None,
    schedule_inventory: dict[str, object] | None = None,
    include_prefill_diff: bool = True,
    include_entry_plan: bool = True,
    include_session_log: bool = True,
    include_schedule_inventory: bool = True,
    include_review_only: bool = True,
    include_upload_packet_docs: bool = True,
    portal_packet_text: str | None = None,
) -> None:
    schedule_candidates = schedule_candidates or ["salary"]
    persona_modules = persona_modules or []
    schedule_statuses = schedule_statuses or {"salary": "portal_ready"}
    portal_packet = portal_packet or build_portal_packet()
    schedule_inventory = schedule_inventory or build_schedule_inventory()
    portal_packet_metadata = portal_packet.get("metadata", {})
    if isinstance(portal_packet_metadata, dict):
        portal_packet_metadata["active_persona_modules"] = list(persona_modules)
        portal_packet_metadata["selection_audit_complete"] = (
            selection_audit_complete.lower() == "yes"
        )
    inventory_metadata = schedule_inventory.get("metadata", {})
    if isinstance(inventory_metadata, dict):
        inventory_metadata["active_persona_modules"] = list(persona_modules)

    (case_root / "outputs").mkdir(parents=True, exist_ok=True)

    profile_lines = [
        "fy: FY_2025-26",
        "ay: AY 2026-27",
        "return_mode: original",
        "filing_goal: return_workpaper_pack",
        f"execution_mode: {execution_mode}",
        f"portal_fill_status: {portal_fill_status}",
        "preferred_browser: chrome",
        "login_state: human_logged_in",
        f"likely_itr_form: {likely_itr_form}",
        "schedule_candidates:",
    ]
    profile_lines.extend(f"  - {item}" for item in schedule_candidates)
    profile_lines.append("persona_modules:")
    profile_lines.extend(f"  - {item}" for item in persona_modules)
    (case_root / "profile.yaml").write_text(
        "\n".join(profile_lines) + "\n",
        encoding="utf-8",
    )

    (case_root / "schedule_map.md").write_text(
        build_schedule_map(schedule_statuses),
        encoding="utf-8",
    )
    (case_root / "outputs" / "filing-readiness.md").write_text(
        "# Filing Readiness\n\n"
        f"- Ready for manual portal or utility entry: {ready_for_entry}\n"
        f"- Schedule selection audit complete: {selection_audit_complete}\n"
        f"- Visible schedules classified: {visible_schedules_classified}\n"
        f"- Stale selections resolved: {stale_selections_resolved}\n"
        f"- Upload packet readiness: {upload_packet_readiness}\n",
        encoding="utf-8",
    )
    if portal_packet_text is None:
        portal_packet_text = json.dumps(portal_packet, indent=2) + "\n"
    (case_root / "outputs" / "portal-field-map.yaml").write_text(
        portal_packet_text,
        encoding="utf-8",
    )
    if include_schedule_inventory:
        (case_root / "outputs" / "schedule_inventory.yaml").write_text(
            json.dumps(schedule_inventory, indent=2) + "\n",
            encoding="utf-8",
        )
    if include_entry_plan:
        (case_root / "outputs" / "portal-entry-plan.md").write_text(
            "# Portal Entry Plan\n",
            encoding="utf-8",
        )
    if include_review_only:
        (case_root / "outputs" / "review_only_schedules.md").write_text(
            "# Review-Only Schedules\n",
            encoding="utf-8",
        )
    if include_session_log:
        (case_root / "outputs" / "portal-session-log.md").write_text(
            "# Portal Session Log\n",
            encoding="utf-8",
        )
    if include_prefill_diff:
        (case_root / "outputs" / "portal-prefill-diff.md").write_text(
            "# Portal Prefill Diff\n",
            encoding="utf-8",
        )
    if include_upload_packet_docs:
        (case_root / "outputs" / "upload_packets").mkdir(parents=True, exist_ok=True)
        (case_root / "outputs" / "upload_packets" / "README.md").write_text(
            "# Upload Packets\n",
            encoding="utf-8",
        )
        (case_root / "outputs" / "upload_packets" / "112a-status.md").write_text(
            "# 112A Upload Status\n",
            encoding="utf-8",
        )


class CheckPortalPacketTests(unittest.TestCase):
    def test_non_portal_execution_mode_short_circuits(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            (case_root / "profile.yaml").write_text(
                "execution_mode: none\n",
                encoding="utf-8",
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertEqual(errors, [])

    def test_minimal_portal_ready_case_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(case_root)

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertEqual(errors, [])

    def test_yaml_style_portal_packet_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            yaml_portal_packet = """metadata:
  active_persona_modules: []
  selection_audit_complete: true
  upload_packets:
    112a_csv:
      status: scaffold_only
      template_path: ''
      notes: fixture
  schedule_field_packets:
    salary:
      status: ready
      summary: ''
      source_refs: []
branch_questions:
  presumptive_route:
    value: false
  audit_applicable:
    value: false
  transfer_pricing_applicable:
    value: false
  director_in_company:
    value: false
  partner_in_firm_or_llp:
    value: false
  foreign_assets_or_signing_authority:
    value: false
  foreign_tax_credit_claimed:
    value: false
  unlisted_shares_held:
    value: false
  refund_account_selected:
    value: true
part_a_general_information:
  filing_status: {}
  taxpayer_profile: {}
  audit_information: {}
bank_details:
  refund_account_choice:
    account_last4: '0861'
    ifsc: ABCD0123456
    source: portal
    status: required
table_rows:
  director_companies: []
  unlisted_equity_rows: []
  capital_gain_rows:
    - asset: MF
      amount: 1
  foreign_asset_rows: []
source_refs: []
review_flags: []
"""
            write_case_fixture(
                case_root,
                portal_packet_text=yaml_portal_packet,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertEqual(errors, [])

    def test_missing_branch_question_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            portal_packet = build_portal_packet()
            del portal_packet["branch_questions"]["partner_in_firm_or_llp"]
            write_case_fixture(case_root, portal_packet=portal_packet)

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("partner_in_firm_or_llp" in error for error in errors),
                errors,
            )

    def test_missing_filing_readiness_file_returns_clean_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(case_root)
            (case_root / "outputs" / "filing-readiness.md").unlink()

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertEqual(
                errors,
                [
                    "outputs/filing-readiness.md is required when execution_mode includes portal draft filling."
                ],
            )

    def test_malformed_portal_packet_returns_clean_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            malformed_packet = """metadata:
  schedule_field_packets:
    salary: [broken
"""
            write_case_fixture(
                case_root,
                portal_packet_text=malformed_packet,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertEqual(len(errors), 1)
            self.assertIn("outputs/portal-field-map.yaml is not valid JSON or YAML", errors[0])

    def test_unsupported_form_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(case_root, likely_itr_form="ITR-5")

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(any("ITR-5" in error for error in errors), errors)

    def test_missing_portal_entry_plan_fails_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(case_root, include_entry_plan=False)

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("outputs/portal-entry-plan.md is required" in error for error in errors),
                errors,
            )

    def test_blank_upload_packet_readiness_stays_blank_and_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(case_root, upload_packet_readiness="")

            readiness = check_portal_packet_module.parse_filing_readiness(
                case_root / "outputs" / "filing-readiness.md"
            )
            self.assertEqual(readiness["upload_packet_readiness"], "")

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("must record upload packet readiness explicitly" in error for error in errors),
                errors,
            )

    def test_missing_schedule_inventory_fails_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(case_root, include_schedule_inventory=False)

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertEqual(
                errors,
                [
                    "outputs/schedule_inventory.yaml is required when execution_mode includes portal draft filling."
                ],
            )

    def test_selected_screen_without_screen_mode_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            schedule_inventory = build_schedule_inventory()
            schedule_inventory["screens"]["Schedule Salary"]["screen_mode"] = ""
            write_case_fixture(case_root, schedule_inventory=schedule_inventory)

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("Screen 'Schedule Salary' uses unknown screen_mode" in error for error in errors),
                errors,
            )

    def test_stale_schedule_without_deselect_or_evidence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            schedule_inventory = build_schedule_inventory()
            schedule_inventory["screens"]["Schedule AL"] = {
                "selected": True,
                "visible": True,
                "applicable": True,
                "screen_mode": "manual_input",
                "why_selected": "Portal shows it.",
                "deselect_if_possible": False,
                "evidence": [],
                "related_schedule_ids": ["al"],
            }
            write_case_fixture(
                case_root,
                persona_modules=["professional_44ada_no_books"],
                schedule_inventory=schedule_inventory,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("Schedule AL is present without explicit applicability evidence." in error for error in errors),
                errors,
            )

    def test_44ada_no_books_cannot_treat_manufacturing_or_oi_as_substantive(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            schedule_inventory = build_schedule_inventory()
            schedule_inventory["screens"]["Part A - Manufacturing Account"]["applicable"] = True
            schedule_inventory["screens"]["Part A - Manufacturing Account"]["screen_mode"] = "manual_input"
            schedule_inventory["screens"]["Part A - OI"]["deselect_if_possible"] = False
            schedule_inventory["screens"]["Part A - OI"]["screen_mode"] = "manual_input"
            write_case_fixture(
                case_root,
                schedule_candidates=["bp"],
                schedule_statuses={"bp": "portal_ready"},
                persona_modules=["professional_44ada_no_books"],
                portal_packet=build_portal_packet(),
                schedule_inventory=schedule_inventory,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("Manufacturing Account cannot be treated as substantive" in error for error in errors),
                errors,
            )
            self.assertTrue(
                any("Part A - OI cannot stay selected by default" in error for error in errors),
                errors,
            )

    def test_review_heavy_screens_left_manual_fail_for_44ada(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            schedule_inventory = build_schedule_inventory()
            schedule_inventory["screens"]["Part B-TI"]["screen_mode"] = "manual_input"
            schedule_inventory["screens"]["Schedule BFLA"]["screen_mode"] = "manual_input"
            write_case_fixture(
                case_root,
                schedule_candidates=["bp", "bfla"],
                schedule_statuses={"bp": "portal_ready", "bfla": "portal_ready"},
                persona_modules=["professional_44ada_no_books"],
                schedule_inventory=schedule_inventory,
                portal_packet=build_portal_packet(),
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("Part B-TI must be review-heavy" in error for error in errors),
                errors,
            )
            self.assertTrue(
                any("Schedule BFLA must be review-heavy" in error for error in errors),
                errors,
            )

    def test_missing_table_rows_for_capital_gains_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            portal_packet = build_portal_packet()
            portal_packet["metadata"]["schedule_field_packets"]["cg"]["status"] = ""
            portal_packet["table_rows"]["capital_gain_rows"] = []
            write_case_fixture(
                case_root,
                schedule_candidates=["cg"],
                schedule_statuses={"cg": "portal_ready"},
                portal_packet=portal_packet,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(any("row set for 'cg'" in error for error in errors), errors)

    def test_prefill_diff_required_after_session_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(
                case_root,
                portal_fill_status="in_progress",
                include_prefill_diff=False,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("portal-prefill-diff.md becomes required" in error for error in errors),
                errors,
            )

    def test_session_log_required_after_session_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir)
            write_case_fixture(
                case_root,
                portal_fill_status="in_progress",
                include_session_log=False,
            )

            errors = check_portal_packet_module.collect_portal_packet_errors(case_root)

            self.assertTrue(
                any("portal-session-log.md becomes required" in error for error in errors),
                errors,
            )


if __name__ == "__main__":
    unittest.main()
