## Purpose

Provide a deterministic, read-only way to select complete checklist records for focused audits and
review without hand-copying fields or losing CSV structure.

## ADDED Requirements

### Requirement: Extract complete checklist records
The harness SHALL accept one or more exact checklist item IDs and emit every field from the
authoritative CSV record in a machine-readable format.

#### Scenario: Extract I.6 and H.3
- **GIVEN** the current checklist CSV contains I.6 and H.3
- **WHEN** an operator requests `I.6 H.3`
- **THEN** the output contains exactly two records and preserves all checklist columns

#### Scenario: Reject an unknown item
- **GIVEN** a requested item ID is absent
- **WHEN** extraction runs
- **THEN** the command exits non-zero, identifies the missing ID, and does not emit a misleading partial success

### Requirement: Preserve checklist source
Extraction MUST be read-only and MUST NOT change either checklist representation.

#### Scenario: Extraction has no source side effects
- **GIVEN** the Markdown and CSV checklist hashes are recorded
- **WHEN** extraction completes
- **THEN** both source hashes remain unchanged
