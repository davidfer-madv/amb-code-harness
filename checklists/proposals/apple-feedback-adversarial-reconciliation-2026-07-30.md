# Adversarial reconciliation: Apple feedback checklist proposal

Reviews:

- Claude Opus, `max` effort:
  `prompts/adversarial-reviews/apple-feedback-claude-opus-max-2026-07-30.md`
- GitHub Copilot with Gemini 3.1 Pro Preview, `max` effort:
  `prompts/adversarial-reviews/apple-feedback-copilot-gemini-3.1-pro-max-2026-07-30.md`

Candidate repositories and workspaces were excluded from both model inputs.

## Accepted shared findings

- Cross-channel RCS→SMS fallback is an MSP omnichannel control, not an Apple gateway requirement.
- A 365-day local timer must not authorize unsolicited pre-expiry outreach.
- H.4 remains provisional until the exact duration, qualifying inbound events, and returned error
  are verified.
- Customer-facing naming changes must not rewrite Apple's formal technical schema terms such as
  `CustomInteractiveData`, `bid`, or Apple's own “iMessage app” documentation.
- C.14 must block typing indicators in every state where sending is prohibited.
- C.19 must cover queued, scheduled, retry, replay, campaign, CSAT, and automation paths before any
  Apple API call.
- TCPA language must not be treated as an Apple protocol rule or as a substitute for legal review.
- The “70%” statement is review context, not a checklist pass threshold.

## Findings rejected or narrowed

### Invitation decline identity

Copilot/Gemini said a declined invitation necessarily carries an opaque `sourceId`. Rejected.
Pinned canonical material states that where no prior conversation exists—explicitly including a
declined invitation—the identifier can be the customer's phone number in `tel:` form, and that no
opaque ID exists for the declined conversation. The exact “No” event shape and reset behavior still
need claim-level confirmation, so the proposal does not invent an opaque-ID-to-phone join.

### Bulk invitation evidence

Claude said the bulk and throughput addenda were absent. They are present in the supplied canonical
addenda:

- `2026-07-28-invitation-bulk-throughput-guidance`
- `2026-07-28-throughput-1k-mps-per-msp`

The bulk capability remains a proposed review/program control because the addendum itself records a
reconciliation issue with older “bulk not supported” wording. The 1,000 messages/second figure is a
provisional per-MSP target, not a published hard limit.

### Product naming

Verified public/marketing guidance requires the full “Apple Messages for Business” name and rejects
unapproved variants. The review clarification confirms that the full name has priority and “Apple
Messages” is the approved alternative when the full wording does not fit. “Apple Business” remains
forbidden because Apple launched a separate Apple Business product in April 2026.

### Item placement

- Guided opening and CSAT remain separate E items because atomic, demonstrable obligations are more
  auditable than the current broad E.10 umbrella.
- Brand coaching belongs in G as an Integration Review readiness control, not A, which covers the
  MSP's own Apple registration.
- Cross-channel fallback belongs in a new K section explicitly labeled MSP program/platform
  controls.
- Bulk invitation controls stay adjacent to C.18 as C.23 because they specialize Apple's Invitation
  capability, but J.1 must not treat review/program-class rows as canonical Phase 1 protocol facts.

## Human/Apple holds

- Original feedback artifact, date, reviewer/source, and content hash.
- Exact 365-day authority, timer reset events, and error response.
- Whether first/opt-out compliance copy has mandatory non-configurable elements.
- Exact approved unknown-contact label if the implementation cannot use the review-provided “Apple
  Messages contact.”

## Clarifications accepted after adversarial review

- “Apple Messages” is allowed when “Apple Messages for Business” does not fit.
- Invitation No produces no platform conversation/message; outbound remains blocked until a later
  user-initiated conversation.
- Apple has no RCS-versus-SMS fallback preference. This is a non-Apple-device destination/channel
  fallback—not AMB feature-capability fallback—and is an MSP/brand decision with channel-specific
  consent.
- Bulk capability is campaign/list orchestration over individually paced Invitation requests, not a
  separate Apple bulk API.
