"""
GUS v7 — Phase 35
Evidence Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""

from gus_v7.evidence.evidence_schema_v0_1 import (
    EVIDENCE_KEYS,
    VALID_EVIDENCE_TYPES,
    VALIDATION_STATUS_VALUES,
    REQUIRED_NON_EMPTY_FIELDS,
    HASH_REQUIRED,
    NO_EXTRA_FIELDS_ALLOWED,
)


def validate_evidence_v0_1(evidence: dict) -> str:
    """
    Returns:
        "VALID" or "INVALID"
    """

    # -------------------------
    # STRUCTURE CHECK
    # -------------------------
    if NO_EXTRA_FIELDS_ALLOWED:
        if set(evidence.keys()) != set(EVIDENCE_KEYS):
            return "INVALID"

    # -------------------------
    # REQUIRED FIELDS CHECK
    # -------------------------
    for field in REQUIRED_NON_EMPTY_FIELDS:
        if field not in evidence:
            return "INVALID"
        if evidence[field] in (None, "", []):
            return "INVALID"

    # -------------------------
    # TYPE VALIDATION
    # -------------------------
    if evidence["evidence_type"] not in VALID_EVIDENCE_TYPES:
        return "INVALID"

    # -------------------------
    # VALIDATION STATUS CHECK
    # -------------------------
    if evidence["validation_status"] not in VALIDATION_STATUS_VALUES:
        return "INVALID"

    # -------------------------
    # HASH PRESENCE CHECK
    # -------------------------
    if HASH_REQUIRED and not evidence.get("content_hash"):
        return "INVALID"

    return "VALID"
