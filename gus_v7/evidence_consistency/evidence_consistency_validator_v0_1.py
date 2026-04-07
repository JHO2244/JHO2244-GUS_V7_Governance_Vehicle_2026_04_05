"""
GUS v7 — Phase 39
Evidence Consistency Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""

from gus_v7.evidence.evidence_validator_v0_1 import validate_evidence_v0_1
from gus_v7.evidence.evidence_fingerprint_v0_1 import fingerprint_evidence_v0_1


CONSISTENCY_LOCK_FIELDS = (
    "evidence_type",
    "source_id",
    "validation_status",
)


def validate_evidence_consistency_v0_1(evidence_bundle: tuple[dict, ...]) -> str:
    """
    Returns:
        "consistent" or "inconsistent"

    Fail-closed behavior:
    - invalid bundle shape -> ValueError
    - invalid evidence item -> ValueError
    """
    if not isinstance(evidence_bundle, tuple):
        raise ValueError("INVALID_EVIDENCE_BUNDLE")

    if len(evidence_bundle) < 2:
        raise ValueError("INVALID_EVIDENCE_BUNDLE")

    fingerprints = []
    reference = None

    for evidence in evidence_bundle:
        if validate_evidence_v0_1(evidence) != "VALID":
            raise ValueError("INVALID_EVIDENCE")

        fingerprint = fingerprint_evidence_v0_1(evidence)
        if fingerprint in fingerprints:
            return "inconsistent"
        fingerprints.append(fingerprint)

        locked_view = tuple((field, evidence[field]) for field in CONSISTENCY_LOCK_FIELDS)

        if reference is None:
            reference = locked_view
            continue

        if locked_view != reference:
            return "inconsistent"

    return "consistent"
