#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


PORTAL_EXECUTION_MODES = {
    "portal_draft_fill",
    "utility_json_and_portal_draft_fill",
}

SUPPORTED_PORTAL_FORMS = {
    "ITR-1",
    "ITR-2",
    "ITR-3",
    "ITR-4",
}

READY_SCHEDULE_STATUSES = {
    "filing_ready",
    "portal_ready",
}

REQUIRED_TOP_LEVEL_PORTAL_KEYS = {
    "metadata",
    "branch_questions",
    "part_a_general_information",
    "bank_details",
    "table_rows",
    "source_refs",
    "review_flags",
}

REQUIRED_BRANCH_QUESTIONS = [
    "presumptive_route",
    "audit_applicable",
    "transfer_pricing_applicable",
    "director_in_company",
    "partner_in_firm_or_llp",
    "foreign_assets_or_signing_authority",
    "foreign_tax_credit_claimed",
    "unlisted_shares_held",
    "refund_account_selected",
]

STARTED_PORTAL_STATUSES = {
    "in_progress",
    "paused",
    "ready_for_user_review",
    "completed_pending_user_submit",
    "abandoned",
}

SECTION_STATUS_HEADINGS = {
    "salary": "Salary",
    "hp": "House property (`HP`)",
    "bp": "Business or profession (`BP`)",
    "cg": "Capital gains (`CG`)",
    "os": "Other sources (`OS`)",
    "via": "Deductions and reliefs (`VI-A`)",
}

GROUPED_STATUS_HEADINGS = {
    "Special-rate and threshold-driven sections": {
        "vda": "`VDA`",
        "ei": "`EI`",
        "si": "`SI`",
        "al": "`AL`",
    },
    "Credits and taxes paid": {
        "tds_salary": "TDS on salary",
        "tds_other": "TDS on other income",
        "tcs": "`TCS`",
        "it_paid": "`IT`",
    },
    "Foreign schedules": {
        "fa": "`FA`",
        "fsi": "`FSI`",
        "tr": "`TR`",
    },
    "Set-off and carry forward": {
        "bfla": "`BFLA`",
        "cyla": "`CYLA`",
        "cfl": "`CFL`",
    },
    "Other advanced schedules": {
        "spi": "`SPI`",
        "pti": "`PTI`",
        "amt": "`AMT`",
        "amtc": "`AMTC`",
    },
}

TABLE_ROW_REQUIREMENTS = {
    "cg": "capital_gain_rows",
    "fa": "foreign_asset_rows",
}

CONDITIONAL_TABLE_REQUIREMENTS = {
    "director_in_company": "director_companies",
    "unlisted_shares_held": "unlisted_equity_rows",
}

REQUIRED_READINESS_FILES = {
    "outputs/portal-entry-plan.md": "portal entry plan",
}


class PortalPacketValidationError(Exception):
    """Raised when the portal packet inputs are missing or malformed."""


def normalize_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    return value


def parse_top_level_scalar(text: str, key: str, default: str = "") -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if match is None:
        return default
    return normalize_scalar(match.group(1))


def parse_yaml_list(text: str, key: str) -> list[str]:
    inline_match = re.search(rf"^{re.escape(key)}:\s*\[(.*?)\]\s*$", text, re.MULTILINE)
    if inline_match is not None:
        inner = inline_match.group(1).strip()
        if not inner:
            return []
        return [
            normalize_scalar(item.strip()).strip("`")
            for item in inner.split(",")
            if item.strip()
        ]

    block_match = re.search(rf"^{re.escape(key)}:\s*$", text, re.MULTILINE)
    if block_match is None:
        return []

    items: list[str] = []
    lines = text[block_match.end() :].splitlines()
    for line in lines:
        if not line.strip():
            if items:
                break
            continue
        if not line.startswith("  - "):
            break
        items.append(normalize_scalar(line[4:].strip()).strip("`"))
    return items


def read_required_text(path: Path, display_name: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise PortalPacketValidationError(
            f"{display_name} is required when execution_mode includes portal draft filling."
        ) from None
    except OSError as exc:
        raise PortalPacketValidationError(
            f"Could not read {display_name}: {exc}."
        ) from None


def parse_profile(path: Path) -> dict[str, object]:
    text = read_required_text(path, "profile.yaml")
    return {
        "execution_mode": parse_top_level_scalar(text, "execution_mode", "none"),
        "portal_fill_status": parse_top_level_scalar(
            text,
            "portal_fill_status",
            "not_offered",
        ),
        "likely_itr_form": parse_top_level_scalar(text, "likely_itr_form", ""),
        "schedule_candidates": parse_yaml_list(text, "schedule_candidates"),
    }


def split_level_three_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None

    for line in text.splitlines():
        if line.startswith("### "):
            current_heading = line[4:].strip()
            sections[current_heading] = []
            continue
        if current_heading is not None:
            sections[current_heading].append(line)

    return {
        heading: "\n".join(lines).strip()
        for heading, lines in sections.items()
    }


def extract_section_status(section_body: str) -> str:
    match = re.search(r"^- Status:\s*(.*)$", section_body, re.MULTILINE)
    if match is None:
        return ""
    return normalize_scalar(match.group(1))


def extract_grouped_status(section_body: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.*)$", section_body, re.MULTILINE)
    if match is None:
        return ""
    return normalize_scalar(match.group(1))


def parse_schedule_statuses(path: Path) -> dict[str, str]:
    text = read_required_text(path, "schedule_map.md")
    sections = split_level_three_sections(text)
    statuses: dict[str, str] = {}

    for schedule_id, heading in SECTION_STATUS_HEADINGS.items():
        statuses[schedule_id] = extract_section_status(sections.get(heading, ""))

    for heading, mapping in GROUPED_STATUS_HEADINGS.items():
        section_body = sections.get(heading, "")
        for schedule_id, label in mapping.items():
            statuses[schedule_id] = extract_grouped_status(section_body, label)

    return statuses


def parse_filing_readiness(path: Path) -> str:
    text = read_required_text(path, "outputs/filing-readiness.md")
    match = re.search(
        r"^- Ready for manual portal or utility entry:\s*(.*)$",
        text,
        re.MULTILINE,
    )
    if match is None:
        return ""
    return normalize_scalar(match.group(1))


def is_truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"yes", "true", "ready"}


def load_portal_field_map(path: Path) -> dict[str, object]:
    text = read_required_text(path, "outputs/portal-field-map.yaml")

    try:
        loaded = json.loads(text)
    except json.JSONDecodeError as json_error:
        if yaml is None:
            raise PortalPacketValidationError(
                "outputs/portal-field-map.yaml is not valid JSON, and YAML parsing is "
                f"unavailable in this environment: {json_error.msg}."
            ) from None
        try:
            loaded = yaml.safe_load(text)
        except yaml.YAMLError as yaml_error:
            raise PortalPacketValidationError(
                "outputs/portal-field-map.yaml is not valid JSON or YAML: "
                f"{yaml_error}."
            ) from None

    if not isinstance(loaded, dict):
        raise PortalPacketValidationError(
            "outputs/portal-field-map.yaml must decode to a top-level mapping/object."
        )

    return loaded


def branch_value(entry: object) -> object:
    if isinstance(entry, dict):
        return entry.get("value")
    return entry


def normalize_status(value: str) -> str:
    return value.strip().lower()


def collect_portal_packet_errors(case_root: Path) -> list[str]:
    try:
        profile = parse_profile(case_root / "profile.yaml")
        execution_mode = str(profile["execution_mode"])

        if execution_mode not in PORTAL_EXECUTION_MODES:
            return []

        errors: list[str] = []
        likely_itr_form = str(profile["likely_itr_form"]).strip()
        if likely_itr_form not in SUPPORTED_PORTAL_FORMS:
            errors.append(
                "Portal draft filling supports only ITR-1 through ITR-4; "
                f"found '{likely_itr_form or 'unknown'}'."
            )

        readiness_value = parse_filing_readiness(
            case_root / "outputs" / "filing-readiness.md"
        )
        if not is_truthy(readiness_value):
            errors.append(
                "outputs/filing-readiness.md must explicitly mark the case ready for manual "
                "portal or utility entry before portal drafting."
            )

        schedule_statuses = parse_schedule_statuses(case_root / "schedule_map.md")
        schedule_candidates = [
            str(item).strip()
            for item in profile["schedule_candidates"]
            if str(item).strip()
        ]

        portal_field_map = load_portal_field_map(
            case_root / "outputs" / "portal-field-map.yaml"
        )
        missing_top_level_keys = REQUIRED_TOP_LEVEL_PORTAL_KEYS - set(portal_field_map)
        if missing_top_level_keys:
            errors.append(
                "outputs/portal-field-map.yaml is missing top-level keys: "
                + ", ".join(sorted(missing_top_level_keys))
            )
            return errors

        for relative_path, display_name in REQUIRED_READINESS_FILES.items():
            if not (case_root / relative_path).exists():
                errors.append(
                    f"{relative_path} is required as part of the {display_name} readiness gate."
                )

        metadata = portal_field_map.get("metadata", {})
        schedule_field_packets = {}
        if isinstance(metadata, dict):
            schedule_field_packets = metadata.get("schedule_field_packets", {})
        if not isinstance(schedule_field_packets, dict):
            schedule_field_packets = {}

        branch_questions = portal_field_map.get("branch_questions", {})
        if not isinstance(branch_questions, dict):
            branch_questions = {}

        bank_details = portal_field_map.get("bank_details", {})
        if not isinstance(bank_details, dict):
            bank_details = {}

        table_rows = portal_field_map.get("table_rows", {})
        if not isinstance(table_rows, dict):
            table_rows = {}

        for question_id in REQUIRED_BRANCH_QUESTIONS:
            if question_id not in branch_questions:
                errors.append(
                    "outputs/portal-field-map.yaml is missing required branch question "
                    f"'{question_id}'."
                )
                continue
            if branch_value(branch_questions[question_id]) is None:
                errors.append(
                    f"Branch question '{question_id}' must have an explicit true/false value."
                )

        refund_choice = bank_details.get("refund_account_choice", {})
        if not isinstance(refund_choice, dict):
            refund_choice = {}
        if not normalize_scalar(str(refund_choice.get("account_last4", ""))):
            errors.append(
                "bank_details.refund_account_choice.account_last4 must be filled before portal drafting."
            )

        for schedule_id in schedule_candidates:
            schedule_status = normalize_status(schedule_statuses.get(schedule_id, ""))
            if schedule_status not in READY_SCHEDULE_STATUSES:
                errors.append(
                    f"Schedule '{schedule_id}' must be marked filing_ready or portal_ready in schedule_map.md."
                )

            packet = schedule_field_packets.get(schedule_id, {})
            packet_ready = isinstance(packet, dict) and normalize_status(
                str(packet.get("status", ""))
            ) == "ready"

            table_key = TABLE_ROW_REQUIREMENTS.get(schedule_id)
            table_ready = False
            if table_key is not None:
                rows = table_rows.get(table_key, [])
                table_ready = isinstance(rows, list) and len(rows) > 0

            if not packet_ready and not table_ready:
                if table_key is None:
                    errors.append(
                        "outputs/portal-field-map.yaml is missing a ready schedule field packet "
                        f"for '{schedule_id}'."
                    )
                else:
                    errors.append(
                        "outputs/portal-field-map.yaml is missing a ready schedule field packet "
                        f"or row set for '{schedule_id}'."
                    )

        for branch_key, table_key in CONDITIONAL_TABLE_REQUIREMENTS.items():
            if branch_value(branch_questions.get(branch_key)) is True:
                rows = table_rows.get(table_key, [])
                if not isinstance(rows, list) or len(rows) == 0:
                    errors.append(
                        f"table_rows.{table_key} must contain at least one row when '{branch_key}' is true."
                    )

        portal_fill_status = str(profile["portal_fill_status"]).strip()
        prefill_diff_path = case_root / "outputs" / "portal-prefill-diff.md"
        if portal_fill_status in STARTED_PORTAL_STATUSES and not prefill_diff_path.exists():
            errors.append(
                "outputs/portal-prefill-diff.md becomes required after a live portal session has started."
            )

        session_log_path = case_root / "outputs" / "portal-session-log.md"
        if portal_fill_status in STARTED_PORTAL_STATUSES and not session_log_path.exists():
            errors.append(
                "outputs/portal-session-log.md becomes required after a live portal session has started."
            )

        return errors
    except PortalPacketValidationError as exc:
        return [str(exc)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that a portal draft packet is ready for live portal entry.",
    )
    parser.add_argument(
        "case_root",
        nargs="?",
        default=".",
        help="Path to the case workspace",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    case_root = Path(args.case_root).expanduser()
    try:
        errors = collect_portal_packet_errors(case_root)
    except Exception as exc:  # pragma: no cover - defensive UX fallback
        print(f"ERROR: unexpected validator failure: {exc.__class__.__name__}: {exc}")
        sys.exit(1)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("OK: portal packet is ready for the configured execution mode.")


if __name__ == "__main__":
    main()
