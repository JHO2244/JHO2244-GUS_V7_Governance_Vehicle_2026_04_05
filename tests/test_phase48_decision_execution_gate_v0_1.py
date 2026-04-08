"""
GUS v7 — Phase 48
Decision Execution Gate Tests (v0.1)

STRICT:
- Validate execution permission only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_execution_gate.decision_execution_gate_v0_1 import (
    apply_decision_execution_gate_v0_1,
)


def test_phase48_allows_confirmed_integrity_envelope():
    envelope = {
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
    }
    assert apply_decision_execution_gate_v0_1(envelope) == "EXECUTE"


def test_phase48_blocks_rejected_integrity_envelope():
    envelope = {
        "final_integrity_verdict": "INTEGRITY_REJECTED",
    }
    assert apply_decision_execution_gate_v0_1(envelope) == "BLOCK"


def test_phase48_blocks_missing_integrity_verdict():
    envelope = {}
    assert apply_decision_execution_gate_v0_1(envelope) == "BLOCK"


def test_phase48_blocks_unknown_integrity_verdict():
    envelope = {
        "final_integrity_verdict": "MAYBE",
    }
    assert apply_decision_execution_gate_v0_1(envelope) == "BLOCK"
