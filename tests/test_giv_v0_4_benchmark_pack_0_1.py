import pytest


def test_benchmark_pack_0_1_is_intentionally_not_implemented_yet() -> None:
    """
    Phase 01 anchor lock.

    The v7 vehicle must be calibrated against 3 real-world benchmark cases
    before any measurement logic is trusted:

    1. Transparent Vendor Selection -> PASS
    2. Conflict-of-Interest Award -> FAIL
    3. Cost-Cutting Unclear Impact -> INSUFFICIENT_EVIDENCE

    This placeholder test fails on purpose until the benchmark pack and
    evaluation surface are implemented.
    """
    pytest.fail(
        "Benchmark Pack 0.1 not implemented yet: "
        "missing 3 real-world anchor cases and evaluation surface."
    )
