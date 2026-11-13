#!/usr/bin/env python3
"""Merge the Apple-feedback proposal into the Linq checklist tracking schema."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = (
    ROOT
    / "checklists"
    / "26_07_17_AMB_Linq_MSP_Integration_Checklist - AMB MSP Integration Checklist (3).csv"
)
DEFAULT_PROPOSAL = (
    ROOT
    / "checklists"
    / "proposals"
    / "AMB_MSP_Integration_Checklist_PROPOSED_Apple_Feedback_2026-07-30.csv"
)
DEFAULT_OUTPUT = (
    ROOT
    / "checklists"
    / (
        "26_07_30_AMB_Linq_MSP_Integration_Checklist - "
        "AMB MSP Integration Checklist (Apple Feedback Update).csv"
    )
)
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_OUTPUT.with_suffix(".md")

ITEM_ID = re.compile(r"[A-Z]\.\d+")
CONTENT_COLUMNS = (
    "Requirement",
    "Description",
    "Key Considerations",
    "Reference (MSP Integration Guide section)",
    "Verification Method",
    "Review Notes",
)
TRACKING_COLUMNS = (
    "Build Status",
    "Demo Video Readiness Status",
    "Video Demo URL",
    "MA Video  Status",
    "MA Notes",
)


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--proposal", type=Path, default=DEFAULT_PROPOSAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT
    )
    return parser.parse_args()


def read_csv(path: Path) -> tuple[list[list[str]], list[str], list[list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    header_index = next(
        index
        for index, row in enumerate(rows)
        if row and row[0].strip() == "Item ID"
    )
    return rows[:header_index], rows[header_index], rows[header_index + 1 :]


def item_records(headers: list[str], rows: list[list[str]]) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        item_id = padded[0].strip() if padded else ""
        if ITEM_ID.fullmatch(item_id):
            records[item_id] = dict(zip(headers, padded))
    return records


def write_markdown(
    path: Path, headers: list[str], rows: list[list[str]]
) -> None:
    lines = [
        "# AMB MSP Integration Checklist — Apple Feedback Update",
        "",
        "> Updated 2026-07-30. Includes I.6, H.3, and the latest Apple review "
        "feedback. This Markdown file is generated from the same merged records "
        "as the matching CSV.",
        "",
        "## Field schema",
        "",
    ]
    lines.extend(f"{index}. {header}" for index, header in enumerate(headers, 1))
    lines.append("")

    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        item_id = padded[0].strip() if padded else ""
        if not ITEM_ID.fullmatch(item_id):
            section = padded[0].strip()
            if section:
                lines.extend([f"## {section}", ""])
            continue

        record = dict(zip(headers, padded))
        lines.extend(
            [
                f"### {item_id} — {record['Requirement']}",
                "",
                f"- **Item ID:** {item_id}",
            ]
        )
        for header in headers[1:]:
            value = record[header] or ""
            lines.append(f"- **{header}:** {value}")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = arguments()
    template_preamble, template_headers, template_rows = read_csv(args.template)
    _, proposal_headers, proposal_rows = read_csv(args.proposal)

    expected_headers = ["Item ID", *CONTENT_COLUMNS, *TRACKING_COLUMNS]
    if template_headers != expected_headers:
        raise ValueError("template schema does not match the expected 12 fields")

    template_by_id = item_records(template_headers, template_rows)
    proposal_by_id = item_records(proposal_headers, proposal_rows)
    missing = template_by_id.keys() - proposal_by_id.keys()
    if missing:
        raise ValueError(
            "proposal is missing template item(s): " + ", ".join(sorted(missing))
        )

    output_rows: list[list[str]] = []
    seen: set[str] = set()
    for proposal_row in proposal_rows:
        proposal_row += [""] * (len(proposal_headers) - len(proposal_row))
        item_id = proposal_row[0].strip() if proposal_row else ""
        if not ITEM_ID.fullmatch(item_id):
            output_rows.append(
                proposal_row[:1] + [""] * (len(template_headers) - 1)
                if proposal_row
                else [""] * len(template_headers)
            )
            continue

        proposal = dict(zip(proposal_headers, proposal_row))
        record = {header: "" for header in template_headers}
        record["Item ID"] = item_id
        for column in CONTENT_COLUMNS:
            record[column] = proposal[column]

        changed = (
            "[MODIFIED]" in proposal["Review Notes"]
            or "[NEW]" in proposal["Review Notes"]
            or item_id not in template_by_id
        )
        if changed:
            record["Build Status"] = "To Do"
            record["Demo Video Readiness Status"] = "To Do"
            record["MA Video  Status"] = "To Do"
        else:
            source = template_by_id[item_id]
            for column in TRACKING_COLUMNS:
                record[column] = source[column]

        output_rows.append([record[header] for header in template_headers])
        seen.add(item_id)

    if seen != proposal_by_id.keys():
        raise ValueError("not every proposal item was written")

    preamble = [row[:] for row in template_preamble]
    preamble[0][0] = (
        "AMB MSP Integration Checklist | Apple Feedback Update 2026-07-30"
    )
    preamble[1][0] = (
        "Detailed reference document: [link to be added by MSP] | "
        "Updated 2026-07-30 | Includes I.6, H.3, and latest Apple review feedback"
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(preamble)
        writer.writerow(template_headers)
        writer.writerows(output_rows)
    write_markdown(args.markdown_output, template_headers, output_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
