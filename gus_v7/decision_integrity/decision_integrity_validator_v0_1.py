"""
GUS v7 — Phase 41
Decision Integrity Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""

from gus_v7.decision_integrity.decision_integrity_schema_v0_1 import (
    DECISION_KEYS,
    VALID_DECISION_OUTPUTS,
    VALID_INTEGRITY_STATUS_VALUES,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
)


def validate_decision_integrity_v0_1(decision: dict) -> str:
    """
    Returns:
        "VALID" or "INVALID"
    """

    # -------------------------
    # STRUCTURE CHECK
    # -------------------------
    if NO_EXTRA_FIELDS_ALLOWED:
        if set(decision.keys()) != set(DECISION_KEYS):
            return "INVALID"

    # -------------------------
    # REQUIRED FIELDS CHECK
    # -------------------------
    for field in REQUIRED_NON_EMPTY_FIELDS:
        if field not in decision:
            return "INVALID"
        if decision[field] in (None, "", []):
            return "INVALID"

    # -------------------------
    # DECISION OUTPUT CHECK
    # -------------------------
    if decision["decision_output"] not in VALID_DECISION_OUTPUTS:
        return "INVALID"

    # -------------------------
    # INTEGRITY STATUS CHECK
    # -------------------------
    if decision["integrity_status"] not in VALID_INTEGRITY_STATUS_VALUES:
        return "INVALID"

    return "VALID"
