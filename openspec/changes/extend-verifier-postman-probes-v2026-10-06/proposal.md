# Proposal: extend Verifier Postman probes from MSP checklist v2026.10.06

## Status

Planning only. This refresh does not modify Verifier, the approved checklist, a tenant, staging, or
production. Implementation requires review of the design, specifications, tasks, and the Phase 2
ADR described below.

## Authority pin

| Artifact | Pin |
|---|---|
| Checklist | `msp-conformance/v2026.10.06`, approved 2026-10-08, 100 items |
| Checklist SHA-256 | `a16748f0fb6dab0a4ede7da733f49361b4c9b651c21318ddc2a205b02ac462d1` |
| Verifier bundle SHA-256 | `1fe897c6babee124c86c8b3f2d63f75b5c4e28daf20352a305f2abb54b3d5aec` |
| AMB-canonical revision | `84322f2e259d21cdb261da1db98465c8a71fa7a8` |
| Verifier Stage baseline | `5876b014572f1cd404d861b66f37db17d97be33f` |

The approved 10.06 bundle contains 24 request definitions bound to 14 existing checklist items. It
inherits the probe content from 9.28 and adds checklist item B.16. This proposal expands scenario
coverage in a successor bundle; it never edits 10.06 in place.

## Problem

The existing probes predominantly prove that the MSP inbound webhook accepts or rejects individual
Apple-shaped requests. Important negative, boundary, state-transition, and outbound behaviors remain
untested. In particular, there is no complete automated family for broken attachment download,
encryption, upload, checksum, timeout, or actionable-error behavior.

The original probe system intentionally chose an inbound-only direction. That safely covers calls
from Verifier to the MSP but cannot establish behavior where the MSP must call an Apple endpoint or
where a result is visible only on a device, in an agent console, in deployed infrastructure, or in
an external system.

## Decisions

### Code remains separate

Code analysis and Postman/probe execution remain independent evidence paths. This change adds no
code-analysis criterion, prompt, verdict, or automatic checklist credit. A probe result cannot
claim that every implementation path is correct, and code analysis cannot claim that a request ran.

### Three execution phases mean direction, not certification maturity

1. **Phase 1 — Verifier to MSP:** Verifier sends Apple-shaped requests to the MSP's configured
   inbound endpoint and observes the immediate response plus only explicitly exposed test-state
   assertions.
2. **Phase 2 — MSP to Verifier, if possible:** a controlled Verifier capture service emulates only
   the minimum Apple gateway/content endpoints needed for the scenario. The MSP is explicitly
   configured for the test environment to call those endpoints. Verifier records request shape,
   order, timestamps, retry behavior, and injected responses. Phase 2 requires a superseding ADR;
   the accepted 2026-07-24 ADR currently permits inbound-only probes.
3. **Phase 3 — other evidence:** use live Apple integration, device/UX review, deployed-configuration
   evidence, security/crypto execution, or human confirmation when neither direction can establish
   the checklist obligation safely.

“If possible” is a hard safety gate. Phase 2 must not use DNS interception, production traffic,
unapproved proxying, or a mechanism that weakens endpoint validation. If the MSP cannot safely
override an Apple endpoint in a disposable test environment, the scenario routes to Phase 3.

### Every new probe belongs to an existing checklist item

The proposal registry for every new check revision must declare:

- a stable check identity and immutable revision;
- exactly one primary `item_code` and UID from checklist v2026.10.06;
- optional secondary existing item bindings only where the same retained exchange independently
  supports both requirements;
- phase/direction and prerequisites;
- the exact observable assertion;
- what the check cannot prove; and
- pass, assertion-fail, could-not-run, and redaction fixtures.

Verifier's current bundle does not import checklist UIDs or a `phase` field. Therefore the UID,
phase and assertion map remain reviewed proposal/build provenance; the generated bundle uses only
its supported fields. The check's `checklist_item_codes` is reference data, while the existing
item's `check_bindings` is the executable association. Validation must reject an unknown item code,
an executable new check with no item binding, or a binding whose method/bucket cannot exercise it.
New checklist items are out of scope.

### Probe naming and checklist visibility

Every newly authored probe MUST expose its primary checklist item in its human-readable name:

`<suite or campaign> · <primary item code> · <specific scenario>`

For example, `NCT staging 20260911 · B.1 · valid inbound message`. A name ending only in `B.1`
is insufficient because one checklist item can require multiple independently reportable scenarios.
For I.5, use names such as `NCT staging 20260911 · I.5 · attachment size boundary` and
`NCT staging 20260911 · I.5 · interactiveDataRef decode chain`.

The visible code is navigation, not authority. The check MUST also list the primary item in
`checklist_item_codes`, the item MUST name the check through `check_bindings`, and build provenance
MUST retain the pinned checklist version and stable UID. Where one observation supports secondary
items, only the primary code appears in the name; secondary codes remain explicit in reference and
binding/assertion maps.

Existing probe names are global natural keys. Renaming an existing probe through ordinary bundle
upsert would create a new identity and can strand bindings or revision history. Any retrofit of the
convention to existing `NCT staging 20260911` probes therefore requires an explicit old-to-new
migration that preserves definition IDs/revisions and updates every bundle binding atomically, or a
separate display-name field approved through its own design change.

## Compatibility with the current Verifier probe engine

Compatibility is split deliberately:

| Capability | Current Stage support | Proposal rule |
|---|---|---|
| Check payload | `name`, `layer`, `sort_order`, `checklist_item_codes`, `requests`, `prompt`, `conversation_group`, `group_position`, `not_asserted` | Phase 1 bundles use only these fields; unknown metadata is forbidden |
| Request | method, relative path, string headers, dictionary body, typed `expected`, label | Every Phase 1 request must validate through the existing `CheckRequest` schema |
| Response assertions | status, latency, content type, JSON-field presence, body contains/not-contains | Do not encode persistence, outbound capture, ordering or UX as an `expected` assertion |
| Target | tenant `base_url` plus relative path | Existing runner is Phase 1 only |
| Authentication | current, malformed-bad, combined stale-`iat`/expired-`exp`, or absent inbound JWT built-ins | A correctly structured JWT signed with a wrong secret, isolated wrong audience, isolated stale/future/missing `iat`, and algorithm variants require an additive runner change |
| Body encoding | JSON dictionary; optional valid gzip | Raw malformed JSON, JSON `null`, truncated/corrupt gzip and arbitrary bytes require an additive raw-body test mode |
| Conversation sequencing | `conversation_group` and `group_position` | May order inbound requests but does not itself assert resulting state |
| Execution eligibility | effective item reaches `postman` and is not bucket `code`; current imported API items execute bindings | Do not attach an executable request to a code/manual item and imply it will run |
| Direction | inbound-only ADR, MSP `base_url` | Phase 2 is design-only until the ADR, schema, planner and runner change |

The current check named `Malformed JSON body` stores `{"__raw__": "{ this is not json "}`. Stage
contains no `__raw__` serialization branch, so the runner emits a valid JSON object rather than raw
malformed JSON. The refreshed work must first classify that existing result as a coverage defect;
it must not copy the pattern into new checks or claim malformed-JSON coverage.

Only the Phase 1 subset that fits these contracts may be authored/imported before runner changes.
Phase 2 definitions and Phase 1 raw-body/JWT-boundary cases remain design records, not bundle
content, until their enabling code and tests exist.

## Proposed scenario register

This is the initial v10.06 register. Individual atomic requests may be grouped only when they prove
one state transition; independent failures remain separate checks.

### Phase 1 — Verifier to MSP

| Existing item | UID | Proposed scenario family | Assertion boundary |
|---|---|---|---|
| B.2 | MSPR-0008 | text, interactive, typing, close and attachment envelopes | MSP inbound endpoint accepts supported envelope classes; downstream rendering is not proved |
| B.9 | MSPR-0015 | valid JWT, structurally valid HS256 signed with a runner-owned wrong secret, wrong audience, and isolated just-inside/at/just-outside `iat` freshness boundary | inbound authentication decision only; current `auth_bad` and `auth_expired` do not faithfully isolate these cases |
| B.12 | MSPR-0018 | valid gzip, corrupt gzip, valid gzip with invalid JSON, JSON `null`, missing envelope `v` | decompression/parsing response only |
| B.13 | MSPR-0019 | valid control; missing Authorization; bad signature; wrong audience; stale `iat`; each other required header omitted independently; structurally invalid valid JSON; Destination-Id/body mismatch; identical replay; conflicting replay | individual validation outcomes and replay decision at the endpoint; internal order is asserted only where overlapping-invalidity probes produce distinguishable responses |
| C.1 | MSPR-0022 | inbound international Unicode and emoji | inbound preservation to the observable MSP assertion surface |
| C.3 | MSPR-0024 | all standard Tapbacks, interactive reaction, sticker/emoji reaction, unsupported variant | accepted/preserved inbound behavior; agent rendering remains Phase 3 |
| C.4 | MSPR-0025 | close event ingestion followed by a Verifier-triggered ordinary inbound event | close-state acceptance; proving no outbound send requires Phase 2 |
| C.8 | MSPR-0029 | time-picker selections with timezone/location/slot variants | inbound selection handling only |
| C.10 | MSPR-0031 | authentication success, failure, cancel, unknown, invalid and expired responses | inbound response-state handling only |
| C.12 | MSPR-0033 | valid and malformed form submissions, optional controls and review/summary data | inbound form processing only |
| C.22 | MSPR-0042 | empty/minimal/full/garbage capability lists and successive changes | current capability state if an approved assertion surface exists |
| C.23 | MSPR-0043 | accepted, declined, opt-out and undeliverable Invitation events | observed state transition; no-response requires time/control evidence |
| D.1 | MSPR-0054 | successive capability values for two destinations | replacement and per-destination isolation if observable |
| E.5 | MSPR-0064 | STOP/UNSUBSCRIBE/SPAM/END/QUIT case variants | inbound trigger acceptance; full send suppression requires Phase 2 |
| H.1 | MSPR-0084 | requests eliciting documented response families | MSP endpoint response taxonomy only |

### Phase 2 — MSP to Verifier capture, if safely configurable

| Existing item | UID | Proposed scenario family | Assertion boundary |
|---|---|---|---|
| B.1 | MSPR-0007 | captured outbound `/message` request, required headers/body and retry response injection | exact emitted request and observed retry behavior |
| B.3 | MSPR-0009 | inbound attachment reference followed by captured `/preDownload`, content download and failure injection | request shape and resulting state; live Apple authorization is not proved |
| B.4 | MSPR-0010 | captured `/preUpload` with encrypted-size boundary and malformed/error responses | emitted request and local/error behavior |
| B.5 | MSPR-0011 | upload URL success, expiry, reuse, partial/4xx/5xx, timeout, missing/bad checksum; assert `/message` is blocked on failure | upload ordering, checksum use and send suppression |
| B.6 | MSPR-0012 | `interactiveDataRef` over threshold through preDownload, download/decrypt and captured `/decodePayload`; inject each stage failure | complete observable call chain in the controlled environment |
| B.7 | MSPR-0013 | captured `/authenticate` payload and response-state cases | emitted request; live OAuth/device flow remains Phase 3 |
| B.8 | MSPR-0014 | captured `/constructPayload` for App Clip, Maps and Music with locale/storefront variants | endpoint use and inputs; Apple-rendered payload remains Phase 3 |
| B.16 | MSPR-0113 | captured Invitation payload including `brandLogo` | outbound payload only; supported-device delivery is Phase 3 |
| C.1 | MSPR-0022 | captured outbound Unicode/emoji from bot and agent paths | transport bytes, not every renderer |
| C.4 | MSPR-0025 | after close, attempt ordinary message and Invitation; capture must remain empty | outbound suppression in the exercised paths |
| C.5 | MSPR-0026 | captured Rich Link request and fallback | wire shape and selected fallback |
| C.6 | MSPR-0027 | captured Quick Reply for bounded yes/no and expected-answer prompts | payload/options; device presentation remains Phase 3 |
| C.7 | MSPR-0028 | captured single/multi-select, multi-section, icon and image List Pickers | outbound matrix and wire shape |
| C.8 | MSPR-0029 | captured outbound Time Picker with required fields | outbound construction and ordering |
| C.9 | MSPR-0030 | captured Apple Pay payload and failure handling | request construction; payment sheet/device completion remains Phase 3 |
| C.10 | MSPR-0031 | captured current OAuth payload, Password AutoFill fields and invalid/expired handling | outbound construction and response behavior |
| C.11 | MSPR-0032 | captured CustomInteractiveData with approved-test `bid` supplied as runtime evidence | wire shape; Apple approval remains Phase 3 |
| C.12 | MSPR-0033 | captured Form controls, summary/review placement and capability fallback | outbound/fallback behavior |
| C.16 | MSPR-0037 | timestamped typing indicator then payload, consecutive payloads and prohibited send | ordering, delay tolerance and per-payload repetition |
| C.23 | MSPR-0043 | Invitation sends across consent/state outcomes | emitted or suppressed request for each state |
| C.27 | MSPR-0048 | paced batch, cancellation, opt-out during queue, retry and audit correlation | exercised campaign behavior only |
| E.5 | MSPR-0064 | after each opt-out trigger, attempt bot, agent, campaign, retry, replay, scheduled and automation sends | brand-wide suppression for every exercised path |
| H.1 | MSPR-0084 | capture service injects response families; observe retries and final classification | response handling and retry policy |
| I.5 | MSPR-0092 | attachment sizes 99,999,999/100,000,000/100,000,001 bytes plus an Apple-style `interactiveDataRef` chain above 10 KB | strict attachment acceptance/rejection and absence/presence of outbound request; successful reference decoding without treating 10 KB as a rejection cap |

### Phase 1 B.9/B.13 ordered-validation family

The Redo evidence identifies a useful rejection sequence, but it must be translated without
overclaiming. Phase 1 MUST cover the following as separate atomic observations:

1. valid signed control with matching headers/body;
2. Authorization omitted;
3. structurally valid HS256 JWT signed with a runner-owned wrong secret;
4. correctly signed JWT with a wrong audience;
5. correctly signed JWT with isolated stale `iat` while `exp` remains valid;
6. each required non-Authorization header omitted independently, including `capability-list`;
7. structurally invalid but syntactically valid JSON envelope;
8. `Destination-Id` header/body mismatch;
9. first delivery, byte-identical replay and same-ID/different-content replay.

The current runner can execute the valid control, Authorization omission, ordinary header omission,
valid-JSON schema failure and Destination-Id mismatch as Tier A. It cannot faithfully execute cases
3–5: `auth_bad` is a malformed token rather than a valid HS256 token signed with a wrong key, and
`auth_expired` changes both `iat` and `exp`. Those cases remain Tier B until the typed JWT profile
lands.

This family does not turn Redo's Destination-Id comparison into the canonical fifth B.13 step. The
comparison is an additional consistency check; canonical B.13 still requires ID uniqueness/replay
protection. A 200 response also does not prove “stored/queued” without an approved tenant-isolated
assertion surface.

The Source-IP check is not a Phase 1 B.13 request. Verifier does not originate from Apple's
`17.0.0.0/8`, and setting `X-Forwarded-For` would be spoofing rather than proof. B.14 remains Phase 3
deployed-edge evidence. If the target correctly blocks Verifier at the edge, the Phase 1 run MUST
return `could_not_run` unless a documented test-only ingress exception exists; it MUST NOT record
tenant failure or silently treat a spoofed header as success.

### Phase 3 — other evidence

| Existing item(s) | Why Phase 1/2 is insufficient | Required route |
|---|---|---|
| B.3–B.6, I.2, I.5 | controlled capture cannot prove interoperability with Apple's real short-lived URLs, encryption material or gateway | live Apple test plus crypto known-answer/negative tests where applicable |
| B.14 | source-IP restriction is deployed ingress behavior and Verifier is not Apple-origin traffic | deployed configuration/approved exception and security review |
| B.16 | brandLogo must arrive and render on a supported device | live Invitation plus device evidence |
| C.2 | actionable agent error categories and safe recovery copy are UX obligations | controlled failures plus agent-console UX review |
| C.3, C.5–C.12 | actual device rendering/interaction is not established by captured JSON | device/UX review |
| C.23 | true no-response passage and Apple delivery/undeliverable semantics may not be reproducible locally | live Apple or trusted attestation |
| I.2 | encryption posture cannot be established by a captured opaque blob alone | security review and executed crypto evidence |
| Apple approval/policy/meeting items | no HTTP exchange can prove approval or policy practice | Apple/MA/human evidence |

## Broken-attachment minimum matrix

The successor proposal is incomplete unless it includes all of the following, bound to existing
items only:

| Case | Primary item | Secondary observation |
|---|---|---|
| Missing/invalid preDownload metadata or signature | B.3 | C.2 error category where visible |
| preDownload rejection, timeout, malformed response or expired URL | B.3 | C.2 |
| truncated/corrupt ciphertext, wrong key or invalid key length | B.3 | I.2 and C.2 where independently asserted |
| missing MIME type with valid filename fallback | B.3 | C.2 only if an error is surfaced |
| plaintext-size/encrypted-size confusion | B.4 | I.5 |
| just below/at/above authoritative attachment limit | I.5 | B.4 and C.2 where independently asserted |
| upload URL expired, reused, partial, rejected or timed out | B.5 | C.2 |
| checksum absent or invalid | B.5 | C.2 |
| any upload failure followed by `/message` emission | B.5, expected negative assertion | C.2 |
| actionable size/type/crypto/network/upstream agent error with no secret leakage | C.2 | I.2/I.5 only for their exact independently observed facts |

One execution may retain evidence relevant to multiple items, but each assertion and binding remains
explicit. A B.3 exchange must not silently make C.2 or I.2 pass.

## Success criteria

- Every new check is bound to an existing v2026.10.06 item/UID and names its assertion boundary.
- No approved 10.06 artifact is mutated or re-scored.
- Code and Postman evidence remain separate.
- Phase 1 remains safe inbound execution.
- Phase 2 cannot run until a superseding ADR and capture-security gates are approved.
- Phase 3 remains visible rather than being converted into a false automated pass.
- Broken attachment failures are diagnosable by exact stage and do not leak secrets.
- Automated observations remain evidence for human review and do not automatically change progress.

