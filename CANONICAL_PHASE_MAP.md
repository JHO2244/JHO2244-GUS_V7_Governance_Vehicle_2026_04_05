# CANONICAL_PHASE_MAP.md

## Purpose

This file is the authoritative truth map for GUS v7 phase numbering where:
- historical file/module names
- historical branch names
- historical chat bridges
- current canonical meaning

do not perfectly align.

This document exists to remove ambiguity **without** rewriting git history or renaming stable code artifacts unnecessarily.

---

## Core Rule

**Repo truth is preserved. Canonical interpretation is documented.**

Therefore:

- existing code file names may remain historical
- existing test file names may remain historical
- branch and commit history remain untouched
- current system meaning is clarified here explicitly

This avoids:
- churn
- broken imports
- fake cleanliness
- loss of provenance

---

## Canonical Doctrine

### 1. Do not rename stable code only to match newer narrative numbering
Historical code names may remain if behavior is correct and provenance matters more than cosmetic consistency.

### 2. One domain must have one canonical authority
If multiple names appear to govern the same responsibility, the canonical authority must be declared explicitly here and enforced in code/tests.

### 3. Temporary campaign labels must not survive as permanent architectural authority
Terms like:
- hardening
- repair
- hotfix
- recovery
- attack response

may exist in:
- branch names
- PR titles
- GRC history
- CTB history

but should not remain as permanent module authority names unless the capability itself is specifically about repair/hardening.

### 4. Vehicle 1 scope lock
No new vehicles, no new domains, and no v8 expansion planning may begin until GUS v7 Vehicle 1 reaches canonical closure.

---

## Current Canonical Truth Map

| Historical Artifact / Label | Current Canonical Meaning | Status | Notes |
|---|---|---|---|
| Phase 61 - Identity Lifecycle Integration | Identity lifecycle enforcement at boundary level | COMPLETE | Canonical identity authority is `global_identity_lifecycle` and boundary integration modules. |
| `historical_decision_analytics` (built as Phase 61 in earlier sequence) | Historical analytics capability | COMPLETE | Preserved as historical file/module naming; treated as legacy precursor within evolving L7 numbering. |
| `risk_assessment` (built as Phase 62 in earlier sequence) | Risk assessment capability | COMPLETE | Preserved as historical file/module naming; sits between historical analytics and later completion layers. |
| `governance_notifications_hooks` | Notifications / hooks capability | PRESENT IN REPO | Must be interpreted through current canonical phase planning before further build decisions. |
| `l7_completion_seal` | L7 completion / final closure capability | PRESENT IN REPO | Existing completion seal artifact remains historical repo truth pending final validation against current closure intent. |

---

## Identity / Execution Authority Clarification

### Canonical identity authority
- `gus_v7/global_identity_lifecycle/global_identity_lifecycle_validator_v0_1.py`

This is the enduring authority for:
- trace ID reuse protection
- decision ID reuse protection
- evidence binding reuse protection
- integrity envelope reuse protection
- replay rejection across admitted history

### Canonical execution/verdict binding authority
- `gus_v7/decision_execution_trace/decision_execution_trace_logger_v0_1.py`

This is the enduring authority for:
- `INTEGRITY_CONFIRMED -> EXECUTE`
- `INTEGRITY_REJECTED -> BLOCK`
- invalid trace rejection at the execution-trace boundary

### Retired temporary authority
The old `phase1_hardening` authority was a historical hardening wrapper and is no longer a canonical architectural owner.

---

## Why This File Exists

GUS v7 evolved through:
- layered build progression
- red-team discovery
- hardening integration
- cross-chat continuity bridges
- corrected workflow law

That process produced real value, but also created naming drift between:
- repo artifacts
- CTB wording
- evolving FAP wording
- canonical interpretation

This file prevents future confusion without falsifying the build journey.

---

## Build Rule Going Forward

Before any future phase build:
1. check repo truth
2. check this canonical phase map
3. follow current FAP/workflow authority
4. do not rename stable code unless there is a structural reason, not a cosmetic one

---

## Scope Lock

Vehicle 1 remains the only active build scope until:
- canonical phase ambiguity is resolved
- final L7 closure is completed
- final seal/closure authority is verified
- pushed main reflects canonical truth

Until then:
- no Vehicle 2 work
- no range expansion
- no speculative new domain buildout

---

## ELI5

Some room names changed while the house was being built.

We are **not** rebuilding the house.

We are writing the official legend so every future builder knows:
- what each room really is
- which room name is historical
- which room authority is final
- 