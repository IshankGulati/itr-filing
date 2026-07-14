#!/usr/bin/env python3
"""Shared persona and portal-screen policy for india-itr-filing.

This module is intentionally stdlib-only so both the bootstrap and validator
scripts can share one machine-readable source of truth without depending on a
package install step.
"""

from __future__ import annotations

from copy import deepcopy


SCREEN_MODE_CHOICES = [
    "manual_input",
    "review_only",
    "auto_derived",
    "mandatory_visible_zero_confirm",
    "not_applicable_visible",
    "blocked",
]

REVIEW_HEAVY_SCREEN_MODES = {
    "review_only",
    "auto_derived",
    "mandatory_visible_zero_confirm",
}

TARGET_COMPOSITE_PERSONA_MODULES = [
    "salary_basic",
    "professional_44ada_no_books",
    "domestic_cap_gains",
    "domestic_112a",
    "domestic_other_sources",
    "foreign_assets",
    "foreign_income",
    "foreign_tax_credit",
    "prior_year_loss_setoff",
    "director_disclosure",
    "unlisted_equity_disclosure",
]

TARGET_COMPOSITE_STARTER_PROFILE = (
    "salary_plus_44ada_no_books_plus_domestic_and_foreign_investments"
)

NO_BOOKS_FAST_PATH_SCREENS = {
    "Part A - Balance Sheet",
    "Part A - P & L",
}

NO_BOOKS_NON_SUBSTANTIVE_SCREENS = {
    "Part A - Manufacturing Account",
    "Part A - Trading Account",
}

STALE_SELECTION_SCREEN_NAMES = {
    "Part A - OI",
    "Schedule UD",
    "Schedule AL",
    "Schedule AMTC",
    "Schedule 80-IB",
    "Schedule 80-IE",
}

DERIVED_OR_FAST_PATH_SCREEN_NAMES = {
    "Part B-TI",
    "Part B-TTI",
    "Tax Paid",
    "Schedule SI",
    "Schedule CYLA",
    "Schedule BFLA",
    "Schedule CFL",
}


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _screen(
    selected: bool,
    visible: bool,
    applicable: bool,
    screen_mode: str,
    why_selected: str,
    *,
    deselect_if_possible: bool = False,
    evidence: list[str] | None = None,
    related_schedule_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "selected": selected,
        "visible": visible,
        "applicable": applicable,
        "screen_mode": screen_mode,
        "why_selected": why_selected,
        "deselect_if_possible": deselect_if_possible,
        "evidence": evidence or [],
        "related_schedule_ids": related_schedule_ids or [],
    }


PERSONA_MODULES: dict[str, dict[str, object]] = {
    "salary_basic": {
        "triggers": [
            "resident or ordinarily resident salary or pension income",
            "salary work remains in scope even when ITR-3 is driven by another module",
        ],
        "likely_itr_form_impact": "Keeps salary schedules in scope across ITR-1, ITR-2, or ITR-3.",
        "required_documents": [
            "Form 16",
            "AIS",
            "TIS",
            "26AS",
        ],
        "must_select": ["salary"],
        "can_select": ["tds_salary"],
        "must_deselect_if_present": [],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Part A - General": _screen(
                True,
                True,
                True,
                "manual_input",
                "General profile answers and branch-driving personal facts still need review.",
                related_schedule_ids=[],
            ),
            "Schedule Salary": _screen(
                True,
                True,
                True,
                "manual_input",
                "Salary rows carry source-driven figures from Form 16 and AIS reconciliation.",
                related_schedule_ids=["salary"],
            ),
        },
        "upload_packets": {},
    },
    "professional_44ada_no_books": {
        "triggers": [
            "professional receipts returned on a presumptive 44ADA basis",
            "no regular books path despite ITR-3 portal routing",
        ],
        "likely_itr_form_impact": "Often forces ITR-3 while still keeping business screens on a no-books fast path.",
        "required_documents": [
            "gross receipt support",
            "Form 16A where available",
            "bank trail",
            "presumptive computation note",
        ],
        "must_select": ["bp"],
        "can_select": ["tds_other", "si", "cyla", "bfla", "cfl"],
        "must_deselect_if_present": [
            "Part A - Manufacturing Account",
            "Part A - Trading Account",
            "Part A - OI",
            "Schedule UD",
        ],
        "derived_schedules": [
            "Part B-TI",
            "Part B-TTI",
            "Tax Paid",
            "Schedule SI",
            "Schedule CYLA",
            "Schedule BFLA",
            "Schedule CFL",
        ],
        "stale_prefill_cleanup_rules": [
            "Treat Manufacturing Account, Trading Account, OI, and UD as stale or non-substantive unless a regular-books or audit path is proven.",
            "Mandatory portal visibility does not convert Balance Sheet or P&L into regular-books data entry for this persona.",
        ],
        "screen_policies": {
            "Schedule BP": _screen(
                True,
                True,
                True,
                "manual_input",
                "Presumptive 44ADA business or profession figures still need direct entry.",
                related_schedule_ids=["bp"],
            ),
            "Part A - Balance Sheet": _screen(
                True,
                True,
                True,
                "mandatory_visible_zero_confirm",
                "ITR-3 may keep the screen visible, but this persona usually follows a minimal zero-confirm path.",
                related_schedule_ids=["bp"],
            ),
            "Part A - P & L": _screen(
                True,
                True,
                True,
                "mandatory_visible_zero_confirm",
                "ITR-3 may keep the screen visible, but this persona usually follows a minimal zero-confirm path.",
                related_schedule_ids=["bp"],
            ),
            "Part A - Manufacturing Account": _screen(
                True,
                True,
                False,
                "not_applicable_visible",
                "This is a stale or portal-overselected screen for a no-books professional persona.",
                deselect_if_possible=True,
                related_schedule_ids=["bp"],
            ),
            "Part A - Trading Account": _screen(
                True,
                True,
                False,
                "not_applicable_visible",
                "This is a stale or portal-overselected screen for a no-books professional persona.",
                deselect_if_possible=True,
                related_schedule_ids=["bp"],
            ),
            "Part A - OI": _screen(
                True,
                True,
                False,
                "not_applicable_visible",
                "Do not keep OI selected by default unless audit or a regular-books path is actually in scope.",
                deselect_if_possible=True,
                related_schedule_ids=["bp"],
            ),
            "Schedule UD": _screen(
                True,
                True,
                False,
                "not_applicable_visible",
                "Unabsorbed depreciation should stay out unless real carryforward evidence exists.",
                deselect_if_possible=True,
                related_schedule_ids=["bp"],
            ),
            "Part B-TI": _screen(
                True,
                True,
                True,
                "review_only",
                "Treat total income as a derived review checkpoint after underlying schedules are entered.",
                related_schedule_ids=["bp", "cg", "os", "fsi", "tr"],
            ),
            "Part B-TTI": _screen(
                True,
                True,
                True,
                "review_only",
                "Treat tax computation as a derived review checkpoint after underlying schedules are entered.",
                related_schedule_ids=["bp", "cg", "os", "fsi", "tr"],
            ),
            "Tax Paid": _screen(
                True,
                True,
                True,
                "review_only",
                "Tax paid is typically a review-heavy or imported screen rather than a first-pass manual destination.",
                related_schedule_ids=["tds_other", "tds_salary", "it_paid", "tcs"],
            ),
            "Schedule SI": _screen(
                True,
                True,
                True,
                "auto_derived",
                "Special-rate computations should usually derive from CG and related rows.",
                related_schedule_ids=["si", "cg"],
            ),
            "Schedule CYLA": _screen(
                True,
                True,
                True,
                "auto_derived",
                "Current-year loss adjustment should usually be review-only unless the portal forces an explicit confirmation.",
                related_schedule_ids=["cyla", "cg", "os"],
            ),
            "Schedule BFLA": _screen(
                True,
                True,
                True,
                "review_only",
                "Brought-forward set-off should be reviewed against prior-year evidence, not treated as generic manual drafting.",
                related_schedule_ids=["bfla", "cg"],
            ),
            "Schedule CFL": _screen(
                False,
                False,
                False,
                "review_only",
                "Only keep CFL in scope if recomputation genuinely leaves a carry-forward balance.",
                related_schedule_ids=["cfl", "cg"],
            ),
        },
        "upload_packets": {},
    },
    "domestic_cap_gains": {
        "triggers": [
            "domestic broker or mutual-fund capital gains",
            "capital gains rows drive SI and potential set-off schedules",
        ],
        "likely_itr_form_impact": "Keeps CG and downstream special-rate schedules in scope.",
        "required_documents": [
            "broker capital-gains report",
            "mutual-fund gains statement",
            "contract-note or lot-level support where needed",
        ],
        "must_select": ["cg"],
        "can_select": ["si", "cyla", "bfla", "cfl"],
        "must_deselect_if_present": [],
        "derived_schedules": [
            "Schedule SI",
            "Schedule CYLA",
            "Schedule BFLA",
            "Schedule CFL",
        ],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Schedule CG": _screen(
                True,
                True,
                True,
                "manual_input",
                "Capital gains rows are substantive portal work.",
                related_schedule_ids=["cg"],
            ),
        },
        "upload_packets": {},
    },
    "domestic_112a": {
        "triggers": [
            "listed equity or equity-oriented fund LTCG taxed under 112A",
        ],
        "likely_itr_form_impact": "Extends CG handling with 112A rows or upload support.",
        "required_documents": [
            "112A-compatible broker or fund lot summary",
            "supporting transaction export when portal upload is unavailable",
        ],
        "must_select": [],
        "can_select": ["cg", "si"],
        "must_deselect_if_present": [],
        "derived_schedules": ["Schedule SI"],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Schedule 112A": _screen(
                True,
                True,
                True,
                "manual_input",
                "112A rows remain substantive even when a future CSV import path exists.",
                related_schedule_ids=["cg", "si"],
            ),
        },
        "upload_packets": {
            "112a_csv": {
                "status": "scaffold_only",
                "notes": "Actual CSV generation requires a checked-in or user-supplied portal template.",
            }
        },
    },
    "domestic_other_sources": {
        "triggers": [
            "domestic interest, dividend, or other routine taxable receipts",
        ],
        "likely_itr_form_impact": "Keeps OS in scope and often activates TDS-on-other-income review.",
        "required_documents": [
            "bank interest statements",
            "dividend reports",
            "AIS",
            "26AS",
        ],
        "must_select": ["os"],
        "can_select": ["tds_other"],
        "must_deselect_if_present": [],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Schedule OS": _screen(
                True,
                True,
                True,
                "manual_input",
                "Other sources usually require direct figure entry or review of prefilled values.",
                related_schedule_ids=["os"],
            ),
        },
        "upload_packets": {},
    },
    "foreign_assets": {
        "triggers": [
            "foreign holdings or signing-authority answers make FA applicable",
        ],
        "likely_itr_form_impact": "Foreign-asset disclosures usually keep ITR-2 or ITR-3 in scope.",
        "required_documents": [
            "foreign broker holdings statement",
            "calendar-year holding support",
            "prior-year FA workpaper where relevant",
        ],
        "must_select": ["fa"],
        "can_select": [],
        "must_deselect_if_present": [],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Schedule FA": _screen(
                True,
                True,
                True,
                "manual_input",
                "Foreign asset rows are substantive because calendar-year disclosure detail matters.",
                related_schedule_ids=["fa"],
            ),
        },
        "upload_packets": {},
    },
    "foreign_income": {
        "triggers": [
            "foreign dividends, interest, or other foreign-source income",
        ],
        "likely_itr_form_impact": "Keeps FSI in scope and can activate TR when FTC is claimed.",
        "required_documents": [
            "foreign broker income statement",
            "withholding report where available",
        ],
        "must_select": ["fsi"],
        "can_select": [],
        "must_deselect_if_present": [],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Schedule FSI": _screen(
                True,
                True,
                True,
                "manual_input",
                "Foreign-source income requires direct reconciliation into FSI rows.",
                related_schedule_ids=["fsi"],
            ),
        },
        "upload_packets": {},
    },
    "foreign_tax_credit": {
        "triggers": [
            "foreign withholding or FTC claim",
        ],
        "likely_itr_form_impact": "Keeps TR and Form 67 coordination in scope.",
        "required_documents": [
            "foreign withholding summary",
            "FTC workpaper",
            "Form 67 support",
        ],
        "must_select": ["tr"],
        "can_select": ["fsi"],
        "must_deselect_if_present": ["Schedule AMTC"],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [
            "AMTC is unrelated to a normal FTC path and should stay out unless AMT credit history exists.",
        ],
        "screen_policies": {
            "Schedule TR": _screen(
                True,
                True,
                True,
                "manual_input",
                "FTC rows require direct treaty and withholding evidence.",
                related_schedule_ids=["tr"],
            ),
            "Schedule AMTC": _screen(
                True,
                True,
                False,
                "not_applicable_visible",
                "AMTC is stale or unrelated unless there is real AMT credit history.",
                deselect_if_possible=True,
                related_schedule_ids=["amtc"],
            ),
        },
        "upload_packets": {},
    },
    "prior_year_loss_setoff": {
        "triggers": [
            "brought-forward loss evidence from prior-year returns",
        ],
        "likely_itr_form_impact": "Activates BFLA and sometimes CFL review.",
        "required_documents": [
            "prior-year filed return or JSON",
            "loss carryforward workpaper",
        ],
        "must_select": ["bfla"],
        "can_select": ["cfl", "cyla"],
        "must_deselect_if_present": [],
        "derived_schedules": [
            "Schedule BFLA",
            "Schedule CFL",
        ],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {},
        "upload_packets": {},
    },
    "director_disclosure": {
        "triggers": [
            "director in company compliance flag",
        ],
        "likely_itr_form_impact": "Usually disqualifies ITR-1 or ITR-4 simplicity and activates Part A disclosures.",
        "required_documents": [
            "company identifiers",
            "DIN or equivalent director detail",
        ],
        "must_select": [],
        "can_select": [],
        "must_deselect_if_present": [],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {
            "Director company disclosures": _screen(
                True,
                True,
                True,
                "manual_input",
                "Director-at-any-time rows are substantive compliance disclosures.",
                related_schedule_ids=[],
            ),
        },
        "upload_packets": {},
    },
    "unlisted_equity_disclosure": {
        "triggers": [
            "unlisted equity held at any time during the previous year",
        ],
        "likely_itr_form_impact": "Usually disqualifies simple presumptive ITR-4 routing and activates row-level disclosures.",
        "required_documents": [
            "opening shareholding detail",
            "acquisition or transfer evidence",
            "closing holdings support",
        ],
        "must_select": [],
        "can_select": [],
        "must_deselect_if_present": ["Schedule AL"],
        "derived_schedules": [],
        "stale_prefill_cleanup_rules": [
            "Schedule AL is separate from unlisted-equity disclosure and should stay out unless the legal threshold is met.",
        ],
        "screen_policies": {
            "Unlisted equity rows": _screen(
                True,
                True,
                True,
                "manual_input",
                "Unlisted share rows are substantive compliance disclosures.",
                related_schedule_ids=[],
            ),
            "Schedule AL": _screen(
                True,
                True,
                False,
                "not_applicable_visible",
                "AL should stay out unless the active-year legal threshold is actually crossed.",
                deselect_if_possible=True,
                related_schedule_ids=["al"],
            ),
        },
        "upload_packets": {},
    },
}


def list_persona_modules() -> list[str]:
    return list(PERSONA_MODULES)


def compose_persona_policy(module_ids: list[str]) -> dict[str, object]:
    aggregated: dict[str, object] = {
        "module_ids": [],
        "must_select": [],
        "can_select": [],
        "must_deselect_if_present": [],
        "derived_schedules": [],
        "required_documents": [],
        "stale_prefill_cleanup_rules": [],
        "screen_policies": {},
        "upload_packets": {},
    }

    for module_id in _dedupe(module_ids):
        module = PERSONA_MODULES.get(module_id)
        if module is None:
            raise KeyError(f"Unknown persona module '{module_id}'.")

        cast_ids = aggregated["module_ids"]
        if isinstance(cast_ids, list):
            cast_ids.append(module_id)

        for key in [
            "must_select",
            "can_select",
            "must_deselect_if_present",
            "derived_schedules",
            "required_documents",
            "stale_prefill_cleanup_rules",
        ]:
            existing = aggregated[key]
            if isinstance(existing, list):
                existing.extend(module.get(key, []))

        aggregated_screen_policies = aggregated["screen_policies"]
        if isinstance(aggregated_screen_policies, dict):
            for screen_name, config in dict(module.get("screen_policies", {})).items():
                copied = deepcopy(config)
                source_modules = copied.get("source_modules", [])
                if not isinstance(source_modules, list):
                    source_modules = []
                source_modules.append(module_id)
                copied["source_modules"] = _dedupe([str(item) for item in source_modules])
                aggregated_screen_policies[screen_name] = copied

        aggregated_upload_packets = aggregated["upload_packets"]
        if isinstance(aggregated_upload_packets, dict):
            for packet_id, config in dict(module.get("upload_packets", {})).items():
                aggregated_upload_packets[packet_id] = deepcopy(config)

    for key in [
        "must_select",
        "can_select",
        "must_deselect_if_present",
        "derived_schedules",
        "required_documents",
        "stale_prefill_cleanup_rules",
    ]:
        values = aggregated[key]
        if isinstance(values, list):
            aggregated[key] = _dedupe([str(item) for item in values])

    return aggregated


def starter_schedule_inventory(
    active_persona_modules: list[str] | None = None,
) -> dict[str, object]:
    composed = compose_persona_policy(TARGET_COMPOSITE_PERSONA_MODULES)
    return {
        "metadata": {
            "starter_profile": TARGET_COMPOSITE_STARTER_PROFILE,
            "starter_persona_modules": TARGET_COMPOSITE_PERSONA_MODULES,
            "active_persona_modules": active_persona_modules or [],
            "screen_mode_choices": SCREEN_MODE_CHOICES,
            "notes": (
                "Starter screen inventory for the target ITR-3 44ADA no-books persona. "
                "Prune or mark rows out of scope if the actual case is simpler."
            ),
        },
        "screens": composed["screen_policies"],
    }


def starter_review_only_screens() -> list[dict[str, str]]:
    composed = compose_persona_policy(TARGET_COMPOSITE_PERSONA_MODULES)
    screens = composed["screen_policies"]
    if not isinstance(screens, dict):
        return []

    review_rows: list[dict[str, str]] = []
    for screen_name, config in screens.items():
        if not isinstance(config, dict):
            continue
        screen_mode = str(config.get("screen_mode", "")).strip()
        if screen_mode not in REVIEW_HEAVY_SCREEN_MODES:
            continue
        review_rows.append(
            {
                "screen": screen_name,
                "screen_mode": screen_mode,
                "why": str(config.get("why_selected", "")).strip(),
            }
        )
    return review_rows
