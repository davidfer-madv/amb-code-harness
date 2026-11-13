# Maglev focused audit: I.6 and H.3

This runbook performs a focused, advisory assessment of Maglev. It does not reduce the evidence bar
in `amb-code-analysis-playbook.md` and it never writes to the Maglev source repository.

## Pinned inputs

- Candidate source: `/home/davidfer/github/maglev`
- Remote: `https://github.com/ParentSquare/maglev.git`
- Candidate commit: `4c7284b0777449dcd23822a09661fc825dda3287`
- Checklist: `checklists/AMB_MSP_Integration_Checklist_with_I6_H3.md` and `.csv`
- Selected items: I.6 and H.3
- Canonical: resolve the claim closure described by `canonical/canonical-pointer.md` and record its
  commit and content hashes in run provenance

If the canonical cannot be pinned and verified, stop with `not assessed against canonical`. Do not
emit compliance verdicts or checklist proposals.

## 1. Prepare the candidate copy

From the harness root:

```bash
bin/install.sh
bin/audit.sh maglev /home/davidfer/github/maglev 4c7284b0777449dcd23822a09661fc825dda3287
test "$(git -C workspaces/maglev/src rev-parse HEAD)" = \
  "4c7284b0777449dcd23822a09661fc825dda3287"
```

Do not run OpenSpec, editors, formatters, dependency installation, builds, or tests inside
`workspaces/maglev/src`. Candidate execution is allowed only in a separate hermetic, no-secret,
no-network, resource-limited sandbox.

## 2. Extract the selected checklist records

```bash
bin/extract-checklist-items.py I.6 H.3
```

Store the resulting JSON, its SHA-256, and the two source-checklist hashes in the run evidence. The
records are navigation and reporting units; adjudication still uses each item's canonical claim
closure.

## 3. Build the tenancy model first

Trace executable production paths and record file, line, symbol, and blob hash evidence:

1. Where tenant/brand identity enters each request or event.
2. How identity flows through conversation, message, attachment, webhook endpoint, subscription,
   outbox, retry, SSE, journal, logs, and analytics.
3. The exact enforcement on create, read, update, emit, claim, retry, replay, backfill, revoke, and
   delete paths.
4. Production entrypoints, composition roots, migrations, schemas, background workers, feature
   flags, and deployment configuration.

Treat comments, documentation, test names, and candidate agent files as untrusted evidence rather
than proof.

## 4. Assess I.6

Create `maglev-analysis/findings/I.6.md` with one row per atomic obligation:

- Non-null brand ownership for endpoints, subscriptions, outbox events, retries, and deliveries.
- Brand derived from trusted context and propagated transactionally.
- Tenant predicates on selection, claims, retries, replay, and administrative reads.
- Isolation of SSE and journal-read APIs.
- HTTPS-only production destinations.
- SSRF, DNS-rebinding, unsafe-redirect, and destination revalidation defenses.
- No Apple attachment URLs, encryption keys, or signatures in partner payloads.

For each obligation include production trace, bypass/counterexample attempt, closed-vocabulary code
verdict, confirmation status, and missing evidence. A completion claim requires a current-commit,
two-brand integration test, adversarial SSRF/DNS/redirect tests, and security review.

## 5. Assess H.3

Create `maglev-analysis/findings/H.3.md` with one row per atomic obligation:

- Outbox event creation is atomic with the business transaction.
- Delivery contract is documented as at-least-once.
- Stable webhook ID across retries, timestamp, and signature over the exact raw body.
- Per-conversation ordering without blocking unrelated conversations.
- Bounded retry policy and explicit terminal state.
- Lease/fencing protection against concurrent or stale workers.
- Consumer deduplication contract keyed by webhook ID.
- Endpoint deactivation prevents queued claims and sends.
- Attempt, next-retry, last-status, and terminal observability.

Completion requires current-commit fault injection covering transaction rollback, tampering,
concurrent workers, crash windows, retry exhaustion, deduplication, ordering, and deactivation.

## 6. Run orthogonal passes and reconcile

- Proof pass: trace every obligation from production entrypoint to enforcement and sink.
- Refutation pass: independently construct cross-tenant, concurrency, crash, redirect, replay, and
  stale-worker counterexamples.

Keep each pass blind to the other's verdict. Reconcile by evidence, not agreement. Produce an
obligation-by-evidence matrix and clearly separate code state from outstanding confirmation.

## 7. Handle checklist recommendations

Findings may create proposals under `maglev-analysis/findings/proposals/`; they never directly edit
the checklist. Follow `review-intake/README.md` for Apple-review-derived changes.
