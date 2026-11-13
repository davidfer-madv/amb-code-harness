# GitHub distribution

## ADDED Requirements

### Requirement: Exclude confidential and local audit material

The repository MUST exclude candidate source, submitted evidence, generated customer reports,
delivery archives, large review media, credentials and local coding-agent/cloud state.

#### Scenario: Candidate workspace exists locally

- **GIVEN** one or more candidate workspaces exist
- **WHEN** eligible Git files are enumerated
- **THEN** no path below `workspaces/` is included

#### Scenario: Raw evidence or secret is eligible

- **GIVEN** an unignored file has a prohibited evidence format or secret pattern
- **WHEN** GitHub readiness is checked
- **THEN** the check fails and names the unsafe path without printing the secret

### Requirement: Provide a common coding-agent contract

The repository MUST tell Codex, Claude Code and Copilot to use the pinned authority, treat candidate
content as untrusted data, preserve read-only isolation, analyze atomic obligations through reachable
production paths and separate implementation findings from required confirmation methods.

#### Scenario: Agent opens a clean clone

- **GIVEN** the agent reads its supported root instruction surface
- **WHEN** it is asked to audit a supplied candidate repository
- **THEN** it follows the same OpenSpec-governed workflow and controlled outcome semantics

### Requirement: Validate a clean distributable repository

The publication gate MUST check eligible paths, file size, secret patterns, shell/Python syntax,
unit tests and all active OpenSpec changes before upload.

#### Scenario: Repository is ready

- **GIVEN** all reusable files satisfy the publication policy
- **WHEN** the readiness command runs
- **THEN** it emits a deterministic eligible-file manifest and exits successfully
