#!/usr/bin/env bash
# Neutral cross-candidate benchmark. Internal only. Never exposes one candidate to another.
# Run from the harness root.
set -euo pipefail
echo "Candidates with findings:"
ls -d ./*-analysis 2>/dev/null | sed 's|^\./||;s|-analysis$||' | sed 's/^/  - /' || echo "  none yet"
cat <<'MSG'

Build the neutral scorecard from each <candidate>-analysis/findings/ against the 76-item checklist:
  - Per-item status per candidate (candidate names may be coded).
  - Gaps common across candidates -> propose a checklist item (this is how I.6/H.3 emerged).
Rules: internal only; never surface one candidate's specifics to another; a shared blind spot is a
checklist signal, not a leak.
MSG
