"""
GUS v7 — Phase 08
Benchmark Case 02 Validator Placeholder (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No scoring
- No inference
- PASS / FAIL only
- Placeholder only: BC-02 logic not implemented yet
"""

from __future__ import annotations


PASS = "PASS"
FAIL = "FAIL"


def validate_benchmark_case_02(case_data: dict) -> str:
    """
    Phase 08 placeholder validator.

    BC-02 is registered as an explicit canonical case route,
    but its real validation logic is intentionally not implemented yet.

    Fail closed on all inputs.
    """
    _ = case_data
    return FAIL
