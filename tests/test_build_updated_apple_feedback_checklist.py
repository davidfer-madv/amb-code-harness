#!/usr/bin/env python3

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "build-updated-apple-feedback-checklist.py"
TEMPLATE = (
    ROOT
    / "checklists"
    / "26_07_17_AMB_Linq_MSP_Integration_Checklist - AMB MSP Integration Checklist (3).csv"
)


class UpdatedAppleFeedbackChecklistTest(unittest.TestCase):
    def test_uses_exact_template_schema_and_preserves_tracking(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "updated.csv"
            markdown_output = Path(directory) / "updated.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--output",
                    str(output),
                    "--markdown-output",
                    str(markdown_output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            def load(path: Path) -> tuple[list[str], dict[str, dict[str, str]]]:
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.reader(handle))
                index = next(i for i, row in enumerate(rows) if row[0] == "Item ID")
                headers = rows[index]
                records = {
                    row[0]: dict(zip(headers, row))
                    for row in rows[index + 1 :]
                    if row and __import__("re").fullmatch(r"[A-Z]\.\d+", row[0])
                }
                return headers, records

            template_headers, template = load(TEMPLATE)
            output_headers, updated = load(output)
            self.assertEqual(output_headers, template_headers)
            self.assertEqual(len(output_headers), 12)
            self.assertEqual(len(updated), 81)
            self.assertEqual(updated["A.1"]["Build Status"], template["A.1"]["Build Status"])
            for item_id in ("H.3", "I.6", "C.23", "E.11", "E.12", "G.6", "H.4", "K.1"):
                self.assertIn(item_id, updated)
                self.assertEqual(updated[item_id]["Build Status"], "To Do")
                self.assertEqual(updated[item_id]["MA Video  Status"], "To Do")
            self.assertEqual(updated["C.2"]["Build Status"], "To Do")
            self.assertIn("not an Apple device", updated["K.1"]["Requirement"])

            markdown = markdown_output.read_text(encoding="utf-8")
            self.assertIn("### H.3 — Reliable, ordered", markdown)
            self.assertIn("### I.6 — Partner delivery tenant isolation", markdown)
            self.assertIn("### K.1 — Configurable fallback", markdown)
            self.assertIn("- **MA Video  Status:** To Do", markdown)


if __name__ == "__main__":
    unittest.main()
