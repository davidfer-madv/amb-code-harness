# Tasks

## 1. Define trusted report schema

- [ ] Add a structured finding schema for authority pins, candidate provenance, atomic obligations,
  methods used, verdict, evidence, limitations and closure work.
- [x] Add the controlled verdict enum. Legacy-result mapping remains pending with the renderer.
- [x] Reject a pass when any mandatory verification method remains unconfirmed.

## 2. Generate item and consolidated reports

- [ ] Add deterministic one-item Markdown rendering.
- [ ] Add index generation and consolidated/item consistency checks.
- [ ] Add stable file naming based on exact item code plus sanitized slug.
- [ ] Test missing item output, duplicate item codes and unknown UIDs.

## 3. Enforce trust boundaries

- [x] Refuse validated report output paths below `workspaces/<candidate>/src` or any candidate repository.
- [x] Validate artifact/package candidate scope and reject cross-candidate package paths.
- [ ] Treat candidate instructions/comments/PDF text as untrusted evidence.
- [ ] Add tests for omitted shared dependency and prompt-injection scenarios.

## 4. Add sanitized packaging

- [x] Build packages from an explicit report allowlist rather than recursive directories.
- [x] Emit a SHA-256 manifest for delivered files.
- [x] Reject raw PDFs, images, Postman environments/results, runtime dumps and source files.
- [x] Add secret-pattern and tracked-`workspaces/` checks before package creation.

## 5. Update policy, playbook and prompts

- [x] Add the format and verdict rules to trusted policy/playbook surfaces.
- [ ] Update the code-analysis prompt to emit structured atomic findings without awarding non-code
  confirmation.
- [ ] Document optional Postman/UX/device/human reconciliation and precedence.
- [x] Refresh `.policy-hashes.txt` after trusted policy-layer changes.

## 6. Validate and document

- [x] Run `openspec validate standardize-multibrand-item-audit-format --strict`.
- [x] Run shell syntax checks for modified scripts.
- [x] Add focused behavioral tests for authority pinning, method completion, isolation and packaging failure cases.
- [ ] Document migration for existing candidate reports without rewriting historical verdicts.

