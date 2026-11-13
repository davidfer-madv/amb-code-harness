## Why

The harness has I.6 and H.3 requirements, but operators lack a repeatable way to extract those rows,
run a focused Maglev assessment, and intake Apple review feedback without prematurely changing the
authoritative checklist. This change makes that workflow reproducible while preserving canonical
authority, candidate isolation, and advisory-only outcomes.

## What Changes

- Add a deterministic command that extracts selected checklist items, including all CSV fields,
  without modifying the source checklist.
- Add a Maglev runbook that pins commit `4c7284b0777449dcd23822a09661fc825dda3287`, prepares an
  isolated read-only workspace, and scopes the first audit to tenancy (I.6) and partner delivery
  reliability (H.3).
- Add a dated Apple-review intake template that records source provenance, direct quotations or
  attachments by reference, affected checklist fields, authority class, conflicts, and proposed
  before/after text.
- Require canonical claim-closure verification and human approval before any proposed review note
  is applied to both checklist formats.
- Define synchronization checks so the Markdown and CSV representations cannot silently diverge.

Non-goals:

- No candidate-source mutation and no OpenSpec installation in Maglev.
- No execution of Maglev code outside a hermetic sandbox.
- No automatic compliance approval or checklist-status mutation.
- No assertion that I.6 or H.3 is Apple-normative; both remain MA/platform controls unless verified
  authoritative evidence says otherwise.
- No checklist note changes until the latest Apple review artifact is supplied and verified.

## Capabilities

### New Capabilities

- `checklist-item-extraction`: Reproducibly extract complete checklist rows by item ID.
- `focused-candidate-audit`: Prepare and conduct a pinned, read-only audit for selected checklist
  items while retaining the mandatory tenancy and adversarial evidence rules.
- `apple-review-intake`: Convert a supplied Apple review into a provenance-backed checklist proposal
  with authority classification, anti-weakening checks, and synchronized Markdown/CSV application.

### Modified Capabilities

None.

## Impact

- Shell surfaces: `bin/audit.sh`, a new checklist extraction command, and focused-audit operator
  documentation.
- Policy surfaces: `playbook/amb-code-analysis-playbook.md`,
  `prompts/audit-prompt-v2.md`, `policy/isolation-rules.md`, and
  `canonical/canonical-pointer.md` remain authoritative inputs and are not weakened.
- Checklist surfaces: `checklists/AMB_MSP_Integration_Checklist_with_I6_H3.md` and `.csv`; updates
  remain proposal-only until review provenance and canonical gates pass.
- Trust boundaries: harness-to-candidate filesystem, canonical-to-checklist authority,
  Apple-review evidence intake, and Markdown/CSV synchronization.
- Compatibility and rollback: existing full-audit commands remain unchanged. The new helper and
  runbook can be removed without changing candidate workspaces or checklist contents.
