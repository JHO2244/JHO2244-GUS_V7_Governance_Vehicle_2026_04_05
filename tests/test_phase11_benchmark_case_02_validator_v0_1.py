"""
GUS v7 — Phase 11
Benchmark Case 02 Validator Tests (v0.1)

STRICT:
- Deterministic
- PASS/FAIL only
- Canonical FAIL benchmark
- Each structural failure still returns FAIL
"""

from gus_v7.validators.benchmark_case_02_validator_v0_1 import (
    FAIL,
    validate_benchmark_case_02,
)


def _build_valid_case():
    return {
        "case_id": "BC-02",
        "case_name": "Conflict-of-Interest Award",
        "case_version": "v0.1",
        "case_class": "benchmark_fail",
        "context": {
            "domain": "vendor_selection",
            "service_type": "logistics_services",
            "selection_scope": "region_y",
            "predeclared_requirement": True,
        },
        "agents": {
            "selecting_authority": "Agent_A",
            "candidate_vendors": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "evaluation_mechanism": "Committee_B",
            "selected_vendor": "Vendor_1",
        },
        "process": [
            "requirement_defined",
            "criteria_defined",
            "vendor_pool_fixed",
            "conflict_present",
            "award_decision_logged",
        ],
        "evidence_pack": {
            "requirement_definition": {
                "id": "REQ-002",
                "description": "Provide logistics services for region Y",
                "timestamp": "T1",
            },
            "criteria_definition": [
                {"id": "C1", "description": "Cost efficiency"},
                {"id": "C2", "description": "Delivery reliability"},
                {"id": "C3", "description": "Service capacity"},
            ],
            "vendor_list": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "conflict_disclosure": {
                "conflict_declared": True,
                "conflicted_party": "Agent_A",
                "relationship_to_selected_vendor": "family_tie",
            },
            "decision_record": {
                "selected_vendor": "Vendor_1",
                "basis": "conflicted_award",
                "timestamp": "T2",
            },
            "traceability_links": {
                "requirement_to_criteria": True,
                "criteria_to_decision": True,
                "conflict_to_decision": True,
                "chain_complete": True,
            },
        },
        "integrity_flags": {
            "criteria_predefined": True,
            "vendor_pool_fixed": True,
            "conflict_declared": True,
            "conflict_unresolved": True,
            "award_integrity_compromised": True,
        },
        "expected_output": "FAIL",
    }


def test_phase11_canonical_bc02_case_returns_fail():
    case = _build_valid_case()
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_wrong_case_id():
    case = _build_valid_case()
    case["case_id"] = "WRONG"
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_wrong_selected_vendor():
    case = _build_valid_case()
    case["agents"]["selected_vendor"] = "Vendor_X"
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_conflict_not_declared():
    case = _build_valid_case()
    case["evidence_pack"]["conflict_disclosure"]["conflict_declared"] = False
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_conflicted_party_mismatch():
    case = _build_valid_case()
    case["evidence_pack"]["conflict_disclosure"]["conflicted_party"] = "Agent_Z"
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_process_order():
    case = _build_valid_case()
    case["process"][0], case["process"][1] = case["process"][1], case["process"][0]
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_traceability_break():
    case = _build_valid_case()
    case["evidence_pack"]["traceability_links"]["chain_complete"] = False
    assert validate_benchmark_case_02(case) == FAIL


def test_phase11_fail_integrity_flag_break():
    case = _build_valid_case()
    case["integrity_flags"]["conflict_unresolved"] = False
    assert validate_benchmark_case_02(case) == FAIL
