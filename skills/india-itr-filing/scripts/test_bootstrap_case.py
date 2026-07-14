#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("bootstrap_case.py")
SPEC = importlib.util.spec_from_file_location("bootstrap_case_module", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load bootstrap module from {SCRIPT_PATH}")

bootstrap_case_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bootstrap_case_module)


class BootstrapCaseTests(unittest.TestCase):
    def test_default_regime_position(self) -> None:
        self.assertEqual(
            bootstrap_case_module.default_regime_position("AY 2026-27"),
            "default_new",
        )
        self.assertEqual(
            bootstrap_case_module.default_regime_position("AY 2023-24"),
            "unknown",
        )

    def test_simple_workpaper_case_stays_lean(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir) / "simple-case"
            bootstrap_case_module.bootstrap_case(
                case_root,
                "FY_2025-26",
                "AY 2026-27",
                False,
                "simple",
                "return_workpaper_pack",
                "none",
            )

            schedule_map = (case_root / "schedule_map.md").read_text(encoding="utf-8")
            profile = (case_root / "profile.yaml").read_text(encoding="utf-8")

            self.assertIn("## Core schedule candidates", schedule_map)
            self.assertNotIn("### Foreign schedules", schedule_map)
            self.assertTrue((case_root / "inputs" / "salary").exists())
            self.assertTrue((case_root / "inputs" / "investments").exists())
            self.assertFalse((case_root / "inputs" / "capital_gains").exists())
            self.assertFalse((case_root / "inputs" / "deductions").exists())
            self.assertFalse((case_root / "inputs" / "foreign").exists())
            self.assertFalse((case_root / "inputs" / "business").exists())
            self.assertFalse((case_root / "inputs" / "prior_year").exists())
            self.assertFalse((case_root / "inputs" / "portal_anchors").exists())
            self.assertFalse((case_root / "outputs" / "itr-draft.json").exists())
            self.assertFalse((case_root / "outputs" / "validation-notes.md").exists())
            self.assertTrue((case_root / "outputs" / "filing-readiness.md").exists())
            self.assertFalse((case_root / "outputs" / "portal-field-map.yaml").exists())
            self.assertTrue((case_root / "case_learnings.md").exists())
            self.assertIn("execution_mode: none", profile)
            self.assertIn("portal_fill_status: not_offered", profile)
            self.assertIn("persona_modules: []", profile)

    def test_json_targeted_case_gets_full_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir) / "json-case"
            bootstrap_case_module.bootstrap_case(
                case_root,
                "FY_2025-26",
                "AY 2026-27",
                False,
                "complex",
                "json_draft_if_feasible",
                "none",
            )

            schedule_map = (case_root / "schedule_map.md").read_text(encoding="utf-8")

            self.assertIn("### Deductions and reliefs (`VI-A`)", schedule_map)
            self.assertIn("- `SI`:", schedule_map)
            self.assertIn("- `AL`:", schedule_map)
            self.assertTrue((case_root / "inputs" / "salary").exists())
            self.assertTrue((case_root / "inputs" / "business").exists())
            self.assertTrue((case_root / "inputs" / "investments").exists())
            self.assertTrue((case_root / "inputs" / "foreign").exists())
            self.assertTrue((case_root / "inputs" / "prior_year").exists())
            self.assertTrue((case_root / "inputs" / "portal_anchors").exists())
            self.assertTrue((case_root / "outputs" / "itr-draft.json").exists())
            self.assertTrue((case_root / "outputs" / "validation-notes.md").exists())
            self.assertTrue((case_root / "outputs" / "filing-readiness.md").exists())
            self.assertFalse((case_root / "outputs" / "portal-field-map.yaml").exists())

    def test_portal_enabled_case_gets_portal_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir) / "portal-case"
            bootstrap_case_module.bootstrap_case(
                case_root,
                "FY_2025-26",
                "AY 2026-27",
                False,
                "simple",
                "return_workpaper_pack",
                "portal_draft_fill",
            )

            profile = (case_root / "profile.yaml").read_text(encoding="utf-8")
            portal_packet = json.loads(
                (case_root / "outputs" / "portal-field-map.yaml").read_text(
                    encoding="utf-8"
                )
            )

            self.assertTrue((case_root / "inputs" / "salary").exists())
            self.assertTrue((case_root / "inputs" / "investments").exists())
            self.assertTrue((case_root / "inputs" / "portal_anchors").exists())
            self.assertFalse((case_root / "inputs" / "business").exists())
            self.assertFalse((case_root / "inputs" / "foreign").exists())
            self.assertFalse((case_root / "outputs" / "itr-draft.json").exists())
            self.assertTrue((case_root / "outputs" / "filing-readiness.md").exists())
            self.assertTrue((case_root / "outputs" / "portal-field-map.yaml").exists())
            self.assertTrue((case_root / "outputs" / "schedule_inventory.yaml").exists())
            self.assertTrue((case_root / "outputs" / "portal-entry-plan.md").exists())
            self.assertTrue((case_root / "outputs" / "review_only_schedules.md").exists())
            self.assertTrue((case_root / "outputs" / "portal-session-log.md").exists())
            self.assertTrue((case_root / "outputs" / "portal-prefill-diff.md").exists())
            self.assertTrue((case_root / "outputs" / "upload_packets" / "README.md").exists())
            self.assertTrue((case_root / "outputs" / "upload_packets" / "112a-status.md").exists())
            self.assertIn("execution_mode: portal_draft_fill", profile)
            self.assertIn("preferred_browser: unknown", profile)
            self.assertIn("persona_modules: []", profile)
            self.assertIn("- login", profile)
            schedule_inventory = json.loads(
                (case_root / "outputs" / "schedule_inventory.yaml").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                sorted(portal_packet.keys()),
                sorted(
                    [
                        "metadata",
                        "branch_questions",
                        "part_a_general_information",
                        "bank_details",
                        "table_rows",
                        "source_refs",
                        "review_flags",
                    ]
                ),
            )
            self.assertIn("active_persona_modules", portal_packet["metadata"])
            self.assertIn("selection_audit_complete", portal_packet["metadata"])
            self.assertIn("upload_packets", portal_packet["metadata"])
            self.assertIn("screens", schedule_inventory)
            self.assertIn("metadata", schedule_inventory)
            self.assertIn(
                "Part A - Manufacturing Account",
                schedule_inventory["screens"],
            )
            self.assertIn(
                "Schedule SI",
                schedule_inventory["screens"],
            )
            self.assertIn(
                "## Part B-TI",
                (case_root / "outputs" / "review_only_schedules.md").read_text(
                    encoding="utf-8"
                ),
            )

    def test_combined_execution_mode_creates_json_and_portal_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_root = Path(tmpdir) / "combined-case"
            bootstrap_case_module.bootstrap_case(
                case_root,
                "FY_2025-26",
                "AY 2026-27",
                False,
                "moderate",
                "return_workpaper_pack",
                "utility_json_and_portal_draft_fill",
            )

            self.assertTrue((case_root / "outputs" / "itr-draft.json").exists())
            self.assertTrue((case_root / "outputs" / "validation-notes.md").exists())
            self.assertTrue((case_root / "outputs" / "portal-field-map.yaml").exists())
            self.assertTrue((case_root / "inputs" / "portal_anchors").exists())


if __name__ == "__main__":
    unittest.main()
