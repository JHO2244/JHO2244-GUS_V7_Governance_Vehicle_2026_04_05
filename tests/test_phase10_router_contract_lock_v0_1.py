"""
GUS v7 — Phase 10
Router Contract Lock Tests (v0.1)

STRICT:
- Deterministic
- No fallback
- No inference
- Contract fully enforced
"""

import pytest

from gus_v7.routing.case_validator_router_v0_1 import (
    route_and_validate_case,
    ROUTER_ALLOWED_OUTPUTS_V0_1,
)


def _build_minimal_valid_case():
    return {
        "case_id": "BC-01",
        "integrity_flags": {
            "criteria_predefined": True,
            "uniform_evaluation": True,
            "evidence_present": True,
            "traceability_complete": True,
            "no_external_influence": True,
        },
    }


def test_phase10_router_output_contract_strict():
    case = _build_minimal_valid_case()
    result = route_and_validate_case(case)
    assert result in ROUTER_ALLOWED_OUTPUTS_V0_1


def test_phase10_router_rejects_non_dict_input():
    assert route_and_validate_case("invalid") == "FAIL"


def test_phase10_router_rejects_missing_case_id():
    case = _build_minimal_valid_case()
    del case["case_id"]
    assert route_and_validate_case(case) == "FAIL"


def test_phase10_router_rejects_empty_case_id():
    case = _build_minimal_valid_case()
    case["case_id"] = ""
    assert route_and_validate_case(case) == "FAIL"


def test_phase10_router_no_fallback_on_unknown_case():
    case = _build_minimal_valid_case()
    case["case_id"] = "UNKNOWN"
    assert route_and_validate_case(case) == "FAIL"


def test_phase10_router_enforces_registry_contract(monkeypatch):
    from gus_v7.registry import case_registry_v0_1

    broken_registry = {
        "BC-01": {
            "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
            "validator_function": "validate_benchmark_case_01",
        }
    }

    monkeypatch.setattr(
        case_registry_v0_1,
        "CASE_REGISTRY_V0_1",
        broken_registry,
    )

    case = _build_minimal_valid_case()
    assert route_and_validate_case(case) == "FAIL"


def test_phase10_router_rejects_non_callable_validator(monkeypatch):
    def fake_import(_):
        class FakeModule:
            validate_benchmark_case_01 = "not_callable"

        return FakeModule()

    monkeypatch.setattr(
        "gus_v7.routing.case_validator_router_v0_1.import_module",
        fake_import,
    )

    case = _build_minimal_valid_case()
    assert route_and_validate_case(case) == "FAIL"


def test_phase10_router_rejects_invalid_output(monkeypatch):
    def fake_validator(_):
        return "SOMETHING_ELSE"

    monkeypatch.setattr(
        "gus_v7.validators.benchmark_case_01_validator_v0_1.validate_benchmark_case_01",
        fake_validator,
    )

    case = _build_minimal_valid_case()
    assert route_and_validate_case(case) == "FAIL"
