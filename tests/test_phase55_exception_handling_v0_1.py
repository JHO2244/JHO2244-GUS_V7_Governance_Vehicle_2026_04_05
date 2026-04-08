"""
GUS v7 — Phase 55
Exception Handling Protocol Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.exception_handling.exception_handling_v0_1 import (
    REQUIRED_EXCEPTION_KEYS,
    VALID_ENFORCEMENT_RESULTS,
    apply_exception_handling_v0_1,
)


def _valid_exception_request():
    return {
        "exception_id": "EX-001",
        "reason_code": "MANUAL_ESCALATION_APPROVED",
        "approved": True,
    }


def test_phase55_valid_enforcement_results_exact_match():
    assert VALID_ENFORCEMENT_RESULTS == (
        "ALLOW",
        "DENY",
    )


def test_phase55_required_exception_keys_exact_match():
    assert REQUIRED_EXCEPTION_KEYS == (
        "exception_id",
        "reason_code",
        "approved",
    )


def test_phase55_allow_is_final():
    assert apply_exception_handling_v0_1("ALLOW", None) == "FINAL_ALLOW"


def test_phase55_deny_without_exception_stays_denied():
    assert apply_exception_handling_v0_1("DENY", None) == "FINAL_DENY"


def test_phase55_deny_with_approved_exception_becomes_final_allow():
    assert (
        apply_exception_handling_v0_1("DENY", _valid_exception_request())
        == "FINAL_ALLOW"
    )


def test_phase55_deny_with_unapproved_exception_stays_denied():
    request = _valid_exception_request()
    request["approved"] = False
    assert apply_exception_handling_v0_1("DENY", request) == "FINAL_DENY"


def test_phase55_rejects_invalid_enforcement_result():
    with pytest.raises(ValueError, match="INVALID_ENFORCEMENT_RESULT"):
        apply_exception_handling_v0_1("UNKNOWN", None)


def test_phase55_rejects_malformed_exception_request():
    request = _valid_exception_request()
    del request["reason_code"]
    with pytest.raises(ValueError, match="INVALID_EXCEPTION_REQUEST"):
        apply_exception_handling_v0_1("DENY", request)


def test_phase55_rejects_empty_reason_code():
    request = _valid_exception_request()
    request["reason_code"] = ""
    with pytest.raises(ValueError, match="INVALID_EXCEPTION_REQUEST"):
        apply_exception_handling_v0_1("DENY", request)
