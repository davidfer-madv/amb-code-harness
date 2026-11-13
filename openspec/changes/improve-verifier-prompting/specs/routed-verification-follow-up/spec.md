## Purpose

Provide bounded recommendations and route inconclusive clauses to applicable evidence methods
without changing the meaning of the original code observation.

## ADDED Requirements

### Requirement: Follow-up recommendations MUST be bounded and grounded
Verifier SHALL request a structured follow-up only for `partial`, `not_found`, or `cannot_tell`
clauses and MUST validate issue, possible work, acceptance evidence, next method, and comment against
trusted clause metadata and verified evidence.

#### Scenario: Outcome clause needs work
- **GIVEN** an unmet outcome clause that does not mandate an implementation mechanism
- **WHEN** follow-up is generated
- **THEN** possible work is presented as a reasonable direction rather than the only compliant mechanism
- **AND** acceptance describes the observable required outcome

#### Scenario: Model invents an unsupported route
- **GIVEN** a clause permits only human confirmation
- **AND** the follow-up model returns `postman`
- **WHEN** the response is validated
- **THEN** the route is rejected
- **AND** the original code observation remains unchanged

### Requirement: Alternate evidence MUST remain method-specific
Postman/API, UX/device, and human evidence MUST be recorded with separate method identity,
provenance, artifacts, and status and MUST NOT overwrite or relabel a code observation.

#### Scenario: Postman confirms runtime behavior after inconclusive code review
- **GIVEN** code analysis is `cannot_tell`
- **AND** an approved Postman test demonstrates the configured API behavior
- **WHEN** evidence is recorded
- **THEN** the code result remains `cannot_tell`
- **AND** the Postman result is separately recorded as supporting evidence

#### Scenario: UX evidence cannot prove tenant isolation
- **GIVEN** a visual recording shows successful user behavior
- **AND** the clause requires internal cross-tenant isolation
- **WHEN** evidence routing is evaluated
- **THEN** UX evidence does not satisfy the isolation clause
- **AND** the required code/database or human route remains pending

### Requirement: Unsupported alternate methods MUST leave the clause unresolved
Verifier MUST NOT route a clause to a method that cannot establish its obligation and SHALL require
human confirmation when configured automated or observational methods cannot settle it.

#### Scenario: No configured route can settle the clause
- **GIVEN** code analysis is inconclusive
- **AND** no configured Postman, UX, or device method can establish the obligation
- **WHEN** follow-up routing runs
- **THEN** the clause remains unresolved
- **AND** human confirmation is requested with the reason

