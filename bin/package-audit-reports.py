#!/usr/bin/env python3
"""Build a sanitized report-only ZIP from an explicit allowlist."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Anthropic key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{24,}"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "JWT bearer token": re.compile(r"Bearer\s+eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", re.I),
}
PROHIBITED_NAME = re.compile(
    r"(?:postman|newman|environment|runtime|dump|capture|evidence|screenshot|recording)", re.I
)


def fail(message: str) -> "NoReturn":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def contained(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--allowlist", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    harness = Path.cwd().resolve()
    reports_root = (harness / "reports").resolve()
    deliverables_root = (harness / "deliverables").resolve()
    allowlist = args.allowlist.resolve()
    output = args.output.resolve()
    if not allowlist.is_file():
        fail(f"allowlist not found: {allowlist}")
    if not contained(output, deliverables_root):
        fail("package output must remain below deliverables/")
    if output.exists():
        fail(f"refusing to overwrite existing package: {output}")

    tracked = subprocess.run(
        ["git", "ls-files", "workspaces"], cwd=harness, text=True, capture_output=True, check=False
    )
    if tracked.returncode == 0 and tracked.stdout.strip():
        fail("Git tracks files below workspaces/; remove them before packaging")

    files: list[Path] = []
    for number, raw in enumerate(allowlist.read_text(encoding="utf-8").splitlines(), 1):
        entry = raw.strip()
        if not entry or entry.startswith("#"):
            continue
        path = (harness / entry).resolve() if not Path(entry).is_absolute() else Path(entry).resolve()
        if not contained(path, reports_root):
            fail(f"allowlist line {number}: report must remain below reports/")
        first = path.relative_to(reports_root).parts[0]
        if not first.startswith(f"{args.candidate}-"):
            fail(f"allowlist line {number}: cross-candidate report path is prohibited")
        if path.suffix.lower() != ".md":
            fail(f"allowlist line {number}: only generated Markdown reports may be packaged")
        if PROHIBITED_NAME.search(path.name):
            fail(f"allowlist line {number}: prohibited raw-evidence filename: {path.name}")
        if path.is_symlink() or not path.is_file():
            fail(f"allowlist line {number}: missing or symlinked report: {path}")
        if path in files:
            fail(f"allowlist line {number}: duplicate report: {path}")
        text = path.read_text(encoding="utf-8")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                fail(f"secret scan detected {label} in {path}")
        files.append(path)
    if not files:
        fail("allowlist contains no reports")

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="madv-package-") as temp:
        manifest = Path(temp) / "MANIFEST.sha256"
        rows = []
        for path in files:
            archive_name = path.relative_to(reports_root).as_posix()
            rows.append(f"{digest(path)}  {archive_name}")
        manifest.write_text("\n".join(sorted(rows)) + "\n", encoding="utf-8")
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(files):
                archive.write(path, path.relative_to(reports_root).as_posix())
            archive.write(manifest, "MANIFEST.sha256")
    os.chmod(output, 0o600)
    print(f"Wrote sanitized package {output} ({len(files)} reports plus manifest)")


if __name__ == "__main__":
    main()
