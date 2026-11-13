# Generated reports

This directory is the local output boundary for generated consolidated and per-item audit reports.
Customer reports are ignored by Git. Do not force-add them without an explicit confidentiality and
secret review.

Use `playbook/item-report-template.md`, validate with `bin/validate-audit-reports.py`, and package
only an explicit sanitized allowlist with `bin/package-audit-reports.py`.
