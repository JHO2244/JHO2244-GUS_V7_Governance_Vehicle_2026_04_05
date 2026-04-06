"""
GUS v7 — Phase 15
Explainability Layer Tests (v0.1)

STRICT:
- Deterministic
- Structured trace only
- No inference
- Explanation result must match validator result
"""

from gus_v7.routing.explainability_v0_1 import explain_benchmark_case_01_v0_1
from gus_v7.validators.benchmark_case_01_validator_v0_1 import (
    PASS,
    FAIL,
    validate_benchmark_case_01,
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


def test_phase15_explainability_valid_case_matches_validator_and_full_trace():
    case = _build_valid_case()

    explanation = explain_benchmark_case_01_v0_1(case)

    assert explanation["result"] == PASS
    assert explanation["result"] == validate_benchmark_case_01(case)
    assert explanation["trace"] == (
        "V1_IDENTITY_LOCK",
        "V2_STRUCTURE_LOCK",
        "V3_PROCESS_SEQUENCE_LOCK",
        "V4_VENDOR_COMPLETENESS_LOCK",
        "V5_CRITERIA_UNIFORMITY_LOCK",
        "V6_EVIDENCE_PRESENCE_LOCK",
        "V7_TRACEABILITY_LOCK",
        "V8_DECISION_LEGITIMACY_LOCK",
        "V9_EXTERNAL_INFLUENCE_LOCK",
        "V10_OUTPUT_LOCK",
    )


def test_phase15_explainability_wrong_case_id_returns_first_failed_rule():
    case = _build_valid_case()
    case["case_id"] = "WRONG"

    explanation = explain_benchmark_case_01_v0_1(case)

    assert explanation["result"] == FAIL
    assert explanation["result"] == validate_benchmark_case_01(case)
    assert explanation["trace"] == ("V1_IDENTITY_LOCK",)


def test_phase15_explainability_process_order_returns_decisive_rule():
    case = _build_valid_case()
    case["process"][0], case["process"][1] = case["process"][1], case["process"][0]

    explanation = explain_benchmark_case_01_v0_1(case)

    assert explanation["result"] == FAIL
    assert explanation["result"] == validate_benchmark_case_01(case)
    assert explanation["trace"] == ("V3_PROCESS_SEQUENCE_LOCK",)


def test_phase15_explainability_traceability_break_returns_decisive_rule():
    case = _build_valid_case()
    case["evidence_pack"]["traceability_links"]["chain_complete"] = False

    explanation = explain_benchmark_case_01_v0_1(case)

    assert explanation["result"] == FAIL
    assert explanation["result"] == validate_benchmark_case_01(case)
    assert explanation["trace"] == ("V7_TRACEABILITY_LOCK",)


def test_phase15_explainability_integrity_break_returns_decisive_rule():
    case = _build_valid_case()
    case["integrity_flags"]["no_external_influence"] = False

    explanation = explain_benchmark_case_01_v0_1(case)

    assert explanation["result"] == FAIL
    assert explanation["result"] == validate_benchmark_case_01(case)
    assert explanation["trace"] == ("V9_EXTERNAL_INFLUENCE_LOCK",)
