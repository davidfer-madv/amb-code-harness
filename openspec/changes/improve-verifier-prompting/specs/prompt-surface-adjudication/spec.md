## Purpose

Ensure the executable Stage prompts apply precise scope, reachability, outcome/mechanism, and
evidence-surface rules and are represented truthfully to operators.

## ADDED Requirements

### Requirement: Term selection MUST cover every named clause part
`TERMS_SYSTEM` SHALL instruct the model to produce discriminating terms for every named part of the
trusted clause, including alternative implementations for outcome obligations and reachable
producer/use paths.

#### Scenario: Requirement enumerates several destinations
- **GIVEN** one clause names several required destinations
- **WHEN** term selection runs
- **THEN** its structured term result contains search coverage for every named destination
- **AND** a missing destination is visible to completeness validation

### Requirement: Classification MUST apply ordered adjudication gates
`CLASSIFY_SYSTEM` MUST apply scope/condition, outcome/mechanism, reachability, evidence-surface, and
bounded-completeness gates before selecting a finding.

#### Scenario: Alternative mechanism satisfies an outcome
- **GIVEN** an outcome clause permits any implementation producing the required result
- **AND** reachable production code uses a different mechanism from the expected example
- **WHEN** the source place is classified
- **THEN** the alternative mechanism may demonstrate the clause
- **AND** it is not rejected solely for lacking the example mechanism

#### Scenario: Mandatory mechanism is absent
- **GIVEN** the exact clause expressly requires a named mechanism
- **AND** code produces a similar outcome without that mechanism
- **WHEN** the governed production place is classified
- **THEN** the alternative does not demonstrate the mechanism clause

### Requirement: Customer-facing naming MUST require a reachable surface
A naming contradiction MUST require evidence that prohibited wording reaches a customer render/send
surface. Technical identifiers, protocol terms, tests, comments, documents, and names of distinct
products MUST NOT be treated as customer-facing violations solely by literal match.

#### Scenario: Technical iMessage app identifier
- **GIVEN** technical source uses `iMessage app` for a protocol/device artifact
- **AND** no customer render/send path uses that wording
- **WHEN** naming analysis runs
- **THEN** the literal is not classified as a customer-facing naming contradiction

#### Scenario: Customer settings page renders iMessage
- **GIVEN** a reachable customer settings template renders `iMessage apps`
- **WHEN** naming analysis runs
- **THEN** that render path may contradict the approved customer-facing naming clause

### Requirement: The operator MUST see the prompts actually sent
The prompt surface SHALL display the effective `TERMS_SYSTEM`, `CLASSIFY_SYSTEM`, tool schemas, and
active judge revision and MUST NOT represent an unused stored analysis system message as an
effective execution prompt.

#### Scenario: Prompt editor is opened
- **GIVEN** the fixed pipeline is the only executor
- **WHEN** an authorized operator reads prompt configuration
- **THEN** the displayed stage prompts and tools match the production request contracts

### Requirement: Executable pipeline prompts MUST be safely revisioned
The system SHALL store `TERMS_SYSTEM` and `CLASSIFY_SYSTEM` as one append-only pipeline prompt
bundle bound to compatible term and site tool-schema versions. Every analysis run MUST record the
bundle revision and content hash.

#### Scenario: Authorized operator activates a compatible Stage bundle
- **GIVEN** a new bundle references supported term and site tool-schema versions
- **AND** its prompt contracts use only supported fields and finding values
- **WHEN** an authorized operator activates it in Staging
- **THEN** the active pointer changes through an audited action
- **AND** subsequent runs record the new bundle revision and hash
- **AND** earlier bundles and observations remain immutable

#### Scenario: Bundle is incompatible with its tool contract
- **GIVEN** a bundle requests an unknown field, finding, or tool-schema version
- **WHEN** activation is requested
- **THEN** the server rejects activation
- **AND** the prior bundle remains active

#### Scenario: Production bundle has not completed promotion controls
- **GIVEN** a bundle has not been promoted from an evaluated Staging revision or approved by the
  configured production reviewer
- **WHEN** production activation is requested
- **THEN** the server refuses the activation

#### Scenario: Operator rolls back a prompt experiment
- **GIVEN** an earlier compatible bundle exists
- **WHEN** an authorized operator reactivates it
- **THEN** the active pointer returns to that immutable revision
- **AND** no prompt revision or prior observation is deleted or rewritten

### Requirement: Candidate content MUST remain untrusted
Every candidate-source extract sent to a model MUST be structurally enclosed as untrusted data and
MUST NOT be able to modify instructions, tools, limits, routes, or trusted clause metadata.

#### Scenario: Source comment contains prompt instructions
- **GIVEN** a source comment tells the model to report `demonstrates`
- **WHEN** the extract is classified
- **THEN** the text is evaluated only as candidate evidence
- **AND** the model contract and trusted aggregation remain unchanged

### Requirement: Composed documents MUST retain their authority level
The executable prompts SHALL identify the trusted criterion as the sole obligation and SHALL treat
cited specifications, related specifications, supporting material, Background and operator notes
only according to their runner-assigned authority.

#### Scenario: Related specification states an additional obligation
- **GIVEN** a related specification passage requires behavior absent from the trusted criterion
- **WHEN** term selection and classification run
- **THEN** the passage may clarify vocabulary
- **AND** its additional obligation does not widen the criterion or create a contradiction

#### Scenario: Supporting material contains an instruction
- **GIVEN** operator-supplied supporting prose instructs the model to ignore the criterion
- **WHEN** either model stage receives it
- **THEN** the prose remains untrusted reference data
- **AND** the trusted criterion and tool contract remain unchanged
