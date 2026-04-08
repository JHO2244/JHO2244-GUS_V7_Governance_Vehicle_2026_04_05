"""
GUS v7 — Phase 41
Decision Integrity Schema (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# DECISION OBJECT KEYS
# =========================

DECISION_KEYS = (
    "decision_id",
    "case_id",
    "decision_output",
    "decision_basis",
    "evidence_binding_id",
    "timestamp",
    "integrity_status",
)


# =========================
# REQUIRED VALUE CONSTRAINTS
# =========================

VALID_DECISION_OUTPUTS = (
    "PASS",
    "FAIL",
    "INSUFFICIENT_EVIDENCE",
    "OUT_OF_SCOPE",
)

VALID_INTEGRITY_STATUS_VALUES = (
    "pending",
    "valid",
    "invalid",
)


# =========================
# FIELD RULES (DECLARATIVE)
# =========================

REQUIRED_NON_EMPTY_FIELDS = (
    "decision_id",
    "case_id",
    "decision_output",
    "decision_basis",
    "evidence_binding_id",
    "timestamp",
    "integrity_status",
)


# =========================
# STRUCTURE LOCK
# =========================

NO_EXTRA_FIELDS_ALLOWED = True


# =========================
# MUTABILITY LOCK
# =========================

IMMUTABLE_AFTER_CREATION = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "D1_STRUCTURE_LOCK",
    "D2_REQUIRED_FIELDS_LOCK",
    "D3_OUTPUT_VALIDITY_LOCK",
    "D4_INTEGRITY_STATUS_LOCK",
    "D5_NO_EXTRA_FIELDS_LOCK",
    "D6_IMMUTABILITY_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_DECISION"
