"""
GUS v7 — Phase 09
Registry Hardening (v0.1)

STRICT:
- Deterministic registry only
- No inference
- No dynamic discovery
- Canonical case-to-module mapping
- Import-time schema validation
- Deep immutability for control-plane structure
"""

from __future__ import annotations

import re
from typing import Any


_REQUIRED_ENTRY_KEYS_V0_1 = (
    "schema_module",
    "validator_module",
    "validator_function",
)

_MODULE_PATH_PATTERN_V0_1 = re.compile(r"^[a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)+$")
_FUNCTION_NAME_PATTERN_V0_1 = re.compile(r"^[a-z_][a-z0-9_]*$")


class FrozenRegistryDictV0_1(dict):
    """
    Immutable dict subtype used to preserve dict compatibility with existing
    router logic while preventing runtime mutation of registry structures.
    """

    def __readonly(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("FrozenRegistryDictV0_1 is immutable")

    __setitem__ = __readonly
    __delitem__ = __readonly
    clear = __readonly
    pop = __readonly
    popitem = __readonly
    setdefault = __readonly
    update = __readonly

    def __ior__(self, other: Any) -> "FrozenRegistryDictV0_1":
        raise TypeError("FrozenRegistryDictV0_1 is immutable")


def _validate_case_id_v0_1(case_id: Any) -> None:
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("Registry case_id must be a non-empty string")


def _validate_module_path_v0_1(module_path: Any, field_name: str) -> None:
    if not isinstance(module_path, str) or not module_path:
        raise ValueError(f"{field_name} must be a non-empty string")
    if _MODULE_PATH_PATTERN_V0_1.fullmatch(module_path) is None:
        raise ValueError(f"{field_name} has invalid module path format")


def _validate_function_name_v0_1(function_name: Any) -> None:
    if not isinstance(function_name, str) or not function_name:
        raise ValueError("validator_function must be a non-empty string")
    if _FUNCTION_NAME_PATTERN_V0_1.fullmatch(function_name) is None:
        raise ValueError("validator_function has invalid function name format")


def _validate_registry_entry_v0_1(case_id: str, entry: Any) -> None:
    _validate_case_id_v0_1(case_id)

    if not isinstance(entry, dict):
        raise TypeError(f"Registry entry for {case_id} must be a dict")

    entry_keys = tuple(entry.keys())
    if entry_keys != _REQUIRED_ENTRY_KEYS_V0_1:
        raise ValueError(
            f"Registry entry for {case_id} must contain exactly "
            f"{_REQUIRED_ENTRY_KEYS_V0_1} in canonical order"
        )

    _validate_module_path_v0_1(entry["schema_module"], "schema_module")
    _validate_module_path_v0_1(entry["validator_module"], "validator_module")
    _validate_function_name_v0_1(entry["validator_function"])


def _freeze_registry_entry_v0_1(entry: dict[str, str]) -> FrozenRegistryDictV0_1:
    return FrozenRegistryDictV0_1(
        {
            "schema_module": entry["schema_module"],
            "validator_module": entry["validator_module"],
            "validator_function": entry["validator_function"],
        }
    )


def _build_hardened_case_registry_v0_1(
    raw_registry: dict[str, dict[str, str]],
) -> FrozenRegistryDictV0_1:
    if not isinstance(raw_registry, dict):
        raise TypeError("Raw registry must be a dict")

    hardened_registry: dict[str, FrozenRegistryDictV0_1] = {}

    for case_id, entry in raw_registry.items():
        _validate_registry_entry_v0_1(case_id, entry)
        hardened_registry[case_id] = _freeze_registry_entry_v0_1(entry)

    return FrozenRegistryDictV0_1(hardened_registry)


_CASE_REGISTRY_SOURCE_V0_1 = {
    "BC-01": {
        "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
        "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
        "validator_function": "validate_benchmark_case_01",
    },
    "BC-02": {
        "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
        "validator_module": "gus_v7.validators.benchmark_case_02_validator_v0_1",
        "validator_function": "validate_benchmark_case_02",
    },
}


CASE_REGISTRY_V0_1 = _build_hardened_case_registry_v0_1(_CASE_REGISTRY_SOURCE_V0_1)
