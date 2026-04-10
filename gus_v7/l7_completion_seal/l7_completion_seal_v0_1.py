"""
GUS v7 — Phase 64
L7 Completion Seal (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

import hashlib
from datetime import datetime
from pathlib import Path

AUTHORIZED_SIGNER = "gus_seal_signing_ed25519_priv.pem"

REQUIRED_PHASES = [
    "Phase_57",
    "Phase_58",
    "Phase_59",
    "Phase_60",
    "Phase_61",
    "Phase_62",
    "Phase_63",
]


def create_l7_completion_seal_v0_1(main_head_sha: str, seals_dir: Path) -> dict:
    """
    Generates a canonical L7 Completion Seal for Phases 57–63.

    Fail-closed behavior:
    - missing seal file -> ValueError
    - missing required input -> ValueError
    """

    if not isinstance(main_head_sha, str) or main_head_sha.strip() == "":
        raise ValueError("INVALID_HEAD_SHA")

    if not isinstance(seals_dir, Path):
        raise ValueError("INVALID_SEALS_DIR")

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

    timestamp = datetime.utcnow().isoformat() + "Z"

    seal = {
        "layer_name": "L7_VEHICLE_COMPLETION",
        "head_sha": main_head_sha,
        "phases_verified": phases_verified,
        "timestamp": timestamp,
        "verifier_signature": None,
    }

    return seal
