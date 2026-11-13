# Adversarial review task: Apple feedback checklist proposal

Act as an independent, hostile checklist and authority reviewer. You are reviewing a proposed delta
to an Apple Messages for Business MSP integration checklist. You must not edit files, run tools,
inspect candidate code, or assume anything beyond the supplied input.

## Review goals

1. Identify direct contradictions between the current checklist, supplied Apple-feedback
   transcription, and canonical/addenda excerpts.
2. Detect duplicated items, misplaced section IDs, obligations incorrectly combined into one row,
   and existing rows that should be modified rather than duplicated.
3. Challenge authority laundering. Separate APPLE_NORMATIVE facts from direct-review guidance,
   LIVE_COMPATIBILITY, MA_PROGRAM, and PLATFORM_SAFETY controls.
4. Detect weakening: removed scope, weaker modality, missing negative cases, missing verification
   planes, or wording that could permit unsolicited messaging, consent bypass, cross-channel
   leakage, or sends after close/opt-out.
5. Challenge the technical details:
   - Does a declined invitation truly mean no opaque ID and what key remains?
   - Is a “No” response the same as decline or a distinct inbound event?
   - What exactly resets invitation/contact blocking state?
   - Does a 365-day expiration timer have sufficient authority and a defined error?
   - Could pre-expiry re-engagement violate the no-unsolicited-outbound rule?
   - Is RCS→SMS fallback an Apple rule or an MSP omnichannel recommendation?
   - Does bulk invitation support conflict with no marketing blasts, consent, or throughput?
   - Are naming corrections over-broad where Apple’s technical schema still says iMessage app?
6. Review verification methods. Every proposed obligation must have enough static, contract,
   integration, UX/human, security, concurrency, timing, and negative evidence planes.
7. Recommend a reconciled item map with exact existing IDs to modify and provisional new IDs.
8. Provide field-ready wording for any row whose draft is materially unsafe or ambiguous:
   Requirement, Description, Key Considerations, Reference, Verification Method, Review Notes.

## Output format

- Executive verdict: ACCEPT / ACCEPT_WITH_CHANGES / REJECT
- Critical blockers
- Authority/classification corrections
- Existing rows to modify
- New rows to add
- Rows to merge/drop
- Anti-weakening and negative-test corrections
- Field-ready replacement wording
- Residual questions requiring Apple or human confirmation

Treat the feedback transcription as a user-attested Apple review pending original-artifact
provenance. Do not invent citations or call a statement Apple-normative merely because the user
attributes it to Apple.
