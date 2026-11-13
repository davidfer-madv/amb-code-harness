#!/usr/bin/env python3
"""Build a full proposal CSV from the authoritative checklist and highlighted delta."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "checklists" / "AMB_MSP_Integration_Checklist_with_I6_H3.csv"
DEFAULT_DELTA = (
    ROOT
    / "checklists"
    / "proposals"
    / "AMB_MSP_Integration_Checklist_PROPOSED_Apple_Feedback_2026-07-30.md"
)
DEFAULT_OUTPUT = (
    ROOT
    / "checklists"
    / "proposals"
    / "AMB_MSP_Integration_Checklist_PROPOSED_Apple_Feedback_2026-07-30.csv"
)

FIELDS = (
    "Requirement",
    "Description",
    "Key Considerations",
    "Reference",
    "Verification Method",
    "Review Notes",
)
NEW_IDS = {"C.23", "E.11", "E.12", "G.6", "H.4", "K.1"}
INSERT_AFTER = {
    "C.22": ["C.23"],
    "E.10": ["E.11", "E.12"],
    "G.5": ["G.6"],
    "H.3": ["H.4"],
    "J.5": ["K.1"],
}
REFERENCE_HEADER = "Reference (MSP Integration Guide section)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--delta", type=Path, default=DEFAULT_DELTA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def normalize_markdown(value: str) -> str:
    lines = [line.strip() for line in value.strip().splitlines()]
    return " ".join(line for line in lines if line)


def parse_delta(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    heading_pattern = re.compile(
        r"^###\s+[🟨🟩]\s+([A-Z]\.\d+)\s+—[^\n]*\n(?P<body>.*?)(?=^###\s|^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    field_pattern = re.compile(
        r"^-\s+\*\*("
        + "|".join(re.escape(field) for field in FIELDS)
        + r"):\*\*\s*(.*?)(?=^-\s+\*\*(?:"
        + "|".join(re.escape(field) for field in FIELDS)
        + r"):\*\*|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    records: dict[str, dict[str, str]] = {}
    for heading in heading_pattern.finditer(text):
        item_id = heading.group(1)
        fields = {
            name: normalize_markdown(value)
            for name, value in field_pattern.findall(heading.group("body"))
        }
        missing = [field for field in FIELDS if field not in fields]
        if missing:
            raise ValueError(f"{item_id}: missing proposal field(s): {', '.join(missing)}")
        records[item_id] = fields
    return records


def read_source(path: Path) -> tuple[list[list[str]], list[str], list[list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    for index, row in enumerate(rows):
        if row and row[0].strip() == "Item ID":
            headers = [field.strip() for field in row]
            return rows[:index], headers, rows[index + 1 :]
    raise ValueError(f"{path}: Item ID header not found")


def proposal_for_csv(proposal: dict[str, str]) -> dict[str, str]:
    """Map the concise Markdown field names onto the authoritative CSV schema."""
    mapped = proposal.copy()
    mapped[REFERENCE_HEADER] = mapped.pop("Reference")
    return mapped


def build_new_record(
    headers: list[str], item_id: str, proposal: dict[str, str]
) -> list[str]:
    record = {header: "" for header in headers}
    record["Item ID"] = item_id
    record.update(proposal_for_csv(proposal))
    record["Review Notes"] = f"[NEW] {record['Review Notes']} PROPOSAL ONLY."
    record["MA Verified Status"] = "UNVERIFIED"
    return [record[header] for header in headers]


def build() -> int:
    args = parse_args()
    proposals = parse_delta(args.delta)
    preamble, headers, source_rows = read_source(args.source)
    width = len(headers)

    unknown_new = NEW_IDS - proposals.keys()
    if unknown_new:
        raise ValueError(f"missing new proposal(s): {', '.join(sorted(unknown_new))}")

    result: list[list[str]] = []
    seen_existing: set[str] = set()
    for source_row in source_rows:
        row = source_row + [""] * (width - len(source_row))
        if len(row) > width:
            raise ValueError(f"source row has {len(row)} fields; expected {width}")
        item_id = row[0].strip()

        if item_id in proposals and item_id not in NEW_IDS:
            record = dict(zip(headers, row))
            record.update(proposal_for_csv(proposals[item_id]))
            record["Review Notes"] = (
                f"[MODIFIED] {record['Review Notes']} PROPOSAL ONLY."
            )
            row = [record[header] for header in headers]
            seen_existing.add(item_id)

        result.append(row)

        for new_id in INSERT_AFTER.get(item_id, []):
            if new_id == "K.1":
                result.append(
                    ["Section K. MSP omnichannel controls (not Apple protocol requirements)"]
                    + [""] * (width - 1)
                )
            result.append(build_new_record(headers, new_id, proposals[new_id]))

    expected_existing = proposals.keys() - NEW_IDS
    missing_existing = expected_existing - seen_existing
    if missing_existing:
        raise ValueError(
            f"existing proposal item(s) absent from source: {', '.join(sorted(missing_existing))}"
        )

    if preamble:
        preamble[0][0] = (
            "PROPOSED — AMB MSP Integration Checklist with Apple feedback "
            "(authoritative checklist unchanged)"
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(preamble)
        writer.writerow(headers)
        writer.writerows(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
