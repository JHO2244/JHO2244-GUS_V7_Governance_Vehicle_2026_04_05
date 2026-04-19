"""
GUS v7 — Phase 56
Governance Seal Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import json
from pathlib import Path

import pytest

from gus_v7.governance_seal.governance_seal_v0_1 import (
    AUTHORIZED_SIGNER,
    REQUIRED_PHASES,
    create_governance_seal,
)
from gus_v7.governance_seal.verify_governance_seal_v0_1 import verify_governance_seal


def _mock_seals_dir(tmp_path: Path) -> Path:
    for phase in REQUIRED_PHASES:
        file = tmp_path / f"{phase}_dummy.json"
        file.write_text(
            json.dumps({"phase": phase}, sort_keys=True),
            encoding="utf-8",
        )
    return tmp_path


def test_phase56_required_phases_exact_match():
    assert REQUIRED_PHASES == [
        "Phase_49",
        "Phase_50",
        "Phase_51",
        "Phase_52",
        "Phase_53",
        "Phase_54",
        "Phase_55",
    ]


def test_phase56_authorized_signer_exact_match():
    assert AUTHORIZED_SIGNER == "gus_seal_signing_ed25519_priv.pem"


def test_phase56_create_and_verify_seal(tmp_path: Path):
    main_sha = "dummy_head_sha"
    seals_dir = _mock_seals_dir(tmp_path)

    seal = create_governance_seal(
        main_sha,
        seals_dir,
        "2026-04-19T10:30:00Z",
    )

    seal["verifier_signature"] = "dummy_signature"

    assert seal["layer_name"] == "L6_GOVERNANCE"
    assert seal["head_sha"] == "dummy_head_sha"
    assert seal["timestamp"] == "2026-04-19T10:30:00Z"
    assert len(seal["phases_verified"]) == 7
    assert verify_governance_seal(seal, seals_dir, main_sha) is True


def test_phase56_rejects_invalid_head_sha(tmp_path: Path):
    seals_dir = _mock_seals_dir(tmp_path)

    with pytest.raises(ValueError, match="INVALID_HEAD_SHA"):
        create_governance_seal(
            "",
            seals_dir,
            "2026-04-19T10:30:00Z",
        )


def test_phase56_rejects_invalid_seals_dir():
    with pytest.raises(ValueError, match="INVALID_SEALS_DIR"):
        create_governance_seal(
            "dummy_head_sha",
            "not-a-path",
            "2026-04-19T10:30:00Z",
        )


def test_phase56_rejects_invalid_timestamp():
    with pytest.raises(ValueError, match="INVALID_TIMESTAMP_UTC"):
        create_governance_seal(
            "dummy_head_sha",
            Path("seals"),
            "2026-04-19T10:30:00",
        )
