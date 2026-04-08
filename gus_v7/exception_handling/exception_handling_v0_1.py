"""
GUS v7 — Phase 55
Exception Handling Protocol (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

VALID_ENFORCEMENT_RESULTS = (
    "ALLOW",
    "DENY",
)


REQUIRED_EXCEPTION_KEYS = (
    "exception_id",
    "reason_code",
    "approved",
)


def apply_exception_handling_v0_1(
    enforcement_result: str,
    exception_request: dict | None,
) -> str:
    """
    Returns:
        "FINAL_ALLOW" or "FINAL_DENY"

    Fail-closed behavior:
    - invalid input -> ValueError
    """

    # -------------------------
    # VALIDATE ENFORCEMENT RESULT
    # -------------------------
    if enforcement_result not in VALID_ENFORCEMENT_RESULTS:
        raise ValueError("INVALID_ENFORCEMENT_RESULT")

    # -------------------------
    # ALLOW IS FINAL
    # -------------------------
    if enforcement_result == "ALLOW":
        return "FINAL_ALLOW"

    # -------------------------
    # DENY → CHECK EXCEPTION
    # -------------------------
    if exception_request is None:
        return "FINAL_DENY"

    if set(exception_request.keys()) != set(REQUIRED_EXCEPTION_KEYS):
        raise ValueError("INVALID_EXCEPTION_REQUEST")

    if exception_request["exception_id"] in (None, "", []):
        raise ValueError("INVALID_EXCEPTION_REQUEST")

    if exception_request["reason_code"] in (None, "", []):
        raise ValueError("INVALID_EXCEPTION_REQUEST")

    if exception_request["approved"] is not True:
        return "FINAL_DENY"

    return "FINAL_ALLOW"
