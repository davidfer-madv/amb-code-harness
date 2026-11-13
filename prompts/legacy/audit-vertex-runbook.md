# AMB audit — Vertex / GCP architecture and runbook

Messaging Advisory, 2026-07-23. Local working doc in `.madv/` (git ignored, never committed).
Companion to `audit-prompt.md` (the portable prompt). This file is the infrastructure: how to run
that prompt automatically on GCP with an Anthropic model on Vertex, every time the partner repo
updates or on manual trigger, writing all artifacts outside the repo.

## Design in one paragraph
The model does judgement and evidence only. Everything deterministic (score tallies, rendering the
CSV/MD/HTML, diffing against the prior run, alerting) is done in code, not by the model, so results
are stable and diffable. The model is called once per run and returns a single structured JSON
object via the `emit_audit` tool (schema in `audit-prompt.md`). Large, stable inputs (system prompt,
the canonical KB, the checklist) are sent as prompt-cached blocks; only the changing code pack and
the prior audit vary between runs.

## Pipeline (trigger to artifact)
1. Trigger: GitHub push webhook on the partner repo, or a manual/API trigger, or a Cloud Scheduler
   cron. Lands on a Cloud Run service (or Cloud Build).
2. Checkout the repo at the new commit SHA (read only clone). Read the last audited SHA from state.
3. Pack the inputs (canonical KB, checklist, code pack or diff, prior audit JSON). See below.
4. Call the Vertex Anthropic model once with the tool `emit_audit` forced.
5. Store the returned JSON in GCS (and/or BigQuery) keyed by SHA.
6. Deterministically render the tracking CSV, markdown, and HTML (same formats as `.madv/*_v3.*`),
   compute the delta versus the prior JSON, and write them to GCS / `.madv/`.
7. Notify (Slack/email) only when a regression or a new external block appears.

## Sourcing the KB (authority #1)
"The KB" is Messaging Advisory's madvamb-kb, not a loose file. Source it deliberately:
- Spine (always in-context, cached): the full AMB_Layer2_Canonical md, exported from the KB at a
  known version/commit. Feeding the whole canonical is more robust and reproducible than retrieval
  for an exhaustive audit, and caching makes it cheap.
- Supplementary KB docs (include when relevant to the changed items): AMB_Verified_Answers,
  AMB_Decision_Records (the DR-## positions), and the gap register (the Gap-## entries). These carry
  the KB's authoritative stance where Apple's own docs are silent or contradictory, which is exactly
  where audits get hard (receipts, rate limits, the Form OS floor, PNG-only interactive images).
- Record provenance: capture the KB version and commit SHA the run used in audit_meta.
  canonical_version. A canonical/KB change forces a FULL re-audit (prior verdicts are invalidated
  when the authority moves).
- Optional live retrieval: the KB also runs an MCP/knowledge service. You may expose it as a tool so
  the model can look up a specific canonical passage on demand, but keep the full canonical as the
  in-context spine so nothing is missed. Retrieval is an augmentation, not a replacement.
- The KB stays upstream: the audit reads the KB read only. It never writes back to madvamb-kb or to
  the partner repo.

## Prompt caching (the main cost lever)
Put the SYSTEM prompt, the CANONICAL KB, and the CHECKLIST in cache-controlled blocks. They are
large (the canonical alone is ~13.5k lines) and stable across runs, so caching cuts both cost and
latency dramatically on frequent triggers. Only the repo pack and the previous audit change between
runs, so keep those as the uncached tail (the user turn). Structure: system = [system_prompt(cached),
canonical(cached), checklist(cached)]; user = [repo_pack + previous_audit].

## Full versus incremental runs
- INCREMENTAL (default, on every push): send the git diff since the last audited SHA plus the full
  current text of each changed non-test file, plus the prior audit JSON. Ask the model to re-verify
  only the touched items, carry the rest forward unchanged, and compute change flags. Cheap; matches
  "run on every repo update." This is exactly how the manual v2 and v3 were produced.
- FULL (periodic: nightly, on release tags, or when the canonical KB or checklist changes): pack the
  whole AMB-relevant tree and re-verify every item from scratch. Always do a FULL run when the
  canonical or checklist changes, since those invalidate prior verdicts.

## What to pack in FULL mode (globs)
internal/channel/**, internal/content/**, internal/domain/**, internal/delivery/**,
internal/flows/**, internal/edge/**, internal/service/**, internal/httpapi/**,
internal/platform/cryptox/**, internal/platform/pgstore/**, internal/app/**, api/parts/**,
proofs/checklist.yaml, proofs/specs/**, proofs/flows/**, proofs/policy/**, all doc.go, and
docs/{timeouts,os-capability-matrix,spec-discrepancies,partner-api}.md. Include *_test.go for the
proof files (they encode the contract). Exclude vendored deps, node_modules, build output, binary
fixtures. A tool like repomix or a simple tar-to-text with these globs works.

## Vertex specifics
Use the Anthropic Vertex SDK (`pip install "anthropic[vertex]"`). Pick the model in your Model
Garden region: for frequent incremental runs, a Sonnet-class model is the cost/quality sweet spot;
for periodic FULL audits, an Opus-class model for depth. Confirm the exact publisher model id in
your Vertex Model Garden (Vertex uses versioned ids). Example:

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(region="us-east5", project_id="YOUR_GCP_PROJECT")

resp = client.messages.create(
    model="claude-sonnet-5@YYYYMMDD",   # confirm the exact Vertex Model Garden id
    max_tokens=16000,
    system=[
        {"type": "text", "text": SYSTEM_PROMPT,
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": f"<canonical>\n{canonical_md}\n</canonical>",
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": f"<checklist>\n{checklist_csv}\n</checklist>",
         "cache_control": {"type": "ephemeral"}},
    ],
    tools=[EMIT_AUDIT_TOOL],
    tool_choice={"type": "tool", "name": "emit_audit"},
    messages=[{"role": "user", "content": user_content}],
)
audit = next(b.input for b in resp.content if b.type == "tool_use")
```

Auth on GCP: run the Cloud Run service as a service account with the Vertex AI User role; the SDK
picks up Application Default Credentials. No API key handling needed.

## Storage, rendering, alerting
- Store each run's emit_audit JSON in GCS at gs://YOUR_BUCKET/audits/{sha}.json and optionally load
  rows into BigQuery for trend queries.
- Render the CSV/MD/HTML deterministically from the JSON with a small script (reuse the renderers
  behind `.madv/*_v3.*`). Do NOT ask the model to produce the CSV or HTML; keep formatting in code
  so every version diffs cleanly.
- Diff against the prior JSON in code to produce the "what changed" table; the model's change_flag
  is a cross-check, not the source of truth for counts.
- Alert on: any REGRESSED item, any new BLOCKED_EXTERNAL, or version_alignment.aligned == false.

## Suggested repo/module layout (all outside the partner repo)
```
amb-auditor/
  prompt.py            # SYSTEM_PROMPT + EMIT_AUDIT_TOOL constants (from audit-prompt.md)
  pack.py              # clone at SHA, build FULL pack or INCREMENTAL diff
  run.py               # AnthropicVertex call with caching, returns emit_audit JSON
  render.py            # JSON -> CSV / MD / HTML (deterministic), score tally, delta table
  store.py             # GCS read/write, last-audited-SHA state, BigQuery load
  notify.py            # Slack/email on regression or new block
  main.py              # Cloud Run entrypoint: webhook -> pack -> run -> store -> render -> notify
```

## Guardrails (operational)
- Read only everywhere: the auditor clones the partner repo and reads the KB; it writes only to GCS
  / `.madv/`. It never commits to the partner repo or the KB, matching the constraint honored by
  hand across v1/v2/v3.
- Deterministic where it matters: counts, rendering, and diffing are code, not model output.
- Provenance on every artifact: record partner commit SHA, KB version/commit, checklist version,
  model id, and run timestamp in audit_meta so any artifact is reproducible.
- The rationale behind the prompt's verdict taxonomy and judgement rules lives in `audit-prompt.md`.
