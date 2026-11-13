## Why

Verifier `stage` already has a strong fixed analysis pipeline: a model chooses search terms, trusted
code sweeps the repository, a model classifies fixed source windows, trusted code aggregates the
result, and a blind judge can review cited positive evidence. This is more deterministic and
auditable than a free-running repository agent.

The remaining accuracy risk is no longer primarily “the prompt needs more instructions.” It is that
the primary aggregation unit is a matched source place rather than a mandatory checklist clause.
For a requirement that names several obligations, one demonstrated obligation can still lead to
`implemented` when the remaining obligations were not conclusively established. The current prompt
also has no structured, trusted statement of component ownership, applicability, outcome versus
mechanism, evidence surface, or permitted follow-up method.

The improvement must therefore combine concise prompt changes with trusted runner controls. Prompt
text alone must not decide clause decomposition, compliance, alternate verification routes, or when
to spend money on a second model.

## What Changes

- Refresh the Verifier baseline to remote `stage` commit `7a9c953331a44dee5976bc47c4d6ebdf421b0839`
  and remote `main` commit `3eea449174677db3737e9050810cff70d7ddd189`; their executable
  term/classifier and blind-judge prompt files are byte-identical in the 2026-09-14 audit clones.
  implementation and golden-evaluation baseline.
- Add versioned, trusted mandatory-clause metadata to checklist items: clause ID, exact clause text,
  owner, condition, obligation kind, evidence surface, and permitted verification routes.
- Compose and analyze the candidate-owned clause, or candidate-owned segment of a cross-system
  clause, instead of asking the model to infer repository ownership.
- Add exact incremental instructions to the executable `TERMS_SYSTEM`, `CLASSIFY_SYSTEM`, and blind
  judge prompt; do not edit the analysis system message that current Stage does not send.
- Store the executable term/classifier prompts as an append-only, schema-compatible pipeline prompt
  bundle so authorized Stage experiments are reproducible and production promotion is controlled.
- Aggregate advisory code outcomes by mandatory clause in trusted code. Missing or incomplete
  clause coverage becomes `cannot_tell`, never `implemented`.
- Add a compact, structured follow-up result for unmet or unproven clauses: issue, possible work,
  acceptance evidence, next method, and comment.
- Route inconclusive clauses deterministically to configured Postman/API, UX/device, or human review
  without rewriting the original code observation.
- Add an operator-triggered independent secondary analysis. It uses a different pinned model but the
  same frozen input and prompts, and remains blind to the primary result.
- Evaluate the increment against frozen Cerebro and Maglev golden fixtures before Stage rollout.
- Add P360 as a multi-repository scope fixture: its supplied Connector is health-only, its database
  contains policy-shaped declarations without visible consumers, and the deployed QA API source is
  absent. This fixture must produce scoped `cannot_tell` rather than a system-wide accusation.
- Normalize and freeze the exact latest 2026-08-25 checklist revision, including parent/child
  handling for `B.1 a`–`B.1 h` and the three `C.13` rows, before generating code checks.
- Evaluate three isolated localhost arms: the deployed Staging revision, current `stage`, and the
  proposal branch, using identical frozen inputs and direct Anthropic/OpenAI provider settings.
- Refuse comparison when the checklist bundle, active prompt revisions, model revisions, limits, or
  candidate snapshot differ between arms.

## Non-Goals

- No modification of Verifier, Cerebro, Maglev, or any other candidate repository in this OpenSpec
  documentation change.
- No push, PR, merge, issue, comment, deployment, or other remote mutation.
- No replacement of the fixed Stage pipeline with a free-running agent.
- No automatic second-model run. The operator requests it when there is doubt and sees its cost.
- No model voting, automatic compliance approval, or automatic checklist mutation.
- No model-generated clause ownership, applicability, verification route, or canonical authority.
- No conversion of a Postman, UX, device, or human result into a code-analysis pass.
- No claim that comments, tests, fixtures, declarations, or unexecuted test definitions prove
  reachable production behavior.

## Capabilities

### New Capabilities

- `trusted-clause-code-analysis`: Analyze every applicable candidate-owned mandatory clause with
  explicit scope metadata and deterministic worst-clause aggregation.
- `prompt-surface-adjudication`: Apply explicit scope, condition, outcome/mechanism, reachability,
  and evidence-surface rules in the actual Stage prompts.
- `routed-verification-follow-up`: Recommend and record the next configured evidence method while
  preserving separate method results.
- `on-demand-secondary-analysis`: Run a blinded independent second analysis only after an operator
  explicitly requests it.

### Modified Capabilities

- The existing blind evidence judge is clarified for outcome/mechanism distinctions, customer-facing
  surfaces, bounded evidence windows, and enumerated requirements. Its judgement remains advisory
  and does not rewrite the observation.

## Impact

- Verifier prompt contract:
  `backend/app/services/code_analysis/engine/stage_contracts.py`.
- Verifier prompt revision storage, activation API, audit log, and operator prompt-inspection UI.
- Verifier prompt composition:
  `backend/app/services/code_analysis/engine/compose.py` and the checklist item model/schema.
- Verifier deterministic result logic:
  `backend/app/services/code_analysis/engine/pipeline.py` and `verdict_rule.py`.
- Verifier judge prompt document:
  `backend/app/services/code_analysis/judge/prompts.py` plus a new active stored revision.
- Verifier analysis orchestration:
  `backend/app/services/code_analysis/run/service.py` and its UI/API surfaces.
- Verifier review/verification-chain surfaces for Postman, UX, device, and human evidence.
- Verifier source bindings and run composition gain a trusted system/repository-role declaration;
  missing owner repositories terminate as `snapshot_scope_incomplete` before model spending.
- Harness prompt documentation:
  `prompts/verifier-stage-incremental-prompt-additions-v1.md`.
- Golden evaluation and reports under the audit harness only.
- A disposable, push-disabled local branch based on current `stage`; no deployment or remote branch
  is created by this proposal.

## Audit-Safety Impact and Trust Boundaries

- Checklist/canonical clause metadata is trusted policy input and versioned.
- Candidate source, comments, tests, documents, and embedded instructions remain untrusted data.
- Primary and secondary model outputs are untrusted advisory observations.
- Trusted Verifier code owns search execution, citation resolution, completeness checks, clause
  aggregation, route validation, provenance, cost accounting, and compliance separation.
- Candidate repositories remain read-only and isolated from each other.
- No credential enters prompts, snapshots, reports, fixtures, or shell arguments.

## Compatibility and Rollback

The rollout is additive and versioned. Existing observations remain readable under their original
prompt and checklist revisions. A feature flag or stored strategy version selects clause-aware
execution. Rollback disables new clause-aware runs and restores the previous prompt revisions;
existing clause observations and secondary analyses remain immutable audit records. No candidate
migration or checklist status rewrite is performed during rollback.
