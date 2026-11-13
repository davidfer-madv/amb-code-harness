#!/usr/bin/env python3
"""Validate new item reports, authority pins, verdicts and method completion."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


VERDICTS = {"PASS", "PARTIAL", "NON-COMPLIANT", "NOT FULLY VERIFIABLE", "NOT APPLICABLE"}
REQUIRED_HEADINGS = (
    "Conclusion",
    "Atomic obligations",
    "Executable-code evidence",
    "Non-code evidence",
    "Adversarial checks",
    "Limitations",
    "Required closure",
)


def fail(errors: list[str]) -> "NoReturn":
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def frontmatter(text: str, path: Path) -> dict[str, object]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: missing YAML-style front matter")
    raw, _body = text[4:].split("\n---\n", 1)
    result: dict[str, object] = {}
    for number, line in enumerate(raw.splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{number}: invalid front-matter line")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ValueError(f"{path}:{number}: invalid key {key!r}")
        if key in result:
            raise ValueError(f"{path}:{number}: duplicate key {key!r}")
        if value.startswith("["):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{number}: list must be valid JSON: {exc}") from exc
            result[key] = parsed
        else:
            result[key] = value.strip('"')
    return result


def verification_methods(expression: str) -> tuple[str, set[str]]:
    match = re.fullmatch(r"(ALL|ANY)\(([^()]*)\)", expression.strip())
    if not match:
        raise ValueError("verification_expression must use ALL(...) or ANY(...)")
    methods = {part.strip() for part in match.group(2).split(",") if part.strip()}
    if not methods:
        raise ValueError("verification_expression contains no methods")
    return match.group(1), methods


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--checklist", required=True, type=Path)
    parser.add_argument("--consolidated", required=True, type=Path)
    parser.add_argument("--items-dir", required=True, type=Path)
    args = parser.parse_args()

    harness = Path.cwd().resolve()
    reports_root = (harness / "reports").resolve()
    candidate_source = (harness / "workspaces" / args.candidate / "src").resolve()
    checklist = args.checklist.resolve()
    consolidated = args.consolidated.resolve()
    items_dir = args.items_dir.resolve()
    errors: list[str] = []

    for label, path in (("consolidated report", consolidated), ("items directory", items_dir)):
        if not contained(path, reports_root):
            errors.append(f"{label} must remain below reports/")
        if contained(path, candidate_source):
            errors.append(f"{label} cannot be written below candidate source")
        if contained(path, reports_root):
            first = path.relative_to(reports_root).parts[0]
            if not first.startswith(f"{args.candidate}-"):
                errors.append(f"{label} is not scoped to candidate {args.candidate}")
    if not checklist.is_file():
        errors.append(f"checklist not found: {checklist}")
    if not consolidated.is_file():
        errors.append(f"consolidated report not found: {consolidated}")
    if not items_dir.is_dir():
        errors.append(f"items directory not found: {items_dir}")
    if errors:
        fail(errors)

    checklist_data = json.loads(checklist.read_text(encoding="utf-8"))
    checklist_hash = sha256(checklist)
    checklist_version = str(checklist_data.get("version", ""))
    item_by_code = {item["item_code"]: item for item in checklist_data.get("items", [])}
    index = items_dir / "README.md"
    if not index.is_file():
        fail([f"item index missing: {index}"])
    index_text = index.read_text(encoding="utf-8")
    consolidated_text = consolidated.read_text(encoding="utf-8")
    if checklist_hash not in consolidated_text:
        errors.append("consolidated report does not contain the exact checklist SHA-256")
    if checklist_version not in consolidated_text:
        errors.append("consolidated report does not contain the checklist version")

    item_files = sorted(p for p in items_dir.glob("*.md") if p.name != "README.md")
    if not item_files:
        errors.append("no item Markdown reports found")
    seen_codes: set[str] = set()
    for path in item_files:
        text = path.read_text(encoding="utf-8")
        try:
            meta = frontmatter(text, path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        required = {
            "candidate",
            "item_code",
            "uid",
            "checklist_version",
            "checklist_sha256",
            "candidate_commit",
            "candidate_tree",
            "review_date",
            "verification_expression",
            "confirmed_methods",
            "verdict",
        }
        missing = sorted(required - meta.keys())
        if missing:
            errors.append(f"{path}: missing front-matter fields: {', '.join(missing)}")
            continue
        code = str(meta["item_code"])
        if code in seen_codes:
            errors.append(f"duplicate item code: {code}")
        seen_codes.add(code)
        canonical_item = item_by_code.get(code)
        if not canonical_item:
            errors.append(f"{path}: unknown checklist item {code}")
        elif meta["uid"] != canonical_item.get("uid"):
            errors.append(f"{path}: UID does not match checklist item {code}")
        if meta["candidate"] != args.candidate:
            errors.append(f"{path}: candidate does not match selected candidate")
        if meta["checklist_version"] != checklist_version:
            errors.append(f"{path}: checklist version mismatch")
        if meta["checklist_sha256"] != checklist_hash:
            errors.append(f"{path}: checklist SHA-256 mismatch")
        for field in ("candidate_commit", "candidate_tree"):
            if not re.fullmatch(r"[0-9a-f]{40}", str(meta[field])):
                errors.append(f"{path}: {field} must be a full lowercase 40-character SHA")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta["review_date"])):
            errors.append(f"{path}: review_date must be YYYY-MM-DD")
        verdict = str(meta["verdict"])
        if verdict not in VERDICTS:
            errors.append(f"{path}: unsupported verdict {verdict!r}")
        confirmed = meta["confirmed_methods"]
        if not isinstance(confirmed, list) or not all(isinstance(v, str) for v in confirmed):
            errors.append(f"{path}: confirmed_methods must be a JSON string array")
            confirmed_set: set[str] = set()
        else:
            confirmed_set = set(confirmed)
        try:
            mode, required_methods = verification_methods(str(meta["verification_expression"]))
            if not confirmed_set.issubset(required_methods):
                errors.append(f"{path}: confirmed_methods includes a method outside the expression")
            methods_complete = (
                required_methods.issubset(confirmed_set)
                if mode == "ALL"
                else bool(required_methods & confirmed_set)
            )
            if verdict == "PASS" and not methods_complete:
                errors.append(f"{path}: PASS prohibited because required methods are unconfirmed")
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
        for heading in REQUIRED_HEADINGS:
            if not re.search(rf"^##+\s+{re.escape(heading)}\s*$", text, re.MULTILINE | re.I):
                errors.append(f"{path}: missing section '{heading}'")
        if path.name not in index_text:
            errors.append(f"{path}: missing from item index")
        if path.name not in consolidated_text:
            errors.append(f"{path}: missing from consolidated report")

    if errors:
        fail(errors)
    print(f"Validated {len(item_files)} item reports for {args.candidate}")


if __name__ == "__main__":
    main()
