## Purpose

Ensure strategy documentation changes reflect reconciled evidence while retaining provenance and
unresolved dissent.

## ADDED Requirements

### Requirement: Update documentation only after reconciliation
The harness SHALL update the proposed strategy only after all available model reviews are captured
and the reconciliation table is complete.

#### Scenario: Agreement is established
- **GIVEN** source-backed recommendations have been accepted
- **WHEN** documentation is revised
- **THEN** the new revision identifies the evaluated commit, reviewers, accepted changes, rejected
  proposals, unresolved questions, and verification results

### Requirement: Preserve advisory semantics
The revised documentation MUST keep model observations and agreement advisory and MUST NOT allow a
model or model majority to set checklist compliance.

#### Scenario: All models agree
- **GIVEN** every available reviewer recommends the same verdict
- **WHEN** the strategy records that agreement
- **THEN** the checklist decision remains a deterministic or human-controlled action outside the
  models

### Requirement: Preserve evaluation provenance
The reconciliation report SHALL record model identifiers, CLI versions, permission boundaries,
spend or credit ceilings where available, frozen commit, reviewed files, and candidate cleanliness.

#### Scenario: Audit replay
- **GIVEN** a later reviewer reads the reconciliation report
- **WHEN** they inspect provenance
- **THEN** they can identify exactly which source and strategy revision each model assessed
