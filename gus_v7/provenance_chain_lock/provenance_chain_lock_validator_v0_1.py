"""
GUS v7 - Phase 62
Provenance Chain Lock Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No mutation
- No inference
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


def _build_canonical_reconstructed_path(reconstruction: dict) -> str:
    return (
        f"decision_id={reconstruction['decision_id']}"
        f"|case_id={reconstruction['case_id']}"
        f"|evidence_binding_id={reconstruction['evidence_binding_id']}"
        f"|integrity_envelope_id={reconstruction['integrity_envelope_id']}"
        f"|final_integrity_verdict={reconstruction['final_integrity_verdict']}"
        f"|execution_result={reconstruction['execution_result']}"
        f"|trace_id={reconstruction['trace_id']}"
        f"|trace_timestamp={reconstruction['trace_timestamp']}"
        f"|trace_sequence={reconstruction['trace_sequence']}"
    )


def validate_provenance_chain_lock_v0_1(reconstruction: dict) -> str:
    """
    Returns:
        "PROVENANCE_CHAIN_VALID" or "PROVENANCE_CHAIN_INVALID"

    Fail-closed behavior:
    - malformed reconstruction -> ValueError("INVALID_RECONSTRUCTION")
    """

    if set(reconstruction.keys()) != set(REQUIRED_RECONSTRUCTION_KEYS):
        raise ValueError("INVALID_RECONSTRUCTION")

    for field in REQUIRED_RECONSTRUCTION_KEYS:
        if reconstruction[field] in (None, "", []):
            raise ValueError("INVALID_RECONSTRUCTION")

    canonical_path = _build_canonical_reconstructed_path(reconstruction)

    if reconstruction["reconstructed_path"] != canonical_path:
        return "PROVENANCE_CHAIN_INVALID"

    return "PROVENANCE_CHAIN_VALID"
