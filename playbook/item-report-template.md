# New item report template

Copy this template into `reports/<candidate>-<date>-items/<item>-<slug>.md`. Replace every
placeholder. The structured front matter is mandatory for `bin/validate-audit-reports.py`.

```markdown
---
candidate: example-msp
item_code: C.31
uid: MSPR-0052
checklist_version: v2026.10.06
checklist_sha256: <64 lowercase hex characters>
candidate_commit: <40 lowercase hex characters>
candidate_tree: <40 lowercase hex characters>
review_date: 2026-11-13
verification_expression: ALL(Code, UX)
confirmed_methods: ["Code"]
verdict: PARTIAL
---

# C.31 — Per-brand image library

## Conclusion

State the controlled verdict and summarize why.

## Atomic obligations

List every mandatory clause and its MET, UNMET, UNPROVEN or NOT_APPLICABLE state.

## Executable-code evidence

Trace reachable production behavior and cite exact paths and lines.

## Non-code evidence

Classify every routed artifact and identify what it can and cannot prove.

## Adversarial checks

Record bypasses, negative cases, races, alternative paths and independent review.

## Limitations

State unavailable source, unresolved ownership and evidence boundaries.

## Required closure

Separate implementation work from evidence-retention work and provide observable acceptance criteria.
```

`verification_expression` must be normalized by trusted intake code as `ALL(...)` or `ANY(...)`.
Do not infer this expression from a comma in a checklist export. `confirmed_methods` contains only
methods supported by valid evidence for this exact revision and environment.
