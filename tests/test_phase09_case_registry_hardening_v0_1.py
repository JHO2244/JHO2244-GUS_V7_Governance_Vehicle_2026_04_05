"""
GUS v7 — Phase 09
Registry Hardening Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- Control-plane structure locked
"""

import pytest

from gus_v7.registry.case_registry_v0_1 import (
    CASE_REGISTRY_V0_1,
    FrozenRegistryDictV0_1,
    _build_hardened_case_registry_v0_1,
)


def test_phase09_registry_is_frozen_dict_subtype():
    assert isinstance(CASE_REGISTRY_V0_1, FrozenRegistryDictV0_1)
    assert isinstance(CASE_REGISTRY_V0_1, dict)


def test_phase09_registry_entry_is_frozen_dict_subtype():
    entry = CASE_REGISTRY_V0_1["BC-01"]
    assert isinstance(entry, FrozenRegistryDictV0_1)
    assert isinstance(entry, dict)


def test_phase09_registry_top_level_mutation_blocked():
    with pytest.raises(TypeError):
        CASE_REGISTRY_V0_1["BC-99"] = {
            "schema_module": "gus_v7.cases.fake_case_schema_v0_1",
            "validator_module": "gus_v7.validators.fake_case_validator_v0_1",
            "validator_function": "validate_fake_case",
        }


def test_phase09_registry_nested_mutation_blocked():
    with pytest.raises(TypeError):
        CASE_REGISTRY_V0_1["BC-01"]["validator_function"] = "tampered_function"


def test_phase09_registry_missing_required_key_fails_closed():
    raw_registry = {
        "BC-01": {
            "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
            "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
        }
    }

    with pytest.raises(ValueError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_extra_key_fails_closed():
    raw_registry = {
        "BC-01": {
            "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
            "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
            "validator_function": "validate_benchmark_case_01",
            "extra_key": "not_allowed",
        }
    }

    with pytest.raises(ValueError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_invalid_schema_module_format_fails_closed():
    raw_registry = {
        "BC-01": {
            "schema_module": "gus_v7/cases/benchmark_case_01_schema_v0_1",
            "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
            "validator_function": "validate_benchmark_case_01",
        }
    }

    with pytest.raises(ValueError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_invalid_validator_module_format_fails_closed():
    raw_registry = {
        "BC-01": {
            "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
            "validator_module": "gus_v7.validators.benchmark-case-01-validator-v0-1",
            "validator_function": "validate_benchmark_case_01",
        }
    }

    with pytest.raises(ValueError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_invalid_validator_function_format_fails_closed():
    raw_registry = {
        "BC-01": {
            "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
            "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
            "validator_function": "validate benchmark case 01",
        }
    }

    with pytest.raises(ValueError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_non_dict_entry_fails_closed():
    raw_registry = {
        "BC-01": "not_a_dict",
    }

    with pytest.raises(TypeError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_empty_case_id_fails_closed():
    raw_registry = {
        "": {
            "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
            "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
            "validator_function": "validate_benchmark_case_01",
        }
    }

    with pytest.raises(ValueError):
        _build_hardened_case_registry_v0_1(raw_registry)


def test_phase09_registry_preserves_canonical_values():
    assert CASE_REGISTRY_V0_1["BC-01"]["schema_module"] == (
        "gus_v7.cases.benchmark_case_01_schema_v0_1"
    )
    assert CASE_REGISTRY_V0_1["BC-01"]["validator_module"] == (
        "gus_v7.validators.benchmark_case_01_validator_v0_1"
    )
    assert CASE_REGISTRY_V0_1["BC-01"]["validator_function"] == (
        "validate_benchmark_case_01"
    )
