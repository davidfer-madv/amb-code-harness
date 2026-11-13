# AMB audit — model router + mandatory test execution (v6 addendum)

Messaging Advisory, 2026-07-27. Local working doc in `.madv/` (git ignored). Extends
`audit-prompt-v2.md` and `audit-vertex-runbook-v2.md`. Two additions:
(1) a tiered model router — start on Sonnet, escalate to Opus only on real doubt;
(2) a mandatory "run all code tests" step so completion rests on executed evidence, not reading.

## 1. Tiered model router (Sonnet first, Opus on doubt)
Default every run to Sonnet. The model self-declares when it needs a stronger model; the runner
(auditor-owned code, not the partner repo) re-runs only the flagged items on Opus. This keeps ~90%
of items on the cheap tier while spending Opus only where judgement is load-bearing.

Schema addition (per item in emit_audit): an `escalation` object.
```json
"escalation": {
  "type": "object", "additionalProperties": false,
  "required": ["needs_stronger_model", "reason"],
  "properties": {
    "needs_stronger_model": {"type": "boolean"},
    "reason": {"enum": ["LOW_CONFIDENCE","SECURITY_OR_CRYPTO","TENANCY_OR_CONCURRENCY",
                        "AUTHORITY_CONFLICT","EVIDENCE_CONFLICTING","HIGH_BLAST_RADIUS","NONE"]}
  }
}
```

System-prompt rule (append to audit-prompt-v2):
> Set escalation.needs_stronger_model=true when ANY holds: your confidence_score < 70; the item is a
> crypto, auth, signature, TLS, tenant-isolation, or security claim; it is a concurrency/ordering/
> idempotency claim; applicability is AUTHORITY_CONFLICT; evidence_sufficiency is CONFLICTING; or the
> change under review has high blast radius (shared library, migration, schema, security-sensitive
> file). Escalation is a request for a second, stronger opinion — it never authorizes completion by
> itself, and it never lowers the bar for a required second method or human.

Runner router (in run.py / gate.py):
```text
pass 1: run all items on Sonnet (pinned snapshot), with all test attestations already attached.
collect E = items where escalation.needs_stronger_model OR verdict borderline (PARTIAL/UNKNOWN with
  confidence in [60,80]) OR completion_gate would flip on a single field.
pass 2: re-run ONLY E on Opus (pinned snapshot), same inputs + same attestations.
merge: for an item in E, Opus result wins; record both, and flag divergence for the human queue.
never: promote an item to complete on Sonnet alone if it carries a mandatory SECURITY_REVIEW.
```
Escalation is bounded: cap pass-2 items per run (e.g. <= 25% of the set) and alert if exceeded — a
flood of escalations means the pack or prompt is wrong, not that Opus should absorb it.

## 2. Mandatory "run all code tests" (IMPORTANT)
Static reading never completes an item. Before (or alongside) the model call, the runner executes
the project's real tests at the exact SHA and turns the results into trusted attestations that the
model consumes. This is the second-method channel from the runbook, made non-optional.

The runner MUST, at the audited SHA, in the sandbox (read-only source, ephemeral workspace, no cloud
creds, network off except approved targets):
- `make build` and `make test` (full Go suite).
- `make checklistcheck` and `make proofs-status`.
- `make prove-recheck-all` (every green item's policy proof re-runs; live planes stay UNARMED).
- The exact contract proofs behind technical items (e.g. TestProof_B*/C*/D*/H*/I*), captured per test.
- Coverage (`make coverage`) and arch-boundary tests.
- Optionally, deployed black-box probes (Postman/API) and deployed-config probes (WAF/TLS) where an
  item requires them — these need a live target, so they are attestations, not local runs.
- NEVER a live Apple send unless the repo's explicit arming (DEMO_CONFIRM) is set by a human.

Each executed test becomes an attestation: `{attestation_id, method, result (PASS/FAIL/INCONCLUSIVE),
artifact_digest, executed_for_commit}`. Rules:
- An item may reach completion_gate=ELIGIBLE only if every REQUIRED method has a PASS attestation for
  the exact SHA. A missing or FAIL attestation forces HOLD_SECOND_METHOD or INELIGIBLE.
- A test DEFINITION with no execution result is never sufficient (the audit prompt already forbids
  this; the runner enforces it by only emitting attestations for tests it actually ran).
- If a required test could not run (no DB, no `.git`, no staging), mark it INCONCLUSIVE and the item
  holds — do not silently treat "not run" as pass. (v5 saw exactly this: 18 planes needed Postgres,
  A.6 needed `.git`.)
- Store the full test log + digest in the evidence store; the audit cites the attestation_id.

## 3. Cost note
Sonnet-first + selective Opus keeps cost near the Sonnet line (~$0.36 incremental / ~$3.5 FULL) with
Opus spent only on the flagged minority. Running the test suite is compute (CI minutes), not model
tokens, so it does not change the token cost — it changes what the tokens are allowed to conclude.
