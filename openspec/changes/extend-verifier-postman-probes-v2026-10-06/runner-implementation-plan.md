# Runner implementation plan: Tier B and Phase 2 capture

## Scope

This plan covers two distinct extensions:

1. **Tier B:** safely add raw-body and controlled JWT variants to the existing Verifier-to-MSP
   runner.
2. **Phase 2:** add an MSP-to-Verifier scenario/capture subsystem for MSPs that can safely direct a
   disposable test deployment to Verifier-owned Apple-emulator endpoints.

Neither extension changes Code analysis or grants automatic checklist credit.

## Architecture decision

Keep the current inbound function as one executor:

```text
InboundHttpExecutor
  Verifier -> tenant.base_url + relative path
```

Add Phase 2 as a different executor and orchestrator:

```text
OutboundCaptureScenarioExecutor
  1. create short-lived capture lease
  2. arm scripted capture endpoints/responses
  3. trigger disposable MSP test behavior
  4. receive MSP -> Verifier capture events
  5. wait for success/failure/negative assertion window
  6. evaluate ordered events deterministically
  7. store one scenario result plus retained capture-event evidence
```

Do not reinterpret tenant `base_url`; it remains the MSP inbound webhook. Do not mint Apple-inbound
JWTs for MSP-to-Verifier calls. Do not make a relative check path mean two directions.

## 1. Preserve existing execution as a compatibility adapter

Refactor without behavior changes:

- retain `backend/app/services/probe_execution/runner.py::execute_probe` as the Phase 1 behavior;
- introduce an executor protocol whose current adapter calls `execute_probe` unchanged;
- dispatch by a runner-owned execution mode that defaults to `inbound_http` for every historical
  revision;
- freeze golden tests for URL construction, variables, JWTs, gzip, redaction, timeout, one retry,
  expected matchers and error codes before adding another mode.

Historical revisions and results require no rewrite.

## 2. Tier B: typed raw-body and JWT profiles

### Request-body contract

Replace the implicit dictionary-only body with a backward-compatible discriminated input. Existing
`body: {...}` remains JSON mode. New modes are explicit; never use a magic `__raw__` dictionary key.

Logical shape:

```json
{
  "body_mode": "json_object|json_value|raw_utf8|raw_base64",
  "body": {},
  "raw_body": null,
  "content_encoding_mode": "none|gzip_valid|gzip_corrupt|gzip_truncated"
}
```

Validation rules:

- exactly one body representation;
- `raw_base64` decodes under a strict byte ceiling;
- corrupt/truncated gzip can be generated only from bounded runner-owned transformations;
- headers remain author-controlled but `Content-Encoding` is reconciled with the selected mode;
- transmitted bytes are hashed and safely previewed; arbitrary binary is never decoded into logs;
- current JSON-object serialization stays byte-compatible for historical checks.

This fixes the existing false malformed-JSON check by making raw bytes a typed capability.

### JWT profile contract

Add a constrained `auth_profile`; do not allow arbitrary signing code or arbitrary secret material
in bundle content:

```json
{
  "auth_profile": {
    "kind": "current|missing|claims",
    "signing_key": "configured|runner_wrong",
    "algorithm": "HS256|HS384",
    "audience": "configured|wrong",
    "iat_mode": "present|missing",
    "iat_offset_seconds": 0,
    "exp_offset_seconds": 3600
  }
}
```

Server validation caps offsets to an approved test range, derives `runner_wrong` from a fixed
runner-owned test value that can never equal tenant configuration, and keeps the server as the only
signer. Existing `{{jwt}}`, `{{auth_none}}`, `{{auth_bad}}`, and `{{auth_expired}}` continue to work
for backward compatibility, but their labels remain exact: `auth_bad` is malformed and
`auth_expired` combines stale `iat` with expired `exp`. Exact boundary tests use the typed profile,
a frozen runner clock, and record effective non-secret header/claims in redacted evidence.

The B.9/B.13 acceptance set MUST prove that profiles can independently create:

- current valid HS256;
- current HS256 signed with the runner-owned wrong key;
- current correctly signed HS256 with wrong audience;
- current correctly signed token with missing `iat`;
- correctly signed HS256 with just-inside/at/just-outside and future `iat` while `exp` stays valid;
- correctly signed HS384 for algorithm-pinning rejection; and
- missing Authorization without constructing a token.

No tenant-provided probe variable may supply these security-negative tokens or shadow their profile.

### Files affected

- `backend/app/schemas/probe.py`: typed body/auth profile and strict mutual-exclusion validation.
- `backend/app/services/probe_execution/runner.py`: byte builder and JWT-profile builder.
- `backend/app/services/probe/service.py`: canonical identity includes the new typed fields.
- `backend/app/schemas/checklist.py`: bundle import/export supports the additive fields.
- probe editor/frontend types: explicit body mode; no free-form magic keys.
- tests: schema, canonicalization, import/export, exact wire bytes, redaction and legacy fixtures.

## 3. Phase 2 data contract

Add an immutable scenario specification to a check revision only after the Phase 2 schema is
deployed. Existing revisions default to `inbound_http`.

```json
{
  "execution_mode": "outbound_capture",
  "capture_scenario": {
    "trigger": {
      "kind": "inbound_request|approved_test_hook|manual_arm",
      "reference": "typed trigger definition"
    },
    "steps": [
      {
        "endpoint": "preUpload|upload|preDownload|download|decodePayload|authenticate|constructPayload|message",
        "response_script": "approved immutable script id",
        "assertions": "typed request/capture assertions"
      }
    ],
    "timeout_ms": 30000,
    "negative_window_ms": 5000
  }
}
```

Bundle authors select approved script IDs and typed arguments. They cannot provide executable code,
arbitrary callback URLs or unrestricted response bodies.

Recommended persistence:

- add `execution_mode` and a validated immutable execution document to `ProbeRevision`;
- stamp execution mode and capture target fingerprint on `ProbeRun`;
- add a `ProbeCaptureLease` table with tenant, run, check revision, token hash, expiry and state;
- add append-only `ProbeCaptureEvent` rows for method, logical endpoint, timestamp, redacted headers,
  bounded body metadata/hash, and scripted response identity;
- keep one scenario-level `ProbeResult`, linked to capture events and containing deterministic
  evaluation detail;
- never force multiple asynchronous capture events into the existing
  `(run, check, request_index)` HTTP-answer model.

## 4. Capture service

Prefer a separately deployable capture service or a sharply isolated router/process. It is a public
ingress surface receiving untrusted MSP requests and attachment bytes.

### Lease lifecycle

1. Runner creates a random, single-run lease; store only its hash.
2. Lease contains tenant, run, check revision, allowed logical endpoints, maximum calls/bytes and
   expiry.
3. Capture URLs contain the opaque lease token and fixed logical endpoint, never an arbitrary target.
4. First valid event atomically advances the expected state; duplicates are retained and evaluated.
5. Completion, cancellation, expiry or run fencing closes the lease.
6. Late events are rejected and recorded without changing the result.

### Endpoint behavior

Provide only scenario-scoped endpoints such as:

```text
/capture/{lease}/v1/message
/capture/{lease}/v1/preUpload
/capture/{lease}/upload/{object}
/capture/{lease}/v1/preDownload
/capture/{lease}/download/{object}
/capture/{lease}/v1/decodePayload
/capture/{lease}/v1/authenticate
/capture/{lease}/v1/constructPayload
```

Responses come from immutable allowlisted scripts: success, selected 4xx/5xx, timeout, truncated
transfer, malformed bounded JSON, checksum missing/mismatch, or short-lived URL expiry. A script is
versioned test content, not user code.

### Security controls

- disposable/non-production MSP target attested before arming;
- capture host fixed in server configuration, never tenant-supplied;
- TLS required; redirects disabled; no certificate bypass;
- strict method/path/content-type/size/count allow-lists;
- per-tenant/run token hashing, expiry, rate limiting and replay handling;
- attachment bytes encrypted at rest, short TTL, malware-safe handling and hard size cap;
- Authorization, signatures, keys, signed URLs and tenant variables redacted before persistence;
- no response script may reflect secrets or arbitrary request content;
- worker fence checked before every durable event/result write;
- audit event for lease create/arm/close/expire and test-endpoint configuration confirmation.

## 5. MSP trigger and endpoint override

Phase 2 is possible only when the MSP supplies one of these approved test-only integration methods:

1. a disposable environment configuration that replaces Apple gateway/content base URLs with the
   Verifier capture base URL; and
2. either an inbound event that naturally triggers the outbound behavior or an authenticated,
   tenant-scoped test hook that requests the exact business action.

The endpoint override must be observable and acknowledged before execution. A Boolean UI claim is
insufficient; use a signed/configured environment receipt or a handshake request tied to the lease.
If this capability is absent, planning returns `needs_phase_3`; it does not fail the MSP.

Production credentials must never be sent to the emulator. Use dedicated test credentials and IDs.

## 6. Orchestration and deterministic evaluation

Add a dispatcher in `probe_execution/service.py`:

```text
inbound_http     -> existing synchronous request executor
outbound_capture -> scenario executor + capture lease/event wait
external         -> never scheduled by the probe runner
```

The Phase 2 executor must not hold a database connection while waiting. It should:

1. create/commit the lease and expected scenario state;
2. release the transaction;
3. issue the trigger;
4. poll or consume capture-event notification without holding a DB connection;
5. reopen short transactions to evaluate/finalize under the existing execution fence.

Evaluation is a pure function of the immutable scenario, stamped target, scripted responses and
ordered capture events. It reports:

- `passed_observation` when every required event/assertion is present;
- `failed_observation` only for an MSP-attributable mismatch;
- `could_not_run` for capture, trigger, environment or runner failure;
- `needs_phase_3` when safe capture is unsupported; and
- `needs_rerun` when the target/revision/lease fingerprint changed.

No observation writes a human `ReviewAttempt`.

## 7. Attachment implementation order

Implement the attachment family after the generic capture service:

1. B.4 `/preUpload` request capture and encrypted-size assertion.
2. B.5 upload target, checksum response and `/message` ordering.
3. B.5 injected upload failure with a bounded negative `/message` assertion window.
4. B.3 `/preDownload` capture and controlled encrypted-content download.
5. B.3 corrupt/truncated/wrong-key fixtures, observing only what the MSP exposes.
6. B.6 `interactiveDataRef` chain through preDownload/download/decrypt/decodePayload.
7. C.2 separate UX evidence for actionable agent errors.
8. Live Apple/crypto Phase 3 evidence for properties the emulator cannot establish.

Each scenario stays bound to its existing v2026.10.06 item. Shared capture events may be referenced
by secondary items only through separately evaluated assertions.

## 8. Migration and compatibility

- additive nullable columns/tables only;
- historical check revisions behave as `inbound_http` without rewriting stored JSON;
- old bundles import unchanged;
- new Phase 2 bundles are rejected clearly by older Verifier builds rather than silently degraded;
- Phase 1 run planning, counts, results and UI remain unchanged;
- Phase 2 is feature-flagged globally and per tenant, default off;
- no staging activation until local disposable testing and security review pass.

## 9. Test gates

### Tier B

- exact wire-byte golden tests for every body mode;
- malformed JSON is actually malformed on the wire;
- gzip valid/corrupt/truncated fixtures are byte-distinct;
- JWT just-inside/at/just-outside boundary tests use a frozen clock;
- wrong-secret, wrong-audience, missing/future/stale-`iat` and wrong-algorithm JWT profiles remain
  structurally valid for the exact condition under test;
- B.13 ordered/dominance tests assert internal precedence only when safe response evidence is
  distinguishable;
- all secrets remain absent from stored request/result/log text;
- all historical runner tests remain unchanged and green.

### Phase 2

- lease isolation across tenants/runs and token replay/expiry;
- endpoint/method/body/count/size refusal matrix;
- trigger failure, capture timeout and emulator failure produce `could_not_run`;
- ordered, duplicate, missing, late and unexpected event evaluation;
- negative assertion window cannot pass before the window closes;
- resume/fencing prevents two workers finalizing one scenario;
- attachment success and every injected failure stage;
- no production target/credential acceptance;
- bundle import/export and old-build refusal behavior;
- no automated checklist progress or human-attempt creation.

## 10. Delivery slices

1. ADR and threat model; no code.
2. Freeze current executor behavior behind an adapter.
3. Tier B typed raw-body and JWT profiles.
4. Capture data model and isolated service with synthetic tests.
5. Phase 2 planner/orchestrator in local disposable mode.
6. B.4/B.5 attachment-upload pilot.
7. B.3/B.6 attachment-download/interactive pilot.
8. Remaining existing-item scenario families.
9. Local golden comparison, security review and cost/load measurement.
10. Separate authorization for Stage; production remains disabled.

