"""
GUS v7 - Phase 61
Trace to Governance Pipeline (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No mutation
- No inference
- No external calls
"""

from gus_v7.audit_reconstruction.audit_reconstruction_v0_1 import (
    reconstruct_audit_path_v0_1,
)
from gus_v7.governance_rules.governance_rules_engine_v0_1 import (
    apply_governance_rules_v0_1,
)
from gus_v7.trace_admission_boundary.trace_admission_boundary_v0_1 import (
    admit_trace_with_identity_lifecycle_v0_1,
)


def apply_trace_to_governance_pipeline_v0_1(
    candidate_trace: dict,
    admitted_history: tuple[dict, ...],
) -> str:
    """
    Returns:
        "GOVERNANCE_PASS" or "GOVERNANCE_FAIL"

    Fail-closed behavior:
    - malformed candidate or history -> ValueError("INVALID_TRACE")
    """

    admission_result = admit_trace_with_identity_lifecycle_v0_1(
        candidate_trace,
        admitted_history,
    )

    if admission_result == "TRACE_REJECTED":
        return "GOVERNANCE_FAIL"

    reconstruction = reconstruct_audit_path_v0_1(candidate_trace)
    return apply_governance_rules_v0_1(reconstruction)
