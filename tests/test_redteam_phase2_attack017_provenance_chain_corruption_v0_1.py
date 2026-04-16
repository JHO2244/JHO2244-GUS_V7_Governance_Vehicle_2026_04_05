"""
GUS v7 - Red Team Phase 2 Attack 017
Provenance Chain Corruption (v0.1)

STRICT:
- Deterministic
- Attack proof retained as regression lock
- No mutation
- No inference
"""

import pytest

from gus_v7.governance_rules.governance_rules_engine_v0_1 import (
    apply_governance_rules_v0_1,
)


def _corrupted_reconstruction() -> dict:
    return {
        "trace_id": "TRACE-ATTACK-017",
        "decision_id": "DEC-ATTACK-017",
        "case_id": "BC-017",
        "evidence_binding_id": "EB-ATTACK-017",
        "integrity_envelope_id": "IE-ATTACK-017",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T15:10:00Z",
        "trace_sequence": "0001",
        "reconstructed_path": (
            "decision_id=DEC-FAKE"
            "|case_id=BC-FAKE"
            "|evidence_binding_id=EB-FAKE"
            "|integrity_envelope_id=IE-FAKE"
            "|final_integrity_verdict=INTEGRITY_REJECTED"
            "|execution_result=BLOCK"
            "|trace_id=TRACE-FAKE"
            "|trace_timestamp=1999-01-01T00:00:00Z"
            "|trace_sequence=9999"
        ),
    }


def test_attack017_corrupted_provenance_chain_now_fails_closed():
    with pytest.raises(ValueError, match="INVALID_RECONSTRUCTION"):
        apply_governance_rules_v0_1(_corrupted_reconstruction())

