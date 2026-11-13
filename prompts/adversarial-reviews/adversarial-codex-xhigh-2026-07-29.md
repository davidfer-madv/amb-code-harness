## Adversarial verdict

The strategy is unsafe as written. It can produce polished, well-cited, confidently wrong “implemented” verdicts that survive the proposed refutation pass. The root problems are:

- The distilled checklist row remains the effective adjudication authority.
- Search results are mistaken for production-path coverage.
- Verification Method is mistaken for proof sufficiency.
- Runtime evidence is not bound to the analyzed artifact.
- Repository prose, tests, and simulators remain common-mode or attacker-controlled evidence.

Review provenance: code checkout `5c67de64f51c043177fb22fbc8c70031148509b5`, clean but 259 commits behind locally fetched `origin/main`; canonical checkout `15e1ed0ab0d4774278c68105193d072b19437461`. I also checked relevant `origin/main` versions. No files were modified.

## P0 — must fix before trusting the tool

1. **Row-first adjudication reintroduces exactly the blind spot the tool is meant to prevent.**

A checklist row is a lossy index, not an authority. There is already a decisive counterexample: H.1 is green while claiming Apple publishes `429` and that Invitation `410` means opt-out [proofs/checklist.yaml](/home/davidfer/github/cerebro/proofs/checklist.yaml:2452). The current canonical says:

- No published `429`.
- Organic `410` means the customer closed the conversation.
- Invitation `410` means a missing/incorrect `message-type`; preference-based undeliverability is `404`.

See the [canonical response-code addendum](/home/davidfer/github/AMB-canonical/canonical/addenda/2026-07-27-response-codes-published-no-429.md:15). The fetched `origin/main` still retains the wrong 74-item row, although its notes now admit the contradiction. A tool judging against the row could praise code for implementing a fictional Apple rule.

Fix:

- Never adjudicate code against the row alone.
- Classify outcomes separately as `CODE_VIOLATION`, `CHECKLIST_OMISSION`, `CHECKLIST_CONTRADICTION`, `SPEC_REALITY_DISCREPANCY`, or `UNRESOLVED_AUTHORITY_CONFLICT`.
- Code differing from the checklist does not make the checklist wrong. Only authority evidence can do that.
- If the canonical bundle is unavailable, stale, checksum-invalid, or incompatible with the checklist version, prohibit compliance verdicts and checklist proposals. At most report “checklist-row conformance not assessed against canonical.”

The minimum canonical context per item is a dependency closure, not one retrieved paragraph:

- Exact normative statement, modality, scope, direction, actor, endpoint and conditions.
- Referenced definitions, common tables and flow-specific exceptions.
- Adjacent error, timeout, ordering, security and key-management rules.
- Source rank, version, date, canonical commit/blob hash and supersession status.
- Relevant schemas and fixtures, clearly labeled as normative versus illustrative.
- Conflict register, addenda and disclosed live discrepancies.

For completeness analysis, even that is insufficient: the tool needs a full canonical-claim-to-checklist coverage inventory once per canonical version. Otherwise it cannot reliably discover missing rows.

2. **“Confirmation Route = Verification Method” is logically invalid.**

`Postman`, `UX Testing`, `Provide Code`, and `Verbal` describe how MA may inspect an item. They do not define sufficient technical evidence.

Concrete failures:

- One successful Postman JWT request proves neither all endpoints nor time boundaries, wrong `aud`/`iss`, future timestamps, production configuration, or credential rollover.
- Human observation of a rendered picker proves neither capability enforcement nor tenant isolation.
- A Postman idempotency retry does not prove crash atomicity or concurrent duplicate suppression.
- A sequential Postman send cannot prove per-conversation ordering under two workers.

The suggested “code-only with reasoning where no runtime test applies, e.g. HS256 JWT rotation” is especially wrong. JWT behavior is highly testable: captured wire tokens, golden vectors, clock-boundary cases, all endpoint call sites, old/new secret overlap, and deployment cutover. The canonical requires temporarily accepting both old and new secrets during rollover [canonical JWT key management](/home/davidfer/github/AMB-canonical/canonical/AMB_Layer2_Canonical_v7_0.md:200). Yet the code and configuration hold one secret [config.go](/home/davidfer/github/cerebro/internal/platform/config.go:26), while B.2’s green note treats minting a fresh token as sufficient “rotation” [checklist B.2](/home/davidfer/github/cerebro/proofs/checklist.yaml:234).

Fix:

- Build an obligation-by-evidence matrix.
- Treat `ma_verification` as an external-review presentation route only.
- Define technical planes independently: static reachability, contract, integration, concurrency/crash, configuration/deployment, live protocol, and human UX.
- A test or human attestation satisfies only its named obligations. It never flips the aggregate item automatically.
- “Complete” requires every mandatory obligation and every required plane to carry valid, artifact-bound evidence.

3. **Search-pulled slices must be graph closures, not search hits.**

Limiting prompt context is reasonable. Limiting analysis to matching files is not.

Concrete false greens:

- AES-CTR primitives exist and tests pass, but the audited checkout explicitly says inbound attachment arrays have no production decrypt consumer [attachment-crypto.md](/home/davidfer/github/cerebro/docs/attachment-crypto.md:75). A search for `DecryptAttachment` would report implemented.
- `DecryptAttachment` claims to require a `00` prefix but uses `TrimPrefix`, so a correctly sized unprefixed key is accepted [attachment.go](/home/davidfer/github/cerebro/internal/platform/cryptox/attachment.go:32). Its bad-key test omits that exact case [attachment_test.go](/home/davidfer/github/cerebro/internal/platform/cryptox/attachment_test.go:51). Comments plus a green test name would invite a rubber stamp.
- Capability enforcement lives in `amb.ValidateOutbound`, the service, an injected `FlowSendGate`, the composition root, worker wiring and persistence. The comment claiming the service is its only caller is already stale [outbound.go](/home/davidfer/github/cerebro/internal/channel/amb/outbound.go:21); the flow caller exists in [flowgate.go](/home/davidfer/github/cerebro/internal/app/flowgate.go:74).
- Regular sends use the durable per-conversation queue, while typing calls Apple directly [service.go](/home/davidfer/github/cerebro/internal/service/service.go:628). Concurrent typing and regular sends therefore require a cross-path ordering analysis; inspecting only `ClaimHead` or `Client.Send` is insufficient.
- Inbound deduplication spans the relay, edge replay cache and database. Apple can reuse one message ID for typing followed by text, so the relay uses ID plus content hash [environments.md](/home/davidfer/github/cerebro/docs/environments.md:51). An ID-only “dedupe found” verdict could drop the text.

Fix: seed retrieval with search, then expand through production entrypoints, callers, callees, interface implementations, dependency injection, middleware, configuration, build tags, jobs, schemas, migrations, persistence, serializers, retries and sinks. Stop only when every source-to-sink or entrypoint-to-enforcement path is accounted for. Unresolved reflection, generation or indirect dispatch forces `cannot tell`.

4. **The completeness hunt is too free-form to find systematic cross-cutting failures.**

“Ask what is missing” is not a method strong enough to catch tenant isolation reliably.

The current code demonstrates the exact danger:

- HTTP authentication creates a brand-scoped caller [httpapi.go](/home/davidfer/github/cerebro/internal/httpapi/httpapi.go:68).
- API isolation tests are extensive and convincing.
- But `webhook_endpoints` and `webhook_outbox` carry no `brand_id` [0002_partner_rails.sql](/home/davidfer/github/cerebro/internal/platform/pgstore/migrations/0002_partner_rails.sql:37).
- `activeEndpointsTx` selects every active subscribed endpoint globally and fans each event to all of them [pgstore.go](/home/davidfer/github/cerebro/internal/platform/pgstore/pgstore.go:573).

Thus API isolation can be green while webhook delivery leaks Brand A events to Brand B. Ordering and signing merely make the leak reliable and authentic.

Fix: make completeness a systematic matrix over:

- Every trust boundary: Apple, public API, worker, partner webhook/SSE, console/admin, storage and observability.
- Every tenant-bearing object and operation: create, read, update, emit, claim, retry, replay, backfill, revoke and delete.
- Every identity transition: Apple Business ID → brand → API key → conversation/message/attachment → endpoint.
- Every lifecycle and asynchronous path.
- Every canonical claim, MA-only requirement and platform safety invariant.

Also preserve provenance classification. The tenant-isolation proposal explicitly says it is a Messaging Advisory platform control, not directly stated by Apple [tenant-isolation addendum](/home/davidfer/github/AMB-canonical/team/addenda/2026-07-26-i6-partner-webhook-tenant-isolation.md:64). It must not be laundered into “Apple requires `brand_id` columns.”

5. **Checklist proposals need a machine-enforced anti-weakening and citation-integrity gate.**

“Output a proposal, never edit” is necessary but not sufficient. A persuasive hallucinated proposal can still be accepted by a reviewer.

Every proposal must carry:

- Provisional ID, operation (`add`, `split`, `clarify`, `strengthen`, `relax`, `retire`) and affected existing IDs.
- Requirement class: `APPLE_NORMATIVE`, `MA_PROGRAM`, `PLATFORM_SAFETY`, or `LIVE_COMPATIBILITY`.
- Full before/after text and normalized atomic obligations.
- Scope: directions, endpoints, actors, tenants, message classes, lifecycle and concurrency conditions.
- Exact authority claim IDs selected from the pinned canonical index.
- Canonical commit/blob hash, source version/date/rank, exact line span and an excerpt hash.
- Direct versus indirect derivation, with every proposed clause mapped to evidence.
- Conflicts, superseded sources and discrepancy references.
- Verification planes, negative cases and failure oracle per obligation.
- Why existing rows do not already cover it.
- Dependency/status/evidence impact; proposed items start unverified and inherit no green evidence.
- Explicit `strengthens`, `neutral`, or `weakens` classification.

The model should not author citation strings. It should select canonical claim IDs; a trusted resolver should materialize and verify citations. An unresolved or mismatched citation blocks the proposal.

Any relaxation, removed scope, weaker modality, deleted proof plane, new exception, or retirement must be hard-blocked pending authoritative supersession plus explicit human approval.

6. **“Live/canonical behavior overrides checklist wording” is dangerously broad.**

Live acceptance is not normative authority. A permissive Apple server accepting a payload does not prove Apple permits MSPs to rely on it or that MA will approve it.

Apply distinct handling:

- Reaction threading shown impossible by a captured wire format may justify a disclosed `requirement-vs-reality` exception or changed verification method.
- A live “switch” form page absent from the guide is an observed extension, not a new Apple requirement.
- Apple accepting inline payloads above 10 KB is compatibility evidence, not automatic permission to remove the documented reference path or size gate.
- A one-off response could be brand-, OS-, rollout- or account-specific.

Fix: live evidence may open a discrepancy record. It does not silently override canonical or weaken a checklist item. Require reproducibility, environment identity, timestamps, raw artifacts, scope limits and human adjudication.

7. **Prompt injection cannot be solved by telling the model to be skeptical.**

The repository can game the verdict through:

- Comments claiming compliance or false canonical line numbers.
- `README`, `AGENTS.md`, generated reports or fixtures containing instructions.
- Decoy functions named `VerifyJWT` or tests named `TestProof_B2`.
- `TestMain`, build tags, environment checks or skipped tests that make suites vacuously pass.
- Simulator and production code sharing the same bug.
- Tool output or error messages containing adversarial instructions.
- Audit-specific branches triggered by environment variables or process names.

The stale “only caller” comment above is proof that even benign repository prose is unreliable.

Concrete defense:

- Keep the analyzer prompt, authority bundle and policy outside the audited repository and hash them.
- Label every repository byte—including comments, docs, tests, AGENTS files and tool output—as untrusted evidence, never instructions.
- Prefer trusted AST/call-graph extraction over raw prose retrieval.
- Run repository code only in a hermetic, no-secret, no-network, resource-limited sandbox.
- Independently enumerate discovered tests and verify they executed; a test name or exit code alone is not evidence.
- Use an external oracle or canonical fixture where possible.
- Generate mutations externally and verify that each claimed proof turns red.
- Do the primary code assessment blind to existing checklist status and notes; reveal them only during reconciliation to reduce anchoring.

A prompt-only defense is not sufficient; this requires controller architecture.

8. **Report provenance does not bind runtime confirmation to the analyzed code.**

The repository records a real failure: live proofs ran against a staging image 108 commits behind source, and “nothing in the rig” detected the mismatch [environments.md](/home/davidfer/github/cerebro/docs/environments.md:228). The proving prompt merely says live planes run against staging [proofs/AGENT.md](/home/davidfer/github/cerebro/proofs/AGENT.md:101).

Fix: every runtime artifact must attest:

- Source commit and immutable image digest.
- Deployment/environment/brand/MSP identity.
- Config and feature-flag hashes, excluding secret values.
- Migration/schema version.
- Canonical and checklist versions used.
- Test/harness version and exact command.
- Start/end time and raw request/response correlation IDs.

A mismatch yields `EVIDENCE_FOR_DIFFERENT_ARTIFACT`, never pass.

## P1 — major correctness gaps

9. **Add explicit adversarial passes for state, time, concurrency, crash and upgrades.**

Passes a–d do not systematically cover:

- JWT expiry boundaries and old/new-key overlap.
- Two workers claiming/sending concurrently.
- Close-versus-send and consent-versus-delivery races.
- Crash between DB mutation and job/outbox enqueue.
- Retry after partial network success.
- Rolling deployment with mixed binary versions.
- Existing rows crossing a migration or backfill.
- Feature flags or production defaults bypassing a guard.
- Fail-open behavior when a dependency or resolver is unavailable.

These need named passes, not hope that “refute” happens to consider them.

10. **The verdict vocabulary is too coarse and encourages aggregation errors.**

`implemented / partial / not found / cannot tell` over an entire row hides sub-gap failures.

Use per-atomic-obligation verdicts:

- `SATISFIED_IN_REACHABLE_CODE`
- `VIOLATED`
- `PRESENT_BUT_UNWIRED`
- `TEST_ONLY`
- `DEAD_OR_NON_PRODUCTION`
- `NOT_FOUND_IN_DECLARED_SCOPE`
- `UNRESOLVED`

Aggregate by the worst mandatory obligation. Include coverage and unresolved-path fields; never convert model confidence into compliance status.

11. **Simulator success is not independent confirmation.**

H.1 tests a simulated `429` because both the checklist and simulator encode it. That validates internal consistency around a false premise, not Apple compliance. AES round trips can similarly pass when encrypt and decrypt share the same wrong implementation.

Require at least one independent oracle:

- Canonical golden vector.
- External reference implementation.
- Raw captured Apple wire evidence.
- Differential implementation.
- Mutation proving the asserted guard is load-bearing.

12. **Cross-audit reconciliation is useful triage, not validation.**

Two models can agree because both were anchored by the same green status, comment, simulator or retrieved row. A difference is not automatically a finding, and agreement is not proof.

Make audits genuinely orthogonal:

- One proves the claim from production entrypoints.
- One constructs counterexamples and bypasses.
- Use different retrieval seeds.
- Keep each blind to the other’s verdict.
- Reconcile by re-adjudicating evidence, not by voting.
- Report both shared blind spots and differences.

13. **“Not found” needs an absence-proof protocol.**

Never emit plain `not found`. Emit:

- Exact commit/tree assessed.
- Included and excluded build targets.
- Queries, protocol literals and semantic symbols searched.
- Entry points and sinks enumerated.
- Generated code, migrations, infra and external dependencies checked.
- Indirect/dynamic paths unresolved.

If any required scope is unavailable, the verdict is `cannot tell`, not `not found`.

## P2 — hardening and review usability

14. **Expand provenance beyond commit/checklist/model.**

Include dirty-tree state, submodules/LFS, toolchain and dependency locks, build tags, target role, OS/architecture, analyzer prompt hash, retrieval-tool version, canonical commit and addenda set. “Model” alone is not reproducible provenance.

15. **Add evidence freshness and invalidation rules.**

Canonical updates, code changes in the transitive path, migration changes, simulator changes, deployment changes or proof changes must invalidate affected evidence automatically. File-name proximity is insufficient; use a dependency/claim graph.

16. **Force counterexample-first reporting.**

For every positive obligation, require:

- Strongest attempted counterexample.
- Exact production path traced.
- Guard and sink locations.
- Negative test or mutation.
- Remaining bypasses.
- Why the test oracle is independent.

This makes a reviewer evaluate the weakest link rather than rubber-stamp a polished conclusion.

## Minimum per-item prompt contract

A safe per-item prompt should require this structure:

```text
AUTHORITY
- pinned canonical/checklist commits and versions
- atomic canonical claims and verified citation IDs
- conflicts, exceptions, addenda, live discrepancies

SCOPE
- production entrypoints, actors, directions, message classes and tenants
- build/config/deployment assumptions
- unresolved dynamic paths

TRACE PER OBLIGATION
- source -> validation/enforcement -> persistence/queue -> sink
- all callers and alternate/bypass paths
- migrations and asynchronous retry/replay paths

VERDICT PER OBLIGATION
- status from the closed vocabulary
- executable evidence, not comments/test names
- counterexample attempted
- negative/mutation evidence
- uncertainty and excluded scope

CONFIRMATION PLAN
- technical evidence planes required
- MA presentation method separately
- artifact/deployment binding requirements

CHECKLIST ASSESSMENT
- covered / omitted / contradictory / ambiguous
- never infer checklist correctness from current code

PROPOSAL
- only when authority and citation gates pass
- full obligation diff, trust tier and anti-weakening classification
```

The decisive change is this: the checklist row should be a navigation and reporting unit, while atomic pinned authority claims and complete production-path traces are the adjudication units. Without that inversion, the tool will reproduce the same blind spots with greater rhetorical confidence.
