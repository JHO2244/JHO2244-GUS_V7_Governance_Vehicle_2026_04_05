"""
GUS v7 — Phase 54
Policy Enforcement Layer (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

VALID_GOVERNANCE_RESULTS = (
    "GOVERNANCE_PASS",
    "GOVERNANCE_FAIL",
)


def enforce_policy_v0_1(governance_result: str) -> str:
    """
    Returns:
        "ALLOW" or "DENY"

    Fail-closed behavior:
    - invalid input -> ValueError
    """

    if governance_result not in VALID_GOVERNANCE_RESULTS:
        raise ValueError("INVALID_GOVERNANCE_RESULT")

    if governance_result == "GOVERNANCE_PASS":
        return "ALLOW"

    return "DENY"
