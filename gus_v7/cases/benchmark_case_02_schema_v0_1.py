"""
GUS v7 — Phase 11
Benchmark Case 02 Schema (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# CASE IDENTITY (LOCKED)
# =========================

CASE_ID = "BC-02"
CASE_NAME = "Conflict-of-Interest Award"
CASE_VERSION = "v0.1"
CASE_CLASS = "benchmark_fail"
EXPECTED_OUTPUT = "FAIL"


# =========================
# TOP-LEVEL SCHEMA KEYS
# =========================

TOP_LEVEL_KEYS = (
    "case_id",
    "case_name",
    "case_version",
    "case_class",
    "context",
    "agents",
    "process",
    "evidence_pack",
    "integrity_flags",
    "expected_output",
)


# =========================
# CONTEXT SCHEMA
# =========================

CONTEXT_KEYS = (
    "domain",
    "service_type",
    "selection_scope",
    "predeclared_requirement",
)

CONTEXT_DOMAIN_REQUIRED = "vendor_selection"


# =========================
# AGENTS SCHEMA
# =========================

AGENTS_KEYS = (
    "selecting_authority",
    "candidate_vendors",
    "evaluation_mechanism",
    "selected_vendor",
)


# =========================
# PROCESS (STRICT ORDER LOCK)
# =========================

PROCESS_SEQUENCE = (
    "requirement_defined",
    "criteria_defined",
    "vendor_pool_fixed",
    "conflict_present",
    "award_decision_logged",
)


# =========================
# EVIDENCE PACK SCHEMA
# =========================

EVIDENCE_PACK_KEYS = (
    "requirement_definition",
    "criteria_definition",
    "vendor_list",
    "conflict_disclosure",
    "decision_record",
    "traceability_links",
)


# -------------------------
# REQUIREMENT
# -------------------------

REQUIREMENT_KEYS = (
    "id",
    "description",
    "timestamp",
)

REQUIREMENT_ID_REQUIRED = "REQ-002"


# -------------------------
# CRITERIA
# -------------------------

CRITERIA_IDS_REQUIRED = ("C1", "C2", "C3")


# -------------------------
# CONFLICT DISCLOSURE
# -------------------------

CONFLICT_DISCLOSURE_KEYS = (
    "conflict_declared",
    "conflicted_party",
    "relationship_to_selected_vendor",
)


# -------------------------
# DECISION RECORD
# -------------------------

DECISION_KEYS = (
    "selected_vendor",
    "basis",
    "timestamp",
)

DECISION_BASIS_REQUIRED = "conflicted_award"


# -------------------------
# TRACEABILITY
# -------------------------

TRACEABILITY_KEYS = (
    "requirement_to_criteria",
    "criteria_to_decision",
    "conflict_to_decision",
    "chain_complete",
)


# =========================
# INTEGRITY FLAGS
# =========================

INTEGRITY_FLAG_KEYS = (
    "criteria_predefined",
    "vendor_pool_fixed",
    "conflict_declared",
    "conflict_unresolved",
    "award_integrity_compromised",
)


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "V1_IDENTITY_LOCK",
    "V2_STRUCTURE_LOCK",
    "V3_PROCESS_SEQUENCE_LOCK",
    "V4_VENDOR_COMPLETENESS_LOCK",
    "V5_CONFLICT_DISCLOSURE_LOCK",
    "V6_SELECTED_VENDOR_LOCK",
    "V7_TRACEABILITY_LOCK",
    "V8_CONFLICT_UNRESOLVED_LOCK",
    "V9_AWARD_INTEGRITY_FAILURE_LOCK",
    "V10_OUTPUT_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_FAIL"
