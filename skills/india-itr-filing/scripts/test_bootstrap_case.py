#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
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
            )

            schedule_map = (case_root / "schedule_map.md").read_text(encoding="utf-8")

            self.assertIn("## Core schedule candidates", schedule_map)
            self.assertNotIn("### Foreign schedules", schedule_map)
            # A simple workpaper case stays lean (no JSON scaffold) but still tracks readiness.
            self.assertFalse((case_root / "outputs" / "itr-draft.json").exists())
            self.assertFalse((case_root / "outputs" / "validation-notes.md").exists())
            self.assertTrue((case_root / "outputs" / "filing-readiness.md").exists())

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
            )

            schedule_map = (case_root / "schedule_map.md").read_text(encoding="utf-8")

            self.assertIn("### Deductions and reliefs (`VI-A`)", schedule_map)
            self.assertIn("- `SI`:", schedule_map)
            self.assertIn("- `AL`:", schedule_map)
            self.assertTrue((case_root / "outputs" / "itr-draft.json").exists())
            self.assertTrue((case_root / "outputs" / "validation-notes.md").exists())
            self.assertTrue((case_root / "outputs" / "filing-readiness.md").exists())


if __name__ == "__main__":
    unittest.main()
