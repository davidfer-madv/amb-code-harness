# Automated Code Review — How It Works
Messaging Advisory · 2026-07-28 · implementation / technical design

Cost is covered separately (cost-analysis-2026-07-28.md). This describes the system.

## Pipeline (per run, pinned to one commit)
1. FETCH — read-only, pinned to an exact commit. Secrets (.env, keys, certs) excluded before
   analysis. Source exists only for the run, then discarded; we retain the commit id, file listing,
   and the code snippets cited as evidence.
2. ORIENT — once per commit, build a map of the codebase (stack, entry points, where AMB logic,
   message builders, auth and config live). Reused by every check. The codebase is never sent
   wholesale.
3. CHECK — one per checklist item. Each check gets the map, its own criterion (the checklist row),
   and targeted search results it pulls itself (pattern search, bounded file reads, symbol and
   caller lookup, explore-style). Not the whole repository.
4. RESULT — per item: a code finding, a confirmation route, evidence (file:line + snippet),
   and reasoning.
5. CONFIRM — an item is passed only when its confirmation route is satisfied (a passing API test,
   or a human check), never by the code finding alone.

## The criterion is the checklist row, not the canonical
Each check judges against the checklist item (Requirement, Key Considerations, References), which is
distilled from the MA canonical knowledge base. The full canonical is not sent to the model; it
remains the human reference behind the row and the source the references point to.

## Verdict model (two parts, so a code green is never mistaken for done)
- Code finding: implemented (code) | partial | not found | cannot tell.
- Confirmation route, taken from the item's Verification Method column:
  - Postman item -> an executed API test against the staging endpoint confirms it.
  - UX Testing item -> a human on-device / UX check confirms it.
  - Provide Code item -> code evidence may suffice; where no runtime test applies (e.g. HS256 JWT
    rotation) it is code-plus-reasoning with a security sign-off.
  - Verbal / 3-way / Apple-supplied -> out of scope for code; human or Apple confirms.
Typical output reads "implemented (code), confirmed by Postman" or "implemented (code), pending UX".
"cannot tell" is reported, not guessed, and is not a failure.

## Second method: Postman against the running API (no execution of source)
For API-testable items the pipeline runs the Postman/API test against the candidate's staging
endpoint and folds the result in as evidence. This is a black-box call to the running service, not
execution of the source, so the repo stays read-only. This is what turns "the handler looks right"
into "the endpoint returned the right bytes." Items with no practical runtime test stay
code-plus-reasoning and are flagged as such.

## Model routing
Every check runs on the fast, low-cost model first. Items flagged as low-confidence or high-stakes
(security, crypto, tenant isolation, or any conflict) are re-checked by the stronger model on a
24-hour batch window. The router keeps the fast model on the bulk of items and spends the stronger
model only where judgement is load-bearing. The escalation signal is emitted by the checker and
acted on by the runner, not chosen by hand per run.

## Provenance and the gate
Each run records the exact commit, the checklist version, the model used, and a hash of its inputs,
so any finding is reproducible by re-fetching the commit. Findings are advisory output only and
never write to the checklist automatically; a passing API test (API items) or a reviewer (judgement
items) is what flips a status.

## Two tiers (the access matches the goal)
- Tier 1, Advisory: read-only repo, static, search-based, reviewer confirms. Low-friction,
  continuous per-commit signal.
- Tier 2, Confirmation: adds Postman against a staging endpoint for API items, UX routing for UX
  items, and the model router. Rests on executed evidence; this is what an Apple Integration Review
  needs. No execution of source; no CI integration.

Access: Tier 1 needs read-only repo only. Tier 2 additionally needs a staging API endpoint and a
test token for the Postman items.

## Roadmap
Adversarial hardening: treat all repository content as data and never as instructions; keep every
gate decision in our own code, never in anything the analyzed repo controls.

## Limits
Advisory, not an automated pass. Applies to code checklist items; items verified only by live
testing, UX, or discussion with Apple are routed to those methods, not claimed by the code check.
