"""
GUS v7 — Phase 06
Case Validator Router (v0.1)

STRICT:
- Deterministic routing only
- Fail-closed
- No inference
- No dynamic discovery beyond canonical registry mapping
"""

from __future__ import annotations

from importlib import import_module

from gus_v7.registry.case_registry_v0_1 import CASE_REGISTRY_V0_1


PASS = "PASS"
FAIL = "FAIL"


def route_and_validate_case(case_data: dict) -> str:
    """
    Route a case object to its canonical validator and return PASS or FAIL.

    Fail-closed on:
    - non-dict input
    - missing/invalid case_id
    - unknown registry entry
    - missing validator module/function
    - non-PASS/FAIL validator output
    """
    if not isinstance(case_data, dict):
        return FAIL

    case_id = case_data.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        return FAIL

    registry_entry = CASE_REGISTRY_V0_1.get(case_id)
    if not isinstance(registry_entry, dict):
        return FAIL

    validator_module_path = registry_entry.get("validator_module")
    validator_function_name = registry_entry.get("validator_function")

    if not isinstance(validator_module_path, str) or not validator_module_path:
        return FAIL
    if not isinstance(validator_function_name, str) or not validator_function_name:
        return FAIL

    try:
        validator_module = import_module(validator_module_path)
        validator_function = getattr(validator_module, validator_function_name)
    except Exception:
        return FAIL

    try:
        result = validator_function(case_data)
    except Exception:
        return FAIL

    if result not in (PASS, FAIL):
        return FAIL

    return result
