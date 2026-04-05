"""
GUS v7 — Phase 04
Benchmark Case 01 Validator Tests (v0.1)

STRICT:
- Deterministic
- PASS/FAIL only
- Each FAIL test breaks exactly one rule
"""

from gus_v7.validators.benchmark_case_01_validator_v0_1 import (
    validate_benchmark_case_01,
    PASS,
    FAIL,
)


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


def test_phase04_pass_case():
    case = _build_valid_case()
    assert validate_benchmark_case_01(case) == PASS


def test_phase04_fail_wrong_case_id():
    case = _build_valid_case()
    case["case_id"] = "WRONG"
    assert validate_benchmark_case_01(case) == FAIL


def test_phase04_fail_missing_vendor():
    case = _build_valid_case()
    case["agents"]["candidate_vendors"] = ["Vendor_1", "Vendor_2"]
    assert validate_benchmark_case_01(case) == FAIL


def test_phase04_fail_process_order():
    case = _build_valid_case()
    case["process"][0], case["process"][1] = case["process"][1], case["process"][0]
    assert validate_benchmark_case_01(case) == FAIL


def test_phase04_fail_traceability():
    case = _build_valid_case()
    case["evidence_pack"]["traceability_links"]["chain_complete"] = False
    assert validate_benchmark_case_01(case) == FAIL


def test_phase04_fail_integrity_flag():
    case = _build_valid_case()
    case["integrity_flags"]["no_external_influence"] = False
    assert validate_benchmark_case_01(case) == FAIL
