#!/usr/bin/env python3
"""Extract complete checklist CSV records by exact item ID as JSON."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


DEFAULT_CHECKLIST = Path(
    "checklists/AMB_MSP_Integration_Checklist_with_I6_H3.csv"
)
ITEM_ID_COLUMN = "Item ID"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract complete AMB checklist records by exact item ID."
    )
    parser.add_argument("item_ids", nargs="+", metavar="ITEM_ID")
    parser.add_argument(
        "--checklist",
        type=Path,
        default=DEFAULT_CHECKLIST,
        help=f"checklist CSV path (default: {DEFAULT_CHECKLIST})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write JSON to this path instead of standard output",
    )
    return parser.parse_args()


def load_records(path: Path) -> tuple[list[str], dict[str, dict[str, str]]]:
    try:
        handle = path.open(encoding="utf-8-sig", newline="")
    except OSError as error:
        raise ValueError(f"cannot open checklist {path}: {error}") from error

    with handle:
        reader = csv.reader(handle)
        for row in reader:
            if row and row[0].strip() == ITEM_ID_COLUMN:
                headers = [field.strip() for field in row]
                break
        else:
            raise ValueError(
                f"{path}: header row beginning with {ITEM_ID_COLUMN!r} not found"
            )

        records: dict[str, dict[str, str]] = {}
        for line_number, row in enumerate(reader, start=reader.line_num):
            if not row:
                continue
            row += [""] * (len(headers) - len(row))
            if len(row) > len(headers):
                raise ValueError(
                    f"{path}:{line_number}: expected {len(headers)} fields, "
                    f"found {len(row)}"
                )
            record = dict(zip(headers, row))
            item_id = record[ITEM_ID_COLUMN].strip()
            if not item_id or not any(character.isdigit() for character in item_id):
                continue
            if item_id in records:
                raise ValueError(f"{path}: duplicate checklist item {item_id}")
            records[item_id] = record

    return headers, records


def main() -> int:
    args = parse_args()
    requested = list(dict.fromkeys(args.item_ids))

    try:
        headers, records = load_records(args.checklist)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    missing = [item_id for item_id in requested if item_id not in records]
    if missing:
        print(
            f"error: checklist item(s) not found: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 3

    result = {
        "source": str(args.checklist),
        "columns": headers,
        "items": [records[item_id] for item_id in requested],
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
