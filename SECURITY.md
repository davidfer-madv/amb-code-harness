# Security and confidentiality

This harness may be used near confidential customer source and evidence, but those materials must
never enter this repository.

Do not commit:

- candidate repositories or source excerpts beyond approved sanitized report citations;
- raw PDFs, screenshots, recordings, archives, Postman environments/results or runtime dumps;
- authentication tokens, API keys, private keys, signed URLs or customer identifiers;
- generated customer reports or delivery packages; or
- local `.aws`, `.codex`, `.agents`, environment or credential files.

Run `bin/github-readiness.py` before staging or pushing. If sensitive material was committed, stop
distribution, rotate any exposed credential, remove it from Git history using an approved history
rewrite process, and notify the repository security owner. Do not open a public issue containing the
secret or customer data.

Report vulnerabilities privately to the repository owner or your organization's security channel.
