## Purpose

Ensure a localhost evaluation attributes result differences to the proposed implementation rather
than to different code baselines, checklists, prompts, models, limits, candidate snapshots, or run
conditions.

## ADDED Requirements

### Requirement: The comparison MUST contain three isolated arms
The evaluation SHALL run the exact deployed Staging revision, current `stage`, and the proposal
branch in separate local databases and source stores.

#### Scenario: All three arms are ready
- **GIVEN** each arm records its commit and tree hash
- **AND** each arm has a distinct database and source root
- **WHEN** the experiment begins
- **THEN** no arm can read or write another arm's run, prompt, checklist, or candidate state

#### Scenario: An arm does not match its declared revision
- **GIVEN** an arm's checked-out commit differs from the experiment manifest
- **WHEN** preflight runs
- **THEN** paid model calls are refused
- **AND** the comparison is not reported as valid

### Requirement: Every compared run MUST use frozen equivalent inputs
The harness SHALL verify equivalent checklist content, candidate tree, clause selection, prompt and
tool contracts, model revision, generation settings, limits, and operator instruction before
comparing two runs.

#### Scenario: Inputs are equivalent
- **GIVEN** all comparison hashes and normalized settings match
- **WHEN** paired runs finish
- **THEN** their results may enter the comparison report

#### Scenario: A prompt or checklist differs unexpectedly
- **GIVEN** either run has an unexpected prompt, tool, checklist, or candidate hash
- **WHEN** comparison preflight evaluates the pair
- **THEN** it labels the pair non-comparable
- **AND** excludes it from improvement metrics

### Requirement: Anthropic and OpenAI requests MUST use identical registered contracts per provider
Each provider comparison SHALL use the same pinned model identifier, generation settings, price
revision, prompt bundle, limits, and frozen input in all eligible arms.

#### Scenario: A provider model is available in every arm
- **GIVEN** one pinned model revision is registered identically in all arms
- **WHEN** the provider comparison runs
- **THEN** every request records the same model and settings identity
- **AND** token and cost measurements remain separated by provider and workload

#### Scenario: A model identifier or setting differs
- **GIVEN** one arm has a different identifier, generation setting, or price revision
- **WHEN** paid-run preflight runs
- **THEN** that provider comparison is refused until parity is restored

### Requirement: Checklist provenance MUST be demonstrated before evaluation
The experiment SHALL record the named August CSV hash, a normalized semantic hash, and the imported
Verifier bundle hash. A live Staging checklist SHALL be called current only after an authenticated
export is compared against those values.

#### Scenario: Live Staging matches the August checklist
- **GIVEN** an authorized read-only export of the active canonical checklist
- **WHEN** normalized item IDs and material fields match the August source
- **THEN** the report may state that Staging uses that checklist
- **AND** it records both source and export hashes

#### Scenario: Live Staging cannot be read
- **GIVEN** the checklist API requires authentication that the evaluator does not have
- **WHEN** provenance is reported
- **THEN** the report says the live checklist is unconfirmed
- **AND** repository artifacts are not substituted as proof of database state

### Requirement: Split and malformed checklist rows MUST be normalized before code planning
The intake SHALL preserve intentional atomic child requirements, merge presentation-only fragments
under their parent, reject malformed rows, and exclude requirements whose declared `Provide Code`
method has no source-observable assertion.

#### Scenario: Endpoint parent contains eight independently testable children
- **GIVEN** `B.1 a` through `B.1 h` each state a distinct endpoint obligation
- **WHEN** the checklist is normalized
- **THEN** all eight retain stable child identities under one parent
- **AND** completeness requires an outcome for every applicable child

#### Scenario: Construct Payload is split into presentation fragments
- **GIVEN** `C.13 a`, `C.13 b`, and `C.13 c` collectively state one requirement with three variants
- **WHEN** the checklist is normalized
- **THEN** one parent requirement owns three mandatory clauses
- **AND** one variant cannot make the parent implemented

#### Scenario: Declared code method has no source assertion
- **GIVEN** `A.3` asks only for planning of external approval lead times
- **WHEN** code-analysis planning runs
- **THEN** it is excluded from source analysis
- **AND** it is routed to the appropriate human or project evidence method

### Requirement: Paid evaluation MUST be staged and cost bounded
The experiment SHALL run offline tests first, then a small paired smoke set, and only then the frozen
golden set under an explicit per-arm and total cost ceiling.

#### Scenario: Smoke evaluation satisfies safety gates
- **GIVEN** offline tests pass and the cost preview is approved
- **WHEN** the smoke set finishes without critical false greens or parity failures
- **THEN** the operator may authorize the larger golden run

#### Scenario: A safety or parity gate fails
- **GIVEN** a critical false green, invalid citation, unexpected input hash, or spend ceiling breach
- **WHEN** the harness detects it
- **THEN** later paid batches do not start
- **AND** completed immutable results remain available for diagnosis
