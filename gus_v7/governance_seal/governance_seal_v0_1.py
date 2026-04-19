"""
GUS v7 — Phase 56
Governance Seal (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

import hashlib
from pathlib import Path

AUTHORIZED_SIGNER = "gus_seal_signing_ed25519_priv.pem"

REQUIRED_PHASES = [
    "Phase_49",
    "Phase_50",
    "Phase_51",
    "Phase_52",
    "Phase_53",
    "Phase_54",
    "Phase_55",
]


def _validate_timestamp_utc(timestamp_utc: str) -> None:
    if not isinstance(timestamp_utc, str) or timestamp_utc.strip() == "":
        raise ValueError("INVALID_TIMESTAMP_UTC")

    if not timestamp_utc.endswith("Z"):
        raise ValueError("INVALID_TIMESTAMP_UTC")


def create_governance_seal(
    main_head_sha: str,
    seals_dir: Path,
    timestamp_utc: str,
) -> dict:
    """
    Generates a canonical Governance Seal for L6 (Phases 49–55)

    Fail-closed behavior:
    - missing seal file -> ValueError
    - invalid required input -> ValueError
    """

    if not isinstance(main_head_sha, str) or main_head_sha.strip() == "":
        raise ValueError("INVALID_HEAD_SHA")

    if not isinstance(seals_dir, Path):
        raise ValueError("INVALID_SEALS_DIR")

    _validate_timestamp_utc(timestamp_utc)

    phases_verified = []

    for phase in REQUIRED_PHASES:
        seal_file = next(seals_dir.glob(f"{phase}_*.json"), None)
        if seal_file is None or not seal_file.is_file():
            raise ValueError(f"MISSING_SEAL: {phase}")

        with open(seal_file, "r", encoding="utf-8") as f:
            seal_content = f.read()

        seal_hash = hashlib.sha256(seal_content.encode("utf-8")).hexdigest()

        phases_verified.append(
            {
                "phase": phase,
                "seal_file": str(seal_file),
                "seal_hash": seal_hash,
            }
        )

    seal = {
        "layer_name": "L6_GOVERNANCE",
        "head_sha": main_head_sha,
        "phases_verified": phases_verified,
        "timestamp": timestamp_utc,
        "verifier_signature": None,
    }

    return seal
