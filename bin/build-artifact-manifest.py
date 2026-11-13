#!/usr/bin/env python3
"""Create a deterministic, candidate-isolated manifest of submitted audit evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


TYPE_BY_SUFFIX = {
    ".md": "document",
    ".txt": "document",
    ".pdf": "pdf",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
    ".mp4": "video",
    ".mov": "video",
    ".zip": "archive",
    ".har": "http_capture",
    ".log": "runtime_log",
    ".json": "json",
    ".csv": "table",
}
SENSITIVE_NAME = re.compile(r"(?:secret|token|credential|environment|private[-_ ]?key|\.env)", re.I)


def fail(message: str) -> "NoReturn":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def contained(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def classify(path: Path) -> str:
    lower = path.name.lower()
    if "postman_collection" in lower:
        return "postman_collection"
    if "postman_environment" in lower:
        return "postman_environment"
    if "newman" in lower or "postman_result" in lower:
        return "executed_test_result"
    return TYPE_BY_SUFFIX.get(path.suffix.lower(), "other")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    harness = Path.cwd().resolve()
    candidate_root = (harness / "workspaces" / args.candidate).resolve()
    if not candidate_root.is_dir():
        fail(f"candidate workspace not found: {candidate_root}")
    evidence_root = (args.evidence_root or candidate_root / "evidence").resolve()
    if not contained(evidence_root, candidate_root):
        fail("evidence root must remain inside the selected candidate workspace")
    source_root = (candidate_root / "src").resolve()
    if contained(evidence_root, source_root):
        fail("candidate source is not an evidence intake directory")
    if not evidence_root.is_dir():
        fail(f"evidence directory not found: {evidence_root}")

    output = (args.output or harness / f"{args.candidate}-analysis" / "artifact-manifest.json").resolve()
    allowed_output = (harness / f"{args.candidate}-analysis").resolve()
    if not contained(output, allowed_output):
        fail("manifest output must remain in the selected candidate analysis directory")

    artifacts = []
    for path in sorted(evidence_root.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_symlink():
            fail(f"symlink evidence is prohibited: {path}")
        if not path.is_file():
            continue
        resolved = path.resolve()
        if not contained(resolved, evidence_root):
            fail(f"evidence path escapes intake root: {path}")
        stat = resolved.stat()
        artifacts.append(
            {
                "artifact_id": f"ART-{len(artifacts) + 1:04d}",
                "path": resolved.relative_to(candidate_root).as_posix(),
                "filename": resolved.name,
                "sha256": sha256(resolved),
                "bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "type": classify(resolved),
                "sensitive_name": bool(SENSITIVE_NAME.search(resolved.name)),
                "item_codes": [],
                "routing_state": "unmapped",
                "provenance": {
                    "candidate_revision": None,
                    "environment": None,
                    "observed_at": None,
                },
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format": "madv-artifact-manifest-v1",
        "candidate": args.candidate,
        "evidence_root": evidence_root.relative_to(candidate_root).as_posix(),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output} ({len(artifacts)} artifacts; all initially unmapped)")


if __name__ == "__main__":
    main()
