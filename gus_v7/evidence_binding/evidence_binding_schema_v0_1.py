"""
GUS v7 — Phase 34
Evidence Binding Contract (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# TOP-LEVEL BINDING KEYS
# =========================

EVIDENCE_BINDING_KEYS = (
    "evaluation_result",
    "evidence_bundle",
    "binding_integrity",
)


# =========================
# EVIDENCE BUNDLE RULES
# =========================

EVIDENCE_BUNDLE_TYPE_REQUIRED = "tuple"
EVIDENCE_BUNDLE_MIN_ITEMS = 1
EVIDENCE_BUNDLE_ORDER_REQUIRED = True
EVIDENCE_BUNDLE_ITEMS_MUST_CONFORM_TO = "PHASE33_EVIDENCE_SCHEMA_V0_1"


# =========================
# BINDING INTEGRITY KEYS
# =========================

BINDING_INTEGRITY_KEYS = (
    "binding_status",
    "bundle_count",
    "all_evidence_bound",
    "binding_mode",
)


# =========================
# REQUIRED VALUE CONSTRAINTS
# =========================

VALID_BINDING_STATUS_VALUES = (
    "unverified",
    "verified",
)

BINDING_MODE_REQUIRED = "deterministic_attachment"


# =========================
# STRUCTURE LOCKS
# =========================

REQUIRED_NON_EMPTY_FIELDS = (
    "evaluation_result",
    "evidence_bundle",
    "binding_integrity",
)

NO_EXTRA_FIELDS_ALLOWED = True
IMMUTABLE_AFTER_CREATION = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "B1_STRUCTURE_LOCK",
    "B2_REQUIRED_FIELDS_LOCK",
    "B3_EVIDENCE_BUNDLE_PRESENCE_LOCK",
    "B4_EVIDENCE_BUNDLE_ORDER_LOCK",
    "B5_PHASE33_CONFORMANCE_LOCK",
    "B6_BINDING_INTEGRITY_LOCK",
    "B7_NO_EXTRA_FIELDS_LOCK",
    "B8_IMMUTABILITY_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_REJECTION"
