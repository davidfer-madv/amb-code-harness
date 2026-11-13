## Purpose

Define a reproducible, isolated, evidence-backed adversarial evaluation of the Verifier stage AI
strategy across multiple model systems.

## ADDED Requirements

### Requirement: Use frozen equal inputs
The evaluation SHALL give each reviewer the same Verifier commit, strategy proposal, schema, and
review questions and MUST NOT provide another reviewer's conclusion before that reviewer finishes.

#### Scenario: Independent model review
- **GIVEN** stage commit `9ac99cd97883ed8d571dc26daed44fd82cf9f803` and strategy v1.1
- **WHEN** Opus, Fable, Copilot, or Codex reviews the strategy
- **THEN** the reviewer evaluates those frozen inputs without seeing another model's verdict

### Requirement: Preserve source and remote state
The evaluation MUST expose no write, shell, push, or remote-mutation capability to external model
reviewers and SHALL keep the detached Verifier candidate clean and push-disabled.

#### Scenario: Review completes
- **GIVEN** a reviewer has finished
- **WHEN** candidate state is verified
- **THEN** candidate HEAD is unchanged, Git status is empty, and the push URL remains `DISABLED`

### Requirement: Reconcile by evidence
The evaluator SHALL classify every material recommendation as accepted, rejected, unresolved, or
out of scope and MUST require resolving source citations or repeatable tests before acceptance.

#### Scenario: Unsupported consensus
- **GIVEN** several reviewers agree on a claim but cite no resolving source or test
- **WHEN** reconciliation occurs
- **THEN** the claim is not accepted merely because a majority agreed

#### Scenario: Evidence-backed dissent
- **GIVEN** one reviewer disagrees and its cited source contradicts the other reviewers
- **WHEN** the citation resolves against the frozen commit
- **THEN** reconciliation follows the source evidence and records the disagreement

### Requirement: Report model unavailability honestly
The evaluator MUST record a requested model as unavailable when the authenticated CLI cannot run it
and MUST NOT substitute another model while retaining the requested model's label.

#### Scenario: Requested alias is unavailable
- **GIVEN** a requested model alias is rejected by its CLI
- **WHEN** the evaluation proceeds
- **THEN** the report contains the refusal and makes no agreement claim for that model
