"""
GUS v7 — Phase 44
Decision Trace Linking Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""


def validate_decision_trace_linking_v0_1(
    decision: dict,
    evidence_binding: dict,
    evidence_trace: dict,
) -> str:
    """
    Returns:
        "LINKED" or "UNLINKED"
    """

    decision_binding_id = decision.get("evidence_binding_id")
    binding_id = evidence_binding.get("binding_id")
    trace_binding_id = evidence_trace.get("binding_id")
    trace_chain_complete = evidence_trace.get("chain_complete")

    # -------------------------
    # REQUIRED LINK FIELDS
    # -------------------------
    if not decision_binding_id:
        return "UNLINKED"

    if not binding_id:
        return "UNLINKED"

    if not trace_binding_id:
        return "UNLINKED"

    # -------------------------
    # REFERENCE CONSISTENCY
    # -------------------------
    if decision_binding_id != binding_id:
        return "UNLINKED"

    if binding_id != trace_binding_id:
        return "UNLINKED"

    # -------------------------
    # TRACE COMPLETENESS
    # -------------------------
    if trace_chain_complete is not True:
        return "UNLINKED"

    return "LINKED"
