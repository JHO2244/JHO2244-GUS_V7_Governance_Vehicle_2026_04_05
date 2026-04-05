"""
GUS v7 — Phase 03
Benchmark Case 01 Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No scoring
- No inference
- PASS / FAIL only
"""

from __future__ import annotations

from gus_v7.cases.benchmark_case_01_schema_v0_1 import (
    AGENTS_KEYS,
    CASE_CLASS,
    CASE_ID,
    CASE_NAME,
    CASE_VERSION,
    CONTEXT_DOMAIN_REQUIRED,
    CONTEXT_KEYS,
    CRITERIA_IDS_REQUIRED,
    CRITERIA_RESULT_KEYS_REQUIRED,
    DECISION_BASIS_REQUIRED,
    DECISION_KEYS,
    EVALUATION_RECORD_KEYS,
    EVIDENCE_PACK_KEYS,
    EXPECTED_OUTPUT,
    INTEGRITY_FLAG_KEYS,
    PROCESS_SEQUENCE,
    REQUIREMENT_ID_REQUIRED,
    REQUIREMENT_KEYS,
    TOP_LEVEL_KEYS,
    TRACEABILITY_KEYS,
)


PASS = "PASS"
FAIL = "FAIL"


def validate_benchmark_case_01(case_data: dict) -> str:
    """
    Validate Benchmark Case 01 deterministically.

    Returns:
        PASS if every required rule is satisfied.
        FAIL on any structural or rule violation.
    """
    if not isinstance(case_data, dict):
        return FAIL

    if tuple(case_data.keys()) != TOP_LEVEL_KEYS:
        return FAIL

    if case_data.get("case_id") != CASE_ID:
        return FAIL
    if case_data.get("case_name") != CASE_NAME:
        return FAIL
    if case_data.get("case_version") != CASE_VERSION:
        return FAIL
    if case_data.get("case_class") != CASE_CLASS:
        return FAIL
    if case_data.get("expected_output") != EXPECTED_OUTPUT:
        return FAIL

    context = case_data.get("context")
    if not isinstance(context, dict):
        return FAIL
    if tuple(context.keys()) != CONTEXT_KEYS:
        return FAIL
    if context.get("domain") != CONTEXT_DOMAIN_REQUIRED:
        return FAIL
    if not isinstance(context.get("service_type"), str) or not context.get("service_type"):
        return FAIL
    if not isinstance(context.get("selection_scope"), str) or not context.get("selection_scope"):
        return FAIL
    if context.get("predeclared_requirement") is not True:
        return FAIL

    agents = case_data.get("agents")
    if not isinstance(agents, dict):
        return FAIL
    if tuple(agents.keys()) != AGENTS_KEYS:
        return FAIL
    if not isinstance(agents.get("selecting_authority"), str) or not agents.get("selecting_authority"):
        return FAIL
    candidate_vendors = agents.get("candidate_vendors")
    if not isinstance(candidate_vendors, list) or len(candidate_vendors) < 2:
        return FAIL
    if len(candidate_vendors) != len(set(candidate_vendors)):
        return FAIL
    if any(not isinstance(vendor, str) or not vendor for vendor in candidate_vendors):
        return FAIL
    if not isinstance(agents.get("evaluation_mechanism"), str) or not agents.get("evaluation_mechanism"):
        return FAIL

    process = case_data.get("process")
    if not isinstance(process, list):
        return FAIL
    if tuple(process) != PROCESS_SEQUENCE:
        return FAIL

    evidence_pack = case_data.get("evidence_pack")
    if not isinstance(evidence_pack, dict):
        return FAIL
    if tuple(evidence_pack.keys()) != EVIDENCE_PACK_KEYS:
        return FAIL

    requirement_definition = evidence_pack.get("requirement_definition")
    if not isinstance(requirement_definition, dict):
        return FAIL
    if tuple(requirement_definition.keys()) != REQUIREMENT_KEYS:
        return FAIL
    if requirement_definition.get("id") != REQUIREMENT_ID_REQUIRED:
        return FAIL
    if not isinstance(requirement_definition.get("description"), str) or not requirement_definition.get("description"):
        return FAIL
    if not isinstance(requirement_definition.get("timestamp"), str) or not requirement_definition.get("timestamp"):
        return FAIL

    criteria_definition = evidence_pack.get("criteria_definition")
    if not isinstance(criteria_definition, list):
        return FAIL
    if len(criteria_definition) != len(CRITERIA_IDS_REQUIRED):
        return FAIL

    seen_criteria_ids: list[str] = []
    for criterion in criteria_definition:
        if not isinstance(criterion, dict):
            return FAIL
        if tuple(criterion.keys()) != ("id", "description"):
            return FAIL
        criterion_id = criterion.get("id")
        if criterion_id not in CRITERIA_IDS_REQUIRED:
            return FAIL
        if criterion_id in seen_criteria_ids:
            return FAIL
        if not isinstance(criterion.get("description"), str) or not criterion.get("description"):
            return FAIL
        seen_criteria_ids.append(criterion_id)

    if tuple(seen_criteria_ids) != CRITERIA_IDS_REQUIRED:
        return FAIL

    vendor_list = evidence_pack.get("vendor_list")
    if not isinstance(vendor_list, list):
        return FAIL
    if vendor_list != candidate_vendors:
        return FAIL

    evaluation_records = evidence_pack.get("evaluation_records")
    if not isinstance(evaluation_records, list):
        return FAIL
    if len(evaluation_records) != len(candidate_vendors):
        return FAIL

    seen_vendor_ids: list[str] = []
    for record in evaluation_records:
        if not isinstance(record, dict):
            return FAIL
        if tuple(record.keys()) != EVALUATION_RECORD_KEYS:
            return FAIL

        vendor_id = record.get("vendor_id")
        if vendor_id not in candidate_vendors:
            return FAIL
        if vendor_id in seen_vendor_ids:
            return FAIL
        seen_vendor_ids.append(vendor_id)

        criteria_results = record.get("criteria_results")
        if not isinstance(criteria_results, dict):
            return FAIL
        if tuple(criteria_results.keys()) != CRITERIA_RESULT_KEYS_REQUIRED:
            return FAIL

        evidence_refs = record.get("evidence_refs")
        if not isinstance(evidence_refs, list) or len(evidence_refs) == 0:
            return FAIL
        if any(not isinstance(ref, str) or not ref for ref in evidence_refs):
            return FAIL

    if tuple(seen_vendor_ids) != tuple(candidate_vendors):
        return FAIL

    decision_record = evidence_pack.get("decision_record")
    if not isinstance(decision_record, dict):
        return FAIL
    if tuple(decision_record.keys()) != DECISION_KEYS:
        return FAIL
    if decision_record.get("selected_vendor") not in candidate_vendors:
        return FAIL
    if decision_record.get("basis") != DECISION_BASIS_REQUIRED:
        return FAIL
    if not isinstance(decision_record.get("timestamp"), str) or not decision_record.get("timestamp"):
        return FAIL

    traceability_links = evidence_pack.get("traceability_links")
    if not isinstance(traceability_links, dict):
        return FAIL
    if tuple(traceability_links.keys()) != TRACEABILITY_KEYS:
        return FAIL
    if any(traceability_links.get(key) is not True for key in TRACEABILITY_KEYS):
        return FAIL

    integrity_flags = case_data.get("integrity_flags")
    if not isinstance(integrity_flags, dict):
        return FAIL
    if tuple(integrity_flags.keys()) != INTEGRITY_FLAG_KEYS:
        return FAIL
    if any(integrity_flags.get(key) is not True for key in INTEGRITY_FLAG_KEYS):
        return FAIL

    return PASS
