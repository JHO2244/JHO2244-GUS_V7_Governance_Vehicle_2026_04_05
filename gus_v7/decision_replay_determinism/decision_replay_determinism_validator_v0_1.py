"""
GUS v7 — Phase 45
Decision Replay Determinism Validator (v0.1)

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


def _evaluate_once(decision: dict, evidence_binding: dict, evidence_trace: dict) -> tuple[str, str, str]:
    return (
        validate_decision_integrity_v0_1(decision),
        validate_decision_state_consistency_v0_1(decision),
        validate_decision_trace_linking_v0_1(
            decision,
            evidence_binding,
            evidence_trace,
        ),
    )


def validate_decision_replay_determinism_v0_1(
    decision: dict,
    evidence_binding: dict,
    evidence_trace: dict,
) -> str:
    """
    Returns:
        "DETERMINISTIC" or "NON_DETERMINISTIC"
    """

    first = _evaluate_once(decision, evidence_binding, evidence_trace)
    second = _evaluate_once(decision, evidence_binding, evidence_trace)

    if first != second:
        return "NON_DETERMINISTIC"

    return "DETERMINISTIC"
