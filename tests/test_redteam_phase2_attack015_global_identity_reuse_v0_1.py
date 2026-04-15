"""
GUS v7 - Red Team Phase 2 Attack 015
Global Identity Reuse Across Separate Validation Scopes (v0.1)

STRICT:
- Deterministic
- Fail-first attack proof
- No mutation
- No inference
"""

from gus_v7.phase1_hardening.phase1_hardening_validator_v0_1 import (
    validate_phase1_hardening_v0_1,
)


def _trace_a() -> dict:
    return {
        "trace_id": "TRACE-ATTACK-015",
        "decision_id": "DEC-ATTACK-015",
        "case_id": "BC-015-A",
        "evidence_binding_id": "EB-ATTACK-015",
        "integrity_envelope_id": "IE-ATTACK-015",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T12:00:00Z",
        "trace_sequence": "0001",
    }


def _trace_b_reused_ids_new_scope() -> dict:
    return {
        "trace_id": "TRACE-ATTACK-015",
        "decision_id": "DEC-ATTACK-015",
        "case_id": "BC-015-B",
        "evidence_binding_id": "EB-ATTACK-015",
        "integrity_envelope_id": "IE-ATTACK-015",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T12:05:00Z",
        "trace_sequence": "0002",
    }


def test_attack015_allows_global_identity_reuse_across_separate_scopes():
    result_a = validate_phase1_hardening_v0_1(_trace_a(), ())
    result_b = validate_phase1_hardening_v0_1(
        _trace_b_reused_ids_new_scope(),
        (),
    )

    assert result_a == "HARDENING_VALID"
    assert result_b == "HARDENING_VALID"
