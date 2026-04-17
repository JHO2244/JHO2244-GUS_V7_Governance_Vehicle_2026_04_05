"""
GUS v7 - Red Team Phase 2 Attack 016
Cross-Batch Replay Injection (v0.1)

STRICT:
- Deterministic
- Fail-first attack proof
- No mutation
- No inference
"""

from gus_v7.global_identity_lifecycle.global_identity_lifecycle_validator_v0_1 import (
    validate_global_identity_lifecycle_v0_1,
)


def _original_trace() -> dict:
    return {
        "trace_id": "TRACE-ATTACK-016",
        "decision_id": "DEC-ATTACK-016",
        "case_id": "BC-016-A",
        "evidence_binding_id": "EB-ATTACK-016",
        "integrity_envelope_id": "IE-ATTACK-016",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T13:00:00Z",
        "trace_sequence": "0001",
    }


def _replayed_trace_new_context() -> dict:
    return {
        "trace_id": "TRACE-ATTACK-016",
        "decision_id": "DEC-ATTACK-016",
        "case_id": "BC-016-B",
        "evidence_binding_id": "EB-ATTACK-016",
        "integrity_envelope_id": "IE-ATTACK-016",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T13:05:00Z",
        "trace_sequence": "0002",
    }


def test_attack016_rejects_cross_batch_replay_in_new_context():
    result_a = validate_global_identity_lifecycle_v0_1(_original_trace(), ())
    result_b = validate_global_identity_lifecycle_v0_1(
        _replayed_trace_new_context(),
        (_original_trace(),),
    )

    assert result_a == "IDENTITY_LIFECYCLE_VALID"
    assert result_b == "IDENTITY_LIFECYCLE_INVALID"
