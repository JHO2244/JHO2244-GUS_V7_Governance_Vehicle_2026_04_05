"""
GUS v7 — Phase 53
Governance Rules Engine (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

REQUIRED_RECONSTRUCTION_KEYS = (
    "trace_id",
    "decision_id",
    "case_id",
    "evidence_binding_id",
    "integrity_envelope_id",
    "final_integrity_verdict",
    "execution_result",
    "trace_timestamp",
    "trace_sequence",
    "reconstructed_path",
)

VALID_EXECUTION_RESULTS = ("EXECUTE", "BLOCK")


def apply_governance_rules_v0_1(reconstruction: dict) -> str:
    """
    Returns:
        "GOVERNANCE_PASS" or "GOVERNANCE_FAIL"

    Fail-closed behavior:
    - malformed reconstruction -> ValueError
    """

    # -------------------------
    # STRUCTURE VALIDATION
    # -------------------------
    if set(reconstruction.keys()) != set(REQUIRED_RECONSTRUCTION_KEYS):
        raise ValueError("INVALID_RECONSTRUCTION")

    for field in REQUIRED_RECONSTRUCTION_KEYS:
        if reconstruction[field] in (None, "", []):
            raise ValueError("INVALID_RECONSTRUCTION")

    # -------------------------
    # VALUE VALIDATION
    # -------------------------
    execution_result = reconstruction["execution_result"]
    integrity_verdict = reconstruction["final_integrity_verdict"]

    if execution_result not in VALID_EXECUTION_RESULTS:
        raise ValueError("INVALID_RECONSTRUCTION")

    # -------------------------
    # GOVERNANCE RULES
    # -------------------------
    if integrity_verdict == "INTEGRITY_CONFIRMED":
        if execution_result == "EXECUTE":
            return "GOVERNANCE_PASS"
        return "GOVERNANCE_FAIL"

    else:
        if execution_result == "BLOCK":
            return "GOVERNANCE_PASS"
        return "GOVERNANCE_FAIL"
    