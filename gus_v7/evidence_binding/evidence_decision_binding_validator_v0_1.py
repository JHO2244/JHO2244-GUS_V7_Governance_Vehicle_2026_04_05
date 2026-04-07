"""
GUS v7 — Phase 40
Evidence Decision Binding Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""

from gus_v7.evidence.evidence_validator_v0_1 import validate_evidence_v0_1
from gus_v7.evidence_consistency.evidence_consistency_validator_v0_1 import (
    validate_evidence_consistency_v0_1,
)


def validate_evidence_decision_binding_v0_1(
    evaluation_result: str,
    evidence_bundle: tuple[dict, ...],
) -> str:
    """
    Returns:
        "BOUND" or "REJECTED"

    Fail-closed behavior:
    - invalid bundle shape -> ValueError
    - invalid evidence item -> ValueError
    """
    if evaluation_result not in ("PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "OUT_OF_SCOPE"):
        raise ValueError("INVALID_EVALUATION_RESULT")

    if not isinstance(evidence_bundle, tuple):
        raise ValueError("INVALID_EVIDENCE_BUNDLE")

    if len(evidence_bundle) == 0:
        return "REJECTED"

    for evidence in evidence_bundle:
        if validate_evidence_v0_1(evidence) != "VALID":
            raise ValueError("INVALID_EVIDENCE")

    consistency_result = validate_evidence_consistency_v0_1(evidence_bundle)
    if consistency_result != "consistent":
        return "REJECTED"

    return "BOUND"
