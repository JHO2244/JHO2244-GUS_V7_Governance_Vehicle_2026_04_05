"""
GUS v7 — Phase 36
Evidence Fingerprinting (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""

import hashlib

from gus_v7.evidence.evidence_validator_v0_1 import validate_evidence_v0_1


FINGERPRINT_FIELD_ORDER = (
    "evidence_id",
    "evidence_type",
    "source_id",
    "timestamp",
    "content_ref",
    "content_hash",
    "validation_status",
)


def fingerprint_evidence_v0_1(evidence: dict) -> str:
    """
    Returns a deterministic SHA-256 fingerprint for a valid evidence object.

    Fail-closed behavior:
    - invalid evidence -> ValueError
    """
    if validate_evidence_v0_1(evidence) != "VALID":
        raise ValueError("INVALID_EVIDENCE")

    canonical_parts = []
    for field in FINGERPRINT_FIELD_ORDER:
        canonical_parts.append(f"{field}={evidence[field]}")

    canonical_payload = "|".join(canonical_parts)
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
