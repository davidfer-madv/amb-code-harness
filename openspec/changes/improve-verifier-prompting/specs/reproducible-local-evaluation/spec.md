## Purpose

Make the prompt improvement testable on localhost without mutating deployed environments or
candidate repositories and without confusing a successful application startup with a valid prompt
comparison.

## ADDED Requirements

### Requirement: Local evaluation MUST use disposable isolated state
Each comparison arm MUST use a disposable Verifier checkout, a distinct PostgreSQL database or
volume, a distinct source-extraction root, and a push-disabled Git remote. Candidate repositories
MUST remain read-only and MUST be identified by frozen commit and tree hashes.

#### Scenario: Two comparison arms are prepared
- **GIVEN** baseline and proposed prompt arms
- **WHEN** their local configuration is inspected
- **THEN** they do not share a mutable database or source root
- **AND** neither checkout can push to its remote
- **AND** both candidate snapshots are pinned and unmodified

### Requirement: Local startup MUST NOT be treated as evaluation readiness
The local procedure SHALL report that a fresh database has no checklist, checks or model registry
and SHALL require a reviewed checklist bundle, tenant binding, exact model and pricing revisions,
analysis limits, prompt revisions and a frozen candidate snapshot before an evaluation run.

#### Scenario: Application starts with an empty database
- **GIVEN** Verifier responds successfully on localhost
- **AND** no checklist or model revisions have been configured
- **WHEN** evaluation readiness is assessed
- **THEN** the instance is reported as running but not ready for a valid prompt comparison

### Requirement: Provider credentials MUST remain outside experiment artifacts
Provider and read-only source credentials MUST be injected through process environment or an
approved secret manager and MUST NOT appear in commits, command arguments, manifests, prompts,
logs, reports, checklist bundles or exported run data.

#### Scenario: Local paid run is configured
- **GIVEN** an Anthropic or OpenAI model will be called
- **WHEN** the experiment manifest and repository diff are inspected
- **THEN** no provider credential is present
- **AND** the model revision, price and cost ceiling are present without the credential

### Requirement: Baseline and proposal comparisons MUST have input parity
Trusted comparison code SHALL refuse a pair unless checklist bundle, candidate snapshot, model,
generation settings, prices, limits, check template, judge prompt, operator instruction and source
limits match. Only the declared application/prompt treatment MAY differ.

#### Scenario: Proposal uses a different checklist bundle
- **GIVEN** baseline and proposal runs have different normalized checklist hashes
- **WHEN** comparison is requested
- **THEN** the comparison is refused
- **AND** neither result is described as the prompt treatment effect

### Requirement: Paid localhost evaluation MUST be explicitly cost-gated
Offline tests and a dry cost preview MUST precede paid calls. Each paid run MUST have an explicit
nonzero per-check token maximum and dollar ceiling, and the experiment MUST have an operator-approved
total ceiling.

#### Scenario: Provider key exists but cost ceiling is absent
- **GIVEN** provider credentials are available
- **AND** the dollar or token ceiling is zero or unspecified
- **WHEN** a paid run is requested
- **THEN** the run is refused before a provider call

### Requirement: Prompt-only and clause-aware treatments MUST be distinguished
Reports MUST label the v2 text appended to the existing flat tool contracts as a prompt-only
precision pilot. Only the trusted clause-keyed schema and completeness-aware aggregation treatment
may claim deterministic mandatory-part coverage.

#### Scenario: Prompt-only arm avoids one false positive
- **GIVEN** the existing flat `report_terms` and `report_site` schemas remain unchanged
- **WHEN** the improved wording produces a better classification
- **THEN** the improvement is reported as prompt-only precision evidence
- **AND** no completeness guarantee is claimed
