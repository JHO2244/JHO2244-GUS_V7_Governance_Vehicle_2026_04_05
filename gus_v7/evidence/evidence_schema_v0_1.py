"""
GUS v7 — Phase 33
Evidence Authenticity Contract (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# EVIDENCE OBJECT KEYS
# =========================

EVIDENCE_KEYS = (
    "evidence_id",
    "evidence_type",
    "source_id",
    "timestamp",
    "content_ref",
    "content_hash",
    "validation_status",
)


# =========================
# REQUIRED VALUE CONSTRAINTS
# =========================

VALID_EVIDENCE_TYPES = (
    "document",
    "record",
    "log",
    "measurement",
    "external_reference",
)

VALIDATION_STATUS_VALUES = (
    "unverified",
    "verified",
)


# =========================
# FIELD RULES (DECLARATIVE)
# =========================

REQUIRED_NON_EMPTY_FIELDS = (
    "evidence_id",
    "evidence_type",
    "source_id",
    "timestamp",
    "content_ref",
    "content_hash",
    "validation_status",
)


# =========================
# HASH REQUIREMENT
# =========================

HASH_REQUIRED = True


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
    "E1_STRUCTURE_LOCK",
    "E2_REQUIRED_FIELDS_LOCK",
    "E3_TYPE_VALIDITY_LOCK",
    "E4_HASH_PRESENCE_LOCK",
    "E5_NO_EXTRA_FIELDS_LOCK",
    "E6_IMMUTABILITY_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_REJECTION"
