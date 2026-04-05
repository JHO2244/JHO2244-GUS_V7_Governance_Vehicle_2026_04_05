"""
GUS v7 — Phase 13
Router Contract Expansion (v0.1)

STRICT:
- Deterministic routing only
- Fail-closed
- No inference
- No fallback
- No dynamic discovery beyond canonical registry mapping
- Output contract locked to PASS, FAIL, or INSUFFICIENT_EVIDENCE only
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from gus_v7.registry.case_registry_v0_1 import CASE_REGISTRY_V0_1


PASS = "PASS"
FAIL = "FAIL"
INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"

ROUTER_ALLOWED_OUTPUTS_V0_1 = (PASS, FAIL, INSUFFICIENT_EVIDENCE)
ROUTER_REQUIRED_REGISTRY_ENTRY_KEYS_V0_1 = (
    "schema_module",
    "validator_module",
    "validator_function",
)


def _is_valid_case_input_v0_1(case_data: Any) -> bool:
    if not isinstance(case_data, dict):
        return False

    case_id = case_data.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        return False

    return True


def _get_registry_entry_v0_1(case_id: str) -> dict[str, str] | None:
    registry_entry = CASE_REGISTRY_V0_1.get(case_id)
    if not isinstance(registry_entry, dict):
        return None

    entry_keys = tuple(registry_entry.keys())
    if entry_keys != ROUTER_REQUIRED_REGISTRY_ENTRY_KEYS_V0_1:
        return None

    schema_module_path = registry_entry.get("schema_module")
    validator_module_path = registry_entry.get("validator_module")
    validator_function_name = registry_entry.get("validator_function")

    if not isinstance(schema_module_path, str) or not schema_module_path:
        return None
    if not isinstance(validator_module_path, str) or not validator_module_path:
        return None
    if not isinstance(validator_function_name, str) or not validator_function_name:
        return None

    return registry_entry


def _resolve_validator_v0_1(registry_entry: dict[str, str]):
    validator_module_path = registry_entry["validator_module"]
    validator_function_name = registry_entry["validator_function"]

    try:
        validator_module = import_module(validator_module_path)
        validator_function = getattr(validator_module, validator_function_name)
    except Exception:
        return None

    if not callable(validator_function):
        return None

    return validator_function


def route_and_validate_case(case_data: dict) -> str:
    """
    Route a case object to its canonical validator and return a router-approved
    deterministic outcome.

    Contract:
    - input must be a dict with non-empty string case_id
    - routing is canonical via CASE_REGISTRY_V0_1 only
    - no fallback, no inference, no alternative path
    - output must be PASS, FAIL, or INSUFFICIENT_EVIDENCE only

    Fail-closed on:
    - invalid input
    - unknown case_id
    - malformed registry entry
    - validator resolution failure
    - validator exception
    - invalid validator output
    """
    if not _is_valid_case_input_v0_1(case_data):
        return FAIL

    case_id = case_data["case_id"]
    registry_entry = _get_registry_entry_v0_1(case_id)
    if registry_entry is None:
        return FAIL

    validator_function = _resolve_validator_v0_1(registry_entry)
    if validator_function is None:
        return FAIL

    try:
        result = validator_function(case_data)
    except Exception:
        return FAIL

    if result not in ROUTER_ALLOWED_OUTPUTS_V0_1:
        return FAIL

    return result
