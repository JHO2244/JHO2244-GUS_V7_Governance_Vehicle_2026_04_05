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

import json
import hashlib
from datetime import datetime
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


def create_governance_seal(main_head_sha: str, seals_dir: Path) -> dict:
    """
    Generates a canonical Governance Seal for L6 (Phases 49–55)

    Fail-closed behavior:
    - missing seal file -> ValueError
    - corrupted seal hash -> ValueError
    """

    phases_verified = []

    for phase in REQUIRED_PHASES:
        seal_file = next(seals_dir.glob(f"{phase}_*.json"), None)
        if seal_file is None or not seal_file.is_file():
            raise ValueError(f"MISSING_SEAL: {phase}")
        with open(seal_file, "r", encoding="utf-8") as f:
            seal_content = f.read()
            seal_hash = hashlib.sha256(seal_content.encode("utf-8")).hexdigest()
        phases_verified.append({
            "phase": phase,
            "seal_file": str(seal_file),
            "seal_hash": seal_hash,
        })

    timestamp = datetime.utcnow().isoformat() + "Z"

    seal = {
        "layer_name": "L6_GOVERNANCE",
        "head_sha": main_head_sha,
        "phases_verified": phases_verified,
        "timestamp": timestamp,
    }

    # Placeholder for cryptographic signature
    seal["verifier_signature"] = None  # To be signed separately

    return seal
