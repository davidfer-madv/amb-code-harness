## Context

Verifier stage has two analysis strategies, provider adapters, immutable run provenance, and a
blind evidence judge. The existing strategy proposal predates part of that implementation. A
multi-model review is useful only if every reviewer assesses the same facts and cannot mutate the
evaluated source.

## Goals / Non-Goals

**Goals:**

- Test whether Codex, Opus 5, Fable 5, and GitHub Copilot independently converge on the strategy.
- Identify disagreements that reveal ambiguous requirements or unsupported recommendations.
- Produce a source-cited reconciliation record and a revised proposal.

**Non-goals:**

- Treating model agreement as ground truth.
- Comparing writing style, speed, or popularity.
- Running paid live analysis on Cerebro or Maglev in this change.

## Decisions

### Freeze inputs and isolate execution

Every reviewer receives the same stage commit, v1.1 proposal, structured schema, and review rubric.
The detached candidate clone remains read-only and push-disabled. Review output is captured only in
the audit harness.

### Use evidence-weighted reconciliation

Each claim is classified as accepted, rejected, unresolved, or out of scope. Acceptance requires an
exact stage citation or a repeatable test result and no stronger contradicting evidence. Agreement
without evidence is not sufficient; dissent with correct evidence overrides unsupported consensus.

### Preserve independence

Reviewers do not receive another reviewer's conclusion. The reconciliation happens only after all
available reviews finish. A model unavailable to the authenticated account is recorded as
unavailable rather than silently replaced.

### Bound permissions and spend

Claude sessions receive only read/search tools, no persistence, and a hard monetary ceiling.
Copilot receives only read/search tools, no GitHub MCP, no network URLs, no custom candidate
instructions, no shell, and a bounded premium-credit allowance. No reviewer receives write tools.

## Trust Boundaries and Data Flow

1. Frozen Verifier clone → read/search-only reviewer context.
2. Stage-aligned proposal/schema → reviewer context as trusted evaluation input.
3. Model response → untrusted review artifact in the harness.
4. Source citations/tests → deterministic reconciliation table.
5. Accepted conclusions → revised prompt strategy and assessment documentation.

Writable scope is limited to `openspec/`, `prompts/anthropic/`, and `reports/` in the audit harness.

## Failure Behavior

- If a requested model is unavailable, record the exact CLI refusal and continue with remaining
  reviewers; do not claim four-way agreement.
- If a reviewer attempts a write or network action, deny it and mark the review invalid.
- If citations do not resolve against the frozen commit, reject the associated claim.
- If reviewers disagree and source does not settle it, retain the point as unresolved and do not
  incorporate it as an agreed recommendation.

## Migration Plan

Add the evaluation record and a v1.2 strategy revision after reconciliation. Retain v1.1 as the
comparison baseline and mark its successor explicitly. No candidate migration is involved.
