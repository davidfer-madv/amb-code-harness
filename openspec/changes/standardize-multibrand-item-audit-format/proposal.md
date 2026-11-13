# Proposal: standardize item-by-item audit reports for every candidate brand/MSP

## Status

Proposed. This change defines trusted harness output and packaging conventions. It does not modify
candidate repositories, the canonical checklist, Verifier, staging or production.

## Problem

Audit results are sometimes delivered only as a consolidated table, while earlier Châtaigne work
showed that reviewers also need an independently shareable document for each checklist item. Without
a standard, item reports can omit authority pins, confuse code presence with confirmed compliance,
lose required verification methods, or accidentally store customer evidence in a tracked path.

## Proposed change

For every new candidate audit, the harness SHALL produce:

1. one consolidated decision report;
2. one Markdown report per assessed checklist item;
3. an index mapping item, UID, verdict, method and file;
4. a provenance manifest suitable for deterministic packaging; and
5. a sanitized delivery archive containing reports only, never raw candidate evidence.

The Châtaigne 2026-10-11 item reports are the initial reference example, but the format is
candidate-neutral and SHALL be used for all brands and MSPs.

## Verdict model

The report format separates implementation assessment from confirmation status. Allowed top-level
outcomes are:

- `PASS` — all atomic obligations and required verification routes are satisfied;
- `PARTIAL` — some obligations or required verification routes remain open;
- `NON-COMPLIANT` — executable behavior or verified runtime evidence contradicts an obligation;
- `NOT FULLY VERIFIABLE` — decisive evidence is unavailable or outside the supplied scope;
- `NOT APPLICABLE` — only with explicit canonical applicability support.

“Not found” and “not confirmed” MUST NOT be reported as a violation without contradictory evidence.

## Audit-safety impact and trust boundaries

- Candidate source and candidate-supplied documents remain untrusted, read-only evidence.
- Raw evidence remains below ignored, candidate-isolated workspace paths.
- Generated reports live in the harness `reports/` tree and must contain sanitized excerpts only.
- Canonical definitions, UIDs, methods and hashes are trusted inputs and must be pinned before a
  compliance verdict is emitted.
- Delivery packaging is a separate sanitization boundary; the archive must be constructed from an
  allowlist of generated reports.
- Cross-candidate evidence is prohibited unless the operator explicitly requests a comparison, in
  which case it must be labeled contextual and cannot prove the target candidate's behavior.

## Affected surfaces

| Surface | Proposed impact |
|---|---|
| Policy | Add report/verdict and confidential-workspace rules |
| Playbook | Add item decomposition and package-review steps |
| Prompt | Require method-aware item documents and uncertainty semantics |
| Shell tooling | Add deterministic report-index/package validation |
| Checklist/canonical pointer | Read-only; pins are copied into report metadata |
| Candidate repositories | No change; never receive harness reports or OpenSpec files |

## Non-goals

- No candidate-source mutation.
- No automatic checklist update or automatic Apple approval.
- No conversion of an AI code finding into a pass when Postman, UX, device, verbal or human review
  is required.
- No raw evidence, secrets, environment files or customer screenshots in the delivery archive.
- No requirement to compare candidates.

## Compatibility and rollback

Existing consolidated reports remain valid. The new item directory and index are additive. A future
implementation can be rolled back by disabling item-package generation without changing historical
reports or candidate workspaces. Verdict vocabulary is intentionally compatible with existing
Châtaigne reports; legacy wording is mapped rather than rewritten in place.

