# Improve Verifier prompting

This OpenSpec package proposes an incremental improvement to the current Verifier `stage`
code-analysis pipeline. It does not modify Verifier or any analyzed candidate repository.

Read in this order:

1. `proposal.md` — why the change is needed and what it changes.
2. `design.md` — exact architecture, prompt locations, data flow, trust boundaries and rollout.
3. `tasks.md` — implementation and validation plan.
4. `specs/` — testable behavioral requirements.
5. `implementation-plan.md` — consolidated environment findings, copy-ready prompts, code changes,
   and the step-by-step delivery plan.
6. `localhost-comparison-plan.md` — controlled three-arm localhost evaluation against deployed and
   current Stage, including checklist provenance and provider parity.
7. `../../../reports/verifier-localhost-runbook-and-prompt-plan-2026-09-06.md` — copy-ready developer setup,
   secret handling, local startup, baseline validation and A/B/C execution instructions.

The copy-ready prompt text referenced by the design is in
`prompts/verifier-stage-latest-checklist-additions-v2.md`. The v1 file remains the historical
August 30 proposal.
