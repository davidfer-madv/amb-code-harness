#!/usr/bin/env python3

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "build-proposed-apple-feedback-checklist.py"
SOURCE = ROOT / "checklists" / "AMB_MSP_Integration_Checklist_with_I6_H3.csv"
DELTA = (
    ROOT
    / "checklists"
    / "proposals"
    / "AMB_MSP_Integration_Checklist_PROPOSED_Apple_Feedback_2026-07-30.md"
)


class ProposedChecklistTest(unittest.TestCase):
    def build(self, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--source",
                str(SOURCE),
                "--delta",
                str(DELTA),
                "--output",
                str(output),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_builds_full_schema_and_inserts_new_items(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "proposal.csv"
            result = self.build(output)
            self.assertEqual(result.returncode, 0, result.stderr)

            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            header_index = next(i for i, row in enumerate(rows) if row[0] == "Item ID")
            headers = rows[header_index]
            records = [
                dict(zip(headers, row))
                for row in rows[header_index + 1 :]
                if row and "." in row[0] and row[0][0].isalpha()
            ]
            by_id = {record["Item ID"]: record for record in records}

            self.assertEqual(len(headers), 12)
            for item_id in ("C.23", "E.11", "E.12", "G.6", "H.4", "K.1"):
                self.assertIn(item_id, by_id)
                self.assertEqual(by_id[item_id]["MA Verified Status"], "UNVERIFIED")
                self.assertIn("[NEW]", by_id[item_id]["Review Notes"])

            self.assertIn("does not use an Apple device", by_id["K.1"]["Description"])
            self.assertIn("no conversation message", by_id["C.18"]["Description"])
            self.assertIn("[MODIFIED]", by_id["E.9"]["Review Notes"])
            self.assertIn(
                "No Apple protocol authority",
                by_id["K.1"]["Reference (MSP Integration Guide section)"],
            )
            self.assertIn(
                "canonical partner PR/marketing addendum",
                by_id["E.9"]["Reference (MSP Integration Guide section)"],
            )


if __name__ == "__main__":
    unittest.main()
