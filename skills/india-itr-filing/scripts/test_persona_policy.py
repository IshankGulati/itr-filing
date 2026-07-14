#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path

import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from persona_policy import compose_persona_policy


FIXTURE_PATH = SCRIPT_DIR / "fixtures" / "persona_policy_cases.json"


class PersonaPolicyTests(unittest.TestCase):
    def test_fixture_cases(self) -> None:
        cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

        for case in cases:
            with self.subTest(case=case["name"]):
                policy = compose_persona_policy(case["modules"])

                for schedule_id in case.get("must_select_contains", []):
                    self.assertIn(schedule_id, policy["must_select"])

                for screen_name in case.get("must_deselect_contains", []):
                    self.assertIn(screen_name, policy["must_deselect_if_present"])

                for screen_name, screen_mode in case.get("screen_modes", {}).items():
                    self.assertIn(screen_name, policy["screen_policies"])
                    self.assertEqual(
                        policy["screen_policies"][screen_name]["screen_mode"],
                        screen_mode,
                    )

                for phrase in case.get("stale_rules_contains", []):
                    self.assertTrue(
                        any(
                            phrase in rule
                            for rule in policy["stale_prefill_cleanup_rules"]
                        ),
                        policy["stale_prefill_cleanup_rules"],
                    )

                for packet_id in case.get("upload_packets_contains", []):
                    self.assertIn(packet_id, policy["upload_packets"])


if __name__ == "__main__":
    unittest.main()
