#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "extract-checklist-items.py"
CHECKLIST = ROOT / "checklists" / "AMB_MSP_Integration_Checklist_with_I6_H3.csv"


class ExtractChecklistItemsTest(unittest.TestCase):
    def run_extract(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--checklist", str(CHECKLIST), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_extracts_complete_i6_and_h3_records_in_requested_order(self) -> None:
        result = self.run_extract("I.6", "H.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([item["Item ID"] for item in payload["items"]], ["I.6", "H.3"])
        self.assertIn("MA Notes", payload["columns"])
        self.assertIn("tenant isolation", payload["items"][0]["Requirement"].lower())
        self.assertIn("at-least-once", payload["items"][1]["Description"])

    def test_unknown_id_fails_without_partial_json(self) -> None:
        result = self.run_extract("I.6", "Z.99")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        self.assertIn("Z.99", result.stderr)

    def test_duplicate_requested_id_is_emitted_once(self) -> None:
        result = self.run_extract("I.6", "I.6")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["items"]), 1)

    def test_output_file_preserves_multiline_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "items.json"
            result = self.run_extract("--output", str(output), "H.3")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["items"][0]["Item ID"], "H.3")


if __name__ == "__main__":
    unittest.main()
