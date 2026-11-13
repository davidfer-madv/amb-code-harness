# Apple review intake

Apple review feedback is evidence input, not automatically normative authority. Never paste a
recommendation directly into the checklist.

1. Copy `apple-review-template.md` to a dated file such as
   `2026-07-30-apple-integration-review.md`.
2. Identify the source artifact without copying confidential content unnecessarily. Record its
   date, origin, scope, SHA-256, storage reference, and access restrictions.
3. Extract each recommendation separately and map it to affected checklist item IDs and fields.
4. Classify it as `APPLE_NORMATIVE`, `MA_PROGRAM`, `PLATFORM_SAFETY`, or `LIVE_COMPATIBILITY`.
5. Resolve canonical claim IDs through the pinned canonical bundle. If unavailable or conflicting,
   stop before proposing checklist text.
6. Record full before/after text for Markdown and every affected CSV field. Classify the diff as
   strengthens, neutral, or weakens.
7. Any weakening requires authoritative supersession and explicit human approval. All other changes
   still require exact-diff human approval.
8. Apply approved changes to Markdown and CSV together, validate I.6/H.3 equivalence, and rerun
   `bin/install.sh` to refresh trusted policy hashes.

Do not describe an operational review recommendation as “Apple requires” unless direct,
authoritative evidence supports that wording.
