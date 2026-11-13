# Tasks: directional Postman probe expansion from v2026.10.06

## Gate 0 — authority and inventory

- [x] Pin checklist v2026.10.06 and its checklist/bundle hashes.
- [x] Record the current 24 checks, 14 bound items and inherited inbound-only direction.
- [x] Keep Code analysis outside this proposal.
- [ ] Have the checklist owner approve the proposed item-to-scenario mapping.
- [ ] Apply `<suite> · <primary item code> · <specific scenario>` to every new probe name and
      validate that the visible code agrees with `checklist_item_codes`, the item's
      `check_bindings`, the pinned checklist version and the provenance UID.
- [ ] Inventory existing `NCT staging 20260911` names and approve an explicit identity-preserving
      rename migration (or a separate display-name field); do not rename natural-key probes through
      ordinary bundle upsert.

## Phase 1 — Verifier to MSP expansion

- [ ] Add a compatibility test that validates every proposed request through Stage's actual
      `BundleCheck`, `CheckRequest` and `ExpectedCriteria` models.
- [ ] Inventory current built-ins, expected matchers, body encodings, request limits and executable
      item buckets; reject any proposal using an unsupported feature.
- [ ] Correct or retire the existing `Malformed JSON body` definition: `__raw__` is not interpreted
      by Stage and currently produces valid JSON.
- [ ] Split Tier A checks from Tier B cases requiring runner changes; import only Tier A initially.
- [ ] Author atomic B.9 JWT checks for valid control, structurally valid wrong-secret HS256,
      wrong audience and isolated just-inside/at/just-outside `iat`; keep unsupported cases out of
      the executable bundle until the typed JWT profile lands.
- [ ] Add B.12 corrupt-gzip, invalid-JSON, null and missing-version checks.
- [ ] Add the B.13 ordered-validation family: missing Authorization; bad signature; wrong audience;
      stale `iat`; each required header omitted independently (including `capability-list`);
      structural-schema failure; Destination-Id/body mismatch; identical replay; conflicting replay;
      and valid control.
- [ ] Add overlapping-invalidity/dominance probes only where responses are distinguishable; never
      claim internal validation order from two cases that both return the same undifferentiated 400.
- [ ] Treat Destination-Id/body consistency as an additional B.13 check, not as a replacement for
      canonical ID uniqueness/replay protection.
- [ ] Record that a 2xx control proves endpoint acceptance only; require an approved assertion
      surface before claiming that the message was stored or queued.
- [ ] Route Source-IP enforcement to B.14 Phase 3. Add a preflight that produces `could_not_run`
      when a non-Apple Verifier runner is correctly blocked and no approved test ingress exists;
      never spoof `X-Forwarded-For` as compliance evidence.
- [ ] Extend C.1, C.3, C.8, C.10 and C.12 inbound matrices.
- [ ] Add C.22/D.1 successive capability and per-destination state checks.
- [ ] Add C.23 Invitation state inputs and E.5 opt-out trigger variants.
- [ ] Expand H.1 response-family observations.
- [ ] Add pass/fail/could-not-run tests and secret-redaction tests for every check.

Acceptance: every request targets the MSP inbound endpoint, binds to an existing 10.06 item, and
states what it cannot prove. Every imported request round-trips through the current schema and a
golden dry-run confirms the intended wire bytes. Unsupported raw-body or JWT-boundary cases remain
unimported until their runner support lands.

## Phase 2 — MSP to Verifier, conditional

- [ ] Review and approve `runner-implementation-plan.md` before implementation.
- [ ] Write and approve an ADR superseding the inbound-only constraint for controlled capture mode.
- [ ] Add schema/planner/runner support without overloading tenant `base_url` or inbound JWT
      semantics; current Phase 1 execution must remain byte-for-byte compatible.
- [ ] Threat-model endpoint override, capture tenancy, SSRF, redirects, TLS, secrets and retention.
- [ ] Implement the disabled-by-default capture/emulator contract in a disposable environment.
- [ ] Prove ordered/timestamped capture, negative assertion windows and fault injection.
- [ ] Add B.1 and B.3–B.8 outbound/callback families.
- [ ] Add the complete broken-attachment matrix for B.3–B.5, C.2, I.2 and I.5.
- [ ] Add dedicated I.5 probes for 99,999,999-byte acceptance, 100,000,000/100,000,001-byte local
      rejection with no outbound call, and the `interactiveDataRef` decode chain above 10 KB. Never
      model 10 KB as an outbound rejection limit.
- [ ] Add outbound rich-message families C.1, C.5–C.12 and B.16 payload construction.
- [ ] Add stateful suppression/sequencing for C.4, C.16, C.23, C.27 and E.5.
- [ ] Add H.1 retry/final-classification response injection.
- [ ] Demonstrate that unsupported MSPs route to Phase 3 without being marked failed.

Acceptance: no Phase 2 traffic can reach production or an arbitrary host; every capture is tied to
one tenant, run, source revision, checklist version and check revision.

## Phase 3 — other evidence routes

- [ ] Define the handoff record for live Apple, device/UX, deployed-config, security and human work.
- [ ] Route real attachment interoperability and crypto evidence for B.3–B.6/I.2/I.5.
- [ ] Route B.14 ingress restrictions to deployed-config/security evidence.
- [ ] Route B.16 delivery/brandLogo and C.2 actionable errors to device/UX evidence.
- [ ] Keep no-response, Apple approval and policy claims unresolved until appropriate evidence exists.

Acceptance: no unautomatable obligation disappears and no Phase 3 requirement receives a fabricated
Postman pass.

## Bundle and review gates

- [ ] Produce a successor bundle derived from 10.06; never mutate the approved artifact.
- [ ] Validate all new checks have known existing item/UID bindings and method-compatible placement.
- [ ] Keep UID/phase/assertion maps in reviewed build provenance; emit no unsupported bundle keys.
- [ ] Assert `checklist_item_codes` never substitutes for item `check_bindings`.
- [ ] Reject executable bindings on items the current HTTP planner skips unless the successor
      bundle deliberately and validly changes their method/bucket contract.
- [ ] Validate both checklist-only and with-checkpoints forms round-trip identically.
- [ ] Preview changes and explicitly adopt only disposable/local tenants first.
- [ ] Compare observations with human results; investigate every disagreement.
- [ ] Require hosted Quality, security review, backup/rehearsal and explicit staging authorization.

