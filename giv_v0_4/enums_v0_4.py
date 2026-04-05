from __future__ import annotations

from enum import Enum


class GIVHardOutputStateV0_4(str, Enum):
    """
    Hard output states for the Governance Integrity Verifier vehicle.

    These are closed and authoritative for GIV v0.4.
    """

    PASS = "PASS"
    FAIL = "FAIL"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
