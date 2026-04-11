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
from gus_v7.evidence_binding.evidence_binding_schema_v0_1 import (
    VALID_EVALUATION_RESULTS,
)


def validate_evidence_decision_binding_v0_1(
    evaluation_result: str,
    evidence_bundle: tuple[dict, ...],
    supported_evaluation_results: tuple[str, ...],
) -> str:
    """
    Returns:
        "BOUND" or "REJECTED"

    Fail-closed behavior:
    - invalid inputs -> ValueError
    """

    # -------------------------
    # EVALUATION RESULT CHECK
    # -------------------------
    if evaluation_result not in VALID_EVALUATION_RESULTS:
        raise ValueError("INVALID_EVALUATION_RESULT")

    # -------------------------
    # SUPPORTED RESULTS CHECK
    # -------------------------
    if not isinstance(supported_evaluation_results, tuple):
        raise ValueError("INVALID_SUPPORTED_RESULTS")

    if len(supported_evaluation_results) == 0:
        raise ValueError("INVALID_SUPPORTED_RESULTS")

    for result in supported_evaluation_results:
        if result not in VALID_EVALUATION_RESULTS:
            raise ValueError("INVALID_SUPPORTED_RESULTS")

    # -------------------------
    # ALIGNMENT ENFORCEMENT
    # -------------------------
    if evaluation_result not in supported_evaluation_results:
        return "REJECTED"

    # -------------------------
    # EVIDENCE BUNDLE CHECK
    # -------------------------
    if not isinstance(evidence_bundle, tuple):
        raise ValueError("INVALID_EVIDENCE_BUNDLE")

    if len(evidence_bundle) == 0:
        return "REJECTED"

    for evidence in evidence_bundle:
        if validate_evidence_v0_1(evidence) != "VALID":
            raise ValueError("INVALID_EVIDENCE")

    # -------------------------
    # CONSISTENCY CHECK
    # -------------------------
    consistency_result = validate_evidence_consistency_v0_1(evidence_bundle)
    if consistency_result != "consistent":
        return "REJECTED"

    return "BOUND"
