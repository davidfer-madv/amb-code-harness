# Design: immutable bundled checklist release

## Authority and data flow

`AMB-canonical` remains the upstream authority and the normal audit input. The approved JSON and
provenance are copied into `checklists/msp-conformance/v2026.10.06/` with a harness-owned checksum
manifest. The copy is a synchronized fallback/reference for a team member who cannot locate the
canonical checkout; it is not an automatically selected audit default.

If the fallback is needed, the operator verifies its fixed digest and explicitly supplies its path
to `bin/audit.sh`, which records its resolved path and digest as before.

There is no `latest` symlink or automatic discovery. A future release requires a separate reviewed
copy/update so audits cannot silently change authority.

## Integrity and failure behavior

A unit test checks the fallback copy's fixed approved SHA-256, version, declared/actual item counts, provenance
approval status and provenance version. Any content drift fails validation and therefore fails the
GitHub-readiness gate. A missing or invalid bundle prohibits a verdict; operators must not fall back
to an unverified checklist.

## Trust boundaries and write scope

Only trusted harness documentation, tests, OpenSpec files and the versioned checklist bundle are
written. Nothing below `workspaces/<candidate>/src`, no customer evidence and no external canonical
repository is changed. The upstream provenance is informational evidence about the release; it is
not executable instruction.

## Canonical claim closure

The checklist row remains only the reporting unit. The external canonical claim closure is still
required for adjudication, as specified by the audit playbook. Bundling the checklist does not copy
or replace that authority and does not make the fallback the normal audit source.
