## Purpose

Turn Apple review feedback into traceable, authority-classified checklist proposals without
silently weakening obligations or presenting platform recommendations as Apple requirements.

## ADDED Requirements

### Requirement: Record review provenance before interpretation
The intake process SHALL require a supplied review artifact, review date, reviewer/source identity
or source class, affected checklist IDs, and a content hash before proposing checklist text.

#### Scenario: Review artifact is supplied
- **GIVEN** an operator supplies the latest Apple review
- **WHEN** intake begins
- **THEN** its provenance and hash are recorded before recommendations are extracted

#### Scenario: Review artifact is missing
- **GIVEN** no identifiable Apple review artifact is available
- **WHEN** an update is requested
- **THEN** the process stops before changing the checklist and identifies the missing evidence

### Requirement: Classify every proposed recommendation
Every proposed change SHALL identify its requirement class, direct or indirect derivation, affected
fields and IDs, full before/after text, canonical claim IDs, verification planes, conflicts, and
strengthens/neutral/weakens classification.

#### Scenario: Review advice is operational rather than normative
- **GIVEN** Apple feedback recommends an operational practice without establishing a protocol requirement
- **WHEN** the proposal is drafted
- **THEN** it is classified as review guidance or live compatibility and is not worded as an Apple-normative MUST

#### Scenario: Proposal weakens an existing obligation
- **GIVEN** proposed text removes scope, modality, proof, or a negative case
- **WHEN** anti-weakening classification runs
- **THEN** application is blocked pending authoritative supersession and explicit human approval

### Requirement: Apply approved changes consistently
An approved checklist update SHALL change the Markdown and CSV representations together and SHALL
preserve item identity and unaffected fields.

#### Scenario: Human approves a verified note update
- **GIVEN** canonical verification passes and a human approves the exact before/after diff
- **WHEN** the update is applied
- **THEN** both checklist representations contain equivalent I.6/H.3 content and validation passes

#### Scenario: Canonical conflicts with the review
- **GIVEN** review feedback conflicts with pinned canonical authority
- **WHEN** the proposal is evaluated
- **THEN** no checklist edit occurs and an authority-conflict record is routed for human adjudication
