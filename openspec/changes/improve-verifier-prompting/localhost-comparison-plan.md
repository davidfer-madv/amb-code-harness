# Localhost comparison plan: deployed Stage vs current Stage vs proposal

**Prepared:** 2026-08-30; refreshed 2026-09-06  
**Remote mutations:** forbidden  
**Candidate mutations:** forbidden  
**Paid calls:** only after parity, offline tests, cost preview, and explicit authorization

## 1. Decision

Test three isolated arms:

| Arm | Revision | Purpose |
|---|---|---|
| A — deployed Staging | `8d142b5b759207dbbb8e20fdd2076aae7b0ffe0c` | Reproduce what the deployed application code can do today |
| B — current Stage replication | `8d142b5b759207dbbb8e20fdd2076aae7b0ffe0c` | Detect environment/data variance; collapse into A when all frozen inputs also match |
| C — proposal | local branch `proposal/improve-code-analysis-prompting` from `8d142b5…` | Measure only the proposed increment |

The proposal workspace is:

```text
workspaces/verifier-prompt-localhost-20260830/src
```

Its GitHub fetch URL is retained and its push URL is `DISABLED`. No remote branch exists.

The copy-ready setup and execution commands are maintained in
`../../../reports/verifier-localhost-runbook-and-prompt-plan-2026-09-06.md`. This comparison plan remains the
experimental protocol; the runbook is the operator procedure.

## 2. Checklist status and provenance

Historical August source used by the first plan:

```text
checklists/August - Updated Checklist - 26_07_30_AMB_Linq_MSP_Integration_Checklist - AMB MSP Integration Checklist (Apple Feedback Update) (1).csv
SHA-256: bbdf5becf3cea61dd390f94baa8ae05ee796d41aba770615130fe7ca20ba01c8
```

The file contains 82 recognized item rows. The checked-in `prod-linq-items.json` artifact on current
Stage contains 73 rows and predates the August source. It lacks `C.23`, `D.6`, `E.11`, `E.12`,
`G.6`, `H.3`, `H.4`, `I.6`, and `K.1`; many shared items also differ materially.

This does **not** establish the content of the live Staging database. Verifier deliberately stores
canonical checklists as versioned database data and does not seed production content from the
repository. The unauthenticated Staging checklist endpoint returned HTTP 401. Therefore the current
answer is:

> Live Staging use of the named August checklist is unconfirmed. The repository artifact is older,
> and an authenticated read-only checklist export is required.

Before evaluation, an authorized operator must:

1. open Staging and identify the canonical version bound to the test tenant;
2. export that version through its read-only checklist bundle endpoint;
3. record version ID, version number, created time, item count and bundle hash;
4. normalize and compare item IDs plus material fields with the August CSV;
5. record tenant overrides and the tenant checklist revision, if any.

Do not compare filenames. Compare normalized item content and revision identifiers.

## 3. Convert the CSV once, outside the experiment

Current Verifier no longer imports CSV. Build one reviewed `verifier-checklist-bundle/v1` document
from the August source, retaining all supported authored fields and explicitly mapping unsupported
columns. Preview the bundle import in localhost and resolve every validation error or warning before
creating the three databases.

The frozen manifest records:

- source CSV byte hash;
- normalized semantic hash;
- generated bundle byte hash;
- mapping-tool revision;
- item IDs and count;
- check/code-check bindings;
- section names and week layout;
- fields that could not be represented.

The same reviewed bundle bytes are imported into all three local arms. Nothing is imported into live
Staging as part of this experiment.

For the refreshed experiment, the exact latest source is
`[LATEST] 2026_08_25_AMB_MSP_Integration_Checklist_With_Apple_Feedback - 26_07_30_AMB_Linq_MSP_Integrati.csv`
with SHA-256 `ec683e809643bb6d9774c509e70c47d86e9d46633949fe2a6fe3e322c7c57f40`.
Its split B.1 and C.13 rows and stray row `81` must be normalized explicitly before import.

## 4. Capture the real Staging baseline

With authorized read-only access, export or record:

- deployed commit (`/api/health` currently reports `8d142b5`);
- canonical checklist bundle and tenant binding/override revision;
- active check-template revision and hash;
- active blind-judge revision and hash;
- registered model IDs, provider, generation settings and price revisions;
- analysis-limit revision;
- guide revision;
- selected checks and operator instruction;
- prior run IDs, observations, citations, trails, raw responses where retained, usage and cost.

Secrets are never exported. If the application lacks a safe run-export endpoint, read the existing
authenticated run endpoints and write a harness-side immutable manifest; do not query or mutate the
production database directly.

## 5. Build isolated localhost arms

Use three checkouts and three Postgres databases. Give every arm a different:

- database name/volume;
- `SOURCE_ROOT`;
- HTTP port;
- session secret;
- admin account used only for the experiment.

Never share a database volume. A run stamps revisions from its own database, so copying one mutable
database between arms after runs begin would invalidate provenance.

Start each checkout using its documented local workflow:

```bash
cp .env.example .env
make dev
```

Use shell or secret-manager injection for `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`; do not write API
keys into committed files, manifests, logs, command arguments, or reports. The current Docker
rehearsal compose file does not automatically forward these keys, so either use `make dev` with
process environment variables or add a local untracked compose override.

## 6. Provider and model parity

Verifier reaches Claude through `anthropic_api` and OpenAI through `openai_api`. Models and their
prices are database registry rows, not environment variables. For each provider, copy the exact
Staging registry contract into all local arms:

- provider;
- exact pinned model identifier, including date/version suffix;
- generation settings;
- capability declaration;
- input, output, cache-read and cache-write prices;
- price-table revision.

Do not compare “Claude” with “OpenAI” as though provider differences measure the prompt change.
Compare A/B/C within one provider/model first. Provider-to-provider agreement is a separate
robustness result.

If the deployed model is no longer callable, record that fact and choose one currently callable
pinned model for all three local arms. Do not silently substitute it while calling the result a
reproduction of the historical Staging run.

## 7. Freeze every experimental input

Create a manifest per paired case containing:

```text
experiment_id
arm
application_commit + tree_hash
candidate_name + commit + tree_hash
checklist_bundle_hash + canonical_version_id
tenant_override_revision/hash
clause/item/check stable IDs
effective criterion hash
terms prompt + tool schema hash
classifier prompt + tool schema hash
check-template revision/hash
judge revision/hash
model/provider/settings/price revision
analysis-limit revision
guide revision
operator instruction hash
source extraction limits
```

The comparison tool refuses a pair when any controlled field differs, except the declared treatment:
application revision and, for Arm C, the proposed prompt/runner version.

## 8. Run order

### Step 1 — Offline validation

Run focused unit tests, prompt/tool contract tests, citation-resolution tests, deterministic
aggregation tests, checklist-bundle validation and experiment-manifest parity checks. No provider
calls occur.

### Step 2 — Dry cost preview

Preview identical selected checks in A/B/C for one Claude model and one OpenAI model. Record the
maximum per arm and total. Set explicit per-run and total experiment ceilings.

### Step 3 — Small paired smoke set

Use 5–10 human-labelled clauses covering:

- a reachable implementation;
- a declaration without a use path;
- an alternative mechanism satisfying an outcome;
- a mandatory mechanism absent;
- customer-facing naming versus a technical identifier;
- a composite clause with one missing part;
- ownership outside the candidate repository;
- an incomplete/provider-failure control.

Run A/B/C in randomized arm order. Run Claude and OpenAI as separate paired blocks.

### Step 4 — Gate

Stop if there is any critical false `implemented`, invalid citation, incomplete-to-conclusive
conversion, parity mismatch, cross-snapshot path, or unexplained spend divergence.

### Step 5 — Frozen golden set

Run the approved Cerebro and Maglev code-verifiable clauses against pinned read-only snapshots.
Keep candidates in separate runs and contexts. Do not touch either repository.

### Step 6 — Repeatability sample

Repeat a stratified subset at least three times per arm/model. Deterministic sweep and aggregation
should remain identical for identical structured model answers; model-output variance is reported,
not hidden by majority vote.

## 9. Comparison report

Report per clause and aggregate:

- result and undetermined reason;
- mandatory-clause coverage;
- verified citations and invalid citation count;
- false green, false negative and exact advisory agreement;
- wrong-owner, wrong-surface and mechanism/outcome errors;
- search/classification completeness;
- run-to-run variance;
- input/output/cache tokens;
- actual provider cost and latency;
- recommendation usefulness and correct next-method routing;
- human-review workload.

Required views:

1. deployed Staging A versus current Stage B;
2. current Stage B versus proposal C — the primary treatment effect;
3. Claude A/B/C;
4. OpenAI A/B/C;
5. Claude versus OpenAI agreement, clearly labelled as robustness rather than truth.

The golden label is human-reviewed source/test evidence. Neither the previous Staging result nor
model agreement becomes truth by itself.

## 10. Promotion decision

Consider proposing the branch for normal review only when:

- all input-parity checks pass;
- there are zero critical false greens;
- mandatory-clause recall is at least 95%;
- exact advisory agreement is at least 90%;
- no invalid citation is accepted;
- the incremental cost per corrected/resolved clause is measured and acceptable;
- remaining disagreements are routed to Postman/API, UX/device, or human confirmation;
- a person approves the report.

Promotion would then follow the repository's normal OpenSpec, review, `stage`, and `main` workflow.
This localhost plan performs no push, PR, merge, deployment, or live checklist import.
