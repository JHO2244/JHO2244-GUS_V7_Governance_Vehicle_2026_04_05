"""
GUS v7 — Phase 54
Policy Enforcement Layer Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.policy_enforcement.policy_enforcement_v0_1 import (
    VALID_GOVERNANCE_RESULTS,
    enforce_policy_v0_1,
)


def test_phase54_valid_governance_results_exact_match():
    assert VALID_GOVERNANCE_RESULTS == (
        "GOVERNANCE_PASS",
        "GOVERNANCE_FAIL",
    )


def test_phase54_pass_maps_to_allow():
    assert enforce_policy_v0_1("GOVERNANCE_PASS") == "ALLOW"


def test_phase54_fail_maps_to_deny():
    assert enforce_policy_v0_1("GOVERNANCE_FAIL") == "DENY"


def test_phase54_is_deterministic():
    assert enforce_policy_v0_1("GOVERNANCE_PASS") == "ALLOW"
    assert enforce_policy_v0_1("GOVERNANCE_PASS") == "ALLOW"


def test_phase54_rejects_invalid_input():
    with pytest.raises(ValueError, match="INVALID_GOVERNANCE_RESULT"):
        enforce_policy_v0_1("UNKNOWN")
