## Context

At the frozen baseline, Verifier Stage executes four primary steps:

1. `TERMS_SYSTEM` asks a model for literal, symbol, and concept search terms.
2. trusted code searches the frozen repository snapshot;
3. `CLASSIFY_SYSTEM` asks a model to classify each fixed source place;
4. trusted code aggregates the classifications.

A separate blind judge can assess qualifying cited evidence. The large
`engine/prompts.py::DEFAULT_SYSTEM_MESSAGE` is not sent by this strategy, so editing it would create
the appearance of a prompt improvement without changing model behavior.

## Goals

- Prevent a composite requirement from becoming `implemented` when only some mandatory clauses are
  demonstrated.
- Reduce false violations caused by wrong repository ownership or by requiring an optional
  implementation mechanism.
- Improve naming analysis by requiring proof of a customer render/send surface.
- Produce useful, bounded recommendations and acceptance evidence.
- Continue inconclusive analysis through applicable Postman, UX/device, or human evidence.
- Allow an independent secondary model when an operator has doubts without automatic spend or
  anchoring on the first result.
- Preserve Stage's deterministic search, immutable observations, verified citations, and advisory
  semantics.

## Non-Goals

- Reintroducing the withdrawn exploratory strategy as the default.
- Asking a model to decompose authoritative checklist text at runtime.
- Treating a blind citation judge as an independent repository search.
- Treating model confidence as an automatic routing trigger.
- Combining evidence methods into one opaque verdict.

## Proposed Architecture

```text
versioned checklist + canonical closure
                |
                v
trusted mandatory-clause packet
                |
      candidate-owned clause only
                |
                v
TERMS_SYSTEM -> deterministic sweep -> CLASSIFY_SYSTEM
                |                         |
                +---------- trail --------+
                              |
                              v
                  trusted clause aggregation
                              |
            +-----------------+------------------+
            |                                    |
     verified positive                    unmet / unproven
            |                                    |
       blind judge                    compact follow-up result
                                                 |
                            configured Postman / UX / device / human

Operator has doubt
        |
        v
same frozen clause and source + different pinned model
        |
        v
independent primary pipeline, blind to first observation
        |
        v
deterministic comparison; disagreement remains visible
```

## Decision 1: Clause metadata is trusted policy data

Each mandatory clause carries:

```json
{
  "clause_id": "I.6.3",
  "text": "Exact mandatory clause text",
  "owner": "candidate_repo",
  "obligation_kind": "mechanism",
  "condition": null,
  "evidence_surface": "production_code",
  "verification_routes": ["code", "database_test"]
}
```

Closed vocabularies:

- `owner`: `candidate_repo`, `external_component`, `cross_system`, `unknown`;
- `obligation_kind`: `outcome`, `mechanism`, `evidence`;
- `evidence_surface`: `production_code`, `customer_rendered`, `protocol`, `configuration`,
  `runtime`, `external`;
- routes: only methods registered by Verifier policy.

The packet is authored and reviewed with the checklist. The model may report suspected metadata
conflict, but cannot change it. Unknown ownership or unevaluated conditionality is `cannot_tell` and
routes to human resolution.

## Decision 2: Change the prompts that actually execute

### Term selection

Append the approved “Coverage and scope” block to `TERMS_SYSTEM` in
`engine/stage_contracts.py`. It requires coverage of every named part, alternative mechanisms for
outcome obligations, producer and use paths, and customer render/send surfaces.

### Site classification

Append the approved “Mandatory adjudication gates” block to `CLASSIFY_SYSTEM` in the same module.
The ordered gates are:

1. scope and condition;
2. outcome versus expressly required mechanism;
3. production reachability;
4. evidence surface;
5. bounded-place completeness.

Retain the initial four site findings: `demonstrates`, `contradicts`, `mentions_only`, and
`unrelated`. Provider, budget, search, extraction, and unanswered-site failures remain trusted
run-level `cannot_tell` states rather than a model-selected fifth finding.

### Blind judge

Append the approved scope block to a new stored judge-prompt revision. Updating only the Python
default is insufficient for an existing deployment because the active revision is stored in the
database. The judge remains blind and cannot move the original verdict.

### Prompt text source

The exact initial text is maintained in
`prompts/verifier-stage-latest-checklist-additions-v2.md`. Implementation SHALL copy it into the
Verifier change and then make the Verifier tests and stored prompt revision the operational source
of truth. The unused analysis system message MUST NOT be presented as the effective Stage prompt.

### Executable prompt bundle

The two executable pipeline prompts SHALL be stored as one append-only, revisioned bundle together
with the compatible `report_terms` and `report_site` schema versions. The bundle content hash covers
both prompt texts and both schema-version identifiers. Every run stamps that revision and hash.

Staging may activate a compatible experimental bundle through an authorized, audited action.
Production may activate only a bundle promoted from an evaluated Staging revision, or through the
equivalent production reviewer approval. Activation validates all referenced findings, fields and
tool versions before changing the active pointer. Rollback reactivates an earlier immutable bundle.

The legacy stored analysis system message retains its exploratory-strategy meaning. It SHALL NOT be
repurposed as the pipeline bundle because doing so would make historical revisions ambiguous.

## Decision 3: Run and aggregate per mandatory clause

The safest initial implementation composes one mandatory clause per check and reuses the current
term/site tool schemas. This avoids asking one model answer to carry several clause verdicts.

The runner computes:

```text
all applicable candidate-owned mandatory clauses demonstrated -> implemented
some demonstrated and any unmet or unproven                  -> partial
complete owned-scope search and none demonstrated            -> not_found
required step incomplete or ownership/applicability open      -> cannot_tell
```

A cross-system item with a demonstrated candidate segment and an unproven external segment is
`partial`, not a candidate-code violation and not fully implemented.

To control cost, the first evaluation SHALL measure one terms call per clause against an optional
item-level, clause-keyed term call. The lower-cost form may replace the first only if it preserves
mandatory-clause recall and structured-output validity on the golden set.

## Decision 4: Recommendations are a separate bounded contract

Only `partial`, `not_found`, and `cannot_tell` clauses receive a follow-up call. The reporting tool
requires:

- `issue`;
- `possible_work`;
- `acceptance`;
- `next_method`;
- `comment`.

The server validates the method against the trusted clause packet. An outcome requirement cannot be
given one invented mandatory mechanism. Empty or invalid recommendations do not change the clause
result.

## Decision 5: Alternate evidence complements code evidence

Trusted route configuration chooses the next action:

1. safe configured API probe or manual Postman for an API-observable clause;
2. automated or human UX/device review for rendered, temporal, accessibility, or agent-experience
   behavior;
3. human confirmation when neither route can settle the clause or evidence conflicts.

Each result retains its own method, provenance, artifacts, and status. The overall checklist state
is computed from configured AND/OR verification rules; no alternate result edits the code
observation.

## Decision 6: Secondary model is operator-triggered and independent

The secondary run uses:

- a different pinned model revision selected by the operator;
- the identical frozen source and checklist/clause revisions;
- identical prompts, tools, limits, and deterministic aggregation;
- no primary verdict, rationale, citations, search terms, or model identity.

After both finish, trusted code compares clause verdicts and verified citations. Agreement is
advisory. Disagreement remains visible and routes to configured evidence or human review. There is
no model vote and no automatic stronger-model escalation.

## Files and Surfaces

### Verifier implementation targets

- `backend/app/services/code_analysis/engine/stage_contracts.py`
- `backend/app/services/code_analysis/engine/compose.py`
- `backend/app/services/code_analysis/engine/pipeline.py`
- `backend/app/services/code_analysis/engine/verdict_rule.py`
- `backend/app/services/code_analysis/judge/prompts.py`
- `backend/app/services/code_analysis/run/service.py`
- checklist models, schemas, migrations, import/export and tenant overrides
- review/verification-chain repositories and schemas
- analysis run UI, model picker, cost preview, comparison, and follow-up display

### Harness-only planning/evaluation targets

- `prompts/verifier-stage-incremental-prompt-additions-v1.md`
- frozen Cerebro and Maglev fixture manifests
- golden labels and evaluation reports
- this OpenSpec package

## Trust Boundaries

1. Checklist/canonical metadata → trusted runner input.
2. Candidate snapshot → untrusted, read-only source data.
3. Model response → untrusted structured claim.
4. Citation resolution and clause aggregation → trusted deterministic code.
5. Postman/UX/device artifacts → method-specific evidence, not source-code evidence.
6. Human decision → final confirmation where policy requires it.

Candidate-controlled text can never alter the system prompt, tools, route configuration, spend
limit, clause metadata, or result aggregation.

## Filesystem and Remote Safety

- Candidate source remains below an isolated `workspaces/<name>/src` snapshot and is never written.
- Evaluation output remains in candidate-specific analysis directories.
- Cerebro and Maglev content is never combined into one model context.
- Push URLs remain disabled for audit clones.
- This proposal authorizes no remote GitHub write and no deployment.

## Failure Behavior

- Missing or invalid clause metadata: refuse the clause-aware run or record `cannot_tell`; never fall
  back to model-inferred ownership.
- Missing canonical closure: prohibit compliance conclusions and checklist-update proposals.
- Provider refusal, timeout, malformed tool call, budget exhaustion, incomplete search, truncated
  extraction, or unanswered site: preserve `cannot_tell` with the exact reason.
- Invalid citation: reduce the asserting observation according to existing Stage rules.
- Invalid follow-up method: reject it server-side and retain the original clause result.
- Secondary model unavailable: record unavailability and keep the primary observation unchanged.
- Primary/secondary disagreement: retain both and require configured evidence or human review.
- Candidate instruction attempts: keep them inside the untrusted envelope and record only as source
  evidence if relevant.
- Cross-candidate path or context mixing: refuse the run.

## Cost Controls

- No automatic secondary run.
- Show the secondary model, token ceiling, and estimated maximum cost before confirmation.
- Cache stable trusted prefixes where provider policy permits.
- Keep one candidate source window per classification call.
- Run the recommendation stage only for non-implemented clauses and cap every output field.
- Record input, output, cache-read, cache-write, latency, and dollar cost separately for primary,
  judge, follow-up, and secondary operations.
- Evaluate cost per corrected or resolved clause, not agreement rate alone.

## Golden Evaluation and Acceptance

Use frozen Cerebro and Maglev snapshots and human-reviewed clause labels. Neither a model nor the
current Stage result is golden solely because it is existing behavior.

Minimum pilot gates:

- zero false `implemented` results on critical security, consent, tenant-isolation, and lifecycle
  fixtures;
- at least 95% mandatory-clause recall;
- at least 90% exact advisory-verdict agreement with the golden set;
- no invalid or cross-snapshot citation accepted;
- no incomplete run converted to `not_found` or `implemented`;
- no external/unknown-owned clause converted to a candidate-code violation solely by absence;
- no secondary run without recorded operator confirmation and cost preview;
- no alternate evidence method rewriting the code observation;
- report variance, latency, tokens, cost, and human-review load before promotion.

## Rollout Plan

1. Implement behind a strategy/version flag on a disposable branch based on current `stage`.
2. Add trusted clause metadata for the frozen evaluation subset.
3. Add and unit-test the executable prompt changes.
4. Add clause aggregation and completeness failures.
5. Run Stage and Stage-plus-increment on identical fixtures.
6. Reconcile false positives, false negatives, and cost.
7. Add follow-up routing and on-demand secondary analysis.
8. Repeat the golden evaluation.
9. Present results for human approval before merging or deploying.
10. Promote through `stage` and then `main` only under the repository's normal reviewed workflow.

Rollback selects the prior strategy/prompt revision; it does not delete new immutable observations.
