## Why

The initial Verifier stage assessment and Claude Opus review agree that the proposed Sonnet/Opus
strategy is directionally sound but must preserve stage's stronger evidence controls. Before the
strategy is proposed to the stage team, the conclusion needs a reproducible multi-model adversarial
evaluation rather than relying on one model family or one reviewer.

## What Changes

- Freeze Verifier `stage` commit `9ac99cd97883ed8d571dc26daed44fd82cf9f803` as the evaluated source.
- Give Claude Opus 5, Claude Fable 5, GitHub Copilot, and Codex the same bounded review question and
  the same stage-aligned proposal.
- Require exact source citations, explicit agreement/disagreement, and separate factual findings
  from recommendations.
- Define a deterministic reconciliation gate for accepting a recommendation into the final
  strategy documentation.
- Update the stage assessment and prompt strategy only after the reconciliation record is complete.

Non-goals:

- No change to Verifier, `stage`, `chore/cleanup`, or any candidate repository.
- No Git push, PR, issue, comment, or other remote mutation.
- No automatic implementation of agreed recommendations.
- No model majority may override source evidence, tests, checklist authority, or human approval.
- No use of the Anthropic API key previously exposed in chat.

## Capabilities

### New Capabilities

- `multi-model-strategy-evaluation`: Run bounded, read-only, same-input adversarial reviews and
  reconcile claims through evidence rather than model prestige or majority.
- `strategy-documentation-reconciliation`: Update the proposed AI strategy only for accepted,
  provenance-backed conclusions while preserving dissent and residual uncertainty.

### Modified Capabilities

None.

## Impact

- OpenSpec surfaces: this change package.
- Prompt surfaces: `prompts/anthropic/amb-code-audit-stage-aligned-v1.1.md` and its successor.
- Report surfaces: `reports/verifier-stage-ai-strategy-assessment-2026-08-12.md` and a new
  multi-model reconciliation report.
- Trust boundaries: model-to-source evidence, candidate read isolation, credential handling, and
  documentation acceptance.
- Compatibility and rollback: additive evaluation artifacts only. Reverting the new report and
  strategy revision restores v1.1 without touching Verifier or candidate source.
