"""
GUS v7 — Phase 37
Evidence Trace Linking Schema (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# TOP-LEVEL TRACE KEYS
# =========================

EVIDENCE_TRACE_KEYS = (
    "evaluation_id",
    "evidence_fingerprints",
    "trace_integrity",
)


# =========================
# EVIDENCE FINGERPRINT RULES
# =========================

EVIDENCE_FINGERPRINTS_TYPE_REQUIRED = "tuple"
EVIDENCE_FINGERPRINTS_MIN_ITEMS = 1
EVIDENCE_FINGERPRINTS_ORDER_REQUIRED = True
EVIDENCE_FINGERPRINTS_UNIQUE_REQUIRED = True
EVIDENCE_FINGERPRINT_FORMAT_REQUIRED = "sha256_hex"


# =========================
# TRACE INTEGRITY KEYS
# =========================

TRACE_INTEGRITY_KEYS = (
    "trace_status",
    "fingerprint_count",
    "all_links_present",
    "link_mode",
)


# =========================
# REQUIRED VALUE CONSTRAINTS
# =========================

VALID_TRACE_STATUS_VALUES = (
    "unverified",
    "verified",
)

LINK_MODE_REQUIRED = "deterministic_trace_link"


# =========================
# STRUCTURE LOCKS
# =========================

REQUIRED_NON_EMPTY_FIELDS = (
    "evaluation_id",
    "evidence_fingerprints",
    "trace_integrity",
)

NO_EXTRA_FIELDS_ALLOWED = True
IMMUTABLE_AFTER_CREATION = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "T1_STRUCTURE_LOCK",
    "T2_REQUIRED_FIELDS_LOCK",
    "T3_FINGERPRINT_PRESENCE_LOCK",
    "T4_FINGERPRINT_ORDER_LOCK",
    "T5_FINGERPRINT_UNIQUENESS_LOCK",
    "T6_FINGERPRINT_FORMAT_LOCK",
    "T7_TRACE_INTEGRITY_LOCK",
    "T8_NO_EXTRA_FIELDS_LOCK",
    "T9_IMMUTABILITY_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_REJECTION"
