# Contributing

## Before changing the harness

Read `AGENTS.md`, `openspec/config.yaml`, the active OpenSpec changes and the relevant policy or
playbook. Non-trivial changes require an OpenSpec proposal/design/spec/tasks update.

Candidate repositories and raw evidence are not contribution material. Do not add customer names,
source, screenshots, videos, PDFs, Postman environments/results, tokens or audit deliverables.

## Validation

```bash
bash -n bin/*.sh
python3 -m py_compile bin/*.py tests/*.py
python3 -m unittest discover -s tests -v
openspec validate --all --strict --no-interactive
bin/github-readiness.py
```

Pull requests should explain the trust boundary affected, the OpenSpec change, tests added and any
residual human or runtime validation. Do not weaken a safety gate merely to make a test pass.
