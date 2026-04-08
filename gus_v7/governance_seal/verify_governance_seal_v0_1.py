"""
GUS v7 — Phase 56
Governance Seal Verifier (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

import json
import hashlib
from pathlib import Path


REQUIRED_PHASES = [
    "Phase_49",
    "Phase_50",
    "Phase_51",
    "Phase_52",
    "Phase_53",
    "Phase_54",
    "Phase_55",
]


def verify_governance_seal(seal: dict, seals_dir: Path, main_head_sha: str) -> bool:
    """
    Verifies the canonical Governance Seal for L6 (Phases 49–55)

    Returns True if seal is valid, else raises ValueError.
    """

    if seal["layer_name"] != "L6_GOVERNANCE":
        raise ValueError("INVALID_LAYER_NAME")

    if seal["head_sha"] != main_head_sha:
        raise ValueError("HEAD_MISMATCH")

    phases_verified = seal.get("phases_verified", [])
    if len(phases_verified) != len(REQUIRED_PHASES):
        raise ValueError("MISSING_PHASES")

    for phase_info in phases_verified:
        phase_name = phase_info.get("phase")
        if phase_name not in REQUIRED_PHASES:
            raise ValueError(f"UNKNOWN_PHASE: {phase_name}")

        seal_file_path = Path(phase_info.get("seal_file", ""))
        if not seal_file_path.is_file():
            raise ValueError(f"MISSING_SEAL_FILE: {phase_name}")

        with open(seal_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if expected_hash != phase_info.get("seal_hash"):
            raise ValueError(f"SEAL_HASH_MISMATCH: {phase_name}")

    # Signature verification placeholder (future step)
    if seal.get("verifier_signature") is None:
        raise ValueError("MISSING_SIGNATURE")

    return True
