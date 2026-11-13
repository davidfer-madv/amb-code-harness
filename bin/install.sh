#!/usr/bin/env bash
# Install/verify the harness in MA's environment (run once, from the harness root).
set -euo pipefail
echo "Checking required tools..."
missing=0
for c in git jq python3 sha256sum; do
  if command -v "$c" >/dev/null; then echo "  ok: $c"; else echo "  MISSING: $c"; missing=1; fi
done
if [ "$missing" -ne 0 ]; then
  echo "Install required tools before running an audit." >&2
  exit 2
fi
echo "Checking optional workflow tools..."
for c in openspec codex claude copilot; do
  command -v "$c" >/dev/null && echo "  ok: $c" || echo "  optional/missing: $c"
done
echo "Hashing the trusted policy layer (playbook + checklists + prompts + policy)..."
find playbook checklists prompts policy -type f -print0 | sort -z | xargs -0 sha256sum > .policy-hashes.txt
echo "Wrote .policy-hashes.txt ($(wc -l < .policy-hashes.txt) files). Re-run after any harness change."
