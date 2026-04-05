"""
GUS v7 — Phase 05
Case Registry (v0.1)

STRICT:
- Deterministic registry only
- No inference
- No dynamic discovery
- Canonical case-to-module mapping
"""

from __future__ import annotations


CASE_REGISTRY_V0_1 = {
    "BC-01": {
        "schema_module": "gus_v7.cases.benchmark_case_01_schema_v0_1",
        "validator_module": "gus_v7.validators.benchmark_case_01_validator_v0_1",
        "validator_function": "validate_benchmark_case_01",
    },
}
