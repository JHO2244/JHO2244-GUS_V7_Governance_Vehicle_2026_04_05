"""
GUS v7 — Phase 15
Explainability Layer (v0.1)

STRICT:
- Deterministic explanation only
- No inference
- No fallback
- No natural-language generation
- Structured trace only
"""

from __future__ import annotations

from gus_v7.cases.benchmark_case_01_schema_v0_1 import (
    AGENTS_KEYS as BC01_AGENTS_KEYS,
    CASE_CLASS as BC01_CASE_CLASS,
    CASE_ID as BC01_CASE_ID,
    CASE_NAME as BC01_CASE_NAME,
    CASE_VERSION as BC01_CASE_VERSION,
    CONTEXT_DOMAIN_REQUIRED as BC01_CONTEXT_DOMAIN_REQUIRED,
    CONTEXT_KEYS as BC01_CONTEXT_KEYS,
    CRITERIA_IDS_REQUIRED as BC01_CRITERIA_IDS_REQUIRED,
    CRITERIA_RESULT_KEYS_REQUIRED as BC01_CRITERIA_RESULT_KEYS_REQUIRED,
    DECISION_BASIS_REQUIRED as BC01_DECISION_BASIS_REQUIRED,
    DECISION_KEYS as BC01_DECISION_KEYS,
    EVALUATION_RECORD_KEYS as BC01_EVALUATION_RECORD_KEYS,
    EVIDENCE_PACK_KEYS as BC01_EVIDENCE_PACK_KEYS,
    EXPECTED_OUTPUT as BC01_EXPECTED_OUTPUT,
    INTEGRITY_FLAG_KEYS as BC01_INTEGRITY_FLAG_KEYS,
    PROCESS_SEQUENCE as BC01_PROCESS_SEQUENCE,
    REQUIREMENT_ID_REQUIRED as BC01_REQUIREMENT_ID_REQUIRED,
    REQUIREMENT_KEYS as BC01_REQUIREMENT_KEYS,
    TOP_LEVEL_KEYS as BC01_TOP_LEVEL_KEYS,
    VALIDATION_RULES as BC01_VALIDATION_RULES,
    TRACEABILITY_KEYS as BC01_TRACEABILITY_KEYS,
)

PASS = "PASS"
FAIL = "FAIL"


def explain_benchmark_case_01_v0_1(case_data: dict) -> dict[str, object]:
    """
    Return a deterministic structured explanation for Benchmark Case 01.

    Contract:
    - result is PASS or FAIL only
    - trace is a tuple of rule ids
    - PASS returns all satisfied rules in canonical order
    - FAIL returns the first decisive failed rule only
    """
    satisfied_rules: list[str] = []

    if not isinstance(case_data, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    if tuple(case_data.keys()) != BC01_TOP_LEVEL_KEYS:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    identity_ok = (
        case_data.get("case_id") == BC01_CASE_ID
        and case_data.get("case_name") == BC01_CASE_NAME
        and case_data.get("case_version") == BC01_CASE_VERSION
        and case_data.get("case_class") == BC01_CASE_CLASS
        and case_data.get("expected_output") == BC01_EXPECTED_OUTPUT
    )
    if not identity_ok:
        return {"result": FAIL, "trace": ("V1_IDENTITY_LOCK",)}
    satisfied_rules.append("V1_IDENTITY_LOCK")

    context = case_data.get("context")
    agents = case_data.get("agents")
    process = case_data.get("process")
    evidence_pack = case_data.get("evidence_pack")
    integrity_flags = case_data.get("integrity_flags")

    if not isinstance(context, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if tuple(context.keys()) != BC01_CONTEXT_KEYS:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if context.get("domain") != BC01_CONTEXT_DOMAIN_REQUIRED:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(context.get("service_type"), str) or not context.get("service_type"):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(context.get("selection_scope"), str) or not context.get("selection_scope"):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if context.get("predeclared_requirement") is not True:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    if not isinstance(agents, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if tuple(agents.keys()) != BC01_AGENTS_KEYS:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    candidate_vendors = agents.get("candidate_vendors")
    if not isinstance(agents.get("selecting_authority"), str) or not agents.get("selecting_authority"):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(candidate_vendors, list) or len(candidate_vendors) < 2:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if len(candidate_vendors) != len(set(candidate_vendors)):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if any(not isinstance(vendor, str) or not vendor for vendor in candidate_vendors):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(agents.get("evaluation_mechanism"), str) or not agents.get("evaluation_mechanism"):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    if not isinstance(process, list):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    if not isinstance(evidence_pack, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if tuple(evidence_pack.keys()) != BC01_EVIDENCE_PACK_KEYS:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    requirement_definition = evidence_pack.get("requirement_definition")
    criteria_definition = evidence_pack.get("criteria_definition")
    vendor_list = evidence_pack.get("vendor_list")
    evaluation_records = evidence_pack.get("evaluation_records")
    decision_record = evidence_pack.get("decision_record")
    traceability_links = evidence_pack.get("traceability_links")

    if not isinstance(requirement_definition, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if tuple(requirement_definition.keys()) != BC01_REQUIREMENT_KEYS:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if requirement_definition.get("id") != BC01_REQUIREMENT_ID_REQUIRED:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(requirement_definition.get("description"), str) or not requirement_definition.get("description"):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(requirement_definition.get("timestamp"), str) or not requirement_definition.get("timestamp"):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    if not isinstance(criteria_definition, list):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(vendor_list, list):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(evaluation_records, list):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(decision_record, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(traceability_links, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if not isinstance(integrity_flags, dict):
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}
    if tuple(integrity_flags.keys()) != BC01_INTEGRITY_FLAG_KEYS:
        return {"result": FAIL, "trace": ("V2_STRUCTURE_LOCK",)}

    satisfied_rules.append("V2_STRUCTURE_LOCK")

    if tuple(process) != BC01_PROCESS_SEQUENCE:
        return {"result": FAIL, "trace": ("V3_PROCESS_SEQUENCE_LOCK",)}
    satisfied_rules.append("V3_PROCESS_SEQUENCE_LOCK")

    if vendor_list != candidate_vendors:
        return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
    if len(evaluation_records) != len(candidate_vendors):
        return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}

    seen_vendor_ids: list[str] = []
    for record in evaluation_records:
        if not isinstance(record, dict):
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
        if tuple(record.keys()) != BC01_EVALUATION_RECORD_KEYS:
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
        vendor_id = record.get("vendor_id")
        if vendor_id not in candidate_vendors:
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
        if vendor_id in seen_vendor_ids:
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
        seen_vendor_ids.append(vendor_id)

        criteria_results = record.get("criteria_results")
        if not isinstance(criteria_results, dict):
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
        if tuple(criteria_results.keys()) != BC01_CRITERIA_RESULT_KEYS_REQUIRED:
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}

        evidence_refs = record.get("evidence_refs")
        if not isinstance(evidence_refs, list) or len(evidence_refs) == 0:
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
        if any(not isinstance(ref, str) or not ref for ref in evidence_refs):
            return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}

    if tuple(seen_vendor_ids) != tuple(candidate_vendors):
        return {"result": FAIL, "trace": ("V4_VENDOR_COMPLETENESS_LOCK",)}
    satisfied_rules.append("V4_VENDOR_COMPLETENESS_LOCK")

    if len(criteria_definition) != len(BC01_CRITERIA_IDS_REQUIRED):
        return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}

    seen_criteria_ids: list[str] = []
    for criterion in criteria_definition:
        if not isinstance(criterion, dict):
            return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}
        if tuple(criterion.keys()) != ("id", "description"):
            return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}
        criterion_id = criterion.get("id")
        if criterion_id not in BC01_CRITERIA_IDS_REQUIRED:
            return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}
        if criterion_id in seen_criteria_ids:
            return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}
        if not isinstance(criterion.get("description"), str) or not criterion.get("description"):
            return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}
        seen_criteria_ids.append(criterion_id)

    if tuple(seen_criteria_ids) != BC01_CRITERIA_IDS_REQUIRED:
        return {"result": FAIL, "trace": ("V5_CRITERIA_UNIFORMITY_LOCK",)}
    satisfied_rules.append("V5_CRITERIA_UNIFORMITY_LOCK")

    if tuple(requirement_definition.keys()) != BC01_REQUIREMENT_KEYS:
        return {"result": FAIL, "trace": ("V6_EVIDENCE_PRESENCE_LOCK",)}
    if requirement_definition.get("id") != BC01_REQUIREMENT_ID_REQUIRED:
        return {"result": FAIL, "trace": ("V6_EVIDENCE_PRESENCE_LOCK",)}
    satisfied_rules.append("V6_EVIDENCE_PRESENCE_LOCK")

    if tuple(traceability_links.keys()) != BC01_TRACEABILITY_KEYS:
        return {"result": FAIL, "trace": ("V7_TRACEABILITY_LOCK",)}
    if any(traceability_links.get(key) is not True for key in BC01_TRACEABILITY_KEYS):
        return {"result": FAIL, "trace": ("V7_TRACEABILITY_LOCK",)}
    satisfied_rules.append("V7_TRACEABILITY_LOCK")

    if tuple(decision_record.keys()) != BC01_DECISION_KEYS:
        return {"result": FAIL, "trace": ("V8_DECISION_LEGITIMACY_LOCK",)}
    if decision_record.get("selected_vendor") not in candidate_vendors:
        return {"result": FAIL, "trace": ("V8_DECISION_LEGITIMACY_LOCK",)}
    if decision_record.get("basis") != BC01_DECISION_BASIS_REQUIRED:
        return {"result": FAIL, "trace": ("V8_DECISION_LEGITIMACY_LOCK",)}
    if not isinstance(decision_record.get("timestamp"), str) or not decision_record.get("timestamp"):
        return {"result": FAIL, "trace": ("V8_DECISION_LEGITIMACY_LOCK",)}
    satisfied_rules.append("V8_DECISION_LEGITIMACY_LOCK")

    if any(integrity_flags.get(key) is not True for key in BC01_INTEGRITY_FLAG_KEYS):
        return {"result": FAIL, "trace": ("V9_EXTERNAL_INFLUENCE_LOCK",)}
    satisfied_rules.append("V9_EXTERNAL_INFLUENCE_LOCK")

    satisfied_rules.append("V10_OUTPUT_LOCK")

    if tuple(satisfied_rules) != BC01_VALIDATION_RULES:
        return {"result": FAIL, "trace": ("V10_OUTPUT_LOCK",)}

    return {"result": PASS, "trace": tuple(satisfied_rules)}
