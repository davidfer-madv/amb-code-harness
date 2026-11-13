## Context

See `proposal.md` for motivation. The source checklist exists as a human-readable Markdown file and
a quoted, multiline CSV file. Candidate source is prepared by `bin/audit.sh` under a read-only
workspace. Review feedback can be authoritative, advisory, ambiguous, or incompatible with the
pinned canonical, so direct checklist mutation is unsafe.

## Goals / Non-Goals

**Goals:**

- Make selected checklist records reproducibly available to operators and tools.
- Give Maglev a focused runbook that preserves the full evidence bar.
- Turn Apple feedback into a reviewable proposal with machine-checkable provenance and consistency.

**Non-Goals:**

- Building a general spreadsheet editor or changing candidate code.
- Treating Apple review acceptance as normative protocol authority.
- Completing I.6/H.3 from static inspection alone.

## Decisions

### Use CSV as the extraction source

The extraction helper will parse the CSV with a standards-compliant CSV parser and emit JSON. This
preserves quoted commas and multiline fields and exposes named columns. Extracting Markdown with
line-oriented shell tools was rejected because it cannot provide every structured field reliably.

### Keep focused audit selection in operator documentation

The existing `bin/audit.sh` remains the single candidate preparation path. A Maglev runbook will
invoke it with an exact SHA, describe the authority bundle, and specify I.6/H.3 output artifacts.
Adding a second clone/preparation implementation was rejected because it could drift from isolation
controls.

### Stage review input separately from the checklist

Review artifacts or references, hashes, extracted recommendations, and proposed diffs will live
under a dated proposal directory in `review-intake/`. Trusted harness files may cite the review;
candidate source never receives it. The checklist is edited only in a later, explicit approval
step. Directly appending free-form “latest review” notes was rejected because provenance and
authority would be lost.

### Enforce authority and consistency outside prompts

The workflow will require source hashes and exact affected IDs and will validate extraction and
Markdown/CSV agreement in trusted harness tooling where practical. Prompts explain classification,
but prompt wording alone is not the gate.

## Trust Boundaries and Data Flow

1. Maglev source → read-only `workspaces/maglev/src` → code evidence →
   `maglev-analysis/findings/`.
2. Pinned canonical → verified claim closure → adjudication input; it is never copied into Maglev.
3. Apple review artifact → hashed intake record → classified recommendation → human-approved
   checklist proposal.
4. Approved proposal → synchronized Markdown and CSV edits → refreshed policy hashes.

Writable scope is limited to this harness, especially `maglev-analysis/`, `review-intake/`,
`openspec/`, documentation, helpers, and—only after approval—the checklist files.

## Risks / Trade-offs

- **Review provenance is unavailable** → Stop at the intake template and request the artifact.
- **CSV and Markdown encode different detail** → Validate affected IDs across both and require an
  explicit mapping in the proposal.
- **A focused audit misses a shared bypass** → Retain mandatory tenancy-first graph closure and trace
  all I.6/H.3 production paths rather than keyword-searching only webhook files.
- **Review guidance is mistaken for Apple law** → Require authority classification and direct versus
  indirect derivation before approval.
- **Existing Maglev workspace is stale** → Compare workspace HEAD to the recorded SHA before every run.

## Migration Plan

Additive only: introduce the helper, runbook, and intake template; validate them against the current
checklist and Maglev SHA. Existing full-audit commands continue unchanged. Rollback removes the new
helper and documents without changing candidate source or checklist content.

## Open Questions

- The location and provenance of the latest Apple review artifact must be supplied before any
  recommendation text or checklist diff can be finalized.
