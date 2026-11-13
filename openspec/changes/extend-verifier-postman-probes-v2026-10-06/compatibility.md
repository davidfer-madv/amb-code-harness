# Compatibility assessment: current Verifier Stage

## Result

The proposal is compatible only when delivered in tiers. Phase 1 Tier A checks can use the current
bundle and runner contracts. Tier B scenarios need additive inbound-runner features. Phase 2 needs a
new capture subsystem and a superseding ADR. Phase 3 is not probe execution.

## Current contracts that must not be bypassed

| Contract | Current behavior | Consequence |
|---|---|---|
| `BundleCheck.extra` | unknown keys forbidden | no `phase`, UID or custom assertion keys in current bundles |
| `CheckRequest.body` | JSON dictionary | no native JSON null/scalar or arbitrary/raw bytes |
| gzip | runner compresses the generated JSON when `expected.compress=true` | valid gzip only; corrupt gzip is not currently expressible |
| URL | `tenant.base_url + relative path` | current runner is Verifier-to-MSP only |
| expected response | status, latency, content type, JSON field presence, body contains/not contains | no persistence, callback-capture, ordering or “nothing emitted” assertion |
| built-ins | `jwt`, `msgId`, `businessId`, `appleUserId`, `auth_none`, `auth_bad`, `auth_expired` | `auth_bad` is malformed, not a valid wrong-secret HS256 token; `auth_expired` changes both `iat` and `exp`; exact wrong-secret/audience/time/algorithm cases need typed runner support |
| sequencing | conversation group + position | orders requests; does not prove state by itself |
| association | item `check_bindings` | check `checklist_item_codes` is reference-only |
| eligibility | Postman method plus planner bucket guard | `code` items are deliberately skipped by HTTP execution; `manual_postman` is not automated |
| check size | at most 50 requests | large matrices must be split into cohesive atomic families |

## Existing coverage defect discovered

`NCT staging 20260911 · Malformed JSON body` carries:

```json
{"body": {"__raw__": "{ this is not json "}}
```

No Stage runner code interprets `__raw__`. It serializes the dictionary normally and sends valid
JSON. The check therefore does not exercise malformed JSON. It should be corrected only after a
typed raw-body mode is designed, implemented and tested; until then its observed result must not be
used as malformed-JSON evidence.

## Compatibility acceptance tests

1. Parse the successor bundle with the exact Stage `ChecklistBundle` model.
2. Round-trip import/export and confirm check requests, labels, group metadata, `not_asserted`, and
   item bindings are unchanged.
3. Resolve the effective tenant checklist and prove every intended Tier A check appears exactly once
   in the run plan.
4. Execute through the real runner with a local capture target and compare method, URL, headers,
   decoded body bytes and compression against golden fixtures.
5. Prove unresolved variables, missing tenant identity, bad credentials and runner failures yield
   `error`/`could_not_run`, not tenant failure.
6. Prove code and manual-Postman items are not accidentally sent by the HTTP runner.
7. Prove a check containing any unsupported key, expected criterion or body mode is rejected before
   import.
8. Preserve existing 24 checks and their histories; append new identities/revisions only.
9. Golden-capture the B.13 Tier A family and prove the wire request really omits the selected header,
   carries a valid signed control, sends the intended schema defect, and creates the literal
   Destination-Id/body mismatch.
10. Prove a blocked source-IP preflight becomes `could_not_run`, not tenant failure, and prove no
    bundle check claims B.14 from an `X-Forwarded-For` value supplied by Verifier.
