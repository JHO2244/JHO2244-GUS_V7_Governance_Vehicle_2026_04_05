"""
GUS v7 — Phase 47
Decision Integrity Envelope (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
- No input mutation
"""

from gus_v7.decision_integrity.decision_integrity_validator_v0_1 import (
    validate_decision_integrity_v0_1,
)
from gus_v7.decision_state_consistency.decision_state_consistency_validator_v0_1 import (
    validate_decision_state_consistency_v0_1,
)
from gus_v7.decision_trace_linking.decision_trace_linking_validator_v0_1 import (
    validate_decision_trace_linking_v0_1,
)
from gus_v7.decision_replay_determinism.decision_replay_determinism_validator_v0_1 import (
    validate_decision_replay_determinism_v0_1,
)


def build_decision_integrity_envelope_v0_1(
    decision: dict,
    evidence_binding: dict,
    evidence_trace: dict,
) -> dict:
    """
    Returns a deterministic integrity envelope.
    """

    integrity_result = validate_decision_integrity_v0_1(decision)
    consistency_result = validate_decision_state_consistency_v0_1(decision)
    trace_result = validate_decision_trace_linking_v0_1(
        decision,
        evidence_binding,
        evidence_trace,
    )
    replay_result = validate_decision_replay_determinism_v0_1(
        decision,
        evidence_binding,
        evidence_trace,
    )

    final_integrity_verdict = "INTEGRITY_CONFIRMED"
    if (
        integrity_result != "VALID"
        or consistency_result != "CONSISTENT"
        or trace_result != "LINKED"
        or replay_result != "DETERMINISTIC"
    ):
        final_integrity_verdict = "INTEGRITY_REJECTED"

    return {
        "decision": decision,
        "integrity_result": integrity_result,
        "consistency_result": consistency_result,
        "trace_result": trace_result,
        "replay_result": replay_result,
        "final_integrity_verdict": final_integrity_verdict,
        "immutable_after_creation": True,
    }
