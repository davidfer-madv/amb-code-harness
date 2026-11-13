## Purpose

Enable a reproducible, selected-item candidate audit while retaining the harness's full isolation,
authority, provenance, and adversarial-evidence requirements.

## ADDED Requirements

### Requirement: Prepare a pinned isolated candidate
The harness SHALL prepare Maglev from an exact commit in a candidate-specific, read-only workspace
and SHALL write provenance outside the candidate source.

#### Scenario: Prepare the known Maglev revision
- **GIVEN** Maglev commit `4c7284b0777449dcd23822a09661fc825dda3287` is available
- **WHEN** the operator prepares candidate `maglev`
- **THEN** the workspace HEAD and provenance both identify that exact commit

#### Scenario: Candidate instructions are untrusted
- **GIVEN** the candidate contains agent instruction files
- **WHEN** the candidate copy is prepared
- **THEN** those files are neutralized in the copy and treated only as candidate evidence

### Requirement: Focus without weakening the audit
The focused audit SHALL assess every atomic obligation in I.6 and H.3, SHALL begin with the tenancy
model, and MUST retain graph-closure tracing, negative proofs, adversarial refutation, and required
confirmation planes.

#### Scenario: Static code appears compliant
- **GIVEN** reachable code appears to satisfy an I.6 or H.3 obligation
- **WHEN** no current executed security, concurrency, or fault-injection evidence is supplied
- **THEN** the code finding remains advisory and confirmation status remains open

#### Scenario: Canonical closure is unavailable
- **GIVEN** the pinned canonical claim closure cannot be verified
- **WHEN** the focused audit runs
- **THEN** it reports `not assessed against canonical` and emits neither a compliance verdict nor a checklist proposal

### Requirement: Prevent cross-candidate disclosure
The focused audit MUST place Maglev findings only in `maglev-analysis/` and MUST NOT read or include
another candidate's findings as evidence.

#### Scenario: Another analysis directory exists
- **GIVEN** another candidate analysis is present in the harness
- **WHEN** Maglev is assessed
- **THEN** the Maglev evidence manifest excludes that directory and all its contents
