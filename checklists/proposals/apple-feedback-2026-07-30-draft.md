# Draft mapping: Apple feedback to checklist changes

This is an adversarial-review input, not the authoritative checklist. Candidate repositories are
out of scope. Proposed wording uses these labels:

- **[CORRECTION]** fixes a contradiction.
- **[STRENGTHENED]** adds a missing obligation to an existing item.
- **[NEW]** creates a new checklist item.
- **[CLASSIFICATION]** prevents review or platform guidance from being presented as an Apple
  protocol fact.

## Existing-list improvements

### E.9 — **[CORRECTION] Product and feature naming**

Replace the current rule that forbids “Apple Messages.” Proposed requirement:

> Use “Apple Messages for Business” as the full channel/product name in platform UI,
> documentation, onboarding, templates, and review materials; “Apple Messages” is acceptable
> shorthand where context is clear. Do not call the channel “Apple Business” or “iMessage,” and do
> not imply Apple endorses the brand. Use “app extension” in customer-facing copy rather than
> “iMessage app extension,” while preserving Apple’s formal protocol/schema terms where exact
> technical names are required. Default unknown contacts to “Apple Messages contact,” not “Apple
> Business Contact.”

Class: APPLE_NORMATIVE naming plus review-attested UI examples. Verification: UX Testing plus
repository/UI string scan.

### C.6 — **[STRENGTHENED] Quick Reply messages**

Add: use Quick Reply for every yes/no, confirmation, or other bounded expected-answer prompt with
two to five choices; do not require free text where a tappable response can represent the answer.
Keep List Picker for more than five choices.

Class: APPLE_NORMATIVE UX guidance. Verification: Postman plus UX Testing across bot and agent flows.

### C.14 — **[STRENGTHENED] Typing indicator message**

Clarify: every outbound payload from bot, automation, or live agent—including text, attachment,
Quick Reply, List Picker, Time Picker, Form, rich link, authentication, and Apple Pay—must be
preceded by a visible typing indicator for at least one second. Back-to-back payloads each require
their own indicator. Test actual production sequencing, not merely indicator support.

Class: APPLE_NORMATIVE/review-confirmed. Verification: Postman plus timed device UX capture.

### C.2 — **[STRENGTHENED] Attachment upload failure feedback**

Add: reject over-limit, unsupported, encryption, and transport failures with a specific,
agent-actionable reason and safe user-facing copy; do not collapse all failures into “upload
failed.” Never expose keys, internal URLs, or secrets in either message.

Class: LIVE_COMPATIBILITY / PLATFORM_SAFETY pending direct canonical claim. Verification: UX Testing
plus negative tests for size, type, crypto, timeout, and upstream status.

### C.16 and J.5 — **[STRENGTHENED] Client landing-page Connect flow**

Require and demonstrate the entire Apple Business Register Connect handoff: terms acceptance,
authentication, business/account linking, and an explicit successful-connection confirmation, with
correct Apple Messages for Business naming throughout. C.16 owns implementation; J.5 remains the
review demonstration gate.

Class: APPLE_NORMATIVE process/UX. Verification: end-to-end UX Testing from the Connect button.

### C.18 — **[STRENGTHENED] Invitation lifecycle**

Add distinct states and behavior for invitation accepted, declined, explicit “No,” no response,
undeliverable, opted out, and later user-initiated reset. A decline cannot continue as a
conversation because no opaque user ID exists. Store blocking state by normalized destination
phone number where the flow has no opaque ID, and clear only on a qualifying later inbound event.

Class: APPLE_NORMATIVE identity/flow plus review-attested state behavior. Verification: Postman and
state-transition tests.

### C.19 — **[STRENGTHENED] Preflight send block after close**

Clarify that every agent, bot, automation, scheduled, queued, retry, replay, and campaign path must
check closed state and block before calling Apple. Purge or terminally suppress already queued work.
Restore sending only after a qualifying user restart.

Class: APPLE_NORMATIVE plus PLATFORM_SAFETY closure. Verification: concurrent close-versus-send and
queued-retry tests plus UX Testing.

### E.4 — **[STRENGTHENED] Consent records for invitations and campaigns**

Require an auditable opt-in record before every invitation list or campaign: brand, channel,
purpose/category, subject/destination, source, timestamp, disclosure/version, and revocation state.
Apple may accept multiple collection channels, but the MSP must retain evidence. “TC/TPCA
compliant” wording is not by itself proof and does not replace jurisdiction-specific legal review.

Class: APPLE_NORMATIVE consent obligation; record schema is MA_PROGRAM/PLATFORM_SAFETY.
Verification: policy review plus consent-ledger and negative campaign tests.

### E.5 — **[STRENGTHENED] Opt-out, configurable compliance copy, and later reset**

Require case-insensitive STOP and UNSUBSCRIBE handling across bot, agent, campaign, retry, and
automation paths. First-message and opt-out compliance copy must be configurable per brand without
allowing mandatory disclosures to be removed. Record phone-number blocking when no opaque ID
exists; only a later qualifying user-initiated message or fresh opt-in may reset the applicable
state.

Class: mixed APPLE_NORMATIVE and MA_PROGRAM configuration. Verification: policy review plus
end-to-end trigger, race, and reset tests.

### C.11 and C.20 — **[CORRECTION] Customer-facing app-extension naming**

Rename customer-facing checklist language to “Custom app extensions (CustomInteractiveData)” and
“app extension configuration.” Preserve `bid`, `CustomInteractiveData`, and Apple’s exact SDK or
schema terminology in technical evidence.

Class: naming correction; no protocol behavior change. Verification: documentation/UI scan and
existing Postman/code proof.

## New items and section placement

### A.7 — **[NEW] Coach brands before experience design and review**

Requirement: during brand onboarding, explain Apple Messages for Business conversation,
consent, interaction, naming, and review expectations and explicitly contrast material differences
from WhatsApp and RCS. Record brand acknowledgement and resolve journey-design gaps before
Integration Review.

Section rationale: A covers onboarding and pre-review readiness. Class: MA_PROGRAM informed by Apple
review. Verification: 3 Way Meeting plus onboarding artifact.

### E.11 — **[NEW] Guided opening and tappable triage**

Requirement: greet promptly, identify automation where applicable, and pair the opening with a
Quick Reply of up to five highest-volume intents unless entry-point intent or the initial message
already determines routing. Keep intent selection brand-specific and evidence-backed; the reported
“70%” figure is context, not a pass threshold.

Section rationale: E covers conversation design. Class: APPLE_NORMATIVE UX guidance.
Verification: UX Testing using representative entry points and first turns.

### E.12 — **[NEW] Resolution check and post-interaction CSAT**

Requirement: after resolving a use case, ask whether anything else is needed and provide relevant
Quick Reply options. Once the interaction is actually complete, offer a CSAT experience; use
descriptive labels rather than bare 1–5 numbers and use Form Message when the survey has multiple
questions, with capability-aware fallback. Do not send CSAT after every FAQ or before resolution.

Section rationale: E covers conversational design. Class: APPLE_NORMATIVE/review guidance.
Verification: UX Testing including supported and fallback devices.

### H.4 — **[NEW] 365-day gateway session-expiration lifecycle**

Requirement: track the last qualifying inbound message and treat the Apple gateway session as
expiring 365 days later, pending direct authority verification. Surface approaching and actual
expiry to authorized brand operators; block or route expired sends based on Apple’s returned error;
and reinvite or re-engage only when valid consent and Apple policy permit. Any qualifying inbound
reply resets the timer. Pre-expiry outreach must not become unsolicited messaging.

Section rationale: H owns response, timeout, and TTL behavior. Class: LIVE_COMPATIBILITY pending
canonical confirmation. Verification: time-boundary, error-mapping, consent, and clock-skew tests.

### C.23 — **[NEW] Cross-channel fallback after invitation or delivery failure**

Requirement: for eligible, consented destinations, route failed invitations or undeliverable
messages through the brand’s registered RCS channel and then SMS, while preserving purpose,
consent, opt-out, content, and audit state per channel. Never silently fallback where a channel
lacks consent or registration.

Section rationale: C covers required platform features; this is not an Apple gateway protocol
requirement. Class: MA_PROGRAM / PLATFORM_SAFETY / LIVE_COMPATIBILITY. Verification: cross-channel
integration tests and consent-policy review.

### C.24 — **[NEW] Bulk invitation campaign controls**

Requirement: support consented contact lists and invitation campaigns at scale with per-record
validation, deduplication, resumable batching, progressive ramp-up, staggered submissions, response
and status monitoring, bounded retries, cancellation, per-brand fairness, and auditable results.
Target no more than the provisional 1,000 messages/second aggregate per-MSP guidance, and coordinate
large or time-sensitive sends with Apple. Bulk capability never waives consent or unsolicited
messaging restrictions.

Section rationale: C covers Invitation capability; separate placement avoids overloading C.18’s
single-recipient lifecycle. Class: APPLE_REVIEW_GUIDANCE plus MA_PROGRAM/PLATFORM_SAFETY.
Verification: large-list, pacing, fairness, cancellation, opt-out-race, and fault-injection tests.

## Items that should not be duplicated

- Do not add another generic typing item; strengthen C.14.
- Do not add another close-event item; strengthen C.19 and cross-reference E.5.
- Do not add another generic opt-in or opt-out item; strengthen E.4/E.5.
- Do not create a second landing-page implementation item; strengthen C.16 and keep J.5 as the
  demonstration gate.
- Do not encode “70%” as a measurable compliance threshold.
- Do not call RCS→SMS fallback, upload error wording, or 365-day coaching Apple protocol facts until
  claim resolution supports that classification.
