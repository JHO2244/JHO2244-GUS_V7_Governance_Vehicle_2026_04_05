"""
GUS v7 — Phase 62
Risk Assessment Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# RISK ASSESSMENT KEYS
# =========================

RISK_ASSESSMENT_KEYS = (
    "risk_level",
    "risk_flags_count",
    "instability_detected",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = RISK_ASSESSMENT_KEYS


# =========================
# VALUE CONSTRAINTS
# =========================

VALID_RISK_LEVELS = (
    "LOW",
    "MEDIUM",
    "HIGH",
)

RISK_FLAGS_COUNT_INTEGER = True
NO_NEGATIVE_VALUES = True
INSTABILITY_BOOLEAN_ONLY = True


# =========================
# STRUCTURE LOCK
# =========================

NO_EXTRA_FIELDS_ALLOWED = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "R1_STRUCTURE_LOCK",
    "R2_REQUIRED_FIELDS_LOCK",
    "R3_RISK_LEVEL_LOCK",
    "R4_INTEGER_FLAG_COUNT_LOCK",
    "R5_NON_NEGATIVE_LOCK",
    "R6_BOOLEAN_INSTABILITY_LOCK",
    "R7_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_RISK_ASSESSMENT"
