# Directional probe expansion

## ADDED Requirements

### Requirement: Every new probe MUST bind to an existing pinned checklist item

The reviewed build manifest for every new probe revision MUST identify a primary item code and UID
present in the pinned checklist. The generated Verifier bundle MUST use the existing check schema,
MUST list item codes only in the supported `checklist_item_codes` reference field, and MUST create
execution associations only through existing item `check_bindings`. Any secondary binding MUST
independently map a retained assertion to requirement text for that existing item. Unknown, unbound
or method-incompatible executable probes MUST be rejected.

Every new probe name MUST use `<suite or campaign> · <primary item code> · <specific scenario>`.
The item code shown in the name MUST agree with the primary code in reviewed provenance and in
`checklist_item_codes`, but MUST NOT be treated as an execution binding. Existing probe names are
natural keys and MUST NOT be retrofitted by delete-and-recreate or ordinary renamed bundle upsert;
an approved migration MUST preserve definition identity, revision history and all bindings.

#### Scenario: An unbound check is imported

- **GIVEN** a new check with no existing v2026.10.06 item/UID binding
- **WHEN** bundle validation runs
- **THEN** import is rejected
- **AND** the error names the check and missing binding

### Requirement: Probe phase MUST describe traffic direction and evidence boundary

Each proposed check MUST be classified in reviewed build provenance as `verifier_to_msp`,
`msp_to_verifier`, or `other`. Current bundles MUST NOT add an unsupported `phase` key. Direction
MUST NOT be used as a certification level. Executable checks MUST state what they cannot prove using
the existing `not_asserted` field; assertion mapping remains reviewed provenance until a compatible
typed field is approved.

#### Scenario: Captured JSON does not prove device rendering

- **GIVEN** a Phase 2 check captures a syntactically correct rich payload
- **WHEN** the result is recorded
- **THEN** the payload assertion may pass
- **AND** device rendering remains a Phase 3 requirement

### Requirement: Phase 2 MUST fail closed to could-not-run

MSP-to-Verifier capture MUST be disabled unless the target is a disposable test environment with an
approved endpoint override and capture contract. Any target, tenant, TLS, correlation or safety
mismatch MUST produce `could_not_run`, never tenant failure or success.

#### Scenario: MSP cannot override the Apple gateway safely

- **GIVEN** an MSP whose test deployment cannot safely target the Verifier capture service
- **WHEN** a Phase 2 check is planned
- **THEN** no request is sent
- **AND** the result routes to Phase 3
- **AND** the item is not marked failed

### Requirement: Broken attachment probes MUST identify the failing stage

Attachment checks MUST distinguish authorization, download, decryption, preUpload, byte upload,
checksum, message-send suppression and agent-error evidence. A failure at one stage MUST NOT be
reported as proof about an unobserved later stage.

#### Scenario: Upload rejection blocks message emission

- **GIVEN** the capture service returns a configured upload rejection
- **WHEN** the MSP processes an outbound attachment
- **THEN** the result records the upload failure assertion
- **AND** separately asserts that no `/message` request was captured during the bounded window
- **AND** makes no UX claim unless separate Phase 3 evidence is attached

### Requirement: Code and Postman results MUST remain independent

A Postman observation MUST NOT overwrite, relabel or complete a Code observation, and Code analysis
MUST NOT synthesize a probe execution. Checklist method expressions remain deterministic inputs to
human review.

#### Scenario: Postman evidence is added after inconclusive Code analysis

- **GIVEN** an item whose Code observation is `cannot_tell`
- **AND** a bound Postman probe later produces a passed observation
- **WHEN** the item evidence is displayed
- **THEN** the Code observation remains `cannot_tell`
- **AND** the Postman observation is retained separately with its phase and provenance
- **AND** neither observation automatically records a human checklist verdict

### Requirement: New probes MUST round-trip through the active Verifier contract

Before a check is included in a successor bundle, it MUST validate through the active
`BundleCheck`, `CheckRequest` and `ExpectedCriteria` schemas and MUST be exercised by a golden runner
test proving the intended wire request. Unsupported metadata or request encodings MUST remain in the
proposal register until the enabling contract is separately implemented.

#### Scenario: A proposal includes corrupt gzip

- **GIVEN** current Stage can generate valid gzip from a JSON dictionary but cannot author corrupt
  gzip bytes
- **WHEN** the corrupt-gzip scenario is compiled for the current bundle
- **THEN** it is excluded from executable bundle content
- **AND** remains a Tier B planned case
- **AND** no valid-gzip request is mislabeled as corrupt-gzip coverage

#### Scenario: Reference item codes are present without an item binding

- **GIVEN** a check lists `B.13` in `checklist_item_codes`
- **AND** item B.13 does not name the check in `check_bindings`
- **WHEN** the execution plan is resolved
- **THEN** the check is not considered associated for execution
- **AND** validation reports the missing explicit binding

### Requirement: Phase 1 inbound validation MUST preserve the exact tested condition

The B.9/B.13 family MUST use atomic requests for missing Authorization, valid control, valid-HS256
wrong secret, wrong audience, isolated `iat` freshness, each required-header omission, schema
failure, Destination-Id/body mismatch, identical replay and conflicting replay. A malformed JWT MUST
NOT be labelled wrong-secret evidence, a token with both stale `iat` and expired `exp` MUST NOT be
labelled isolated freshness evidence, and Destination-Id consistency MUST NOT replace canonical ID
uniqueness/replay protection.

#### Scenario: Legacy bad token is selected for wrong-secret coverage

- **GIVEN** the current `auth_bad` built-in expands to `BADSIG.BADSIG.BADSIG`
- **WHEN** a check is compiled as “valid HS256 signed with wrong secret”
- **THEN** bundle validation rejects or excludes that check
- **AND** the scenario remains Tier B until the typed runner-owned wrong-key profile exists

#### Scenario: Identical and conflicting replay are tested

- **GIVEN** a valid first request with one message ID
- **WHEN** the byte-identical request is repeated and then the same ID is sent with different content
- **THEN** the identical replay is evaluated for acknowledgement without duplicate processing
- **AND** the conflicting replay is evaluated for rejection without overwriting the original
- **AND** Destination-Id/body matching remains a separate assertion

### Requirement: Source-IP evidence MUST remain outside ordinary Phase 1 traffic

Verifier MUST NOT claim B.14 from a caller-supplied `X-Forwarded-For` header. If an MSP edge correctly
blocks the non-Apple Phase 1 runner and no approved test ingress exists, the run MUST report
`could_not_run`; it MUST NOT fail the MSP or fabricate downstream B.9/B.13 results. B.14 MUST route
to deployed-edge/security evidence or an explicitly approved architecture capable of trustworthy
source provenance.

#### Scenario: Production edge rejects the Verifier runner

- **GIVEN** the runner originates outside `17.0.0.0/8`
- **AND** the MSP production edge correctly enforces B.14
- **WHEN** Phase 1 preflight receives the edge rejection
- **THEN** downstream validation checks are not scored
- **AND** the run records `could_not_run` with the ingress prerequisite
- **AND** B.14 remains pending its deployed-edge evidence

