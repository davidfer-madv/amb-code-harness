# Canonical authority pointer

The Apple AMB canonical is the authority for compliance verdicts. Do NOT copy the canonical claim
closure corpus into this repo. Pin it per run and record the commit + checksum in run provenance.

The approved MSP checklist JSON is retained separately as a byte-identical, checksum-verified
fallback under `checklists/msp-conformance/v2026.10.06/`. `AMB-canonical` remains the normal source;
the fallback exists only so a team member can recover the exact approved checklist if that checkout
cannot be located or accessed.

- Source: madvamb-kb `docs/AMB_Layer2_Canonical_v7_0.md` plus the verified answers, decision
  records, and gap register.
- Per run, record: canonical commit SHA + content hash used, and the exact approved checklist JSON
  version + SHA-256 supplied to `bin/audit.sh`. Never rely on the historical 76-item harness copy or
  a moving `latest` filename as the run authority.
- The adjudication unit is the per-item canonical CLAIM CLOSURE (the exact normative statement plus
  its definitions, adjacent error/timeout/ordering/security rules, and source rank), not the
  distilled checklist row alone.
- If the canonical is unavailable, stale, or checksum-invalid, compliance verdicts and checklist
  proposals are prohibited; report "not assessed against canonical."
