# Reusable candidate audit operator runbook

This is the shortest safe path for onboarding another reviewer or MSP candidate. Run every command
from the `madv-audit-harness` root. Never run the analyzer inside candidate source.

## 1. Resolve immutable inputs

```bash
CANDIDATE=example-msp
CANDIDATE_REPO=/absolute/path/to/example-msp
CANDIDATE_SHA="$(git -C "$CANDIDATE_REPO" rev-parse HEAD)"
CHECKLIST=/absolute/path/to/AMB-canonical/checklists/msp-conformance/v2026.10.06/checklist.json
```

Confirm that `CHECKLIST` is the latest approved—not merely newest—MSP checklist.

If a team member cannot locate or access `AMB-canonical`, this repository retains a byte-identical
fallback at `checklists/msp-conformance/v2026.10.06/checklist.json`. Verify it first with
`(cd checklists/msp-conformance/v2026.10.06 && sha256sum --check SHA256SUMS)`, then explicitly set
`CHECKLIST` to that path. The fallback does not replace the canonical authority and does not remove
the requirement for pinned canonical claim closure.

## 2. Prepare the isolated snapshot

```bash
bin/audit.sh --candidate "$CANDIDATE" --source "$CANDIDATE_REPO" \
  --commit "$CANDIDATE_SHA" --checklist "$CHECKLIST"
```

The command records candidate commit/tree and checklist version/hash, disables pushes and freezes
the copied source read-only.

## 3. Intake evidence

Place raw customer submissions below `workspaces/$CANDIDATE/evidence/`, then run:

```bash
bin/build-artifact-manifest.py --candidate "$CANDIDATE"
```

Review `<candidate>-analysis/artifact-manifest.json`. Assign each artifact to one or more checklist
items or deliberately retain `unmapped`. Never commit this file or raw evidence by default.

## 4. Audit item by item

Follow `playbook/amb-code-analysis-playbook.md`. Start with tenant isolation. Use
`prompts/verifier/msp-code-analysis-operator-prompt-v1.md` for code and
`prompts/verifier/msp-developer-submission-audit-v1.md` when reconciling mixed evidence.

Copy `playbook/item-report-template.md` for every assessed item. A code finding and a required
Postman/UX/verbal confirmation are separate facts. Run a blinded adversarial pass for high-risk or
unresolved clauses.

## 5. Validate reports

```bash
bin/validate-audit-reports.py --candidate "$CANDIDATE" --checklist "$CHECKLIST" \
  --consolidated "reports/$CANDIDATE-YYYY-MM-DD-review.md" \
  --items-dir "reports/$CANDIDATE-YYYY-MM-DD-items"
```

The validator fails closed on bad pins, unknown UIDs, uncontrolled verdicts, incomplete required
methods, missing sections, missing index entries and cross-candidate report paths.

## 6. Package only sanitized reports

Create `<candidate>-analysis/report-allowlist.txt` with one `reports/...md` path per line. Then:

```bash
bin/package-audit-reports.py --candidate "$CANDIDATE" \
  --allowlist "$CANDIDATE-analysis/report-allowlist.txt" \
  --output "deliverables/$CANDIDATE-YYYY-MM-DD.zip"
```

Inspect the ZIP and `MANIFEST.sha256` before delivery. Never add raw evidence to the allowlist.
