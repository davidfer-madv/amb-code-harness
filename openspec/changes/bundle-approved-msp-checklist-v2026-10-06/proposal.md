# Proposal: bundle the approved MSP checklist v2026.10.06

## Status

Proposed for implementation. Remote publication remains an operator action.

## Problem

A clean clone of the audit harness records the approved MSP checklist version and checksum but has
no retained fallback copy if a team member cannot locate or access the separate `AMB-canonical`
checkout.

## Proposed change

1. Copy the approved `msp-conformance/v2026.10.06/checklist.json` into a versioned, immutable
   release directory in this repository.
2. Include its upstream provenance and a checksum manifest that identifies `AMB-canonical` as the
   authority.
3. Document the bundled copy as a checksum-verified fallback/reference, while keeping
   `AMB-canonical` as the normal audit source.
4. Add a deterministic integrity test that fails if the bundled artifact differs from its approved
   SHA-256 or internal item count.
5. Clarify that bundling is distribution, not authority transfer: new checklist versions still
   originate in `AMB-canonical` and require an explicit governed update here.

## Safety impact and trust boundaries

The trusted harness gains a reviewed fallback artifact. Candidate source, evidence and reports
remain outside the bundle and untrusted. The bundled file cannot be silently promoted by a moving
alias, and normal audit runs continue using and recording the exact `AMB-canonical` path, version
and digest.

Affected surfaces are `checklists/`, `README.md`, `canonical/canonical-pointer.md`,
`playbook/reusable-audit-operator-runbook.md`, `openspec/config.yaml`, tests and policy hashes. No
candidate, prompt adjudication rule or shell isolation behavior changes.

## Non-goals

- No candidate-source mutation or execution.
- No automatic compliance approval or authoritative-checklist update.
- No copy of the full canonical claim-closure corpus.
- No switch of the normal audit workflow away from `AMB-canonical`.
- No moving `latest` file or implicit checklist selection.
- No commit, push, pull request or other remote mutation.

## Compatibility and rollback

Existing audits may continue supplying another explicitly approved checklist path. Removing the
bundled release and restoring the external path in documentation rolls back the change without
altering candidate snapshots or prior provenance.
