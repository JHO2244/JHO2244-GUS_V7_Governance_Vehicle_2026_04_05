"""
GUS v7 — Phase 46
Decision Conflict Detection Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""


def validate_decision_conflict_detection_v0_1(
    decision_a: dict,
    decision_b: dict,
) -> str:
    """
    Returns:
        "CONFLICT" or "NO_CONFLICT"
    """

    case_id_a = decision_a.get("case_id")
    case_id_b = decision_b.get("case_id")

    binding_id_a = decision_a.get("evidence_binding_id")
    binding_id_b = decision_b.get("evidence_binding_id")

    output_a = decision_a.get("decision_output")
    output_b = decision_b.get("decision_output")

    # -------------------------
    # REQUIRED REFERENCE FIELDS
    # -------------------------
    if not case_id_a or not case_id_b:
        return "NO_CONFLICT"

    if not binding_id_a or not binding_id_b:
        return "NO_CONFLICT"

    if not output_a or not output_b:
        return "NO_CONFLICT"

    # -------------------------
    # CONFLICT RULE
    # -------------------------
    if (
        case_id_a == case_id_b
        and binding_id_a == binding_id_b
        and output_a != output_b
    ):
        return "CONFLICT"

    return "NO_CONFLICT"
