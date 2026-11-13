# Adversarial review: Apple feedback delta to the AMB MSP Integration Checklist

Reviewed read only against the supplied intake, the draft mapping, the Canonical v6.5 working copy, and the five canonical addenda excerpts. No files touched, no tools run, no candidate source inspected.

`★ Insight ─────────────────────────────────────`
* This checklist already encodes its own authority hierarchy: a header stating the Google Sheet wins on disagreement, inline `[Corrected 21 July 2026]` citations that resolve conflicts in favour of the REST spec, and class tags on H.3 and I.6 marking MSP controls as explicitly not Apple normative. A delta that does not use those three existing mechanisms is fighting the document's grain.
* H.2 contains the exact precedent this delta needs and ignores: the Apple Pay session TTL is recorded as an `expiresAt` epoch with a written instruction to **not** assert a duration. That is the house pattern for an unverified timer, and the 365 day claim is the same shape of claim.
* The most dangerous edits in a compliance checklist are never the new rows. They are the one word modality changes inside existing rows, because those rows are already trusted and already cited.
`─────────────────────────────────────────────────`

## Executive verdict

**ACCEPT_WITH_CHANGES**, conditional. If the corrections below are treated as optional, the verdict is **REJECT**.

Roughly half the delta is a legitimate clarification of rows that already carry canonical citations (C.14, C.19, E.4, E.5, C.16). That half can land. Four items must not merge in any form resembling the draft: the E.9 naming relaxation, C.24 bulk invitations, C.23 cross channel fallback as drafted, and H.4 as a standalone obligation. Four of eight intake safety gates are open, including original artifact identification and claim ID resolution, so nothing in this delta may carry an APPLE_NORMATIVE label today.

## Critical blockers

**B1. Three of the four cross verification claims cite evidence that is not in the supplied evidence set.** The intake asserts support from a use case experience best practices addendum dated 25 July 2026, an invitation bulk throughput guidance addendum dated 28 July 2026, and a throughput 1,000 messages per second per MSP addendum dated 28 July 2026. None of the five supplied canonical addenda are those documents. The supplied set is: actionable keywords including menu, collect key details before escalation, Experience Review checklist version 3.1, invitation subtitle approved format, and partner PR and marketing guidelines version 3.1. Every downstream row that leans on those three citations (E.11, E.12, C.24, and the 1,000 messages per second figure) is currently uncorroborated. This is the single largest authority defect in the package.

**B2. The E.9 naming relaxation contradicts verified Apple documentation and must be rejected.** The partner PR and marketing addendum, verified against an authenticated Apple session and dated 21 July 2026, states: use the full product name in any customer facing or public material, do not abbreviate to AMB in public, and do not use other variations. The Experience Review addendum lists incorrect product naming as an explicit fail signal. The draft would permit "Apple Messages" as shorthand on the authority of an unprovenanced transcription, against two verified addenda and against the existing E.9 prohibition. Under the intake's own authority handling rule, verified canonical wins.

**B3. The draft's own unknown contact label violates the rule the same row is trying to enforce.** The draft forbids "Apple Business" as a channel name and then adopts "Apple Messages contact" as a platform UI string. Under the verified marketing addendum, "Apple Messages" alone is an unapproved variation. The delta cannot forbid variations in one clause and ship one in the next.

**B4. The C.14 draft requires an action C.19 forbids.** C.19 states, verbatim, "No typing or sending after close." The draft's "every outbound payload ... must be preceded by a visible typing indicator" contains no carve out for the closed, left, opted out, or expired states. As written, an implementer following C.14 emits a typing indicator into a closed conversation and breaches C.19.

**B5. Phone number suppression cannot be cleared by an organic inbound without breaking B.8 and I.1.** The draft says to store invitation blocking state by normalized destination phone number and clear it on a qualifying later inbound event. On the organic path the inbound carries an Apple issued opaque ID and no phone number. Clearing the suppression therefore requires joining an opaque ID to a phone number, which B.8 and I.1 prohibit outside an authenticated linkage. The obligation as drafted is either unimplementable or a privacy violation.

**B6. Pre expiry re engagement is unsolicited outbound under E.3.** E.3 permits outbound only within an ongoing user initiated conversation or via approved Invitation templates. A message sent to a user silent for eleven months is neither. The draft's mitigation, "pre expiry outreach must not become unsolicited messaging," states an outcome without a rule and coaches brands toward the violation it disclaims.

**B7. C.24 resolves an open canonical question using absent citations.** C.18 currently carries the open action "confirm whether invitations can be sent via bulk upload." The draft converts that open question into a supported capability at scale, citing the two addenda from B1. An open question cannot be closed by a document that is not in evidence.

**B8. The delta targets a v6.5 artifact using v7.0 era addenda, and the prior handoff is unreconciled.** The checklist markdown is Canonical v6.5 dated 25 June 2026. The addenda bundle supersedes against the v7.0 canonical. Separately, the 21 July 2026 interim corrections to C.3, C.9, A.5, C.18, H.1, H.2, and D.2 carry an explicit warning that they must be reconciled into the Google Sheet or be lost on regeneration, and there is no evidence that reconciliation happened. Layering a second unreconciled delta compounds the drift, and every new row will be lost on the next regeneration. The intake's gate list names "Markdown and CSV" while the checklist header names the Google Sheet as source of truth; those are different artifacts.

**B9. Section C placement launders MSP controls into Apple requirements.** J.1 defines the Phase 1 gate as including "the full set of required features in Section C." Placing cross channel fallback and bulk campaign controls at C.23 and C.24 makes them Apple Phase 1 requirements by operation of J.1, regardless of the class label written underneath.

## Authority and classification corrections

| Draft row | Draft class | Corrected class and reason |
|---|---|---|
| E.9 naming | APPLE_NORMATIVE plus review attested | Split. Full product name and Apple branding rules are APPLE_NORMATIVE via the verified marketing addendum. The shorthand relaxation is **rejected**, not reclassified. The unknown contact label is MA_PROGRAM, unresolved. |
| C.6 Quick Reply | APPLE_NORMATIVE UX guidance | Downgrade to APPLE_REVIEW_GUIDANCE. Canonical C.6 defines the feature and its two to five bound; it does not mandate the feature for every bounded prompt. Partial genuine support exists in the Experience Review fail signal "text only experiences that don't leverage platform features." |
| C.14 typing | APPLE_NORMATIVE / review confirmed | Already canonical at §8.3 and §8.4, including one second, before every message type, and back to back coverage. This is a clarification, not a strengthening. The live agent extension and the payload enumeration are review attested. |
| C.2 upload errors | LIVE_COMPATIBILITY / PLATFORM_SAFETY pending | Accept the class. Add that the limits themselves are canonical at I.5 and must not be restated with new numbers. |
| C.16 and J.5 Connect | APPLE_NORMATIVE process/UX | The Connect button flow is canonical at C.16, C.22, and J.5. The **terms acceptance** step is new and review attested; display and reachability are what E.8 and C.16 actually require. Also, the canonical says Terms of Use, the draft says terms of service. Normalise to Terms of Use. |
| C.18 invitation lifecycle | APPLE_NORMATIVE plus review attested | The opaque ID versus phone number divergence, the 404 undeliverable by user preference semantic, the separate inbound opt out, and the invitation 410 header defect semantic are all canonical. The decline state machine is review attested and partly unattested. The split must be visible inside the row, not only in a class line. |
| E.4 consent | APPLE_NORMATIVE obligation | Correct for §27.4. "Apple may accept multiple collection channels" is review attested only. The record schema is MA_PROGRAM. Note the draft writes the statute as "TC/TPCA", which is garbled and unacceptable in a compliance row. |
| E.11 guided opening | APPLE_NORMATIVE UX guidance | Downgrade to APPLE_REVIEW_GUIDANCE. Real partial support exists in the actionable keywords addendum (menu is expected to surface the triage menu, not an agent) and in the Experience Review "no dead ends" item. The 70 percent figure has no authority and should not appear in the row at all, including as context. |
| E.12 CSAT | APPLE_NORMATIVE / review guidance | Genuine Apple support exists, but from the **wrong addendum**. The Experience Review checklist version 3.1 states verbatim that CSAT surveys use descriptive labels rather than 1 to 5 numbers, are presented as Quick Reply, and that surveys with many questions use Form Message. Recite that citation, not the absent one. |
| H.4 365 day | LIVE_COMPATIBILITY pending | Correct class, wrong instrument. Record in H.2 under the Apple Pay `expiresAt` precedent as an unverified duration with a do not assert instruction. Do not create a standalone obligation. |
| C.23 fallback | MA_PROGRAM / PLATFORM_SAFETY / LIVE_COMPATIBILITY | Class correct, placement wrong. Apple does not govern RCS or SMS at all; this is not merely "not a gateway protocol requirement," it is outside Apple's authority entirely. |
| C.24 bulk | APPLE_REVIEW_GUIDANCE plus MA_PROGRAM | Downgrade to UNRESOLVED pending B1 and B7. C.18 also states invitations require separate gated Apple approval; there is no evidence that approval covers bulk. |
| A.7 coaching | MA_PROGRAM informed by Apple review | Class correct. Placement wrong, and a real Apple citation exists that the draft missed: the Experience Review addendum instructs reviewing the Conversation Design Standards and Plan Your Customer's Journey pages with the MSP before implementation. |

One additional systemic correction: the draft invents verification methods outside the legend, including repository scan, timed device UX capture, state transition tests, consent ledger tests, and fault injection tests. The legend admits six values only. H.3 and I.6 already established the correct convention, mapping bespoke evidence to a legend value with a parenthetical, for example `Provide Code (fault injection delivery test)`. Every proposed row must follow that convention.

## Existing rows to modify

* **E.9** Replace wholesale. Wording below. Do not accept the draft.
* **C.14** Add the suppression carve out and a latency ceiling. Wording below.
* **C.18** Replace the state model. Wording below.
* **C.19** Accept the preflight strengthening, and add the missing reverse direction: a 410 received on send is authoritative and must reconcile local state, because the close webhook may be delayed or lost under the at least once contract in H.3. Add that queue purge covers scheduled CSAT, campaign invitations, and any re engagement job. Define "qualifying user restart" as an inbound message from the user on that conversation, and state that an opt out in force overrides a restart.
* **E.4** Accept the record schema. Fix "TC/TPCA" to TCPA. Add that a prior organic conversation is never evidence of opt in for invitations or notifications. Add that consent records are tenant scoped per I.6 and immutable append only.
* **E.5** Replace the reset clause. Wording below. Restore QUIT, the brand wide scope, the in band Leave Conversation obligation, and the E.6 matrix cross reference, all of which the draft silently dropped.
* **E.6** Add `menu` to the actionable keyword matrix and its mapping to the triage Quick Reply, per the actionable keywords addendum. This is adjacent to the delta but is directly implicated by E.11 and is verified canonical.
* **C.2** Scope the error taxonomy to the limits already stated in I.5 (10 KB body, 10 KB inline interactive data, 100 MB attachment). Replace "never expose keys, internal URLs, or secrets" with a cross reference to I.3 and I.6 rather than a restatement that can drift.
* **C.6** Change "every" to a bounded rule, add the mandatory introductory text before the interactive feature per the Experience Review addendum, and add that a Quick Reply tap used to capture consent is only valid opt in when the preceding disclosure and the E.4 record are both present.
* **C.11 and C.20** Restrict the rename to customer facing and brand facing copy only. Leave checklist row titles, the §18 reference, `bid`, and `CustomInteractiveData` untouched. Note that "app extension" alone is under specified on Apple platforms, where it names a broad class.
* **C.16** Accept the Connect flow strengthening with Terms of Use rather than terms of service, and mark terms **acceptance** as review attested pending confirmation, since C.16 and E.8 currently require display and reachability only. Normalise the location string to C.16's existing precise phrasing.
* **C.22** The draft never mentions this row and it is the direct duplicate of J.5. See merge section.
* **G.1** Absorb the brand coaching obligation here rather than creating A.7. See merge section.
* **H.1** Add a note that no published response code is defined for reachability window expiry, and that an MSP must not invent or assume one. This is required to stop H.4 from being implemented against a fabricated error.
* **H.2** Add the 365 day claim as an unverified row using the Apple Pay `expiresAt` precedent, with an explicit do not assert instruction.
* **J.1** Amend "the full set of required features in Section C" to exclude rows marked as MSP platform controls. Without this amendment, B9 is unfixable by class labels alone.
* **D.2, A.5, J.2** Confirm no rename is applied. All three name the iMessage app as an Apple process or device scope artifact.

## New rows to add

Provisional IDs only. All numbering must be reconfirmed against the Google Sheet before allocation, because this markdown is an MA working copy that already added H.3 and I.6 locally and may not match the sheet's row set.

* **E.11** Guided opening and tappable triage. Scope strictly to the opening triage mechanics. Cross reference E.2 for automation disclosure and E.10 for greeting rather than restating them. Strike the 70 percent figure entirely.
* **E.12** Resolution check and post interaction CSAT. Add the missing prohibition on sending CSAT after leave, close, opt out, or expiry, and cross reference D.4 and D.5 for the Form fallback rather than inventing new fallback language.
* **K.1** Cross channel fallback after invitation or delivery failure. Wording below.
* **K.2** Bulk invitation campaign controls. Wording below, held at PROVISIONAL.
* **H.4** Recommended **not** to be created. If the programme insists on a standalone row, the wording below is the only safe form, and it must ship with a PROVISIONAL status flag on the row itself, not merely a "pending" adjective inside the prose.

Section K is a new section for MSP platform controls that are not Apple requirements. If a new section is rejected, keep C.23 and C.24 as numbers but the J.1 amendment becomes mandatory rather than recommended, and each row must open with the sentence "Not an Apple Phase 1 requirement."

## Rows to merge or drop

* **Drop A.7.** Section A is the MSP's own registration and onboarding lifecycle with Apple across A.1 to A.6, not the MSP's onboarding of its brands. Fold the obligation into **G.1**, which already owns pre review preconditions, and cite the Experience Review addendum's instruction to review the Conversation Design Standards and Plan Your Customer's Journey pages with the MSP before implementation. Add that coaching collateral is itself subject to A.6 embargo and to the marketing addendum's Apple branding rules.
* **Collapse C.22 into J.5.** J.5 already says, in the file, "Restates C.22." Unlike A.5 and J.2, which are an intentional duplicate with a documented planning gate versus launch gate distinction, C.22 and J.5 are the same gate with no distinction. Keep one substantive row and make the other a pure pointer with no independent wording, or the delta will produce three divergent descriptions of one Connect flow across C.16, C.22, and J.5.
* **Move C.23 to K.1 and C.24 to K.2.** Per B9.
* **Do not create H.4 if H.2 can carry the claim.** Preferred outcome.
* **Merge the C.19 and E.5 suppression logic into one state model** referenced from both rows. Leave, close, STOP, decline, and expiry are currently five suppression concepts spread across C.4, C.19, E.5, C.18, and the proposed H.4 with no single precedence rule.

## Anti weakening and negative test corrections

The draft is missing eleven negative cases. Each must be an explicit prohibition with a test, not an implication.

1. No outbound of any kind, **including typing indicators, CSAT, and re engagement**, after close, Leave Conversation, opt out, or expiry.
2. No fallback to RCS or SMS after a decline, an opt out, or a 404 undeliverable by user preference. Fallback is permitted only for technical non delivery. The draft's "never silently fallback where a channel lacks consent" does not close this, because a user preference decline is a consent signal that the draft does not name.
3. No Authentication Message, Apple Pay Message, Form Message, attachment, attachment key, attachment URL, or PII collection may be represented on a fallback channel. E.7 makes this a hard rule and the draft omits it.
4. No invitation to a suppressed destination even when a campaign list includes it, and the suppression check must run per record at send time, not at list import.
5. No consent inferred from a prior conversation, a prior invitation acceptance, or an expiring reachability window.
6. No reset of notification or marketing consent by any inbound message. Only fresh documented opt in, per the existing E.5 sentence the draft dropped.
7. No interpretation of an invitation path 410 as an opt out. It is a missing or incorrect message type header, a sender defect. Misreading it suppresses a user permanently.
8. No join between the phone number suppression store and any opaque ID record. Per B5.
9. No forbidden naming variant in any localisation bundle, template, platform UI string, transcript, or emailed reply threaded under F.6.
10. No bulk send exceeding a brand's configured pacing even when aggregate MSP throughput allows it. The draft states an aggregate per MSP target and a per brand fairness goal with no allocation rule between them.
11. No CSAT before resolution and none after an unresolved abandonment.

Two further weakening notes. First, the draft's C.14 "at least one second" replaces the canonical's "1 second" with an unbounded floor, while the Experience Review addendum lists slow response times as an explicit fail signal. Chaining unbounded indicators across a multi payload response can fail the same review it is meant to pass. Second, the draft's E.5 phrase "the applicable state" is the most dangerous four words in the package, because it is readable as resetting notification consent on an inbound message.

## Field ready replacement wording

### E.9 Product, channel, and feature naming

**Requirement.** Correct Apple product naming and Apple branding across conversation copy, message templates, platform UI, brand facing documentation, onboarding collateral, marketing, and review materials.

**Description.** Use the full product name Apple Messages for Business in any customer facing or public material. Do not abbreviate to AMB in public. Do not use iMessage for Business, Messages Business, Apple Business, Apple Business Chat, Apple Messages standing alone, or any other variation. Do not use Apple logos, product images, or trademarks without prior written Apple approval; Apple supplied Messages for Business button assets must be used unmodified. Inside conversation copy and message templates delivered to the end user, continue to prefer generic wording such as "message us" or "chat", never use iMessage, and never imply that Apple endorses the brand. In brand facing and customer facing explanatory copy, "app extension" is acceptable in place of "iMessage app extension". In checklist rows, technical evidence, API payloads, and Apple process artifacts, retain Apple's exact terms, including iMessage app, the `bid` field, and `CustomInteractiveData`; A.5, J.2, D.2, C.11, and C.20 are not renamed. The default label for an unrecognised contact is unresolved: do not ship "Apple Business Contact", and do not ship any label using Apple Messages without "for Business", pending Apple confirmation.

**Key considerations.** The proposal to permit "Apple Messages" as acceptable shorthand is rejected. It rests on an unprovenanced transcription and contradicts a canonical addendum verified against an authenticated Apple session on 21 July 2026, which forbids other variations in customer facing and public materials, and contradicts the Experience Review fail signal for incorrect product naming. Naming violations also reach places implementers forget: localisation bundles, agent console labels, transcripts, and any reply threaded back under F.6. The pre launch embargo at A.6 governs whether the naming may appear publicly at all.

**Reference.** MSP Integration Guide §27.9. Canonical addendum, partner PR and marketing guidelines version 3.1, Marketing Guidelines, Naming and terminology and Apple branding, verified 25 July 2026. Canonical addendum, Experience Review checklist version 3.1, fail signals. Unknown contact label: no authority, unresolved.

**Verification Method.** Verbal on Apple Policy, plus Provide Code (static string scan across source, templates, localisation bundles, and platform UI asserting every forbidden variant is absent), plus UX Testing (device capture of conversation copy and of the brand operator console).

**Review Notes.** Contains a rejected relaxation; do not reinstate without an original Apple artifact that explicitly supersedes the 21 July 2026 marketing guidance. The unknown contact label is a residual question.

### C.14 Typing indicator message

**Requirement.** A typing indicator precedes every outbound payload, in every permitted sending state, without breaching the post close prohibition or the brand's stated response time.

**Description.** Show typing indicators in both directions. Every outbound payload from a bot, automation, or live agent, including text, attachment, Quick Reply, List Picker, Time Picker, Form, rich link, Authentication, and Apple Pay, is preceded by a visible typing indicator held for one second before the payload is sent, and back to back payloads each carry their own indicator. The indicator is itself an outbound action: it must be blocked by the same preflight check as any message under C.19, and must never be emitted after close, after Leave Conversation, after opt out, or into an expired reachability window. Total indicator time across a multi payload response must remain within the brand's stated response time expectation. The outbound indicator times out after 60 seconds; refresh or stop per H.2.

**Key considerations.** One second is a floor and a target, not an open ended minimum; the Experience Review lists slow response times as a fail signal, so an unbounded stack of indicators can fail the review it is intended to pass. For a live agent, the indicator should reflect real typing rather than a synthetic gate wherever the console can observe it. Test the production send sequence, not indicator support in isolation.

**Reference.** MSP Integration Guide §8, §8.3, §8.4. Cross reference C.19 and H.2. Live agent extension and the payload enumeration are review attested pending claim resolution.

**Verification Method.** Postman, plus UX Testing (timed device capture of a multi payload sequence, plus a close arriving mid sequence, asserting no indicator after the close).

**Review Notes.** Existing canonical already covers one second, every message type, and back to back. This edit is a clarification plus a safety carve out, not a new obligation.

### C.18 Invitation message lifecycle and suppression state

**Requirement.** A defined, tested state model for every invitation outcome, with suppression stored and cleared without crossing the opaque identifier boundary.

**Description.** Model each of the following as a distinct state with a distinct source signal: sent and pending; accepted, at which point Apple issues opaque identifiers and the conversation becomes organic; declined by the user tapping No; no response; opt out delivered as a separate inbound message; undeliverable by user preference returned as 404; and transport or sender defect, where a 410 on the invitation path means a missing or incorrect message type header and must never be interpreted as a user state or as an opt out. Before acceptance the MSP holds no Apple issued opaque identifier; the only retained keys are the MSP supplied destination phone number and the MSP's own message id, so a declined invitation cannot continue as a conversation. Store suppression against the normalized destination phone number in a store that is segregated from all opaque identifier records, and never join the two. Suppression may be cleared only by a fresh documented opt in under E.4, by a subsequent invitation path event that itself carries the destination phone number, or by an authenticated account linkage under C.16 and B.8. An organic inbound never clears invitation suppression, and does not need to, because organic inbound is user initiated and already permits a reply under E.3.

**Key considerations.** Whether tapping No generates any inbound signal to the MSP is unattested in the supplied canonical. If Apple sends nothing on decline, the MSP cannot distinguish declined from no response, and the decline suppression obligation is unimplementable as written; this is a blocking residual question. Suppression scope is per brand, not per campaign. Invitations require separate gated Apple approval and iOS 18.0 or macOS 15.0 minimum.

**Reference.** MSP Integration Guide §20, §20.6.2, §20.8, §21. REST spec Response Codes and Invitations, corrected 21 July 2026. Cross reference B.8, I.1, E.4, E.5. Canonical addendum, approved invitation subtitle format, July 2026. Decline state behaviour: review attested, unresolved.

**Verification Method.** Postman, plus Provide Code (state transition matrix covering all seven states and asserting no opaque to phone join exists in any query path or analytics pipeline), plus Provide Code (negative test asserting an invitation path 410 does not create suppression).

**Review Notes.** Preserves the 21 July 2026 correction that invitation 410 is a header defect. Contains one blocking residual question on the decline signal.

### E.5 Opt out, Leave Conversation, configurable compliance copy, and scoped reset

**Requirement.** Immediate brand wide cessation on any opt out or leave signal, per brand configurable compliance copy that cannot remove mandatory content, and reset rules scoped separately per suppression type.

**Description.** Honour the in band Leave Conversation message and the trigger words STOP, UNSUBSCRIBE, and QUIT, matched case insensitively with leading and trailing whitespace tolerated, in every configured locale, across bot, live agent, campaign, retry, replay, scheduled, and automation paths. Both bot and live agent stop immediately, and the stop applies to the brand, not only the current thread. First message and opt out compliance copy is configurable per brand, but configuration must not remove any mandatory disclosure, must not disable opt out processing or trigger word coverage, must not remove the automated agent disclosure required by E.2, and must be versioned and auditable. Reset is scoped, never global: conversational reachability may resume for the duration of a later user initiated conversation; invitation suppression clears only per C.18; and notification, marketing, or campaign consent is never reset by an inbound message and requires a fresh documented opt in under E.4. Where an opt out and a conversation restart are both in force, the opt out wins.

**Key considerations.** The single most likely defect is a reset rule written broadly enough to restore notification consent when a user simply replies. Trigger word matching must survive localisation, since compliance copy is configurable per brand and may be non English while the matcher is not. E.6's full matrix, including HELP, AGENT, REPRESENTATIVE, and menu, remains in force.

**Reference.** MSP Integration Guide §21, §27.5, §27.6. Cross reference E.2, E.4, E.6, C.4, C.18, C.19. Canonical addendum, actionable keywords version 3.1, for menu. Configurable compliance copy: review attested, unresolved.

**Verification Method.** Verbal on Apple Policy, plus Postman (trigger word coverage per path and per locale), plus Provide Code (race test with an opt out arriving against an in flight send and against a queued campaign, and a negative test asserting no inbound resets notification consent).

**Review Notes.** Restores QUIT, brand wide scope, and Leave Conversation, all dropped by the draft. Replaces the ambiguous phrase "the applicable state".

### H.4 Reachability window expiry (PROVISIONAL, do not merge as an obligation before claim resolution)

**Requirement.** Track the last qualifying inbound per conversation and treat a long reachability window as advisory only, without asserting a duration, an error code, or a re engagement right.

**Description.** Record the timestamp of the last qualifying inbound message per conversation and expose an approaching expiry signal to authorised brand operators only. The reported 365 day duration is user attested and unverified; make the window configurable, do not hard code it, and do not state it as an Apple fact in any brand facing material. Apple publishes no response code for reachability expiry, and 404 already means no longer reachable on organic, so an expired conversation is not reliably distinguishable from an unreachable user; do not invent or assume a code. The local timer is advisory: it must never suppress an otherwise permitted send, and must never authorise a send that consent or suppression rules forbid. No automated outbound may be generated to the end user on the basis of an approaching expiry. Permitted responses to an approaching expiry are: notify the brand operator internally; send an approved Invitation template where invitation eligibility, gated Apple approval, and a current opt in record all hold; or reach the user on another channel with that channel's own independent consent. Note also that Apple retains no conversation history under I.4, so window expiry does not license purging the MSP's own system of record.

**Key considerations.** Which inbound events qualify is undefined. Tapbacks arrive as ordinary text type messages with new ids per C.3; whether a tapback, a read signal, a typing indicator, or an opt out resets the window is unknown. An opt out that resets the timer while forbidding sends is a live contradiction, so consent state must take precedence over window state in all cases. The term "gateway session" does not exist in the canonical and collides with the JWT lifetime in B.2; use a defined term. No integration plane can verify a 365 day boundary against Apple within any review cycle, so verification proves only the MSP's own timer.

**Reference.** No canonical authority. Adjacent: MSP Integration Guide §24 and §30.2, H.1 response code taxonomy, H.2 TTL matrix, E.3 messaging restrictions, I.4. Class LIVE_COMPATIBILITY, PROVISIONAL.

**Verification Method.** Provide Code (injectable clock boundary test at the configured window, plus clock skew and daylight boundary cases, plus a negative test asserting no user facing outbound is generated by the expiry signal, plus a precedence test asserting consent state overrides window state).

**Review Notes.** Recommended treatment is a row in H.2 under the Apple Pay `expiresAt` precedent rather than a standalone obligation. The draft's "coach or automate a pre expiry re engagement message" is rejected as unsolicited outbound under E.3.

### K.1 Cross channel fallback after invitation or delivery failure (MSP platform control, not an Apple requirement)

**Requirement.** Fallback to a registered RCS channel and then SMS only on technical non delivery, only with independent channel specific consent, and never carrying Apple specific content.

**Description.** Not an Apple Phase 1 requirement; Apple does not govern RCS or SMS. Fallback is permitted only where delivery failed for technical or capability reasons. Fallback is prohibited after a decline, after any opt out, after Leave Conversation or close, and after a 404 undeliverable by user preference, all of which are user signals that fallback would circumvent. Each destination channel requires its own registration and its own recorded consent under E.4; the presence of Apple Messages for Business consent is never sufficient. Authentication Messages, Apple Pay Messages, Form Messages, attachments, attachment encryption keys, attachment URLs, and any secure PII collection must never be represented on a fallback channel, per E.7, I.3, and I.5; where a payload cannot be safely downgraded, do not fall back. Define an explicit RCS delivery wait before SMS, and guarantee deduplication so a late RCS success cannot produce a double send. Opt out state, audit trail, and purpose must be maintained per channel and reconciled, and a stop on any channel must be evaluated against the brand wide rule in E.5.

**Key considerations.** The ordering of RCS then SMS has no supplied authority and is an MSP product decision. SMS and RCS carry their own regulatory regimes, and the wording in E.4 that TCPA phrasing is not itself proof applies with equal force here. F.6 already sets a precedent for content leaving the Apple thread and should be read alongside this row.

**Reference.** No Apple authority. Cross reference E.3, E.4, E.5, E.7, I.3, I.5, I.6, C.18, F.6. Class MA_PROGRAM, PLATFORM_SAFETY, LIVE_COMPATIBILITY.

**Verification Method.** Provide Code (cross channel integration test with per channel consent fixtures, negative tests asserting no fallback after decline, opt out, close, or 404 user preference, a content class test asserting Authentication, Apple Pay, Form, and attachment payloads never cross, and a deduplication test on late RCS success), plus Verbal on Apple Policy to confirm Apple raises no objection to the practice.

**Review Notes.** Placement outside Section C is deliberate: J.1 would otherwise make this an Apple Phase 1 requirement.

### K.2 Bulk invitation campaign controls (PROVISIONAL, MSP platform control)

**Requirement.** Consented, paced, cancellable, auditable invitation campaigns, held provisional until bulk support and throughput are confirmed by Apple.

**Description.** Not an Apple Phase 1 requirement, and bulk invitation support is an open question in C.18 that this row does not close. Where bulk is permitted, require per record consent validation at send time and not only at list import, per record suppression checks against the C.18 store, deduplication, resumable batching, progressive ramp up, staggered submission, response and status monitoring, bounded retries, immediate cancellation that purges queued work, per brand pacing that binds independently of any aggregate ceiling, and an auditable per record result. Bulk capability never waives E.3, E.4, or E.5: an opt out arriving mid campaign must purge that record's queued work before any further send is attempted, using the same preflight path as C.19. Apple publishes no 429 and any rate limit inference is MSP side per H.1, so throttling will surface as errors or silent loss rather than a documented signal; treat any aggregate throughput figure as unverified and configurable. Coordinate large or time sensitive sends with Apple before execution.

**Key considerations.** C.18 states invitations require separate gated Apple approval; there is no evidence that approval extends to bulk. The reported 1,000 messages per second aggregate per MSP figure is uncorroborated in the supplied evidence and conflicts operationally with per brand fairness unless an allocation rule is defined. At scale, the distance between an approved invitation campaign and the SMS style marketing blast prohibited by E.3 is procedural, not technical, so the consent and pacing controls are the only thing holding the line.

**Reference.** MSP Integration Guide §20, §20.8, §21, §27.3, §27.4. H.1 on the absence of a published 429. Bulk support and throughput figures: no supplied authority, unresolved. Class MA_PROGRAM, PLATFORM_SAFETY, PROVISIONAL.

**Verification Method.** Postman, plus Provide Code (large list pacing, per brand fairness, cancellation, fault injection, and an opt out race test asserting queued records are purged before send), plus Verbal on Apple Policy (confirm bulk is within the gated invitation approval and confirm any throughput ceiling).

**Review Notes.** Do not merge as a capability statement while B1 and B7 stand. Until then this row documents controls that would apply if bulk is confirmed.

## Residual questions requiring Apple or human confirmation

1. Where is the original Apple feedback artifact, what is its date, who delivered it, and what is its SHA 256? Four intake safety gates depend on this, and no row may carry an APPLE_NORMATIVE label until it is answered.
2. Do the three cited addenda on use case experience best practices, invitation bulk throughput, and 1,000 messages per second per MSP exist? If so, supply them. If not, E.11, E.12, and K.2 lose their stated support.
3. Does Apple explicitly permit "Apple Messages" as shorthand in any surface, and if so does that supersede the 21 July 2026 marketing guidance? Absent a superseding artifact, the answer is no.
4. What is the exact approved label for an unrecognised contact in the platform UI?
5. Does tapping No on an invitation generate any inbound event to the MSP, and if not, how is decline distinguished from no response?
6. Is the reachability window genuinely 365 days, is it measured from the last inbound of any type, and which inbound events qualify as a reset? Do tapbacks, typing indicators, read signals, and opt outs reset it?
7. Which published response code does Apple return on a send into an expired window, given that H.1 lists only seven codes and 404 already means no longer reachable?
8. Does the gated invitation approval in C.18 cover bulk sending, and what is the actual throughput ceiling and its unit of measurement?
9. Does the Connect flow include an affirmative terms acceptance step, or only display and reachability as C.16 and E.8 currently state? Terms of Use or terms of service?
10. Is per brand configurable first message and opt out compliance copy acceptable to Apple, and which elements are mandatory and non removable?
11. Human decision required: create Section K, or keep C.23 and C.24 with the J.1 amendment?
12. Human decision required: were the 21 July 2026 interim corrections reconciled into the Google Sheet? If not, this delta should not proceed until they are, or both deltas will be lost on regeneration.
13. Human decision required: are the provisional IDs E.11, E.12, H.4, K.1, and K.2 actually free in the Google Sheet, which may hold rows absent from this working copy?

Two things the delta got right and should keep: the C.19 preflight framing, which correctly stops the platform from discovering the closed state via a 410, and the refusal to encode the 70 percent figure as a threshold.

This is the chat draft, as required before any branded output. Say the word and I will run `/brand-it` to produce the branded version, and I can produce an unbranded copy alongside it if you want both.

