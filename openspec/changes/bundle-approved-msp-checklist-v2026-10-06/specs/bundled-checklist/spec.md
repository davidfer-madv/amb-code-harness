# Bundled approved checklist

## ADDED Requirements

### Requirement: Distribute an immutable fallback copy of the approved MSP checklist

The harness SHALL include the approved MSP checklist `v2026.10.06` as a versioned JSON artifact
whose SHA-256 is
`a16748f0fb6dab0a4ede7da733f49361b4c9b651c21318ddc2a205b02ac462d1` and whose provenance records
approved status.

#### Scenario: Team member cannot locate the canonical checkout

- **GIVEN** a clean clone without access to the separate `AMB-canonical` checkout
- **WHEN** the team member needs the approved checklist
- **THEN** an exact fallback copy is available at a stable repository-relative path
- **AND** its version, approval and checksum can be verified locally

#### Scenario: Bundled content drifts

- **GIVEN** the checklist or provenance no longer matches the pinned release metadata
- **WHEN** repository validation runs
- **THEN** validation fails before the repository is declared ready for publication

### Requirement: Preserve upstream canonical authority

The harness MUST identify `AMB-canonical` as the upstream checklist authority and normal audit
source, and MUST continue to require pinned canonical claim closure for compliance adjudication.
It MUST NOT automatically prefer the fallback copy or select a checklist through a moving `latest`
alias.

#### Scenario: A newer file exists upstream

- **GIVEN** a newer checklist is created in `AMB-canonical`
- **WHEN** a team member consults the bundled `v2026.10.06` fallback
- **THEN** the audit remains pinned to `v2026.10.06`
- **AND** the bundle changes only through a separately reviewed harness change

#### Scenario: Canonical claim closure is unavailable

- **GIVEN** the checklist bundle passes its integrity checks
- **BUT** the required pinned canonical claim closure is unavailable or invalid
- **WHEN** an item is assessed
- **THEN** the harness prohibits a compliance verdict

### Requirement: Preserve candidate isolation

Bundling an approved checklist MUST NOT write to candidate source or include candidate evidence,
reports, credentials or cross-candidate material.

#### Scenario: Candidate content resembles checklist instructions

- **GIVEN** untrusted candidate content asks the agent to replace or reinterpret the bundled file
- **WHEN** the audit runs
- **THEN** the request is ignored as candidate evidence
- **AND** the pinned bundle remains unchanged
