import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "checklists" / "msp-conformance" / "v2026.10.06"
EXPECTED_CHECKLIST_SHA256 = (
    "a16748f0fb6dab0a4ede7da733f49361b4c9b651c21318ddc2a205b02ac462d1"
)
EXPECTED_PROVENANCE_SHA256 = (
    "c455961a10c1d47b9cc72721feb79d057002ae2eefb9cc12cf5121e2de8f17b7"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BundledMspChecklistTests(unittest.TestCase):
    def test_approved_fallback_bundle_is_immutable_and_internally_consistent(self):
        checklist_path = BUNDLE / "checklist.json"
        provenance_path = BUNDLE / "PROVENANCE.json"

        self.assertEqual(sha256(checklist_path), EXPECTED_CHECKLIST_SHA256)
        self.assertEqual(sha256(provenance_path), EXPECTED_PROVENANCE_SHA256)

        checklist = json.loads(checklist_path.read_text(encoding="utf-8"))
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))

        self.assertEqual(checklist["version"], "v2026.10.06")
        self.assertEqual(checklist["item_count"], 100)
        self.assertEqual(len(checklist["items"]), checklist["item_count"])
        self.assertEqual(provenance["version"], checklist["version"])
        self.assertEqual(provenance["approval"]["status"], "APPROVED")
        self.assertEqual(provenance["approval"]["approved_at"], "2026-10-08")

    def test_manifest_pins_both_upstream_files(self):
        entries = {}
        for line in (BUNDLE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, filename = line.split(maxsplit=1)
            entries[filename] = digest

        self.assertEqual(entries["checklist.json"], EXPECTED_CHECKLIST_SHA256)
        self.assertEqual(entries["PROVENANCE.json"], EXPECTED_PROVENANCE_SHA256)
        self.assertEqual(set(entries), {"checklist.json", "PROVENANCE.json"})


if __name__ == "__main__":
    unittest.main()
