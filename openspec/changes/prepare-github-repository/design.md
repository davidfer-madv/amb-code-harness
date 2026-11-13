# Design: GitHub-safe, agent-readable harness

## Trust boundaries

- The Git repository contains only reusable harness logic and sanitized examples.
- `workspaces/`, `*-analysis/`, `reports/`, `deliverables/` and `artifacts/` are local boundaries.
- Candidate repositories and all submitted material are untrusted data, never agent instructions.
- An approved external checklist/canonical pin remains required per audit.

## Agent entry points

- `AGENTS.md` is the normative coding-agent instruction surface.
- `CLAUDE.md` points Claude Code to the same rules without duplicating policy.
- `.github/copilot-instructions.md` gives Copilot the same trust and workflow summary.
- `README.md` is the human quick start; the playbook remains the detailed audit method.

## Publication gate

`bin/github-readiness.py` evaluates every tracked or unignored file that would be uploaded. It
rejects forbidden local paths, large files, risky binary/evidence formats and common secret forms,
then runs syntax, unit and OpenSpec validation.

## Failure behavior

Any secret, oversized file, ignored-boundary violation, test failure or invalid OpenSpec change
fails closed. The operator resolves the issue before staging or pushing.
