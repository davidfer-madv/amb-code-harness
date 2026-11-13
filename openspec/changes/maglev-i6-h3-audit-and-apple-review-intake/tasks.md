## 1. Checklist Extraction

- [x] 1.1 Implement exact-ID extraction of all CSV checklist fields as JSON
- [x] 1.2 Add focused tests for multiline fields, multiple IDs, duplicate IDs, and unknown IDs
- [x] 1.3 Generate and inspect the I.6/H.3 extraction used by the Maglev audit

## 2. Maglev Focused Audit

- [x] 2.1 Add an operator runbook with the pinned Maglev source, commit, authority inputs, and output layout
- [x] 2.2 Prepare the isolated read-only Maglev workspace and verify its provenance
- [x] 2.3 Document the I.6/H.3 obligation and evidence matrices, including required security and fault-injection confirmation

## 3. Apple Review Intake

- [x] 3.1 Add a dated review-intake template with provenance, authority, full-diff, and anti-weakening fields
- [x] 3.2 Add instructions for mapping approved proposals to both Markdown and CSV checklist representations
- [ ] 3.3 Obtain and hash the latest Apple review artifact, then draft its recommendations as proposals
- [ ] 3.4 Resolve canonical citations and receive explicit human approval for the exact checklist diff
- [ ] 3.5 Apply approved notes to both checklist formats and confirm affected records remain synchronized

## 4. Validation and Documentation

- [x] 4.1 Validate script syntax and run focused behavioral tests
- [x] 4.2 Validate the OpenSpec change in strict mode
- [x] 4.3 Update operator documentation for focused audits and review intake
- [x] 4.4 Refresh `.policy-hashes.txt` if any playbook, checklist, prompt, or policy file changes
