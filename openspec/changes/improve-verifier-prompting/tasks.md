## 1. Baseline and OpenSpec validation

- [x] 1.1 Confirm the implementation baseline is current Verifier `stage` and record commit/tree SHA
- [x] 1.2 Confirm the disposable Verifier clone is clean, isolated, and push-disabled
- [x] 1.3 Validate this OpenSpec change before implementation
- [ ] 1.4 Freeze Cerebro and Maglev golden fixture commits, checklist revision, canonical closure, and existing accepted labels
- [x] 1.5 Refresh the Verifier Stage/deployment baseline and prompt-gap analysis for the exact latest 2026-08-25 CSV
- [x] 1.6 Refresh remote Stage/main prompt defaults on 2026-09-14 and confirm their executable prompt files are byte-identical
- [x] 1.7 Audit P360 implementation repositories independently of the QA test tracker and record the 77→114 scope delta

## 2. Trusted clause model

- [ ] 2.1 Define closed vocabularies for owner, obligation kind, evidence surface, and verification route
- [ ] 2.2 Add versioned mandatory-clause storage, schema validation, import/export, and tenant-override behavior
- [ ] 2.3 Refuse duplicate clause IDs, missing clause text, invalid routes, and ownership values outside the vocabulary
- [ ] 2.4 Add explicit candidate, external, cross-system, unknown, conditional, outcome, mechanism, and evidence fixtures
- [ ] 2.5 Prove a model cannot modify trusted clause metadata through repository or checklist text
- [ ] 2.6 Add trusted system scope, repository role, expected component, and known-missing-component metadata
- [ ] 2.7 Emit `cannot_tell / snapshot_scope_incomplete` without a model call when the owning component is not in the supplied snapshot

## 3. Executable prompt changes

- [ ] 3.1 Add append-only pipeline prompt-bundle storage, migration, active pointer, and audit record
- [ ] 3.2 Bind each bundle to compatible `report_terms` and `report_site` schema versions and reject invalid activation
- [ ] 3.3 Add authorized Staging activation, evaluated production promotion, history, and rollback
- [ ] 3.4 Append the approved coverage block to the bundled `TERMS_SYSTEM`
- [ ] 3.5 Append the approved adjudication gates to the bundled `CLASSIFY_SYSTEM`
- [ ] 3.6 Add prompt-surface tests proving the UI/API shows the exact prompts and tools actually sent
- [ ] 3.7 Create and activate a new stored blind-judge prompt revision with the approved scope addition
- [ ] 3.8 Prove the unused analysis system message is not presented as an effective execution prompt
- [ ] 3.9 Preserve bundle revision/hash, judge revision/hash, model revision, and clause revision on every observation

## 4. Clause execution and deterministic aggregation

- [ ] 4.1 Compose one candidate-owned mandatory clause per primary check
- [ ] 4.2 Skip external-owned clauses from candidate-code absence analysis and route them as unproven
- [ ] 4.3 Split cross-system clauses into separately attributable segments
- [ ] 4.4 Implement worst-mandatory-clause aggregation in trusted code
- [ ] 4.5 Make missing, unanswered, truncated, budget-stopped, or unclassified mandatory clauses `cannot_tell`
- [ ] 4.6 Bind the displayed aggregation rule to production behavior with exhaustive branch tests
- [ ] 4.7 Test enumerated requirements where one, some, and all mandatory clauses are demonstrated
- [ ] 4.8 Preserve the derived evidence branch (`contradicts_only`, `mentions_only`, `nothing_shown`) so a contradiction is not displayed as ordinary absence

## 5. Reachability and evidence surfaces

- [ ] 5.1 Add bounded recorded expansion for direct call, registration, enforcement, render, and send paths
- [ ] 5.2 Enforce file, byte, depth, call, and wall-time limits on expansion
- [ ] 5.3 Test customer-facing naming separately from technical identifiers, tests, comments, documentation, and distinct product names
- [ ] 5.4 Test outcome obligations with two different compliant mechanisms
- [ ] 5.5 Test mechanism obligations where an alternative outcome-equivalent implementation is insufficient

## 6. Follow-up recommendations and verification routing

- [ ] 6.1 Add the strict `report_follow_up` schema and bounded prompt
- [ ] 6.2 Run follow-up generation only for `partial`, `not_found`, and `cannot_tell` clauses
- [ ] 6.3 Validate `next_method` against trusted configured routes
- [ ] 6.4 Add separate Postman/API, UX/device, and human result records without rewriting code observations
- [ ] 6.5 Display issue, possible work, acceptance evidence, next method, provenance, and cost
- [ ] 6.6 Refuse unsupported routes and leave the clause unresolved

## 7. On-demand secondary model

- [ ] 7.1 Add an explicit “independent second analysis” operator action and cost preview
- [ ] 7.2 Require a different pinned model revision and explicit operator confirmation
- [ ] 7.3 Reuse the same frozen source, clause packet, prompts, tools, and limits
- [ ] 7.4 Prove the secondary request excludes the primary verdict, rationale, citations, terms, and model identity
- [ ] 7.5 Preserve both immutable observations and compare clause verdicts/citations deterministically
- [ ] 7.6 Route disagreement to configured evidence or human review without voting or automatic compliance change
- [ ] 7.7 Record secondary-model unavailability without substituting a differently labelled model

## 8. Golden evaluation

- [ ] 8.1 Run current Stage and Stage-plus-increment on identical frozen Cerebro and Maglev fixtures
- [ ] 8.2 Measure mandatory-clause recall, exact advisory verdict, false-green count, citation validity, variance, latency, tokens, and cost
- [ ] 8.3 Include corrected Cerebro D.2 and naming/ownership cases as regression fixtures
- [ ] 8.4 Include critical tenant isolation, consent, session expiry, timeout, attachment error, and fallback negative controls
- [ ] 8.5 Run requested secondary-model confirmation only for operator-selected disputed fixtures
- [ ] 8.6 Reconcile all differences by source/test evidence and preserve unresolved dissent
- [ ] 8.7 Refuse promotion if any critical false green, invalid citation acceptance, or incomplete-to-conclusive conversion occurs
- [ ] 8.8 Add P360 fixtures for health-only ownership, unused OS/TTL configuration, disabled SSRF flags, opaque-ID/phone association, and missing deployed source

## 9. Documentation, validation, and rollout

- [ ] 9.1 Update operator documentation for clause results, follow-up routes, and on-demand secondary analysis
- [ ] 9.2 Update cost documentation with measured rather than estimated token and dollar figures
- [ ] 9.3 Run focused unit, schema, migration, prompt-surface, aggregation, isolation, and UI tests
- [ ] 9.4 Run shell syntax checks for changed harness scripts, if any
- [ ] 9.5 Validate the OpenSpec change after implementation
- [ ] 9.6 Refresh policy hashes after trusted prompt, policy, checklist, or playbook changes
- [ ] 9.7 Present the evaluation report for human approval before any Verifier merge or deployment
- [ ] 9.8 Roll out through reviewed `stage`, then reviewed `main`; verify deployed prompt and strategy revisions
- [ ] 9.9 Retain the prior strategy as a reversible fallback and preserve all immutable observations

## 10. Controlled localhost comparison

- [x] 10.1 Create a separate push-disabled local branch from current `stage`
- [x] 10.2 Record the deployed Staging, current Stage, proposal-branch, and checklist file hashes
- [ ] 10.3 Authentically export the live Staging checklist bundle and active prompt/model/limit revisions
- [ ] 10.4 Prove whether the live Staging checklist matches the named August checklist semantically
- [ ] 10.5 Build one normalized bundle from the August CSV and validate it without importing it remotely
- [ ] 10.6 Create isolated databases and source stores for deployed-Stage, current-Stage, and proposal arms
- [ ] 10.7 Register identical pinned Anthropic and OpenAI model revisions and prices in every local arm
- [ ] 10.8 Run offline contract tests before permitting any paid provider request
- [ ] 10.9 Run a small paired smoke set, then the frozen Cerebro and Maglev golden set, in randomized order
- [ ] 10.10 Compare clause outcomes, citations, completeness, variance, latency, tokens, cache usage, cost, and review load
- [ ] 10.11 Publish raw immutable run exports plus a deterministic comparison report without changing checklist status
- [ ] 10.12 Stop promotion when input-parity checks fail or any critical false green appears
- [ ] 10.13 Normalize `B.1 a`–`B.1 h`, merge `C.13 a`–`C.13 c` under one parent, exclude stray row `81`, and resolve non-code `A.3` before planning runs
- [x] 10.14 Document copy-ready disposable localhost setup, dependency installation, secret handling, startup, content/model seeding and shutdown
- [ ] 10.15 Generate and human-review the normalized `verifier-checklist-bundle/v1` used by all local arms
- [ ] 10.16 Record exact smoke/golden model identifiers, prices and explicit per-run/experiment cost ceilings before any provider call
