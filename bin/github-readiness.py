#!/usr/bin/env python3
"""Fail closed if files eligible for GitHub violate repository publication policy."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path


MAX_FILE_BYTES = 10 * 1024 * 1024
FORBIDDEN_PREFIXES = (
    "workspaces/",
    "artifacts/",
    "cerebro-analysis/",
    "maglev-analysis/",
    ".agents/",
    ".codex/",
    ".aws/",
)
FORBIDDEN_SUFFIXES = (
    ".zip",
    ".mp4",
    ".mov",
    ".pdf",
    ".docx",
    ".p12",
    ".pfx",
    ".pem",
    ".key",
    ".har",
)
SECRET_PATTERNS = {
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Anthropic key": re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}"),
    "OpenAI-style key": re.compile(rb"\bsk-[A-Za-z0-9_-]{24,}"),
    "GitHub token": re.compile(rb"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    "AWS access key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "JWT bearer token": re.compile(
        rb"Bearer\s+eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}", re.I
    ),
}


def command(args: list[str], root: Path, *, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=root, check=False, text=True, capture_output=capture)


def eligible_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError("unable to enumerate Git-eligible files")
    paths = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        relative = Path(os.fsdecode(raw))
        paths.append(relative)
    return sorted(paths, key=lambda p: p.as_posix())


def scan(root: Path, paths: list[Path]) -> list[str]:
    errors = []
    for relative in paths:
        name = relative.as_posix()
        path = root / relative
        if any(name.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            errors.append(f"forbidden local/customer path is Git-eligible: {name}")
            continue
        if relative.suffix.lower() in FORBIDDEN_SUFFIXES or name.endswith(".postman_environment.json"):
            errors.append(f"prohibited evidence/credential file is Git-eligible: {name}")
            continue
        if path.is_symlink():
            errors.append(f"symlink is Git-eligible and requires explicit review: {name}")
            continue
        if not path.is_file():
            errors.append(f"non-file Git entry is unsupported: {name}")
            continue
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            errors.append(f"file exceeds 10 MiB publication limit: {name} ({size} bytes)")
            continue
        data = path.read_bytes()
        if b"\0" in data:
            errors.append(f"binary file is Git-eligible: {name}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                errors.append(f"secret scan detected {label} in {name}")
    return errors


def write_manifest(root: Path, paths: list[Path], output: Path) -> None:
    rows = []
    for relative in paths:
        digest = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        rows.append(f"{digest}  {relative.as_posix()}")
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files-only", action="store_true", help="skip syntax, unit and OpenSpec checks")
    parser.add_argument("--manifest", type=Path, default=Path("github-upload-manifest.sha256"))
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if not (root / ".git").is_dir() or not (root / "AGENTS.md").is_file():
        print("error: run from the audit-harness Git root", file=sys.stderr)
        raise SystemExit(2)

    try:
        paths = eligible_files(root)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    errors = scan(root, paths)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)

    manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
    if manifest.resolve().is_relative_to(root):
        ignore_check = command(
            ["git", "check-ignore", "-q", str(manifest.relative_to(root))], root
        )
        if ignore_check.returncode != 0:
            print("error: readiness manifest inside the repository must be Git-ignored", file=sys.stderr)
            raise SystemExit(2)
    write_manifest(root, paths, manifest)
    print(f"Eligible files: {len(paths)}; manifest: {manifest}")

    if args.files_only:
        return
    checks = [
        (["bash", "-n", *[p.as_posix() for p in paths if p.suffix == ".sh"]], "shell syntax"),
        (
            ["python3", "-m", "py_compile", *[p.as_posix() for p in paths if p.suffix == ".py"]],
            "Python compilation",
        ),
        (["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], "unit tests"),
        (
            ["openspec", "validate", "--all", "--strict", "--no-interactive"],
            "OpenSpec validation",
        ),
    ]
    for args_list, label in checks:
        if len(args_list) <= 2:
            continue
        print(f"Running {label}...")
        result = command(args_list, root)
        if result.returncode:
            print(f"error: {label} failed", file=sys.stderr)
            raise SystemExit(result.returncode)
    print("GitHub readiness: PASS (no commit or push performed)")


if __name__ == "__main__":
    main()
