#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("check_schedule_consistency.py")
SPEC = importlib.util.spec_from_file_location("check_schedule_consistency_module", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load consistency-check module from {SCRIPT_PATH}")

check_schedule_consistency_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_schedule_consistency_module)

SKILL_MD = Path(__file__).resolve().parent.parent / "SKILL.md"
FORMS_AND_SCHEDULES_MD = (
    Path(__file__).resolve().parent.parent / "references" / "forms-and-schedules.md"
)


class CheckScheduleConsistencyTests(unittest.TestCase):
    def test_missing_section_four_schedule_bullet_is_reported(self) -> None:
        skill_text = SKILL_MD.read_text(encoding="utf-8")
        forms_text = FORMS_AND_SCHEDULES_MD.read_text(encoding="utf-8")
        broken_forms_text = forms_text.replace(
            "### Special-rate or threshold-driven items\n\n- `SI`\n",
            "### Special-rate or threshold-driven items\n\n",
            1,
        )

        errors = check_schedule_consistency_module.collect_consistency_errors(
            skill_text,
            broken_forms_text,
        )

        self.assertTrue(
            any("schedule_candidates id 'si'" in error for error in errors),
            errors,
        )

    def test_unknown_schedule_like_bullet_is_reported(self) -> None:
        skill_text = SKILL_MD.read_text(encoding="utf-8")
        forms_text = FORMS_AND_SCHEDULES_MD.read_text(encoding="utf-8")
        broken_forms_text = forms_text.replace(
            "### Advanced or niche items\n\n- `AMT`\n- `AMTC`\n",
            "### Advanced or niche items\n\n- `AMT`\n- `AMTC`\n- `XYZ`\n",
            1,
        )

        errors = check_schedule_consistency_module.collect_consistency_errors(
            skill_text,
            broken_forms_text,
        )

        self.assertTrue(
            any("contains schedule-like bullet '`XYZ`'" in error for error in errors),
            errors,
        )

    def test_reference_only_schedule_is_reported(self) -> None:
        skill_text = SKILL_MD.read_text(encoding="utf-8")
        forms_text = FORMS_AND_SCHEDULES_MD.read_text(encoding="utf-8")
        broken_skill_text = skill_text.replace("  - `amtc`\n", "", 1)

        errors = check_schedule_consistency_module.collect_consistency_errors(
            broken_skill_text,
            forms_text,
        )

        self.assertTrue(
            any("documents schedule_candidates id 'amtc'" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
