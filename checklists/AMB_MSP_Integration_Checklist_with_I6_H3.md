<!-- MA working copy 2026-07-29: adds H.3 and I.6 (webhook delivery + tenant isolation). Source: madvamb-kb/docs/AMB_MSP_Integration_Checklist.md. Not the authoritative KB copy. -->

---
tier: reference
updated: 2026-06-25
source: Messaging Advisory Google Sheet "[Latest] 26_06_26_AMB_MSP_Integration_Checklist_Generic_v2" (Canonical v6.5); the sheet wins on disagreement
review-by: 2026-09-25
---

# AMB MSP Integration Checklist (Generic, Canonical v6.5)

Version: Canonical v6.5. Updated 2026-06-25, review refined with generic requirements from Apple's integration review. Source of truth: the Messaging Advisory Google Sheet "[Latest] 26_06_26_AMB_MSP_Integration_Checklist_Generic_v2 (Canonical v6.5, review refined)" on the MessAdv shared drive. This Markdown copy exists so MADVAMB can answer checklist questions; when the sheet and this file disagree, the sheet wins and this file should be regenerated.

Each item lists: the requirement, what to do, key considerations, the MSP Integration Guide reference, the verification method Apple accepts, and any review note from the Apple integration review.

Verification method legend: Apple Supplied (Apple provides it), 3 Way Meeting (walked through with Apple and Messaging Advisory), Postman (API level proof), Provide Code (code inspection), UX Testing (demonstrated on device), Verbal on Apple Policy (policy discussion with Apple).

> **INTERIM SOURCE CORRECTIONS (2026-07-21).** A consistency audit against the REST spec (`AMB_REST_API_spec.md`) found conflicts in items C.3, C.9, A.5, C.18, H.1, H.2, and D.2, all resolved in favor of the REST spec. These are corrected inline below with `[Corrected …]` citations so the live KB serves the right facts now. **The true source is the Google Sheet; these edits MUST be reconciled into that sheet or they will be lost on the next regeneration.** See the companion "Sheet cell edits" handoff.

## Section A. Registration and MSP onboarding

### A.1 Register at register.apple.com

Requirement: create the MSP organisation profile on Apple Business Register and begin the MSP onboarding lifecycle. register.apple.com is the only entry point. The Apple Business Register account that owns the MSP profile is distinct from any Apple Developer account the MSP also needs for Apple Pay; do not conflate the two. The organization primary contact in Apple Business Register must be a legal representative of that organization, using a corporate email address, with admin access. The MSP may be listed as a team member on the organization account.
Reference: MSP Integration Guide §28.1, §28.7. Verification: Apple Supplied. Review note: focus area during the review.

### A.2 Pass capability and go to market review

Requirement: submit the Phase 1 platform capability assessment and the go to market plan to Apple's regional AMB team for review. Apple's regional AMB team is the gatekeeper. Be ready to justify automation coverage, agent availability, brand pipeline, and pricing posture. Phase 1 is the gate; Phase 2 and Phase 3 unlock additional capability tiers later.
Reference: MSP Integration Guide §28.7. Verification: 3 Way Meeting. Review note: Apple might have questions about the topic.

### A.3 Receive Apple API credentials

Requirement: obtain the MSP ID (also called CSP-ID) and the Messaging API secret key from Apple after onboarding is approved. The MSP ID is the value carried in iss (MSP to Apple) and aud (Apple to MSP) on every JWT. The secret key signs every outbound JWT. Treat the secret as production credential material; do not commit, log, or share across environments.
Reference: MSP Integration Guide §4.2, §4.4, §28.7. Verification: Apple Supplied. Review note: fine with Messaging Advisory checking it.

### A.4 Confirm Phase 1 platform capability requirements

Requirement: verify the platform meets every item in Apple's Phase 1 capability matrix (bot builder, message templates, attachment handling, capability detection, agent console, and similar) before booking the Phase 1 demo. Phase 1 has a fixed capability checklist. Gaps surface late and cost weeks; pre validate every item against the current build state, not against the planned end state.
Reference: MSP Integration Guide §28.7 (MSP Capability Requirements). Verification: 3 Way Meeting. Review note: required but not needed for the review.

### A.5 Plan multi day approval dependencies

Requirement: Apple Developer account enrolment, Apple Pay Merchant ID, Payment Processing Certificate, OAuth endpoint approval, and the iMessage app demo all have multi day lead times that block Phase 1 sign off. If a third party processor is the merchant of record for any existing payments product, a separate Apple Developer enrolment is still required for AMB Apple Pay. The brand/merchant owns the Apple Developer account and the Apple Pay Merchant ID and shares the payment certificates with the MSP. [Corrected 2026-07-21 to match both setup guides (Registration & MSP Registration Setup Guides); the prior "MSP must hold its own enrolments" claim was inverted.]
Reference: MSP Integration Guide §28.7 (Multi-Day Approval Items), §16.14, §17.2. Verification: Postman or test code.

### A.6 Honour the pre launch advertising embargo

Requirement: until Apple grants public launch, no marketing, screenshots, brand mentions, or capability claims may appear in any public channel. The embargo covers website, decks, social, partner comms, and press. A breach can delay or revoke launch approval. Internal only material is permitted; external is not.
Reference: MSP Integration Guide §28.8. Verification: Verbal on Apple Policy.

## Section B. Core API transport layer

### B.1 Implement the eight MSP REST API endpoints

Requirement: implement all eight documented endpoints: outbound /message, inbound /message, /preDownload, /preUpload, the returned upload URL, /decodePayload, /authenticate, and /constructPayload. All endpoints under mspgw.push.apple.com use HTTPS. The inbound /message endpoint is hosted by the MSP at a URL registered with Apple; the rest are Apple hosted. /constructPayload is required even if App Clips rich links are not heavily used.
Reference: MSP Integration Guide §3. Verification: Postman.

### B.2 Implement HS256 JWT signing with 1 hour rotation

Requirement: sign every outbound request with an HS256 JWT using the Messaging API secret; iat must be within the last hour at the receiving end. alg is fixed at HS256. iss is the MSP ID on outbound; aud is the MSP ID on inbound (from Apple). Apple rejects tokens with iat older than 1 hour, so cache and rotate tokens accordingly. Reject inbound JWTs that fail signature, iat freshness, or aud match.
Reference: MSP Integration Guide §4.1, §4.2, §4.3, §4.4. Verification: Postman.

### B.3 Set every required HTTP header on every outbound message

Requirement: populate Authorization, id, Source-Id, Destination-Id, Content-Type, and the message type specific headers (interactive headers, attachment headers) on every outbound request. Headers are message type dependent. Interactive messages require additional headers above the standard set. Attachment flows require the encryption headers on /preUpload and /preDownload. Missing headers can cause the message to be rejected silently in some cases.
Reference: MSP Integration Guide §5. Verification: Provide Code.

### B.4 Populate the common HTTP body fields correctly

Requirement: every outbound message body must carry the common fields (id, sourceId, destinationId, type, plus the type specific payload). id must be a unique UUID per message. sourceId and destinationId carry opaque user identifiers, never phone numbers or emails. Reuse of id is treated as a replay and rejected.
Reference: MSP Integration Guide §6. Verification: Provide Code.

### B.5 Implement GZIP request body handling on inbound

Requirement: inbound webhook requests from Apple may arrive gzip compressed; the MSP must decompress before parsing. Inspect Content-Encoding: gzip and decompress before JSON parsing. Failing to handle this surfaces as intermittent body parse errors only under load.
Reference: MSP Integration Guide §28.5. Verification: Postman.

### B.6 Implement the 5 step inbound message validation

Requirement: every inbound request must pass: JWT signature verification, JWT iat freshness check (within 1 hour), required header presence, body schema validation, and id uniqueness with replay protection. Apple expects all five checks. Failure to enforce iat freshness or id uniqueness is a common review finding. Keep a short window id replay cache (1 hour matches the iat window).
Reference: MSP Integration Guide §28.5. Verification: Postman.

### B.7 Restrict inbound ingress to 17.0.0.0/8

Requirement: Apple's webhook traffic originates from the 17.0.0.0/8 CIDR; restrict the inbound /message endpoint to that range at the edge. Apply at the WAF or load balancer, not inside the application. 17.0.0.0/8 is an Apple owned block but is large; combine with JWT verification for defence in depth.
Reference: MSP Integration Guide §28.5. Verification: Postman.

### B.8 Honour the Opaque ID identity model

Requirement: sourceId and destinationId on organic AMB are opaque tokens issued by Apple. Never treat them as, transform them into, or persist them alongside real world identifiers (phone, email, customer ID) outside of an authenticated linkage. Opaque IDs are stable per user brand pair but are not reversible. Logging or analytics pipelines that flatten sourceId into a join key against PII break Apple's privacy contract. Account linking happens via the channel settings landing page, not via id parsing.
Reference: MSP Integration Guide §31.1. Verification: Provide Code.

## Section C. Required features

### C.1 Receiving and sending messages

Requirement: send and receive plain text, international characters, and emojis in both directions. UTF-8 throughout. Validate that emoji surrogate pairs survive serialisation in the agent console, mobile SDK (if any), and logs. Required for both bot and live agent.
Reference: MSP Integration Guide §7, §6, §2. Verification: Postman.

### C.2 Receiving and sending attachments and wallet passes

Requirement: send and receive attachments up to 100 MB using the /preUpload and /preDownload flows with AES CTR per attachment encryption. 100 MB is a hard ceiling per attachment. Encryption is mandatory and uses a per attachment symmetric key transported in the message body, not in HTTP headers. Use the self test vectors in the spec to validate the crypto end to end before submitting for review. Includes wallet passes.
Reference: MSP Integration Guide §11, §11.6, §11.9. Verification: UX Testing.

### C.3 Tapback reactions

Requirement: detect inbound user tapbacks (Loved, Liked, Disliked, Laughed, Emphasized, Questioned) including on interactive payloads, plus stickers and emoji reactions. Inbound only; the MSP does not send outbound tapbacks. Reactions arrive as an ordinary `type: text` message with a new id and carry no original message id; they correlate only by best-effort body text (interactive reactions read "Liked 1 Business Message" and identify no specific message), parsing is locale dependent, and per Apple you display the text as is. [Corrected 2026-07-21 vs `AMB_REST_API_spec.md` message model (type/id fields); the prior "reference the original message id and thread back" claim is unsupported by the spec.]
Reference: MSP Integration Guide §9. Verification: Postman.

### C.4 Receiving Leave Conversation messages

Requirement: when the user leaves the conversation, notify both the live agent and any automated agent, and stop sending further messages on that thread. Leave Conversation is a hard stop. Any outbound after this point is a policy violation and may also be rejected by Apple. The bot or agent must be informed so it does not queue follow ups.
Reference: MSP Integration Guide §7, §21, §27.5. Verification: Postman.

### C.5 Rich Link messages

Requirement: every URL sent by an automated or human agent should be sent as a rich link with title, image, and URL, rather than as bare text, and all examples must render. Apple expects rich link rendering for all URLs, not just marketing links. Auto generated rich links have specific image and metadata requirements; meet them or supply a manually constructed RichLinkData payload.
Reference: MSP Integration Guide §23, §23.9. Verification: Postman. Review note (Messaging Advisory): add fallback information.

### C.6 Quick Reply messages

Requirement: send a single select interactive picker with two to five items (at least two options). Constraint: 2 to 5 items inclusive. Use Quick Reply for short, mutually exclusive choices; use List Picker when more than 5 options or icons and sections are needed.
Reference: MSP Integration Guide §13. Verification: Postman.

### C.7 List Picker message

Requirement: support single select, multi select, multi section, icons, and images on both sent and received list pickers. Cover the matrix of variants in the Phase 1 demo, not just the simplest case. Icons and images have separate size and format constraints; meet both.
Reference: MSP Integration Guide §14. Verification: Postman.

### C.8 Time Picker message

Requirement: send a time picker with multiple time slots, optional location information, and icons. Time slots, locations, and icons are all expected in the demo. Time zones must be handled correctly; surface the agent or bot's intended zone explicitly in the payload.
Reference: MSP Integration Guide §15. Verification: Postman.

### C.9 Apple Pay message

Requirement: send Apple Pay payment requests with merchant session handoff, ApplePayPaymentRequest payload, line items, and shipping methods. Apple Pay requires the Merchant ID registered on the AMB account before sending a request. The brand/merchant owns the Apple Developer account and the Apple Pay Merchant ID and shares the payment certificates with the MSP. Payment Processing Certificate enrolment takes multiple days. Refunds are handled outside Messages for Business and are not an in-band required AMB feature. [Corrected 2026-07-21: (a) ownership matches both setup guides — brand/merchant owns the account and Merchant ID, shares certs with the MSP; (b) `AMB_REST_API_spec.md` Apple Pay section defines no in-band refund flow, so refunds are not a required AMB feature.] Prerequisites: Apple Developer account and Apple Pay Merchant ID configured; the Merchant ID must be on the AMB account first.
Reference: MSP Integration Guide §16, §16.14. Verification: Postman.

### C.10 Authentication message (new OAuth 2.0)

Requirement: implement the new inline OAuth 2.0 authentication flow, including Password AutoFill and channel settings registration of the OAuth endpoint. The new OAuth flow is required; the legacy flow has been deprecated since February 2023 and must not be implemented. Endpoint registration with Apple is a separate multi day step.
Reference: MSP Integration Guide §17, §17.2, §17.9, §17.10. Verification: Postman. Review note (Messaging Advisory): ensure the card calling OAuth is included in the flow.

### C.11 iMessage apps (custom InteractiveData)

Requirement: support custom iMessage apps using the CustomInteractiveData dictionary with the bid field identifying the iMessage app bundle. This is a Phase 1 demo gate. The bid value identifies a specific Apple approved iMessage app bundle; the demo must use a real, approved bid, not a placeholder.
Reference: MSP Integration Guide §18, §28.7. Verification: Postman.

### C.12 Form message

Requirement: support all Form types: splash, select with images (one and several selections), text input, picker, switch, date picker, and summary. Form Message requires iOS 18.4 or later. Fallback (Quick Reply, List Picker, Time Picker, or plain text) is required for devices below iOS 18.4, not optional. Drive the fallback from the parsed capability-list per device.
Reference: MSP Integration Guide §19, §19.6, §26. Verification: Postman.

### C.13 Construct Payload API

Requirement: use /constructPayload to generate App Clips, Apple Maps, and Apple Music rich link payloads server side from a URL. Each of the three payload types must be demonstrated. Required even if these rich link types are not a primary surface for the brand. The API is the only supported way to construct the payload; do not assemble it client side. The demonstration must use a working App Clip URL as evidence. Three sub checks: App Clips, Apple Maps, Apple Music, each demonstrated.
Reference: MSP Integration Guide §22. Verification: UX Testing.

### C.14 Typing indicator message

Requirement: show typing indicators in both directions (inbound from user, outbound from agent or bot). A typing indicator must be displayed before every message type, text or interactive. For messages sent by bots and for messages in sequence, use a 1 second typing indicator before each message, including back to back messages. The outbound typing indicator times out after 60 seconds; refresh or stop accordingly (the 60 second refresh is tracked under H.2, spec section 8.3). Sequencing rules apply when interleaved with regular messages. Not auto green: prove with Postman plus UX.
Reference: MSP Integration Guide §8, §8.3, §8.4. Verification: Postman plus UX Testing.

### C.15 Routing based on entry point parameters

Requirement: use the intentID and groupID attributes on inbound conversation start messages to route to the correct queue, bot flow, or agent skill. intentID and groupID are populated by the entry point, not by the message body. Routing must be deterministic and must respect the brand configured routing matrix. Required for both bot and agent. The use of intentID and groupID at entry points must be demonstrated taking different actions per parameter value.
Reference: MSP Integration Guide §10. Verification: UX Testing.

### C.16 Channel settings and landing page

Requirement: centrally host the brand's channel settings endpoint and a landing page that displays privacy policy and terms of use and supports account linking. The channel settings endpoint is per brand and registered with Apple. The landing page must show Privacy Policy and Terms of Use prominently, and must support OAuth account linking where used. The client landing page is required and must be reachable via the Connect button in Apple Business Register, under Test your Messaging Service Provider connection. The page should let the client understand setup, get support, and confirm the MSP connection.
Reference: MSP Integration Guide §25, §25.1, §25.2. Verification: UX Testing.

### C.17 Device capabilities

Requirement: parse the per device capability-list on every inbound and provide alternate handling for unsupported features. capability-list is per device, not per user. Cache against destinationId. It drives Form Message gating, Invitation eligibility, and any future feature behind a capability flag.
Reference: MSP Integration Guide §26, §26.1, §26.3. Verification: Postman.

### C.18 Invitation messages

Requirement: send business initiated notification messages using Apple managed templates to opted in users, addressed by phone number. Note the divergent identity model: organic AMB uses opaque IDs while Invitations address by phone number. Note the different 410 Gone semantic on Invitations: 410 means a missing or incorrect message-type header; opt-out is delivered as a separate inbound message, and undeliverable-by-user-preference is 404. [Corrected 2026-07-21 vs `AMB_REST_API_spec.md` §Response Codes + Invitations; the prior "410 = opted out of that brand's invitations" claim was unsupported.] Requires separate gated Apple approval; iOS 18.0 / macOS 15.0 minimum. Define the handling when the user declines the invitation (taps No), and confirm whether invitations can be sent via bulk upload.
Reference: MSP Integration Guide §20, §20.6.2, §20.8, §21. Verification: Postman.

### C.19 Block sending after the user closes the conversation

Requirement: when the user closes the conversation, AMB sends a close message to the MSP platform. The platform must block any agent, human or bot, from sending further messages until the user restarts the conversation. No typing or sending after close. Restore the agent send path only when the user restarts the conversation. Confirm the close message is received and that the send block is enforced across the platform.
Reference: `AMB_REST_API_spec.md` §Receiving a Closed Conversation (close message; HTTP 410 on send-after-close). Verification: UX Testing. Verified against spec: yes.
Verification: UX Testing.

### C.20 Channel settings must capture brand specific config for Apple Pay, iMessage App and Authentication payloads

Requirement: channel settings must capture brand specific configuration for Apple Pay, iMessage App, and Authentication payloads.
Reference: MSP Integration Guide §Channel Settings (brand-specific payload configuration). Verification: Provide Code. Verified against spec: yes.

### C.21 Brands must have a GUI to create and edit rich objects without writing JSON or code

Requirement: brands must have a GUI to create and edit rich objects (List Picker, Time Picker, Quick Reply, Form) without writing JSON or code. A demo is expected.
Reference: MSP Integration Guide §Business Tooling (GUI for rich objects). Verification: UX Testing. Verified against spec: yes.
Verification: UX Testing.

### C.22 The client landing page must be demonstrated via the Connect button in the AMB account

Requirement: demonstrate the client landing page starting from the Connect button in the AMB account; a test account is acceptable.
Reference: MSP Integration Guide §Landing Page / Connect Button. Verification: UX Testing. Verified against spec: yes.
Verification: UX Testing.

## Section D. Device capability detection and payload gating

### D.1 Parse capability-list on every inbound

Requirement: extract the capability-list array from every inbound message and persist it against the destinationId / sourceId for use on the next outbound. Capabilities can change between messages (the user switches device). Always use the most recent value, not a cached one from the initial conversation start.
Reference: MSP Integration Guide §26.1, §26.3. Verification: Postman.

### D.2 Maintain an OS minimum and device scope matrix

Requirement: maintain a matrix mapping each interactive feature to its minimum OS version and supported device scope (iPhone, iPad, Mac, Watch). Examples: Form Message requires iOS 18.4 or later and is limited to iPhone and iPad (the spec does not support Form on Mac or Watch); iMessage apps are likewise iPhone/iPad only; Invitations require iOS 18.0 or later. watchOS has no published capability-list row. [Corrected 2026-07-21 vs REST spec device scope; the example must not imply Form or iMessage-app support on Mac or Watch.] Update the matrix whenever Apple ships new feature OS floors. Drive the bot's branch logic and the agent console's affordance lock from this matrix.
Reference: MSP Integration Guide §26.2. Verification: Provide Code.

### D.3 Agent console capability lock

Requirement: the agent console must disable or hide UI affordances for any feature the recipient device does not support. Hard disable, not warn and allow. An agent should not be able to send a Form Message to an iOS 17 device by accident.
Reference: MSP Integration Guide §26.3. Verification: UX Testing.

### D.4 Bot or automation capability switcher

Requirement: bot flows must include a capability aware branch that swaps Form Message for Quick Reply, List Picker, Time Picker, or plain text when the recipient cannot render the preferred type. Switching must happen at send time, using the most recent capability-list, not at flow design time. Apple expects this demonstrated end to end in the review.
Reference: MSP Integration Guide §19.6, §26.3. Verification: UX Testing.

### D.5 Fallback decision tree

Requirement: document and implement a fallback decision tree for every interactive message type: preferred type, fallback type or sequence of types, and user facing copy variants. The tree is per feature and per OS floor; keep it versioned. Reviewers may ask to see the tree itself, not just its outputs. Explicit fallbacks: when Form is absent, send each question as a separate object; convert Select or Picker pages to a Quick Reply with up to 5 options, or a List Picker for longer lists; use a Time Picker in place of a Date Picker; send Input pages as a text message. The same use case must complete on a device that does not support the preferred feature.
Reference: MSP Integration Guide §26.3, §19.6. Verification: Provide Code.

## Section E. Policy, consent, conversational design

### E.1 Live agent availability (or exemption)

Requirement: by default, a live human agent must be available during stated business hours. The exemption to this rule is granted only by Apple's regional AMB team on a case by case basis. If no exemption is granted, the agent escalation path must reach a real human within business hours. If an exemption is granted, Section F replaces this with structured callback or email via form options.
Reference: MSP Integration Guide §27.1. Verification: Verbal on Apple Policy.

### E.2 Bot and automation rules

Requirement: the bot must identify itself as automated, must not impersonate a human, and must always provide a path to escalation (human or, under exemption, callback or email). Apple reviewers test this with explicit prompts such as "are you a bot?"; the bot must answer truthfully.
Reference: MSP Integration Guide §27.2. Verification: Verbal on Apple Policy.

### E.3 Messaging restrictions

Requirement: no SMS style marketing blasts. No unsolicited outbound. Outbound is permitted only as part of an ongoing user initiated conversation, or via approved Invitation Message templates. Approved Invitation templates are the only sanctioned business initiated message path; everything else is reactive. Reviewers actively look for unsolicited outbound.
Reference: MSP Integration Guide §27.3. Verification: Verbal on Apple Policy.

### E.4 Consent rules

Requirement: capture explicit opt in for any non transactional automated notifications, and persist the consent source and timestamp. Consent is per brand, per channel, per notification category. The MSP platform must surface the consent state to brand operators and to bot flows.
Reference: MSP Integration Guide §27.4. Verification: Verbal on Apple Policy.

### E.5 Opt out and Leave Conversation handling

Requirement: honour both the in band Leave Conversation message and the conventional opt out trigger words (STOP, UNSUBSCRIBE, QUIT). Both bot and live agent must stop sending immediately. Trigger words are case insensitive. Stop applies to the brand, not just the current thread. Re engagement after opt out requires a fresh opt in.
Reference: MSP Integration Guide §21, §27.5, §27.6. Verification: Verbal on Apple Policy.

### E.6 Trigger words

Requirement: implement Apple's trigger word matrix (HELP, STOP, AGENT, REPRESENTATIVE, and similar). Each maps to a defined behaviour: escalate, opt out, or contextual help. The default behaviour matrix is published by Apple. Brands may extend but not weaken it. Case insensitive matching; allow leading or trailing whitespace.
Reference: MSP Integration Guide §27.6. Verification: Verbal on Apple Policy.

### E.7 PII request protocol

Requirement: never request sensitive PII (full Social Security Number, full card number, government ID number, account password) in plain conversation. Use Authentication Message, Apple Pay Message, or Form Message instead. This is a hard rule. Agent console templates must enforce it; bot flows must route any such collection to the appropriate secure message type.
Reference: MSP Integration Guide §27.7. Verification: Verbal on Apple Policy.

### E.8 Brand privacy and Terms of Use display

Requirement: the brand's Privacy Policy and Terms of Use must be reachable from the AMB landing page and from the conversation entry context. Display is via the channel settings landing page. The conversation itself should not reproduce policy text in chat; it should link out to the canonical hosted page.
Reference: MSP Integration Guide §25.2, §27.8, §31.5. Verification: Verbal on Apple Policy.

### E.9 Forbidden in conversation language

Requirement: do not use "iMessage", "Apple Messages", or wording that implies Apple endorses the brand, inside conversation copy or templates. Reviewers screen template and bot copy for these terms. Use generic terms ("message us", "chat") instead.
Reference: MSP Integration Guide §27.9. Verification: Verbal on Apple Policy.

### E.10 Conversational design and agent etiquette

Requirement: follow Apple's conversational design guidelines: greeting, agent or bot identification, stated hours, response time expectations, clear handoff language, and notification opt in phrasing where applicable. Spec section §27.9 has detailed subsections covering live agent protocols, automated messaging, triage best practices, response quality, opt in language, and satisfaction surveys. Treat the whole §27.9 as in scope for the demo.
Reference: MSP Integration Guide §27.9. Verification: Verbal on Apple Policy.

## Section F. Human escalation under live agent exemption

Applicable only if a live agent exemption has been granted by Apple. Default deployments must provide a live human agent during business hours.

### F.1 Detect escalation intent

Requirement: the bot or its NLU layer must classify both trigger words (AGENT, REPRESENTATIVE) and free text intent signalling that the user wants a human (for example "talk to a person", "this isn't helping"). Trigger word matching is deterministic; free text intent uses the bot's NLU. False negatives are worse than false positives here; err toward escalation.
Reference: MSP Integration Guide §27.6, §27.9.3. Verification: Verbal on Apple Policy.

### F.2 Present a callback or email choice

Requirement: on escalation, present the user with a structured choice between a callback request and an email reply (collected via Form Message). Use Quick Reply for the binary choice; collect the supporting details (phone number, email, message) via Form Message with fallback to List Picker or plain text on older devices. The in channel handoff must be as seamless as possible; where a live agent is not available, the bot assists the user in composing and sending an email to the brand from within the conversation.
Reference: MSP Integration Guide §13, §19. Verification: UX Testing.

### F.3 Acknowledge the choice in the AMB thread

Requirement: after the user selects callback or email, send a confirmation message in the AMB thread stating what happens next and when. Be specific about the ETA (for example "a team member will call you within 2 business hours"). Vague acknowledgements are flagged by Apple reviewers.
Reference: MSP Integration Guide §27.9. Verification: UX Testing.

### F.4 Handle unclassified free text via clarification

Requirement: if the bot cannot classify a free text turn, ask a single clarification question. If the second turn also fails to classify, escalate per F.2 rather than looping further. One clarification turn maximum before escalation. Looping clarifications frustrate users and surface as a review finding.
Reference: MSP Integration Guide §27.9.3. Verification: UX Testing.

### F.5 Out of hours behaviour

Requirement: for escalations received outside business hours, queue the callback for the next business day and queue the email via form for review the next business day. State the timing explicitly in the thread. Both paths share the same out of hours rule. Do not pretend to be available; do not silently drop the request.
Reference: MSP Integration Guide §27.9.5. Verification: UX Testing.

### F.6 Optional email reply threading

Requirement (optional): when a human responds to the email via form request, thread the reply back into the AMB conversation so the user sees continuity in one surface. Not required by Apple, but materially improves the user experience when permitted by the brand's email system. If implemented, treat each emailed turn as a regular outbound AMB message subject to all standard rules.
Reference: MSP Integration Guide §27.9. Verification: UX Testing.

## Section G. Review submission pack (formerly Experience Review)

### G.1 Pre review preconditions

Requirement: before booking the review, all required features (Section C) are implemented, a sandbox brand is provisioned, the demo script is rehearsed, and both agent and bot are operational. Apple will reject incomplete submissions outright. Run a full internal dress rehearsal first, including a deliberate device capability fallback.
Reference: MSP Integration Guide §28.6. Verification: Verbal on Apple Policy.

### G.2 Five non negotiable UX requirements

Requirement: the submission must demonstrate: live agent escalation reachable (or the exempted callback and email path), opt out works end to end, no PII requested in plain conversation, consent is captured before any opt in notification, and capability aware fallback is shown live. These are tested every review; skipping any one is the most common failure mode.
Reference: MSP Integration Guide §28.6, §27. Verification: Verbal on Apple Policy.

### G.3 Screen recording, three dimensions

Requirement: record three end to end flows: bot flow (entry point through resolution or escalation), agent flow (entry point through agent resolution), and a capability flow that shows the same use case on a device that supports the feature and on a device that does not, demonstrating the fallback to Quick Reply, List Picker, Time Picker, or plain text in place of Form Message. Each recording must include the entry point and a Leave Conversation. Each must be one continuous take, not edited.
Reference: MSP Integration Guide §28.6, §28.6.1. Verification: Verbal on Apple Policy.

### G.4 Recording production method

Requirement: use Apple recommended recording methods (QuickTime mirroring from iOS, or direct iOS screen recording). Native resolution. No edits. Timestamps documented. Edited recordings are rejected. If two takes are needed, submit the second take in full, not a stitched composite.
Reference: MSP Integration Guide §28.6.1. Verification: Verbal on Apple Policy.

### G.5 Submit and iterate

Requirement: submit the pack via Apple Business Register and expect at least one iteration cycle with Apple's regional AMB team. Plan for the iteration. Allocate calendar time for review responses; reviewers usually return comments within a defined SLA but the back and forth can span weeks.
Reference: MSP Integration Guide §28.6, §28.7. Verification: Verbal on Apple Policy.

## Section H. Response codes, retry, timeouts

### H.1 Response code taxonomy

Requirement: implement and respect the published response code taxonomy. Apple publishes these /message response codes only: 200, 400, 401, 403, 404, 410, 500. On organic AMB, 410 Gone means the user closed the conversation, and "no longer reachable/available" is 404 (not 410). On Invitations, 410 means a missing or incorrect message-type header; opt-out arrives as a separate inbound message, and undeliverable-by-user-preference is 404. Apple publishes no 429; any rate-limit handling is an MSP-side inference (see DR-15), so do not list 429 as an Apple response code. Treat organic vs Invitation 410 as distinct states in the MSP data model. [Corrected 2026-07-21 vs `AMB_REST_API_spec.md` §Response Codes (L256-262).]
Reference: MSP Integration Guide §24, §20.8. Verification: Postman.

### H.2 Timeout and TTL matrix

Requirement: maintain a matrix of timeouts and TTLs by message type and flow stage: typing indicator 60 seconds, Apple Pay merchant session TTL (the spec uses an `expiresAt` epoch with no fixed published duration — do NOT assert "5 minutes"; verify against Apple before restating), attachment URL TTLs, and the ratchet between Apple, MSP, and CDN. [Corrected 2026-07-21: the "5 minute" Apple Pay session TTL is unverified; `AMB_REST_API_spec.md` Apple Pay uses an `expiresAt` epoch, not a fixed duration.] Mismatches between MSP timeouts and Apple's published values are a common review finding. Cite the spec values; do not improvise.
Reference: MSP Integration Guide §8.3, §30.2. Verification: Provide Code.

### H.3 Reliable, ordered, signed and revocable partner webhook delivery

Requirement: partner webhook events are created atomically with the business transaction and delivered under a documented at-least-once contract; each event carries a stable webhook-id, timestamp and verifiable Standard Webhooks signature; deliveries preserve per-conversation ordering, retry under a bounded policy, resist concurrent or stale workers via leases and fencing, support consumer dedup on webhook-id, and stop after endpoint deactivation. MSP-platform reliability control; Apple §24/§8.3/§30.2 are analogous Apple-facing context, not direct authority for the MSP-to-partner interface. [Added 2026-07-29 by MA verification; class PLATFORM_SAFETY, not Apple-normative.]
Reference: Cerebro Partner API (docs/partner-api.md); Standard Webhooks specification; analogous MSP Integration Guide §24, §8.3, §30.2. Verification: Provide Code (fault-injection delivery test).

## Section I. Security, privacy, constraints

### I.1 Opaque ID handling

Requirement: sourceId and destinationId are opaque tokens. Never persist them alongside personal identifiers outside of an authenticated linkage. Never use them as join keys against PII tables. Stable per user brand pair, not reversible. Account linking is via the channel settings landing page, not via id parsing. Logging fields and analytics pipelines must respect this.
Reference: MSP Integration Guide §31.1. Verification: Verbal on Apple Policy.

### I.2 Encryption posture

Requirement: TLS 1.2 or later for all in transit traffic. The Messaging API secret is stored in a secrets manager, never in source, logs, or environment files committed to a repository. Apply standard secret hygiene: rotation policy, access auditing, environment separation. Treat AMB credentials with the same posture as production payment credentials.
Reference: MSP Integration Guide §31.2. Verification: Postman.

### I.3 Attachment crypto

Requirement: implement AES CTR per attachment encryption with the key carried in the message body, not in HTTP headers. Decrypt inbound attachments on receipt; encrypt outbound before /preUpload. Use the self test vectors in the spec to verify the crypto end to end. Bugs here typically only show up on a specific file size or content type and are easy to miss without targeted tests.
Reference: MSP Integration Guide §11.6, §11.9. Verification: Verbal on Apple Policy.

### I.4 Message history is not stored at Apple

Requirement: Apple does not retain conversation history; the MSP is the system of record. Reflect this in brand facing documentation and in any data retention or compliance statements. Apple's privacy posture is that the conversation lives on the user's device and on the MSP's systems, not on Apple's. The brand and MSP own the retention policy. Any administrative access requirement (for example FERPA in education, or other regulated sector administrator access regimes) is the MSP's and brand's responsibility to satisfy, not Apple's.
Reference: MSP Integration Guide §31.3. Verification: Verbal on Apple Policy.

### I.5 Payload size constraints

Requirement: message body 10 KB maximum. Inline interactiveData 10 KB maximum (use interactiveDataRef plus /decodePayload above that). Attachments 100 MB maximum. 10 KB on interactiveData is the practical ceiling for List Picker and Form Message; large payloads must use interactiveDataRef. The 100 MB attachment ceiling is hard; for delivery of larger files (for example high resolution documents), use an external delivery surface and link to it via rich link rather than embedding.
Reference: MSP Integration Guide §11.7, §30.1. Verification: Postman.

### I.6 Partner delivery tenant isolation and secure destination handling

Requirement: every partner webhook endpoint, subscription, outbox event, retry and delivery is owned by exactly one brand; events are never delivered to, queried by, or replayed through another brand's endpoint, and the same isolation applies to the SSE firehose and journal-read APIs. Production destinations use HTTPS and are protected against SSRF, DNS rebinding and unsafe redirects. Apple attachment URLs, keys and signatures are not exposed in partner payloads (journal/log secret-minimization is broader; see I.3). MSP-platform security control; Apple's guide implies it through the opaque-ID privacy contract (§31.1) but does not specify the MSP-to-partner interface. [Added 2026-07-29 by MA verification; class MA_PROGRAM / PLATFORM_SAFETY, not Apple-normative.]
Reference: MSP Integration Guide §31.1 (Opaque ID / privacy), cross-ref I.1 and B.8; Standard Webhooks specification. Verification: Provide Code (two-brand integration + adversarial SSRF test).

## Section J. Important checks (Apple review refinements)

### J.1 Confirm platform capability requirements (pre launch gate)

Requirement: pre launch verification gate. Walk through every Phase 1 platform capability item and confirm it is implemented, tested, and demonstrable against the current build state. Phase 1 has a fixed capability checklist that the MSP's platform must support, including: a no code bot builder, message template library, attachment ingestion and delivery, capability-list parsing and gating, an agent console with capability lock, opt in and opt out lifecycle management, and the full set of required features in Section C. Re verify just before launch, not only at the Phase 1 demo.
Reference: MSP Integration Guide §28.7 (MSP Capability Requirements). Verification: 3 Way Meeting.

### J.2 Plan multi day approval dependencies (final gate)

Requirement: final pre launch verification gate confirming all multi day items are complete: Apple Developer account enrolment, Apple Pay Merchant ID, Payment Processing Certificate, OAuth endpoint approval, and the iMessage app demo. This is an intentional duplicate of A.5: A.5 is the planning gate (do these have lead time?); J.2 is the launch gate (are they actually done?). Both are needed; do not collapse them.
Reference: MSP Integration Guide §28.7 (Multi-Day Approval Items). Verification: 3 Way Meeting.

### J.3 The MSP connection in ABR is enabled by Apple manually, not automatically

Requirement: the MSP connection in Apple Business Register is enabled by Apple manually, and only once the MSP is actively working with Apple and Messaging Advisory. It is not automatic.
Reference: Apple onboarding / ABR enablement process (not a REST API item). Verification: Verbal on Apple Policy. Verified against spec: n/a (process).

### J.4 For the Integration Review, upload the demo video to Apple's Box folder, not via ABR

Requirement: upload the demo video to Apple's Box folder (https://apple.ent.box.com/f/1c623a9a22904757a0dccdbc83432f43), not via Apple Business Register. Apple reviews the video, then holds a live demo. This review was formerly called "Experience Review" and is now the Integration Review.
Reference: Apple Integration Review process (not a REST API item). Verification: Verbal on Apple Policy. Verified against spec: n/a (process).

### J.5 Connect button in the AMB account

Requirement: the client landing page must be demonstrated via the Connect button in the AMB account. (Restates C.22; kept because Apple called it out separately in the review.)
Reference: see C.22 (MSP Integration Guide §Landing Page / Connect Button). Verification: UX Testing. Verified against spec: yes.
Verification: UX Testing.
