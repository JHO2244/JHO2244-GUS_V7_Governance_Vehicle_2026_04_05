"""
GUS v7 — Phase 07
Case Validator Router Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- Covers full failure surface
"""

from gus_v7.routing.case_validator_router_v0_1 import route_and_validate_case
from gus_v7.validators.benchmark_case_01_validator_v0_1 import PASS, FAIL


def _build_valid_case():
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
        "case_version": "v0.1",
        "case_class": "benchmark_pass",
        "context": {
            "domain": "vendor_selection",
            "service_type": "logistics_services",
            "selection_scope": "region_x",
            "predeclared_requirement": True,
        },
        "agents": {
            "selecting_authority": "Agent_A",
            "candidate_vendors": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "evaluation_mechanism": "Agent_C",
        },
        "process": [
            "requirement_defined",
            "criteria_defined",
            "vendor_pool_fixed",
            "uniform_evaluation_executed",
            "evidence_recorded",
            "decision_logged",
        ],
        "evidence_pack": {
            "requirement_definition": {
                "id": "REQ-001",
                "description": "Provide logistics services for region X",
                "timestamp": "T1",
            },
            "criteria_definition": [
                {"id": "C1", "description": "Cost efficiency"},
                {"id": "C2", "description": "Delivery reliability"},
                {"id": "C3", "description": "Service capacity"},
            ],
            "vendor_list": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "evaluation_records": [
                {
                    "vendor_id": "Vendor_1",
                    "criteria_results": {"C1": "ok", "C2": "ok", "C3": "ok"},
                    "evidence_refs": ["E1"],
                },
                {
                    "vendor_id": "Vendor_2",
                    "criteria_results": {"C1": "ok", "C2": "ok", "C3": "ok"},
                    "evidence_refs": ["E2"],
                },
                {
                    "vendor_id": "Vendor_3",
                    "criteria_results": {"C1": "ok", "C2": "ok", "C3": "ok"},
                    "evidence_refs": ["E3"],
                },
            ],
            "decision_record": {
                "selected_vendor": "Vendor_1",
                "basis": "criteria_output_alignment",
                "timestamp": "T2",
            },
            "traceability_links": {
                "requirement_to_criteria": True,
                "criteria_to_evaluations": True,
                "evaluations_to_decision": True,
                "chain_complete": True,
            },
        },
        "integrity_flags": {
            "criteria_predefined": True,
            "uniform_evaluation": True,
            "evidence_present": True,
            "traceability_complete": True,
            "no_external_influence": True,
        },
        "expected_output": "PASS",
    }


def test_phase07_router_pass():
    case = _build_valid_case()
    assert route_and_validate_case(case) == PASS


def test_phase07_router_invalid_case_id():
    case = _build_valid_case()
    case["case_id"] = "UNKNOWN"
    assert route_and_validate_case(case) == FAIL


def test_phase07_router_missing_case_id():
    case = _build_valid_case()
    del case["case_id"]
    assert route_and_validate_case(case) == FAIL


def test_phase07_router_non_dict_input():
    assert route_and_validate_case("not_a_dict") == FAIL


def test_phase07_router_registry_missing_mapping():
    case = _build_valid_case()
    case["case_id"] = ""
    assert route_and_validate_case(case) == FAIL


def test_phase07_router_validator_failure_propagation():
    case = _build_valid_case()
    case["integrity_flags"]["no_external_influence"] = False  # breaks validator
    assert route_and_validate_case(case) == FAIL


def test_phase07_router_invalid_validator_output(monkeypatch):
    def bad_validator(_):
        return "INVALID"

    monkeypatch.setattr(
        "gus_v7.validators.benchmark_case_01_validator_v0_1.validate_benchmark_case_01",
        bad_validator,
    )

    case = _build_valid_case()
    assert route_and_validate_case(case) == FAIL
    