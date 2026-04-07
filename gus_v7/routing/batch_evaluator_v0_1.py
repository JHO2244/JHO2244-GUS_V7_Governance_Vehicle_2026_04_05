"""
GUS v7 — Phase 14
Batch Evaluation Engine (v0.1)

STRICT:
- Deterministic batch execution only
- Fail-closed
- No inference
- No fallback
- No aggregation logic
- Preserves input order exactly
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from gus_v7.registry.case_registry_v0_1 import CASE_REGISTRY_V0_1
from gus_v7.routing.case_validator_router_v0_1 import (
    FAIL,
    INSUFFICIENT_EVIDENCE,
    PASS,
    ROUTER_ALLOWED_OUTPUTS_V0_1,
    ROUTER_REQUIRED_REGISTRY_ENTRY_KEYS_V0_1,
)
from gus_v7.routing.execution_contract_v0_1 import accept_execution_contract_v0_1


def _is_valid_batch_case_input_v0_1(case_data: Any) -> bool:
    if not isinstance(case_data, dict):
        return False

    case_id = case_data.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        return False

    return True


def _get_batch_registry_entry_v0_1(case_id: str) -> dict[str, str] | None:
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


def _resolve_batch_validator_v0_1(registry_entry: dict[str, str]):
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


def _evaluate_batch_member_v0_1(case_data: Any) -> str:
    if not _is_valid_batch_case_input_v0_1(case_data):
        return FAIL

    case_id = case_data["case_id"]
    registry_entry = _get_batch_registry_entry_v0_1(case_id)
    if registry_entry is None:
        return FAIL

    validator_function = _resolve_batch_validator_v0_1(registry_entry)
    if validator_function is None:
        return FAIL

    try:
        result = validator_function(case_data)
    except Exception:
        return FAIL

    if result not in ROUTER_ALLOWED_OUTPUTS_V0_1:
        return FAIL

    return result


def evaluate_case_batch_v0_1(case_batch: tuple[dict, ...] | list[dict]) -> tuple[str, ...]:
    """
    Evaluate a batch of case objects deterministically through the canonical
    batch execution path.

    Contract:
    - entry must pass Phase 21 execution contract
    - batch path accepts tuple only
    - output preserves input order exactly
    - output members must be router-approved outcomes only

    Fail-closed on:
    - invalid execution-entry contract
    - single-case dict at batch boundary
    - invalid batch container type
    - impossible output contract drift
    """
    accepted_execution_entry = accept_execution_contract_v0_1(case_batch)
    if accepted_execution_entry is None:
        return (FAIL,)

    if isinstance(accepted_execution_entry, dict):
        return (FAIL,)

    if not isinstance(accepted_execution_entry, tuple):
        return (FAIL,)

    results: list[str] = []

    for case_data in accepted_execution_entry:
        result = _evaluate_batch_member_v0_1(case_data)
        if result not in ROUTER_ALLOWED_OUTPUTS_V0_1:
            return (FAIL,)
        results.append(result)

    return tuple(results)
