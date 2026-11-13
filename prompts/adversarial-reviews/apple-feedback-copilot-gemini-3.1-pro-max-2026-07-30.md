# Adversarial Review Report: Apple Feedback Checklist Proposal

## Executive Verdict
**ACCEPT_WITH_CHANGES**

## Critical Blockers
1. **RCS→SMS Fallback (C.23):** The requirement to fallback to RCS then SMS is an omnichannel MSP product feature, not an Apple Messages for Business protocol requirement. It cannot be mandated in an Apple integration checklist.
2. **Pre-Expiry Re-engagement (H.4):** The draft suggests coaching brands to send a "pre-expiry re-engagement message" before the 365-day session timeout. This directly violates Apple's strict "no unsolicited outbound" rule (E.3) unless the message is an approved, consented template.
3. **"Apple Messages" Shorthand (E.9):** The transcription's claim that "Apple Messages" is an acceptable shorthand contradicts Canonical E.9 and the Apple PR/Marketing Guidelines addendum (which mandates the full "Apple Messages for Business" and forbids variations).
4. **Opaque IDs on Declines (C.18):** The draft claims a declined invitation "cannot continue because no user ID exists." This is technically incorrect. A user tapping "No" or opting out generates an inbound message to the MSP, which inherently carries an Apple opaque `sourceId`. 

## Authority/Classification Corrections
- **C.23 (RCS/SMS fallback):** Out of scope. Drop entirely.
- **E.4 (TCPA compliance):** TCPA is a US legal framework, not an Apple normative standard. Apple requires explicit opt-in; legal compliance is the brand's responsibility. Remove TCPA from the checklist requirement.
- **H.4 (365-day expiration):** Must be strictly classified as `LIVE_COMPATIBILITY` pending direct canonical confirmation from Apple.
- **E.9 (Naming):** Restore the strict prohibition against "Apple Messages" shorthand to align with canonical PR guidelines.

## Existing Rows to Modify
- **E.9 (Product and feature naming):** Reject the allowance for "Apple Messages" shorthand. Accept the correction to use "Apple Messages contact" for unknown contacts and "app extension" for UI copy.
- **E.10 (Conversational design and agent etiquette):** Do not create new rows for conversational flow. Merge the proposed E.11 (Guided opening/triage) and E.12 (Resolution check/CSAT) into this existing row to align with the `2026-07-25-use-case-experience-best-practices` addendum.
- **C.18 (Invitation messages):** Merge the proposed C.24 (Bulk invitation campaigns) into this row. Clarify that bulk pacing (progressive ramp-up, 1,000 msg/sec target) applies here. Correct the technical behavior for declines to acknowledge the opaque ID received.
- **E.4 (Consent):** Accept the strengthened opt-in record auditability but scrub the phrase claiming TCPA compliance inherently meets Apple's rules.
- **C.19 (Preflight send block):** Accept the strengthened wording to block queued/retry messages after a close event.

## New Rows to Add
- **A.7 (Coach brands before experience design and review):** Accept as a `MA_PROGRAM` addition to improve onboarding friction.
- **H.4 (365-day gateway session-expiration lifecycle):** Accept provisionally as `LIVE_COMPATIBILITY`, but alter the wording to strictly forbid unsolicited re-engagement.

## Rows to Merge/Drop
- **DROP C.23:** RCS/SMS cross-channel fallback.
- **DROP C.24:** Merge bulk invitation pacing and controls into C.18.
- **DROP E.11 & E.12:** Merge conversation design elements (triage, CSAT) into E.10.

## Anti-Weakening and Negative-Test Corrections
- **Opt-out and Opaque ID Correlation (C.18/E.5):** The verification method must include tests to ensure the platform successfully correlates an inbound opt-out (which uses an opaque `sourceId`) to the original phone number to permanently block future phone-number-based invitations.
- **Close Event Reset (E.5 / C.19):** Wording must clarify that an external "fresh opt-in" does not bypass an Apple gateway 410 (Leave Conversation) block. Only a new user-initiated inbound message can reset the Apple gateway state to allow outbound messages again.

## Field-Ready Replacement Wording

### C.18 — Invitation messages and bulk campaigns
**Requirement:** Send business-initiated notification messages using Apple-managed templates to opted-in users by phone number. Support progressive pacing and staggered submissions for bulk uploads; target no more than 1,000 messages/second overall and coordinate large pushes with Apple. Define distinct handling for accepted, declined, and opted-out states. A user decline or opt-out arrives as an inbound message containing an opaque `sourceId`; the platform must correlate this intent to the destination phone number to block future invitations. Undeliverable-by-user-preference yields a 404.
**Reference:** MSP Integration Guide §20, §20.6.2, §20.8, §21.
**Verification Method:** Postman, large-list pacing tests, and state-transition tests linking opaque IDs to blocked phone numbers.
**Review Notes:** Apple evaluates bulk pacing and opt-out correlation rigorously.

### E.9 — Forbidden in-conversation language
**Requirement:** Use "Apple Messages for Business" as the full channel/product name in platform UI, documentation, onboarding, and templates. Do not use "Apple Messages", "Apple Business", or "iMessage," and do not imply Apple endorses the brand. Use "app extension" in customer-facing copy rather than "iMessage app extension," preserving formal schema terms only in technical evidence. Default unknown contacts to "Apple Messages contact."
**Reference:** MSP Integration Guide §27.9.
**Verification Method:** UX Testing plus repository/UI string scan.
**Review Notes:** Strict adherence required by Apple PR/Marketing guidelines.

### H.4 — 365-day gateway session-expiration lifecycle
**Requirement:** Track the last qualifying inbound message and treat the Apple gateway session as expiring 365 days later (pending direct Apple confirmation). Surface approaching expiry to authorized brand operators and handle expired-send errors gracefully. Any qualifying inbound reply resets the timer. Pre-expiry outreach is strictly forbidden unless the message is an approved, consented template; do not use arbitrary re-engagement to bypass the "no unsolicited outbound" rule.
**Reference:** Unverified LIVE_COMPATIBILITY observation.
**Verification Method:** Time-boundary and error-mapping tests.
**Review Notes:** Verify exact timeout duration and error code directly with Apple.

## Residual Questions Requiring Apple or Human Confirmation
1. **365-Day Expiration:** Is the 365-day session timeout an exact, documented Apple Gateway threshold, and what exact error code is returned upon expiration?
2. **Upload Error Specifics:** Does the Apple platform reliably return distinct, actionable failure reasons for attachments (size vs. crypto vs. unsupported type) that the MSP can actually parse and surface to agents, or is this merely a UX recommendation?
