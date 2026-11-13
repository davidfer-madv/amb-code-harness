# AMB audit — Vertex / GCP architecture and runbook (v2, hardened)

Messaging Advisory, 2026-07-23. Local working doc in `.madv/` (git ignored). Supersedes
`audit-vertex-runbook.md` (v1) after the Codex adversarial review
(`.madv/codex-adversarial-review-2026-07-23.md`). Companion to `audit-prompt-v2.md`.

Headline correction from v1: the model output is ADVISORY. It never sets checklist status. Two
separate services do the safe work: a read-only Auditor (calls the model) and a Status Applier
(validates, recomputes completion deterministically, and proposes status via a PR). The applier
never pushes to protected main.

## Two-service architecture
1. Auditor (read only): packs inputs, calls the model once per item-batch, returns the raw
   emit_audit JSON. No status authority. No partner-repo write.
2. Runner/Validator (auditor-owned code, NOT partner-repo scripts): builds the pack manifest and all
   hashes from git objects; supplies trusted attestations; validates the model output strictly;
   recomputes completion_gate from required proof planes + attestations; wraps everything in a signed
   provenance envelope.
3. Status Applier: consumes only VALIDATED envelopes, applies the downstream transition rule from
   audit-prompt-v2.md, and opens a PR (or a proposed checklist update). Never writes protected main;
   status flips ride PRs, matching the repo's own rule.

Everything the partner repo controls (packing, file inclusion, applicability, input/evidence hashes,
method satisfaction, status mapping, audit reuse) is decided by auditor-owned code, never by scripts
in the checked-out repo. This is the same class as the Codex C-01 finding (a PR-controlled script
gating its own review): do not let the audited party compute the gate.

## Pipeline
webhook (verified signature, repo allowlist) -> Runner clones at immutable SHA (hooks disabled) ->
build pack + manifest + hashes -> collect trusted attestations -> model call(s) -> strict validate
-> recompute completion -> sign envelope -> store -> Applier opens status PR -> notify/queue humans.

## Provenance: runner-owned envelope (model never invents ids/hashes/timestamps)
```json
{
  "schema_version": "2", "run_id": "uuid", "attempt_id": "uuid",
  "idempotency_key": "sha256(repo,commit,canonical,checklist,prompt,schema,model,mode)",
  "repo": {"repository_id": "...", "commit_sha": "...", "tree_sha": "..."},
  "base_run_id": "...", "mode": "FULL|INCREMENTAL",
  "canonical": {"commit_sha": "...", "content_sha256": "..."},
  "checklist": {"commit_sha": "...", "content_sha256": "..."},
  "prompt": {"version": "...", "sha256": "..."}, "schema_sha256": "...",
  "pack": {"manifest_sha256": "...", "complete": true, "truncated": false, "input_tokens": 0},
  "model": {"provider": "vertex-anthropic", "model_snapshot": "...", "parameters": {}},
  "runner_version": "...", "started_at": "...", "completed_at": "...",
  "raw_response_sha256": "...", "audit_status": "VALIDATED|FAILED_VALIDATION"
}
```
Storage key is the full input tuple, not the bare commit (a bare `{sha}.json` collides across repos,
KB versions, prompts, schemas, models, reruns):
`audits/{repo_id}/{commit}/{input_tuple_hash}/{run_id}.json`. Keep "latest" as a compare-and-swap
index; never overwrite artifacts. An older run must never become "latest" (CAS on ordered SHAs).

## Strict validation (reject, never partially apply)
- Schema with additionalProperties:false at every level; every status-relevant field required.
- Exactly the authoritative checklist ID set, each once; reject missing/duplicate/unknown IDs.
- Conditional rules: PARTIAL requires missing_clause; completion-eligible requires
  evidence_sufficiency=SUFFICIENT_FOR_COMPLETION AND zero open mandatory requirements AND a trusted
  attestation for every required method.
- Reject a claimed executed method whose attestation_id was not supplied through the trusted channel.
- Reject truncation, non-tool content, multiple tool calls, wrong tool, abnormal stop reason.
- Resolve every canonical_anchor and cited blob_sha256; unresolved -> HOLD_INSUFFICIENT_CONTEXT.
- Store the raw response even when rejected, marked FAILED_VALIDATION.
- Immediately before applying, re-check repo SHA + checklist hash + KB hash are still current.

## Trusted attestations (the second-method channel)
The Runner, not the model, executes or collects proof and hands results in as `<attestations>`:
- CONTRACT/UNIT test execution at the exact commit (parsed results, not definitions).
- POSTMAN/API black-box against a deployed environment.
- CRYPTO known-answer + negative vectors; CONCURRENCY/fault-injection runs.
- DEPLOYED_CONFIG probes (WAF, TLS cert, IAM, secret version, live image digest).
- HUMAN_UX / HUMAN_POLICY / APPLE_MA attestations (signed, with reviewer identity + expiry).
Each attestation: {attestation_id, method, result, artifact_digest, executed_for_commit, producer,
trust_domain, expires_at, signature}. The model may mark a method PASS only if a matching attestation
is present; otherwise it must raise the open requirement.

## Sandbox for executing partner code (second methods are hostile-code execution)
- Verify webhook signatures; allowlist repositories.
- Clone by immutable SHA, hooks disabled; read-only source mount + ephemeral writable workspace.
- No inherited cloud credentials in the test sandbox; network disabled except approved test targets.
- CPU/mem/process/file-size/time limits; secret scanning + redaction before any repo content goes to
  the model. VPC-SC/service perimeter, CMEK, access logs, retention policy on prompts and responses.
- No live Apple send without the repo's existing explicit arming mechanism (DEMO_CONFIRM).

## Packing (v1 globs were incomplete)
Add to the FULL pack: cmd/** (composition + many proof tests live here; a handler can look wired but
not be), .github/workflows/**, scripts/prove.sh, tools/checklistcheck, tools/proofrecheck,
proofs/gates.yaml, infra/**, examples/partner-agent/**, Makefile, go.mod, and all migrations. Build a
deterministic pack manifest: every git blob with size, hash, inclusion reason, and any omission. Set
complete=false on any truncation, unreadable LFS pointer, submodule, oversized file, parse failure,
or token-budget exclusion — completion is then impossible for affected items.

## Full vs incremental (incremental reuse must be gated)
Force a FULL re-audit when any of these change: shared libraries, proof/test definitions, build or
config, schemas, migrations, infrastructure, security-sensitive files, dependencies, or the
canonical/checklist/prompt/schema/model. Permit incremental only from an exact validated parent run
with matching KB, checklist, prompt, schema, runner, and model snapshot. Even then, re-run the
deterministic proofs for already-complete items on any relevant change rather than trusting prior LLM
output. Periodically run FULL and diff against incremental; quarantine divergence. Coalesce
superseded webhooks; CAS the "last audited SHA" so out-of-order pushes cannot regress it.

## Batching (one call is not a safety property)
74 evidence-rich items plus canonical can exceed context and the output budget. Use deterministic
batching: one call per bounded item group with an exact ID manifest; a separate cross-cutting
security/structural pass; deterministic aggregation enforcing exact coverage; cached canonical/
checklist blocks shared across calls; retry only failed chunks under the same idempotency tuple; no
silent truncation (fail closed on token ceilings).

## Determinism and model pinning
Rendering and counts are deterministic; judgments are not. Pin one exact model snapshot per audit
policy version; record all generation parameters at lowest supported randomness. Do NOT compare a
Sonnet incremental verdict directly with an Opus full verdict without marking a methodology change.
Shadow-test any prompt/model upgrade against the frozen benchmark (below) before promotion; a model
or prompt change is a FULL re-audit trigger. For completion or security recommendations, run a second
independent assessment as a disagreement detector (two LLM approvals still do not replace execution).

## Prompt-cache correctness
Caching is a cost optimization only, never evidence. Hash the exact serialized cached blocks and
store those hashes in the envelope; invalidate on any byte change (not a version label); never treat
a provider cache hit as proof an audit previously passed; test cached and uncached requests give
equivalent serialized inputs. Reconcile the system-block layout (runbook) with the user-template
layout (prompt) so they cannot silently diverge.

## Human-in-the-loop
Alert and queue (not just on regressions/blocks/version-mismatch): HOLD_HUMAN, HOLD_SECOND_METHOD,
HOLD_CONFLICT, HOLD_INSUFFICIENT_CONTEXT, schema/truncation failures, any prompt_injection_flags, any
completion promotion, and stale/expired evidence. Record reviewer identity, decision, scope,
timestamp, artifact hashes, expiry, and rejection reason. Require two-person approval for security-
and Apple-review-critical completions.

## Audit the auditor
Maintain a frozen adversarial benchmark of known defects: the C-01 review-cache bypass, C-02 cross-
tenant webhook fanout, the ownership-transition race, vacuous/skipped tests, deleted proof
assertions, fake evidence paths, prompt injection in comments/checklist notes, a route not wired,
static infra differing from deployed, and a canonical/checklist conflict. Primary metric: false-
complete rate. A single false green blocks prompt/model promotion. Periodically human red-team a
sample of completion-eligible results; mutation-test the method-coverage logic.

## Evidence store (suitable for Apple Integration Review)
Immutable/versioned GCS (object lock for accepted review evidence). Each package: full source commit
+ deployed image digest; canonical/checklist/prompt/schema versions; environment + brand/test
identity; device model + OS; UTC timestamps + expiry; sanitized request/response bodies + Apple
correlation ids; platform-side AND device-side results; screenshots/video where rendering matters;
human attestation identity; artifact hashes + signed manifest; redaction log + chain of custody.

## Cost and concurrency
Idempotency-tuple trigger dedup; coalesce superseded pushes; CAS state updates; per-run token/cost
ceilings that fail closed (never truncate); retry budgets + dead-letter; separate quotas for
incremental / full / live verification; per-item and per-method cost reporting; a guaranteed periodic
FULL audit even if incremental volume exhausts budget.

## Module layout
```
amb-auditor/
  prompt.py       # SYSTEM_PROMPT + EMIT_AUDIT_TOOL (v2)
  pack.py         # git-object pack + manifest + hashes (auditor-owned, not repo scripts)
  attest.py       # run/collect trusted attestations (sandboxed); emit attestation records
  run.py          # AnthropicVertex call(s), batching, caching, pinned model snapshot
  validate.py     # strict schema + coverage + attestation + freshness validation
  gate.py         # recompute completion_gate deterministically; downstream transition rule
  envelope.py     # runner-owned provenance envelope + signature
  store.py        # immutable GCS paths + CAS latest index + BigQuery
  apply.py        # Status Applier: open PR only, never push protected main
  notify.py       # human queue + alerts
  bench.py        # frozen adversarial benchmark; false-complete metric
```

## Production vs local
In production, write only to the external evidence store. Local `.madv/` rendering is an explicitly
manual, non-authoritative export for these advisory reviews. The model calls no external service
except, optionally, a single named read-only trusted KB tool (if used, record every retrieval in
provenance and amend the system prompt to permit exactly that tool).

## Status: gated
Treat the whole pipeline as advisory-only / unsafe for automated checklist mutation until every P0
control here and in audit-prompt-v2.md is implemented and the benchmark's false-complete rate is
zero on the frozen set.
