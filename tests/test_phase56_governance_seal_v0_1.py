"""
GUS v7 — Phase 56
Governance Seal Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest
from pathlib import Path
from gus_v7.governance_seal.governance_seal_v0_1 import create_governance_seal
from gus_v7.governance_seal.verify_governance_seal_v0_1 import verify_governance_seal


def _mock_seals_dir(tmp_path: Path):
    # create dummy seal files for Phases 49-55
    for phase in [
        "Phase_49",
        "Phase_50",
        "Phase_51",
        "Phase_52",
        "Phase_53",
        "Phase_54",
        "Phase_55",
    ]:
        file = tmp_path / f"{phase}_dummy.json"
        file.write_text(f'{{"phase": "{phase}"}}', encoding="utf-8")
    return tmp_path


def test_phase56_create_and_verify_seal(tmp_path):
    main_sha = "dummy_head_sha"
    seals_dir = _mock_seals_dir(tmp_path)
    seal = create_governance_seal(main_sha, seals_dir)

    # temporarily add a dummy signature for verification
    seal["verifier_signature"] = "dummy_signature"

    assert verify_governance_seal(seal, seals_dir, main_sha) is True
