#!/usr/bin/env python3
"""Fail if SKILL.md's schedule_candidates enum drifts from forms-and-schedules.md.

SKILL.md lists a fixed set of schedule_candidates ids (e.g. `via`, `bfla`) that the agent
uses to profile a case. Those ids only mean something because forms-and-schedules.md section
4 spells out the matching schedules and when they apply. Nothing enforces that the two stay
in sync, so a rename or addition on one side can silently leave the other stale. This script
extracts the schedule_candidates enum, extracts only section 4's schedule bullets, and checks
that the two resolve to the same ids so drift fails loudly instead of quietly confusing
whoever reads SKILL.md next.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_MD = SCRIPT_DIR.parent / "SKILL.md"
FORMS_AND_SCHEDULES_MD = SCRIPT_DIR.parent / "references" / "forms-and-schedules.md"

SCHEDULE_LABEL_TO_ID = {
    "HP": "hp",
    "BP": "bp",
    "CG": "cg",
    "OS": "os",
    "VDA": "vda",
    "EI": "ei",
    "VI-A": "via",
    "SI": "si",
    "AL": "al",
    "FA": "fa",
    "FSI": "fsi",
    "TR": "tr",
    "TCS": "tcs",
    "IT": "it_paid",
    "BFLA": "bfla",
    "CYLA": "cyla",
    "CFL": "cfl",
    "SPI": "spi",
    "PTI": "pti",
    "AMT": "amt",
    "AMTC": "amtc",
}

SPECIAL_REFERENCE_BULLET_TO_ID = {
    "salary schedule": "salary",
    "TDS salary schedule": "tds_salary",
    "TDS on salary": "tds_salary",
    "TDS on other income": "tds_other",
}


def extract_schedule_candidate_ids(skill_md_text: str) -> list[str]:
    match = re.search(
        r"^- `schedule_candidates`\n((?:  - `\w+`\n)+)",
        skill_md_text,
        re.MULTILINE,
    )
    if not match:
        raise ValueError("Could not find a schedule_candidates block in SKILL.md")
    return re.findall(r"^  - `(\w+)`$", match.group(1), re.MULTILINE)


def extract_reference_schedule_section(forms_text: str) -> str:
    match = re.search(
        r"^## 4\. Common schedule candidates by head\n(.*?)(?=^## |\Z)",
        forms_text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(
            "Could not find the '## 4. Common schedule candidates by head' section in "
            "references/forms-and-schedules.md"
        )
    return match.group(1)


def extract_reference_schedule_bullets(forms_text: str) -> list[str]:
    section = extract_reference_schedule_section(forms_text)
    return re.findall(r"^- (.+)$", section, re.MULTILINE)


def reference_bullet_to_schedule_id(bullet: str) -> str | None:
    special_id = SPECIAL_REFERENCE_BULLET_TO_ID.get(bullet)
    if special_id is not None:
        return special_id

    # Match the same token shape is_schedule_like_reference_bullet recognizes (digits
    # allowed) so a label like `26AS` resolves through the map instead of being silently
    # skipped by one check and flagged by the other.
    match = re.match(r"`([A-Z0-9-]+)`(?:$| )", bullet)
    if not match:
        return None
    return SCHEDULE_LABEL_TO_ID.get(match.group(1))


def is_schedule_like_reference_bullet(bullet: str) -> bool:
    return (
        bullet == "salary schedule"
        or bullet.startswith("TDS ")
        or re.match(r"`[A-Z0-9-]+`(?:$| )", bullet) is not None
    )


def collect_consistency_errors(skill_md_text: str, forms_text: str) -> list[str]:
    ids = extract_schedule_candidate_ids(skill_md_text)
    reference_bullets = extract_reference_schedule_bullets(forms_text)

    errors = []
    documented_ids = set()

    for bullet in reference_bullets:
        schedule_id = reference_bullet_to_schedule_id(bullet)
        if schedule_id is None:
            if is_schedule_like_reference_bullet(bullet):
                errors.append(
                    "references/forms-and-schedules.md section 4 contains schedule-like "
                    f"bullet {bullet!r}, but this script does not know how to map it to a "
                    "schedule_candidates id. Update the parser or the docs together."
                )
            continue
        documented_ids.add(schedule_id)

    for schedule_id in ids:
        if schedule_id not in documented_ids:
            errors.append(
                f"schedule_candidates id '{schedule_id}' in SKILL.md is not documented by a "
                "matching section-4 bullet in references/forms-and-schedules.md."
            )

    undocumented_reference_ids = documented_ids - set(ids)
    for stale_id in sorted(undocumented_reference_ids):
        errors.append(
            "references/forms-and-schedules.md documents schedule_candidates id "
            f"'{stale_id}' in section 4, but SKILL.md no longer lists it in "
            "schedule_candidates."
        )
    return errors


def main() -> int:
    skill_md_text = SKILL_MD.read_text(encoding="utf-8")
    forms_text = FORMS_AND_SCHEDULES_MD.read_text(encoding="utf-8")
    ids = extract_schedule_candidate_ids(skill_md_text)

    errors = collect_consistency_errors(skill_md_text, forms_text)

    if errors:
        print("Schedule consistency check failed:\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(ids)} schedule_candidates ids all resolve to documented labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
