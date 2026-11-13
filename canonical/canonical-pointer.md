# Canonical authority pointer

The Apple AMB canonical is the authority for compliance verdicts. Do NOT copy it into this repo.
Pin it per run and record the commit + checksum in the run provenance.

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
