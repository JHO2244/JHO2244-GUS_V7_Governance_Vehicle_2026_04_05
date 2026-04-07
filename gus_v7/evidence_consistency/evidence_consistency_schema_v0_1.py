"""
GUS v7 — Phase 38
Evidence Consistency Schema (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# TOP-LEVEL CONSISTENCY KEYS
# =========================

EVIDENCE_CONSISTENCY_KEYS = (
    "evaluation_id",
    "evidence_fingerprints",
    "consistency_result",
    "consistency_integrity",
)


# =========================
# EVIDENCE FINGERPRINT RULES
# =========================

EVIDENCE_FINGERPRINTS_TYPE_REQUIRED = "tuple"
EVIDENCE_FINGERPRINTS_MIN_ITEMS = 2
EVIDENCE_FINGERPRINTS_ORDER_REQUIRED = True
EVIDENCE_FINGERPRINTS_UNIQUE_REQUIRED = True


# =========================
# CONSISTENCY RESULT
# =========================

VALID_CONSISTENCY_RESULTS = (
    "consistent",
    "inconsistent",
)


# =========================
# CONSISTENCY INTEGRITY KEYS
# =========================

CONSISTENCY_INTEGRITY_KEYS = (
    "consistency_status",
    "checked_pairs",
    "conflicts_detected",
    "consistency_mode",
)


# =========================
# REQUIRED VALUE CONSTRAINTS
# =========================

VALID_CONSISTENCY_STATUS_VALUES = (
    "unverified",
    "verified",
)

CONSISTENCY_MODE_REQUIRED = "deterministic_structural_consistency"


# =========================
# STRUCTURE LOCKS
# =========================

REQUIRED_NON_EMPTY_FIELDS = (
    "evaluation_id",
    "evidence_fingerprints",
    "consistency_result",
    "consistency_integrity",
)

NO_EXTRA_FIELDS_ALLOWED = True
IMMUTABLE_AFTER_CREATION = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "C1_STRUCTURE_LOCK",
    "C2_REQUIRED_FIELDS_LOCK",
    "C3_MIN_EVIDENCE_LOCK",
    "C4_FINGERPRINT_ORDER_LOCK",
    "C5_FINGERPRINT_UNIQUENESS_LOCK",
    "C6_CONSISTENCY_RESULT_LOCK",
    "C7_INTEGRITY_LOCK",
    "C8_NO_EXTRA_FIELDS_LOCK",
    "C9_IMMUTABILITY_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_REJECTION"
