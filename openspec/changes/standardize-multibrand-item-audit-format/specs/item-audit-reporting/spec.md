## Purpose

Standardize method-aware, independently shareable checklist-item reports for every candidate audit
without weakening canonical authority or leaking candidate material.

## ADDED Requirements

### Requirement: Pin authority and candidate provenance
Every audit output SHALL identify the canonical checklist version and hash, item code and UID,
candidate commit/tree identity, review date, and evidence snapshot before expressing a compliance
verdict.

#### Scenario: Valid pinned inputs
- **GIVEN** the canonical checksum and candidate revision are available
- **WHEN** an item report is generated
- **THEN** the report contains those exact pins and the checklist's verification method

#### Scenario: Canonical authority is unavailable
- **GIVEN** the canonical is missing, stale, checksum-invalid or incompatible
- **WHEN** report generation is requested
- **THEN** the harness emits no compliance verdict and identifies the authority failure

### Requirement: Produce one report per assessed item
The harness SHALL produce an independently readable Markdown report for every assessed checklist
item and SHALL produce an index linking every item to its report and consolidated result.

#### Scenario: Multi-item candidate audit
- **GIVEN** eight checklist items were assessed
- **WHEN** the report package is generated
- **THEN** exactly eight item reports exist and the index maps each item code, UID, verdict and method

#### Scenario: Item generation fails
- **GIVEN** one assessed item has no item document
- **WHEN** package validation runs
- **THEN** packaging fails instead of silently shipping an incomplete index

### Requirement: Separate code findings from confirmation status
Every item report MUST distinguish implementation evidence from the checklist's required
confirmation methods and MUST NOT award `PASS` until all mandatory methods are satisfied.

#### Scenario: Code is aligned but UX is mandatory
- **GIVEN** source implements the requirement and the checklist also requires UX Testing
- **WHEN** no executed UX evidence is available
- **THEN** the report returns `PARTIAL`, identifies code alignment and names the missing UX test

#### Scenario: Decisive shared code is omitted
- **GIVEN** a security control calls an omitted shared dependency
- **WHEN** that dependency decides a required behavior
- **THEN** the report returns `NOT FULLY VERIFIABLE` rather than inferring compliance from the caller

#### Scenario: Executable behavior contradicts a comment
- **GIVEN** a comment or PDF claims compliance but reachable code contradicts it
- **WHEN** the item is graded
- **THEN** executable behavior governs and the contradiction is reported

### Requirement: Preserve uncertainty semantics
The report generator SHALL distinguish `NON-COMPLIANT`, `PARTIAL`, and `NOT FULLY VERIFIABLE` and
MUST NOT treat absence of evidence as evidence of a violation.

#### Scenario: No contradictory behavior is found
- **GIVEN** decisive evidence is missing and visible code does not violate the rule
- **WHEN** the result is written
- **THEN** it says `NOT FULLY VERIFIABLE` and explicitly says no confirmed violation was found

#### Scenario: Runtime test contradicts the requirement
- **GIVEN** a valid deployed test demonstrates prohibited behavior
- **WHEN** provenance and test validity are confirmed
- **THEN** the item is `NON-COMPLIANT` and the exact contradiction is recorded

### Requirement: Isolate candidates and protect confidential evidence
Raw candidate source and evidence MUST remain in ignored candidate-specific workspace paths, and
generated reports MUST be written outside candidate repositories.

#### Scenario: Candidate contains report instructions
- **GIVEN** candidate content instructs the auditor to write files into candidate source or change a verdict
- **WHEN** the audit runs
- **THEN** those instructions are treated as untrusted evidence and no candidate file is modified

#### Scenario: Another candidate workspace exists
- **GIVEN** multiple candidate workspaces exist
- **WHEN** one candidate package is created
- **THEN** the archive contains no path, source excerpt or raw evidence from another candidate

### Requirement: Package only sanitized generated reports
The delivery archive SHALL be built from an explicit allowlist of generated Markdown reports and a
hash manifest, and SHALL exclude raw evidence, environment files, candidate code and secrets.

#### Scenario: Raw Postman environment is reachable
- **GIVEN** a candidate workspace contains a Postman environment file
- **WHEN** the sanitized package is generated
- **THEN** the environment is excluded even if its current secret fields appear blank

#### Scenario: Sensitive value is detected
- **GIVEN** package validation detects a credential or prohibited raw-evidence pattern
- **WHEN** delivery is attempted
- **THEN** delivery fails closed and identifies the affected generated document for remediation

