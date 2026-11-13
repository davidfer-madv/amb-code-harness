# Phase 1 B.9/B.13 ordered webhook-validation plan

## Decision

Verifier should test the Redo-style rejection sequence, but current Phase 1 can execute only part of
it faithfully. This plan adds the missing cases without confusing an observable response with proof
of internal order, persistence or source-IP enforcement.

Canonical B.13 requires replay protection. Destination-Id/body matching is valuable additional
validation, but it is not the fifth canonical step and cannot replace replay tests.

## Current runner finding

Reviewed Verifier source: `/home/davidfer/github/Verifier` at local commit
`e071a218e9695525d83e8d40df92acd5f0a44949` on branch
`feat/amb-video-ux-analyzer`. The worktree is dirty and was read only. The proposal's pinned Stage
baseline `5876b014572f1cd404d861b66f37db17d97be33f` was also inspected directly with `git show`; it has
the same relevant constraints: `auth_bad` is `BADSIG.BADSIG.BADSIG`, `auth_expired` combines
`iat=-7200` with expired `exp`, request bodies are dictionaries, and valid gzip is driven by
`expected.compress`. No Verifier branch or worktree was modified.

| Capability | Current Phase 1 | Conclusion |
|---|---|---|
| Valid inbound HS256 | `{{jwt}}` | Usable Tier A control. |
| Authorization absent | `{{auth_none}}` drops the header | Usable Tier A case. |
| Wrong signing secret | `{{auth_bad}}` emits malformed `BADSIG.BADSIG.BADSIG` | Not faithful; Tier B runner change required. |
| Wrong audience | No constrained built-in/profile | Tier B runner change required. |
| Stale `iat` | `{{auth_expired}}` sets stale `iat` and expired `exp` together | Does not isolate freshness; Tier B required. |
| Header omission | Author a request without the header | Tier A. |
| Valid-JSON schema failure | Dictionary body with missing/wrong fields | Tier A. |
| Destination header/body mismatch | Literal wrong header with valid body | Tier A. |
| Identical replay | Ordered requests can share an authored tenant variable, but `{{msgId}}` is fresh per request | Tier A only after a runner-owned shared group variable or safely generated run variable is defined; do not depend on tenant-controlled security-negative data. |
| Conflicting replay | Same requirement as identical replay plus changed content | Same gating as above; state assertion may require approved test-state evidence. |
| Source IP in `17/8` | Runner originates outside Apple | Not Phase 1; route B.14 to deployed-edge/security evidence. |
| Stored/queued result | Immediate response only | Not proved without an approved assertion surface. |

## Atomic request matrix

| ID | Request condition | Expected observation | Tier | Primary item |
|---|---|---|---|---|
| V0 | Valid JWT, all required headers, valid matching body, fresh unique ID | documented 2xx | A | B.13 |
| V1 | Authorization omitted; remaining request otherwise valid | 401 | A | B.13 |
| V2 | Structurally valid current HS256 signed with runner-owned wrong secret | 403 | B | B.9/B.13 |
| V3 | Correct signature, wrong `aud`, current `iat` | 403 | B | B.9/B.13 |
| V4a | Correct token just inside freshness boundary, valid `exp` | accepted authentication path | B | B.9 |
| V4b | Correct token at defined boundary under frozen clock | owner-approved exact expectation | B | B.9 |
| V4c | Correct token just outside freshness boundary, valid `exp` | 403 | B | B.9/B.13 |
| V4d | Correct token with future `iat`, valid `exp` | 403 | B | B.9 |
| V5-* | Omit `id`, `source-id`, `destination-id`, `capability-list`, and any other canonical required header one at a time | documented rejection per header | A | B.13 |
| V6 | Valid JWT/headers; syntactically valid JSON missing required envelope fields | 400 | A | B.13 |
| V7 | Valid JWT/body; Destination-Id header differs from body `destinationId` | 400 | A | B.13 |
| V8a | First valid delivery of replay ID | documented 2xx and one processing effect if observable | A+state | B.13 |
| V8b | Byte-identical replay of V8a | acknowledge without a second processing effect | A+state | B.13 |
| V8c | Same ID as V8a with different content | reject; original remains unchanged | A+state | B.13 |

`capability-list` is included because canonical B.13 treats it as required. Content-Type handling may
be its own case if the target/server framework normalizes it differently; the expected response must
come from the authoritative checklist/developer kit, not from Redo's implementation.

## Order assertions

Independent rejection cases prove coverage, not necessarily order. Add dominance cases only when
the earlier/later outcomes are distinguishable:

| Combined invalidities | Expected result | Supported inference |
|---|---|---|
| Missing Authorization + invalid schema | 401 | Authorization check precedes schema. |
| Bad JWT + invalid schema | 403 | JWT validation precedes schema. |
| Invalid schema + destination mismatch | Both currently map to 400 | No order inference unless stable safe error codes distinguish them. |

Do not claim “only then parsed and queued” from a 200 response. Queue/storage needs a tenant-isolated
read-only assertion endpoint, datastore evidence or separate trusted evidence. If unavailable, the
result says “accepted by endpoint.”

## Source-IP prerequisite

A normal Verifier request cannot present a trustworthy Apple source address. `X-Forwarded-For` is
not evidence because a secure edge should replace or reject untrusted forwarding data.

Phase 1 therefore uses this rule:

1. Run an ingress preflight.
2. If the non-Apple runner is blocked and no approved test exception exists, mark downstream checks
   `could_not_run` with prerequisite `apple_source_or_approved_test_ingress`.
3. If a documented staging-only Verifier ingress exception exists, run V0–V8 while retaining JWT
   and all other validation.
4. Evaluate B.14 independently through WAF/load-balancer configuration and trusted allowed/denied
   runtime evidence. Never award B.14 from a spoofed header.

## Runner improvements

1. Add a typed, constrained JWT profile with runner-owned wrong key, wrong audience, missing/future/
   offset `iat`, wrong algorithm and frozen-clock evidence.
2. Add a runner-owned per-check shared UUID variable for replay groups. It must be generated by
   Verifier, stable across the group's requests and unavailable for tenant shadowing.
3. Add stable safe error-code assertions if MSP responses expose them; otherwise limit order claims.
4. Add an optional approved state-assertion adapter for “processed once/original retained.” A 2xx
   response alone never satisfies those assertions.
5. Add ingress-prerequisite/could-not-run classification before downstream B.9/B.13 probes.
6. Golden-test exact wire bytes, omitted headers, JWT claims/signature profile, response assertions,
   redaction and replay-group identity.

## Acceptance criteria

- Every case is bound to B.9, B.13 or B.14 as specified; no new checklist item is invented.
- Tier A cases run with the historical Phase 1 wire contract unchanged.
- Tier B cases cannot import as executable until schema/runner/golden tests land.
- A malformed JWT cannot pass as wrong-secret evidence.
- A combined stale-`iat`/expired-`exp` token cannot pass as isolated freshness evidence.
- Destination mismatch does not replace replay protection.
- B.14 is never inferred from caller-controlled forwarding headers.
- A blocked runner produces `could_not_run`, not an MSP failure.
- Stored/queued and duplicate-processing claims require an approved state assertion.

