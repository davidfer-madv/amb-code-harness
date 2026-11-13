#!/usr/bin/env bash
# Prepare an isolated, pinned, read-only candidate snapshot.
set -euo pipefail

usage() {
  cat <<'HELP'
madv-audit-harness — audit.sh

USAGE
  bin/audit.sh --candidate NAME --source PATH_OR_URL --commit SHA --checklist CHECKLIST.json
  bin/audit.sh NAME PATH_OR_URL SHA CHECKLIST.json

REQUIRED INPUTS
  --candidate   Candidate label used below workspaces/ and for the analysis directory.
  --source      Read-only source repository URL or local path.
  --commit      Exact 7-40 character hexadecimal commit SHA; moving branches are rejected.
  --checklist   Exact canonical checklist JSON used for this run.

WHAT IT DOES
  - clones a no-hardlink copy into workspaces/NAME/src;
  - detaches the copy at the requested commit and disables pushes;
  - records candidate and checklist version/hash provenance;
  - renames candidate agent instruction files as untrusted evidence; and
  - makes the candidate snapshot read-only.

The candidate repository is never modified. Analysis and reports must be written outside src/.
Legacy three-argument invocation is rejected because it cannot pin checklist authority.
HELP
}

die() { echo "error: $*" >&2; exit 2; }

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ] || [ "$#" -eq 0 ]; then
  usage
  exit 0
fi

NAME="" SRC="" COMMIT="" CHECKLIST=""
if [ "$#" -eq 3 ] && [[ "${1:-}" != --* ]]; then
  die "--checklist is required; legacy three-argument audits are prohibited"
fi
if [ "$#" -eq 4 ] && [[ "${1:-}" != --* ]]; then
  NAME="$1"; SRC="$2"; COMMIT="$3"; CHECKLIST="$4"
else
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --candidate) [ "$#" -ge 2 ] || die "--candidate requires a value"; NAME="$2"; shift 2 ;;
      --source) [ "$#" -ge 2 ] || die "--source requires a value"; SRC="$2"; shift 2 ;;
      --commit) [ "$#" -ge 2 ] || die "--commit requires a value"; COMMIT="$2"; shift 2 ;;
      --checklist) [ "$#" -ge 2 ] || die "--checklist requires a value"; CHECKLIST="$2"; shift 2 ;;
      *) die "unknown argument '$1'; run bin/audit.sh --help" ;;
    esac
  done
fi

[ -n "$NAME" ] || die "--candidate is required"
[ -n "$SRC" ] || die "--source is required"
[ -n "$COMMIT" ] || die "--commit is required"
[ -n "$CHECKLIST" ] || die "--checklist is required; unpinned audits are prohibited"
[[ "$NAME" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]] || die "invalid candidate name"
[[ "$COMMIT" =~ ^[0-9a-fA-F]{7,40}$ ]] || die "commit must be an exact hexadecimal SHA"
[ -f "$CHECKLIST" ] || die "checklist not found: $CHECKLIST"
command -v jq >/dev/null || die "jq is required"
command -v sha256sum >/dev/null || die "sha256sum is required"

CHECKLIST_ABS="$(cd "$(dirname "$CHECKLIST")" && pwd -P)/$(basename "$CHECKLIST")"
CHECKLIST_VERSION="$(jq -er '.version | strings | select(length > 0)' "$CHECKLIST_ABS")" \
  || die "checklist has no non-empty .version"
CHECKLIST_DECLARED_COUNT="$(jq -er '.item_count | numbers' "$CHECKLIST_ABS")" \
  || die "checklist has no numeric .item_count"
CHECKLIST_ACTUAL_COUNT="$(jq -er '.items | length' "$CHECKLIST_ABS")" \
  || die "checklist has no .items array"
[ "$CHECKLIST_DECLARED_COUNT" -eq "$CHECKLIST_ACTUAL_COUNT" ] \
  || die "checklist item_count ($CHECKLIST_DECLARED_COUNT) does not match items length ($CHECKLIST_ACTUAL_COUNT)"
CHECKLIST_SHA256="$(sha256sum "$CHECKLIST_ABS" | awk '{print $1}')"
CHECKLIST_SOURCE_SHA256="$(jq -r '.source_sha256 // "not-declared"' "$CHECKLIST_ABS")"

WS="workspaces/$NAME"
OUT="${NAME}-analysis"
SRC_DIR="$WS/src"
mkdir -p "$WS" "$OUT/findings"

if [ -e "$SRC_DIR" ] && [ ! -d "$SRC_DIR/.git" ]; then
  die "$SRC_DIR exists but is not a Git worktree"
fi
if [ ! -d "$SRC_DIR/.git" ]; then
  git clone --no-hardlinks --no-checkout "$SRC" "$SRC_DIR"
else
  chmod -R u+w "$SRC_DIR" 2>/dev/null || true
fi

git -C "$SRC_DIR" fetch --tags -q origin "$COMMIT" 2>/dev/null \
  || git -C "$SRC_DIR" fetch --all -q \
  || die "unable to fetch requested commit"
git -C "$SRC_DIR" checkout -q --detach "$COMMIT"
RESOLVED_COMMIT="$(git -C "$SRC_DIR" rev-parse HEAD)"
case "$RESOLVED_COMMIT" in "$COMMIT"*) ;; *) die "resolved commit does not match requested SHA" ;; esac
TREE_SHA="$(git -C "$SRC_DIR" rev-parse 'HEAD^{tree}')"
git -C "$SRC_DIR" remote set-url --push origin /dev/null

# Candidate-controlled agent files remain available as evidence but cannot act as harness instructions.
find "$SRC_DIR" -maxdepth 3 \( -iname 'CLAUDE.md' -o -iname 'AGENTS.md' -o -iname 'GEMINI.md' \
  -o -iname '.cursorrules' -o -iname 'copilot-instructions.md' \) -print \
  -exec sh -c 'case "$1" in *.candidate-evidence) ;; *) mv "$1" "$1.candidate-evidence" ;; esac' _ {} \; \
  2>/dev/null || true
if [ -d "$SRC_DIR/.claude" ]; then
  mv "$SRC_DIR/.claude" "$SRC_DIR/.claude.candidate-evidence"
fi

{
  echo "candidate: $NAME"
  echo "source: $SRC"
  echo "commit: $RESOLVED_COMMIT"
  echo "tree_sha: $TREE_SHA"
  echo "checklist_path: $CHECKLIST_ABS"
  echo "checklist_version: $CHECKLIST_VERSION"
  echo "checklist_sha256: $CHECKLIST_SHA256"
  echo "checklist_source_sha256: $CHECKLIST_SOURCE_SHA256"
  echo "checklist_item_count: $CHECKLIST_ACTUAL_COUNT"
  echo "policy_hashes: .policy-hashes.txt"
  echo "neutralized_agent_config: renamed to *.candidate-evidence in the isolated copy"
} > "$OUT/provenance.txt"

chmod -R a-w "$SRC_DIR" 2>/dev/null || true

cat <<MSG
Read-only copy ready: $SRC_DIR @ $RESOLVED_COMMIT
Checklist pinned:     $CHECKLIST_VERSION ($CHECKLIST_SHA256)
Findings directory:   $OUT/findings
Provenance:           $OUT/provenance.txt

NEXT: build the evidence manifest, then run per-item analysis from the harness root.
MSG
