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
            json.dumps({"ok": True, "phase": phase}, sort_keys=True),
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
        timestamp_utc="2026-04-19T10:00:00Z",
    )

    assert result == {
        "layer_name": "L7_VEHICLE_COMPLETION",
        "head_sha": "abc123",
                "phases_verified": [
            {
                "phase": "Phase_57",
                "seal_file": str(seals_dir / "Phase_57_example.json"),
                "seal_hash": "1bd1327125198b71318c2430e06017e6feedf5786aecce504c89734c379b204a",
            },
            {
                "phase": "Phase_58",
                "seal_file": str(seals_dir / "Phase_58_example.json"),
                "seal_hash": "f223b364e5d0914263132cdd4523a8d3d6efd6c944a8efe5ee72c6e518575657",
            },
            {
                "phase": "Phase_59",
                "seal_file": str(seals_dir / "Phase_59_example.json"),
                "seal_hash": "42e78033656527f712a4d561d8b74d4b13c0d90d5faedbb98d494bcdcb47c4f5",
            },
            {
                "phase": "Phase_60",
                "seal_file": str(seals_dir / "Phase_60_example.json"),
                "seal_hash": "3463202bd861179dd051b6a3f2fbe7345312365031d489f2a9b9b51a5ec59f80",
            },
            {
                "phase": "Phase_61",
                "seal_file": str(seals_dir / "Phase_61_example.json"),
                "seal_hash": "7850ff8380be24dfdd8cfeeb0b92b85ff72556c0ab437fc0419a9f43cbeb8800",
            },
            {
                "phase": "Phase_62",
                "seal_file": str(seals_dir / "Phase_62_example.json"),
                "seal_hash": "2324975a73a1c8c30f67533f5902c2b20bf7a38e8826290f3c9de3064ed67282",
            },
            {
                "phase": "Phase_63",
                "seal_file": str(seals_dir / "Phase_63_example.json"),
                "seal_hash": "43b664f6e4f307e47d7a835c33f2b7fa4ed8ff03e39247cdc510f2513d207c04",
            },
        ],
        "timestamp": "2026-04-19T10:00:00Z",
        "verifier_signature": None,
    }


def test_phase64_create_l7_completion_seal_rejects_invalid_head_sha(tmp_path: Path):
    seals_dir = _write_phase_seals(tmp_path)

    with pytest.raises(ValueError, match="INVALID_HEAD_SHA"):
        create_l7_completion_seal_v0_1(
            main_head_sha="",
            seals_dir=seals_dir,
            timestamp_utc="2026-04-19T10:00:00Z",
        )


def test_phase64_create_l7_completion_seal_rejects_invalid_seals_dir():
    with pytest.raises(ValueError, match="INVALID_SEALS_DIR"):
        create_l7_completion_seal_v0_1(
            main_head_sha="abc123",
            seals_dir="not-a-path",
            timestamp_utc="2026-04-19T10:00:00Z",
        )


def test_phase64_create_l7_completion_seal_rejects_invalid_timestamp():
    with pytest.raises(ValueError, match="INVALID_TIMESTAMP_UTC"):
        create_l7_completion_seal_v0_1(
            main_head_sha="abc123",
            seals_dir=Path("seals"),
            timestamp_utc="2026-04-19T10:00:00",
        )


def test_phase64_create_l7_completion_seal_rejects_missing_phase_seal(tmp_path: Path):
    seals_dir = _write_phase_seals(tmp_path)
    (seals_dir / "Phase_63_example.json").unlink()

    with pytest.raises(ValueError, match="MISSING_SEAL: Phase_63"):
        create_l7_completion_seal_v0_1(
            main_head_sha="abc123",
            seals_dir=seals_dir,
            timestamp_utc="2026-04-19T10:00:00Z",
        )
