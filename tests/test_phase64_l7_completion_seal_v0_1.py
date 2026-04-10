"""
GUS v7 — Phase 64
L7 Completion Seal Tests (v0.1)

STRICT:
- Validate deterministic layer seal creation
- Fail-closed enforcement
- No inference
"""

import json
from pathlib import Path

import pytest

from gus_v7.l7_completion_seal.l7_completion_seal_v0_1 import (
    AUTHORIZED_SIGNER,
    REQUIRED_PHASES,
    create_l7_completion_seal_v0_1,
)


def _write_phase_seals(tmp_path: Path) -> Path:
    seals_dir = tmp_path / "seals"
    seals_dir.mkdir()

    for phase in REQUIRED_PHASES:
        seal_path = seals_dir / f"{phase}_example.json"
        seal_path.write_text(
            json.dumps({"phase": phase, "ok": True}, sort_keys=True),
            encoding="utf-8",
        )

    return seals_dir


def test_phase64_required_phases_exact_match():
    assert REQUIRED_PHASES == [
        "Phase_57",
        "Phase_58",
        "Phase_59",
        "Phase_60",
        "Phase_61",
        "Phase_62",
        "Phase_63",
    ]


def test_phase64_authorized_signer_exact_match():
    assert AUTHORIZED_SIGNER == "gus_seal_signing_ed25519_priv.pem"


def test_phase64_create_l7_completion_seal_accepts_valid_inputs(tmp_path: Path):
    seals_dir = _write_phase_seals(tmp_path)

    result = create_l7_completion_seal_v0_1(
        main_head_sha="abc123",
        seals_dir=seals_dir,
    )

    assert result["layer_name"] == "L7_VEHICLE_COMPLETION"
    assert result["head_sha"] == "abc123"
    assert result["verifier_signature"] is None
    assert len(result["phases_verified"]) == 7
    assert result["timestamp"].endswith("Z")


def test_phase64_create_l7_completion_seal_rejects_invalid_head_sha(tmp_path: Path):
    seals_dir = _write_phase_seals(tmp_path)

    with pytest.raises(ValueError, match="INVALID_HEAD_SHA"):
        create_l7_completion_seal_v0_1(
            main_head_sha="",
            seals_dir=seals_dir,
        )


def test_phase64_create_l7_completion_seal_rejects_invalid_seals_dir():
    with pytest.raises(ValueError, match="INVALID_SEALS_DIR"):
        create_l7_completion_seal_v0_1(
            main_head_sha="abc123",
            seals_dir="not-a-path",
        )


def test_phase64_create_l7_completion_seal_rejects_missing_phase_seal(tmp_path: Path):
    seals_dir = _write_phase_seals(tmp_path)
    (seals_dir / "Phase_63_example.json").unlink()

    with pytest.raises(ValueError, match="MISSING_SEAL: Phase_63"):
        create_l7_completion_seal_v0_1(
            main_head_sha="abc123",
            seals_dir=seals_dir,
        )
