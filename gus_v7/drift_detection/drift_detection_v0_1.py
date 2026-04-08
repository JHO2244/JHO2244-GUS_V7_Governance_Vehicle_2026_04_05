"""
GUS v7 — Phase 52
Drift Detection (v0.1)

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

DRIFT_COMPARISON_FIELDS = (
    "decision_id",
    "case_id",
    "evidence_binding_id",
    "integrity_envelope_id",
    "final_integrity_verdict",
    "execution_result",
    "reconstructed_path",
)


def detect_drift_v0_1(
    baseline_reconstruction: dict,
    candidate_reconstruction: dict,
) -> str:
    """
    Returns:
        "NO_DRIFT" or "DRIFT_DETECTED"

    Fail-closed behavior:
    - malformed reconstruction -> ValueError
    """

    if set(baseline_reconstruction.keys()) != set(REQUIRED_RECONSTRUCTION_KEYS):
        raise ValueError("INVALID_RECONSTRUCTION")

    if set(candidate_reconstruction.keys()) != set(REQUIRED_RECONSTRUCTION_KEYS):
        raise ValueError("INVALID_RECONSTRUCTION")

    for field in REQUIRED_RECONSTRUCTION_KEYS:
        if baseline_reconstruction[field] in (None, "", []):
            raise ValueError("INVALID_RECONSTRUCTION")
        if candidate_reconstruction[field] in (None, "", []):
            raise ValueError("INVALID_RECONSTRUCTION")

    for field in DRIFT_COMPARISON_FIELDS:
        if baseline_reconstruction[field] != candidate_reconstruction[field]:
            return "DRIFT_DETECTED"

    return "NO_DRIFT"
