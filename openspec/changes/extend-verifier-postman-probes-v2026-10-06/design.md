# Design: directional Postman probe expansion for v2026.10.06

## Architecture

```text
Phase 1: Verifier runner  ----Apple-shaped inbound----> MSP webhook

Phase 2: MSP test deployment ----Apple-bound request----> Verifier capture/emulator
          Verifier trigger      ----inbound setup-------> MSP webhook

Phase 3: live Apple / device / UX / deployed config / security / human evidence
```

The three phases classify the direction and evidence surface. They do not represent automatic
certification levels.

## Phase 1 contract

Phase 1 retains the accepted inbound-probe model. A request targets the configured tenant base URL,
uses Apple-to-MSP authentication/envelope semantics, and evaluates an immediate response matcher.
State assertions are allowed only through an approved tenant-isolated test assertion interface;
response `2xx` alone must never be interpreted as proof of downstream state.

## Phase 2 contract

Phase 2 is disabled by default and requires a superseding ADR for
`2026-07-24-inbound-probe-direction`.

Required controls:

1. Disposable test environment and explicit per-run endpoint override; never production.
2. Capture URLs owned by Verifier and scoped to one tenant/run with unguessable correlation IDs.
3. TLS validation remains enabled; no DNS poisoning or certificate bypass.
4. Strict endpoint allow-list, SSRF protection, redirect refusal, request/body size limits and
   egress timeouts.
5. Secrets and authorization material redacted before storage; raw attachment bytes retained only
   when explicitly required, encrypted, size-limited and automatically expired.
6. Scripted response injection for success, 4xx, 5xx, timeout, malformed response and partial
   transfer, with every injected behavior stamped in the result.
7. Timestamped ordered capture and a negative assertion window for “nothing was emitted.”
8. Resume/retry fencing so stale workers cannot contaminate a later run.
9. A capability handshake proving the MSP actually applied the test endpoint configuration.
10. Automatic fallback to Phase 3—not a failure—when safe endpoint override is unavailable.

The emulator implements only the behavior needed for a named check. It must not be described as an
Apple-compatible gateway or used to infer production interoperability.

## Check identity and bindings

Current Verifier bundle compatibility takes precedence. A Phase 1 check uses the existing
`BundleCheck` shape; it does not add `phase`, `primary_item`, `assertions`, UID, or another unknown
field because `extra="forbid"` correctly rejects them:

```json
{
  "name": "NCT staging 20260911 · B.13 · replayed inbound message id",
  "layer": "apple",
  "sort_order": 100,
  "checklist_item_codes": ["B.13"],
  "requests": [
    {
      "method": "POST",
      "path": "/message",
      "headers": {"Authorization": "Bearer {{jwt}}", "id": "{{replayId}}"},
      "body": {"v": 1, "id": "{{replayId}}"},
      "expected": {"status_codes": [200, 400, 409]},
      "label": "first/replayed pair is completed by the authored request list"
    }
  ],
  "prompt": "",
  "conversation_group": "b13-replay",
  "group_position": 0,
  "not_asserted": "Does not prove every producer path or durable replay retention."
}
```

The reviewed proposal/build manifest separately records phase, primary UID, secondary assertion
maps and prerequisites. `checklist_item_codes` helps readers but never creates a binding. The
existing checklist item explicitly names the check in `check_bindings`; only such a binding is
executable.

New probe names follow `<suite or campaign> · <primary item code> · <specific scenario>`. The
scenario segment is mandatory because item code alone is not unique enough for a multi-probe
requirement. A visible item code never replaces `checklist_item_codes`, `check_bindings`, pinned
checklist provenance or stable UID. Because the current name is a global natural key, existing
names may be retrofitted only through an identity-preserving migration or a separately designed
display-name field, not by importing a renamed check as if it were the same definition.

The example above is illustrative and incomplete as an executable replay family: it needs two
ordered requests sharing `{{replayId}}` and item-specific expected results. The builder, schema and
runner—not prompt prose—must validate the final request list.

Secondary bindings require their own assertion mapping in the reviewed manifest. Shared traffic is
an optimization; it is not shared verdict semantics.

## Compatibility tiers

### Tier A — importable and executable with current Stage

- ordinary JSON dictionary bodies;
- valid gzip through `expected.compress`;
- relative requests to the configured MSP `base_url`;
- supported header/body variables;
- immediate response assertions from `ExpectedCriteria`;
- ordered inbound request groups; and
- bindings on currently executable API/Postman items.

For the B.13 validation family, Tier A includes a valid control, omission of Authorization through
`{{auth_none}}`, omission of each other authored header, structurally invalid dictionary envelopes,
literal Destination-Id/body mismatch, and immediate status/body assertions. These checks validate
observable outcomes, not internal handler order or persistence.

### Tier B — requires additive Phase 1 runner support

- raw malformed JSON, JSON scalar/null or arbitrary bytes;
- deliberately corrupt/truncated gzip;
- configurable JWT audience and exact iat/expiry offsets;
- durable state assertions beyond the immediate HTTP response; and
- assertion of emitted or suppressed outbound traffic.

For B.9/B.13, Tier B specifically includes a syntactically and structurally valid HS256 token signed
with a runner-owned wrong key, correctly signed wrong-audience tokens, isolated missing/stale/future
`iat`, wrong-algorithm tokens, and frozen-clock freshness boundaries. The legacy `auth_bad` token is
malformed and MUST NOT be labelled “wrong signing secret”; legacy `auth_expired` changes both `iat`
and `exp` and MUST NOT be labelled an isolated `iat` test.

### Tier C — requires Phase 2 subsystem

- an MSP-to-Verifier target/capture identity separate from tenant `base_url`;
- capture listener and injected Apple/content responses;
- timestamp/order/negative-window assertions;
- safe attachment byte fixtures and fault injection; and
- planner/result semantics for conditional capture capability.

Tier B/C checks must not be placed into a bundle that current Stage can import as if it could
execute them faithfully.

## Validation order and ingress boundary

Phase 1 may infer precedence only by combining two invalid conditions whose documented responses
are distinguishable. For example, missing Authorization plus invalid schema returning 401 supports
authentication-before-schema. It cannot infer schema-before-destination when both failures return an
undifferentiated 400. If the MSP exposes stable safe error codes, those codes may be added as typed
body assertions; otherwise the result records the two independent rejection outcomes and leaves
internal order unconfirmed.

Source-IP enforcement is outside this executor's proof boundary. A Phase 1 runner outside
`17.0.0.0/8` cannot both prove B.14 enforcement and exercise downstream validation on the same
production endpoint. The allowed routes are: an owner-approved test-only ingress exception with JWT
and all other validation retained, or Phase 3 deployed-edge evidence. Supplying an
`X-Forwarded-For: 17.x` header is never accepted as B.14 evidence.

## Result states

- `passed_observation`: every declared assertion matched.
- `failed_observation`: an MSP-attributable assertion did not match.
- `could_not_run`: configuration, capture, network, emulator or runner failure prevented assessment.
- `needs_phase_3`: the required behavior is not safely observable through Phase 1 or 2.
- `needs_rerun`: evidence no longer matches the pinned target/revision.

Skipped, malformed, unbound or partially executed checks never pass.

## Versioning

The proposal starts from approved `v2026.10.06` but produces a new owner-reviewed bundle version.
It does not change requirement text, UID, verification expression or checkpoint placement. The new
bundle records check additions/bindings and a migration map from 10.06. Tenant adoption is explicit.

The implementation sequence, data model, capture lease, security controls and test gates are in
`runner-implementation-plan.md`.

