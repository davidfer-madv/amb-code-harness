# Proposed checklist delta — Apple review feedback

Status: **PROPOSAL ONLY — DO NOT REPLACE THE AUTHORITATIVE CHECKLIST**

Legend:

- 🟨 **MODIFIED** — replace or extend an existing record.
- 🟩 **NEW** — proposed new record.
- 🟥 **HOLD** — field contains unverified or conflicting authority and cannot be marked green.

For existing rows, preserve current Build Status, Demo Video Readiness Status, Video Demo URL, MA
Verified Status, and MA Notes unless a human explicitly approves a status change. New rows begin
with all status fields blank and `MA Verified Status = UNVERIFIED`.

## Proposed modifications

### 🟨 C.2 — Receiving and sending attachments and wallet passes

- **Requirement:** Receiving and sending attachments, wallet passes, and actionable upload errors
- **Description:** Preserve the existing 100 MB, `/preUpload`, `/preDownload`, AES-CTR, key
  transport, and test-vector obligations. When an upload or download fails, the agent console MUST
  show a specific actionable category—size limit, unsupported type, encryption/validation,
  timeout/network, or upstream rejection—rather than only “upload failed,” and MUST provide safe
  user-facing recovery copy.
- **Key Considerations:** Derive the reason from validated local checks or an actual upstream
  response; do not invent precision Apple did not return. Cross-reference I.3/I.5/I.6 for limits
  and secret minimization. Never display keys, signatures, internal URLs, or raw sensitive errors.
- **Reference:** MSP Integration Guide §11, §11.6, §11.9; I.3; I.5. Error-copy specificity:
  user-transcribed Apple review, provenance pending.
- **Verification Method:** UX Testing plus Provide Code (negative tests for size, type, encryption,
  timeout, and upstream rejection).
- **Review Notes:** **[STRENGTHENED][LIVE_COMPATIBILITY/PLATFORM_SAFETY]** Exact Apple error
  taxonomy remains unverified.

### 🟨 C.6 — Quick Reply messages

- **Requirement:** Quick Reply messages for bounded choices and confirmations
- **Description:** Preserve the two-to-five single-select constraint. Use Quick Reply for yes/no,
  confirmations, and other bounded expected-answer prompts whenever two to five tappable choices
  fully represent the answer; do not force open text for such prompts. Use List Picker for more than
  five options.
- **Key Considerations:** Precede the interactive object with concise introductory text. A Quick
  Reply tap counts as consent only when the preceding disclosure and E.4 record requirements are
  satisfied. Do not show a choice after close, Leave Conversation, or opt-out.
- **Reference:** MSP Integration Guide §13; canonical Conversation Design Standards; canonical
  addendum `2026-07-25-use-case-experience-best-practices`.
- **Verification Method:** Postman plus UX Testing across representative bot, automation, and agent
  confirmations.
- **Review Notes:** **[STRENGTHENED][APPLE_REVIEW_GUIDANCE]** The supplied “70%” statistic is not a
  pass threshold.

### 🟨 C.14 — Typing indicator message

- **Requirement:** One-second typing indicator before every permitted outbound payload
- **Description:** Show a visible typing indicator for one second before every outbound payload from
  bot, automation, or live agent, including text, attachments, Quick Reply, List Picker, Time
  Picker, Form, rich link, Authentication, and Apple Pay. Each back-to-back payload requires its own
  indicator. Preserve the 60-second timeout/refresh rule.
- **Key Considerations:** The indicator is itself outbound and MUST pass the same preflight
  eligibility check as the payload. Emit neither indicator nor payload after close, Leave
  Conversation, opt-out, or another sending prohibition. Test actual production sequencing and
  avoid excessive cumulative delay.
- **Reference:** MSP Integration Guide §8, §8.3, §8.4; cross-reference C.19, E.5, H.2.
- **Verification Method:** Postman plus UX Testing (timed device recording, back-to-back sequence,
  and close-during-sequence negative case).
- **Review Notes:** **[CLARIFIED][APPLE_NORMATIVE/REVIEW_CONFIRMED]**

### 🟨 C.16 — Channel settings and landing page

- **Requirement:** Brand channel settings and complete Client Landing Page Connect flow
- **Description:** Preserve per-brand channel settings, privacy, Terms of Use, support, and account
  linking. The Connect handoff MUST demonstrate the applicable terms step, MSP authentication,
  linking of the Apple-provided business identity to the MSP client account, and an explicit
  successful-connection confirmation using correct Apple Messages for Business naming.
- **Key Considerations:** Use the exact terms presented by the live Apple/MSP flow; do not conflate
  display with affirmative acceptance without evidence. Internal test accounts may provide less
  brand metadata than production accounts. Avoid logging handoff credentials or identifiers.
- **Reference:** MSP Integration Guide §25, §25.1, §25.2; Verified Answer “Client Landing Page:
  hosted by the MSP, not by Apple”; user-transcribed review for terms/auth/success sequence.
- **Verification Method:** UX Testing from Apple Business Register Connect through success
  confirmation.
- **Review Notes:** **[STRENGTHENED][APPLE_PROCESS/UX]** Terms-acceptance semantics need original
  artifact confirmation.

### 🟨 C.18 — Invitation messages and lifecycle state

- **Requirement:** Invitation messages with explicit consent, decline, no-response, opt-out, and
  undeliverable states
- **Description:** Preserve Apple-managed templates, phone-number addressing, gated approval,
  platform floors, and response-code semantics. Model pending, accepted, declined/No, no-response,
  opt-out, user-preference-undeliverable, and sender/transport-error states distinctly. When the
  user selects No, no conversation message or opaque user ID is delivered for display in the MSP
  platform and the platform MUST NOT continue messaging. Conversational sending becomes eligible
  only after the user initiates a new conversation.
- **Key Considerations:** Invitation 410 is a missing/incorrect `message-type` header, not opt-out.
  User-preference undeliverable is 404. Do not invent an opaque-ID-to-phone join. Store
  pre-conversation suppression per brand and normalized destination. A later user-initiated
  conversation restores conversational reply eligibility but does not automatically recreate
  campaign or notification consent.
- **Reference:** MSP Integration Guide §20, §20.6.2, §20.8, §21; REST API Invitation and
  CloseSession identity rules; B.8 and I.1.
- **Verification Method:** Postman plus Provide Code (state-transition and negative response-code
  tests).
- **Review Notes:** **[STRENGTHENED][MIXED APPLE_NORMATIVE/APPLE_REVIEW_ATTESTED]** No is
  intentionally not represented as a platform message.

### 🟨 C.19 — Block sending after the user closes the conversation

- **Requirement:** Preflight block and queue suppression after close
- **Description:** On close, block every live-agent, bot, automation, typing, scheduled, queued,
  campaign, CSAT, retry, and replay path before an Apple API call. Suppress or terminally cancel
  queued work. Restore conversational sending only after a qualifying user-initiated restart and
  only when no stronger opt-out or consent prohibition remains.
- **Key Considerations:** Handle close-versus-send and close-versus-worker races atomically. A 410
  received on an organic send reconciles local state if a close event was delayed or missed; never
  reuse the invitation meaning of 410.
- **Reference:** REST API “Receiving a Closed Conversation”; MSP Integration Guide §7, §21, §27.5;
  H.1.
- **Verification Method:** UX Testing plus Provide Code (concurrent close/send, queued retry, and
  stale-worker tests).
- **Review Notes:** **[STRENGTHENED][APPLE_NORMATIVE/PLATFORM_SAFETY]**

### 🟨 E.4 — Consent rules

- **Requirement:** Auditable opt-in before automated notifications, invitations, lists, or campaigns
- **Description:** Require a current opt-in record before each non-transactional automated
  notification, Invitation list, or campaign. Record brand, channel, purpose/category,
  destination/subject, collection source, timestamp, disclosure/version, and revocation state.
  Apple may accept consent collected through multiple business channels when a valid record exists.
- **Key Considerations:** Consent is per brand, channel, and purpose. Never infer campaign consent
  from a prior conversation, invitation acceptance, reachability window, or another channel. The
  schema is an MA/platform control; jurisdiction-specific legal and TCPA review remains independent.
  Scope records by tenant and retain immutable audit history.
- **Reference:** MSP Integration Guide §27.4; I.6; user-transcribed Apple review on acceptable
  collection sources.
- **Verification Method:** Verbal on Apple Policy plus Provide Code (consent-ledger and negative
  campaign tests).
- **Review Notes:** **[STRENGTHENED][APPLE_NORMATIVE + MA_PROGRAM]** “TCPA compliant” is not accepted
  as evidence by itself.

### 🟨 E.5 — Opt-out and Leave Conversation handling

- **Requirement:** Immediate brand-wide opt-out with configurable, non-weakening compliance copy
- **Description:** Preserve Leave Conversation and case-insensitive STOP, UNSUBSCRIBE, and QUIT
  handling across bot, agent, campaign, retry, replay, scheduled, and automation paths. Stop applies
  to the brand, not only a thread. First-message and opt-out compliance copy may be configured per
  brand, but mandatory disclosure, automation identification, trigger coverage, and processing
  cannot be removed.
- **Key Considerations:** Version configuration and audit changes. Reset each state separately:
  a later user-initiated conversation restores permission to reply within that conversation, like
  the restart after Leave Conversation or STOP, but does not automatically restore separate
  notification/campaign consent. Cross-reference C.18 for pre-conversation phone suppression and
  C.19 for close.
- **Reference:** MSP Integration Guide §21, §27.5, §27.6; E.2/E.4/E.6; review transcription for
  configurable copy.
- **Verification Method:** Verbal on Apple Policy plus Postman plus Provide Code (opt-out/send race,
  queued-campaign purge, localization, and no-consent-reset tests).
- **Review Notes:** **[STRENGTHENED][MIXED APPLE_NORMATIVE/MA_PROGRAM]**

### 🟨 E.9 — Product, channel, and feature naming

- **Requirement:** Correct Apple Messages for Business naming without confusing Apple Business or
  iMessage
- **Description:** Use “Apple Messages for Business” as the priority product/channel name in
  customer-facing, public, onboarding, marketing, platform, and Integration Review surfaces. When
  the full name does not fit the available wording or label, “Apple Messages” is the approved
  alternative—for example, “Apple Messages user.” Do not call the channel “Apple Business,” “Apple
  Business Chat,” or “iMessage,” and do not imply Apple endorsement. “Apple Business” now names a
  separate Apple platform. In customer-facing explanatory copy prefer “app extension”; preserve
  Apple's exact `iMessage app`, `CustomInteractiveData`, and `bid` terminology in technical schema,
  code, and evidence.
- **Key Considerations:** Use the full name whenever practical and document surfaces that require
  the shorter form. Replace “Apple Business Contact” with “Apple Messages contact” as the default
  unknown-contact label; if the product uses “user” rather than “contact,” use “Apple Messages
  user.” Scan localization bundles, templates, agent UI, and review material.
- **Reference:** MSP Integration Guide §27.9; canonical partner PR/marketing addendum; Apple 2026
  Apple Business announcement; user-transcribed review.
- **Verification Method:** Verbal on Apple Policy plus Provide Code (localized UI/template string
  scan) plus UX Testing.
- **Review Notes:** **[CORRECTION][APPLE_REVIEW_CLARIFIED]** Full name has priority; short form is
  allowed only where the full wording does not fit.

### 🟨 E.10 — Conversational design and agent etiquette

- **Requirement:** Conversational design umbrella and traceable review coverage
- **Description:** Preserve greeting, automation/agent identification, stated hours, response-time
  expectations, clear handoff, opt-in phrasing, triage, response quality, and satisfaction-survey
  coverage. Treat E.11 and E.12 as separately demonstrable sub-gates rather than allowing this
  umbrella row alone to turn them green.
- **Key Considerations:** A broad policy attestation does not satisfy the first-turn or
  post-resolution device scenarios.
- **Reference:** MSP Integration Guide §27.9; E.11; E.12.
- **Verification Method:** Verbal on Apple Policy plus UX Testing.
- **Review Notes:** **[CLARIFIED][ANTI-OVER-GREENING]**

### 🟨 J.5 — Connect button in the Apple Messages for Business account

- **Requirement:** Demonstrate the full Client Landing Page connection journey
- **Description:** From the live Connect entry point, demonstrate the applicable terms step,
  authentication, business/account linking, and the explicit successful-connection confirmation.
  C.16 owns implementation; J.5 is the final review evidence gate.
- **Key Considerations:** Keep a continuous capture and correct product naming. A test account is
  acceptable, but document its reduced metadata.
- **Reference:** C.16; MSP Integration Guide Landing Page/Connect Button.
- **Verification Method:** UX Testing.
- **Review Notes:** **[STRENGTHENED][REVIEW GATE]** This is intentionally evidence-focused, not a
  duplicate implementation requirement.

## Proposed new items

### 🟩 E.11 — Guided opening and tappable triage

- **Requirement:** Guided opening with top-use-case Quick Replies
- **Description:** Promptly greet the user, identify automation when applicable, and pair the
  opening with a Quick Reply containing up to five brand-specific top intents unless the entry-point
  intent or initial message already determines routing.
- **Key Considerations:** Do not ignore a clear user-written intent to force a menu. Keep options
  current using actual brand demand data. The reported 70% concentration is context only.
- **Reference:** Conversation Design Standards; canonical addendum
  `2026-07-25-use-case-experience-best-practices`.
- **Verification Method:** UX Testing across generic and intent-specific entry points.
- **Review Notes:** **[NEW][APPLE_REVIEW_GUIDANCE]** Status fields blank; MA Verified Status
  `UNVERIFIED`.

### 🟩 E.12 — Resolution check and post-interaction CSAT

- **Requirement:** Ask whether more help is needed and offer CSAT after resolution
- **Description:** After resolving a use case, ask whether anything else is needed and provide
  relevant Quick Reply options. When the interaction is actually complete, offer CSAT. Use
  descriptive choices rather than bare 1–5 numbers; use Form Message for multi-question surveys
  with capability-aware fallback.
- **Key Considerations:** Do not send CSAT after every FAQ, before resolution, after close/Leave
  Conversation/opt-out, or from an expired/disallowed state. Do not let a scheduled CSAT bypass
  C.19. Cross-reference D.4/D.5 for fallback.
- **Reference:** MSP Integration Guide §27.9; canonical Experience Review v3.1 addendum; canonical
  addendum `2026-07-25-use-case-experience-best-practices`.
- **Verification Method:** UX Testing on supported and fallback devices plus Provide Code
  (suppression test).
- **Review Notes:** **[NEW][APPLE_REVIEW_GUIDANCE]** Status fields blank; MA Verified Status
  `UNVERIFIED`.

### 🟩 G.6 — Coach brands before Integration Review

- **Requirement:** Set brand expectations before journey implementation and review
- **Description:** Before Integration Review, coach the brand on Apple Messages for Business
  interaction design, consent, opt-out, rich features, response behavior, naming, and review
  expectations, explicitly contrasting material differences from WhatsApp and RCS. Resolve known
  journey gaps before recording or live review.
- **Key Considerations:** Record acknowledgement, decisions, and unresolved exceptions. Coaching
  content follows A.6 embargo and E.9 naming rules. This is a readiness/program control, not an Apple
  REST obligation.
- **Reference:** Integration Review process; Conversation Design Standards; user-transcribed Apple
  feedback.
- **Verification Method:** 3 Way Meeting plus Verbal on Apple Policy.
- **Review Notes:** **[NEW][MA_PROGRAM/APPLE_REVIEW_GUIDANCE]** Status fields blank; MA Verified
  Status `UNVERIFIED`.

### 🟩 C.23 — Bulk invitation campaign controls

- **Requirement:** Consented, paced, cancellable, and auditable bulk Invitation campaigns
- **Description:** Support eligible Invitation contact lists and campaign orchestration at scale
  with per-record validation, consent and suppression checks at send time, deduplication, resumable
  batching, progressive ramp-up, staggered submissions, bounded retries, cancellation, per-brand
  fairness, and auditable per-record results. The platform sends individually addressed, approved
  Apple Invitation requests in paced batches; this item does not assert a separate Apple bulk API.
- **Key Considerations:** Bulk never waives E.3/E.4/E.5 or gated Invitation approval. Treat 1,000
  messages/second as a provisional aggregate per-MSP target, not a hard published limit; keep it
  configurable and coordinate large/time-sensitive sends with Apple. Apple publishes no 429. An
  opt-out or close racing a campaign MUST purge unsent work.
- **Reference:** MSP Integration Guide §20, §20.8, §21; canonical addenda
  `2026-07-28-invitation-bulk-throughput-guidance` and
  `2026-07-28-throughput-1k-mps-per-msp`; H.1.
- **Verification Method:** Postman plus Provide Code (large-list pacing, fairness, cancellation,
  fault-injection, deduplication, and opt-out-race tests) plus Verbal on Apple Policy.
- **Review Notes:** **[NEW][APPLE_REVIEW_GUIDANCE + MA_PROGRAM/PLATFORM_SAFETY]** Reconciles older
  “bulk unsupported” wording: bulk refers to MSP list/campaign orchestration, while Apple receives
  individual Invitation requests.

### 🟩 H.4 — Reachability-window expiration lifecycle

- **Requirement:** Provisional tracking and safe handling of the reported 365-day reachability window
- **Description:** Track the last qualifying inbound per conversation and surface approaching or
  observed expiry internally to authorized brand operators. The reported 365-day duration is
  provisional until direct authority is resolved. A qualifying inbound may reset the window, but
  MUST NOT reset opt-out or campaign consent.
- **Key Considerations:** Do not invent an Apple error code, hard-code an unverified duration, or
  use the timer to authorize outbound. No arbitrary pre-expiry re-engagement is allowed. Outreach is
  permitted only through an approved, consented Invitation or another channel with independent
  consent. Define qualifying events, clock skew, and precedence of consent/close over reachability.
- **Reference:** User-transcribed Apple review; adjacent H.1/H.2/E.3/E.4/E.5. No resolved canonical
  claim yet.
- **Verification Method:** Provide Code (injectable-clock boundary, reset, skew, returned-error,
  no-outbound, and consent-precedence tests) plus Verbal on Apple Policy.
- **Review Notes:** **[NEW][LIVE_COMPATIBILITY][PROVISIONAL]** 🟥 **HOLD:** duration, event set, and
  error response. Cannot become green before authority resolution.

## Proposed Section K — MSP omnichannel controls, not Apple protocol requirements

### 🟩 K.1 — Consent-safe non-Apple-device channel fallback

- **Requirement:** Configurable fallback to registered RCS, SMS, or both when the destination is not
  an Apple device
- **Description:** When the intended recipient does not use an Apple device and therefore cannot
  receive an Apple Messages for Business Invitation or conversation, the MSP may use the brand's
  registered RCS channel, SMS channel, or both only when each selected channel has its own valid
  consent and the content can be represented safely. Apple recommends having fallback capability
  but expresses no preference for RCS, SMS, or their order.
- **Key Considerations:** This is destination/channel fallback, not Section D Apple device-feature
  capability fallback and not a retry of an Apple payload. Never use it to bypass decline, opt-out,
  Leave Conversation, close, or user-preference suppression. Never carry Apple-specific
  Authentication, Apple Pay, Form, attachment keys/URLs, or secure PII flows to another channel. If
  both RCS and SMS are configured, define order, wait time, promotion, late-success deduplication,
  per-channel audit, and opt-out precedence.
- **Reference:** User-transcribed review; cross-reference E.3/E.4/E.5/E.7/I.3/I.5/I.6. No Apple
  protocol authority.
- **Verification Method:** Provide Code (cross-channel consent, negative eligibility, content-class,
  timeout, and late-success deduplication tests) plus policy/legal review.
- **Review Notes:** **[NEW][MA_PROGRAM/PLATFORM_SAFETY/APPLE_REVIEW_GUIDANCE]** Apple has no channel
  preference; MSP/brand policy selects the fallback. Status fields blank; MA Verified Status
  `UNVERIFIED`.

## Field/status application rules

- Existing rows: update only Requirement, Description, Key Considerations, Reference, Verification
  Method, and Review Notes after approval. Preserve all status/URL/MA fields.
- New rows: leave Build Status, Demo Video Readiness Status, Video Demo URL, and MA Notes blank; set
  MA Verified Status to `UNVERIFIED`.
- Rows with 🟥 **HOLD** cannot become green/done and cannot be described as Apple-normative.
- Apply the exact approved wording to Markdown and CSV together, then refresh `.policy-hashes.txt`.
