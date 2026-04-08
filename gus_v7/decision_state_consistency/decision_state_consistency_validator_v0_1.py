"""
GUS v7 — Phase 43
Decision State Consistency Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""

from gus_v7.decision_integrity.decision_integrity_schema_v0_1 import (
    VALID_DECISION_OUTPUTS,
    VALID_INTEGRITY_STATUS_VALUES,
)


def validate_decision_state_consistency_v0_1(decision: dict) -> str:
    """
    Returns:
        "CONSISTENT" or "INCONSISTENT"
    """

    output = decision.get("decision_output")
    status = decision.get("integrity_status")

    # -------------------------
    # BASIC ENUM SAFETY
    # -------------------------
    if output not in VALID_DECISION_OUTPUTS:
        return "INCONSISTENT"

    if status not in VALID_INTEGRITY_STATUS_VALUES:
        return "INCONSISTENT"

    # -------------------------
    # CONSISTENCY RULES
    # -------------------------

    # Rule 1: invalid status cannot carry valid decision
    if status == "invalid":
        return "INCONSISTENT"

    # Rule 2: PASS must be valid
    if output == "PASS" and status != "valid":
        return "INCONSISTENT"

    # Rule 3: FAIL must be valid
    if output == "FAIL" and status != "valid":
        return "INCONSISTENT"

    # Rule 4: INSUFFICIENT_EVIDENCE must not be invalid
    if output == "INSUFFICIENT_EVIDENCE" and status == "invalid":
        return "INCONSISTENT"

    return "CONSISTENT"

