import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "bin" / script), *args], cwd=cwd, text=True, capture_output=True, check=False
    )


def checklist(path: Path) -> tuple[str, str]:
    data = {
        "format": "test",
        "version": "v-test-1",
        "item_count": 1,
        "source_sha256": "a" * 64,
        "items": [
            {
                "item_code": "C.31",
                "uid": "MSPR-0052",
                "definition": {"requirement": "Per-brand image library"},
            }
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    return data["version"], hashlib.sha256(path.read_bytes()).hexdigest()


class ReusableAuditWorkflowTests(unittest.TestCase):
    def test_github_readiness_excludes_local_boundaries_and_rejects_secret(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text(
                "workspaces/\ngithub-upload-manifest.sha256\n", encoding="utf-8"
            )
            (root / "AGENTS.md").write_text("safe instructions\n", encoding="utf-8")
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            hidden = root / "workspaces/customer/src"
            hidden.mkdir(parents=True)
            ignored_marker = "sk-" + "ant-should-never-be-scanned\n"
            (hidden / "secret.txt").write_text(ignored_marker, encoding="utf-8")

            passed = run("github-readiness.py", "--files-only", cwd=root)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            manifest = (root / "github-upload-manifest.sha256").read_text(encoding="utf-8")
            self.assertIn("AGENTS.md", manifest)
            self.assertNotIn("workspaces", manifest)

            synthetic_secret = "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz123456\n"
            (root / "unsafe.md").write_text(synthetic_secret, encoding="utf-8")
            rejected = run("github-readiness.py", "--files-only", cwd=root)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("Anthropic key", rejected.stderr)

    def test_audit_requires_and_records_checklist_pin(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"
            source.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=source, check=True)
            subprocess.run(["git", "config", "user.email", "audit@example.invalid"], cwd=source, check=True)
            subprocess.run(["git", "config", "user.name", "Audit Test"], cwd=source, check=True)
            (source / "README.md").write_text("candidate\n", encoding="utf-8")
            (source / "AGENTS.md").write_text("untrusted\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=source, check=True)
            subprocess.run(["git", "commit", "-qm", "test"], cwd=source, check=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
            check = root / "checklist.json"
            version, check_hash = checklist(check)

            legacy = run("audit.sh", "acme", str(source), commit, cwd=root)
            self.assertNotEqual(legacy.returncode, 0)
            self.assertIn("checklist is required", legacy.stderr)

            result = run(
                "audit.sh",
                "--candidate",
                "acme",
                "--source",
                str(source),
                "--commit",
                commit,
                "--checklist",
                str(check),
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            provenance = (root / "acme-analysis" / "provenance.txt").read_text(encoding="utf-8")
            self.assertIn(f"checklist_version: {version}", provenance)
            self.assertIn(f"checklist_sha256: {check_hash}", provenance)
            self.assertTrue((root / "workspaces/acme/src/AGENTS.md.candidate-evidence").is_file())
            push_url = subprocess.check_output(
                ["git", "-C", str(root / "workspaces/acme/src"), "remote", "get-url", "--push", "origin"],
                text=True,
            ).strip()
            self.assertEqual(push_url, "/dev/null")

    def test_artifact_manifest_is_scoped_and_deterministic(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            evidence = root / "workspaces/acme/evidence"
            evidence.mkdir(parents=True)
            (evidence / "C31.pdf").write_bytes(b"pdf evidence")
            (evidence / "staging.postman_environment.json").write_text("{}", encoding="utf-8")
            result = run("build-artifact-manifest.py", "--candidate", "acme", cwd=root)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((root / "acme-analysis/artifact-manifest.json").read_text())
            self.assertEqual(manifest["artifact_count"], 2)
            self.assertTrue(all(a["routing_state"] == "unmapped" for a in manifest["artifacts"]))
            environment = next(a for a in manifest["artifacts"] if "environment" in a["filename"])
            self.assertEqual(environment["type"], "postman_environment")
            self.assertTrue(environment["sensitive_name"])

    def test_validator_prevents_pass_with_missing_all_method(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            reports = root / "reports"
            items = reports / "acme-2026-11-13-items"
            items.mkdir(parents=True)
            check = root / "checklist.json"
            version, check_hash = checklist(check)
            item_name = "C.31-brand-image-library.md"
            body = f"""---
candidate: acme
item_code: C.31
uid: MSPR-0052
checklist_version: {version}
checklist_sha256: {check_hash}
candidate_commit: {'b' * 40}
candidate_tree: {'c' * 40}
review_date: 2026-11-13
verification_expression: ALL(Code, UX)
confirmed_methods: [\"Code\"]
verdict: PASS
---
# C.31 — Per-brand image library
## Conclusion
Test.
## Atomic obligations
Test.
## Executable-code evidence
Test.
## Non-code evidence
Test.
## Adversarial checks
Test.
## Limitations
Test.
## Required closure
Test.
"""
            (items / item_name).write_text(body, encoding="utf-8")
            (items / "README.md").write_text(item_name, encoding="utf-8")
            consolidated = reports / "acme-2026-11-13-review.md"
            consolidated.write_text(f"{version}\n{check_hash}\n{item_name}\n", encoding="utf-8")
            args = (
                "--candidate",
                "acme",
                "--checklist",
                str(check),
                "--consolidated",
                str(consolidated),
                "--items-dir",
                str(items),
            )
            failed = run("validate-audit-reports.py", *args, cwd=root)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("PASS prohibited", failed.stderr)

            fixed = body.replace('["Code"]', '["Code", "UX"]')
            (items / item_name).write_text(fixed, encoding="utf-8")
            passed = run("validate-audit-reports.py", *args, cwd=root)
            self.assertEqual(passed.returncode, 0, passed.stderr)

    def test_packager_uses_allowlist_and_rejects_secrets(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            report = root / "reports/acme-2026-11-13-review.md"
            report.parent.mkdir(parents=True)
            report.write_text("sanitized report\n", encoding="utf-8")
            allowlist = root / "allowlist.txt"
            allowlist.write_text("reports/acme-2026-11-13-review.md\n", encoding="utf-8")
            output = root / "deliverables/acme-2026-11-13.zip"
            result = run(
                "package-audit-reports.py",
                "--candidate",
                "acme",
                "--allowlist",
                str(allowlist),
                "--output",
                str(output),
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(
                    sorted(archive.namelist()),
                    ["MANIFEST.sha256", "acme-2026-11-13-review.md"],
                )

            unsafe = root / "reports/acme-2026-11-13-unsafe.md"
            unsafe.write_text("Authorization: Bearer eyJaaa.bbb.ccc\n", encoding="utf-8")
            allowlist.write_text("reports/acme-2026-11-13-unsafe.md\n", encoding="utf-8")
            rejected = run(
                "package-audit-reports.py",
                "--candidate",
                "acme",
                "--allowlist",
                str(allowlist),
                "--output",
                str(root / "deliverables/acme-unsafe.zip"),
                cwd=root,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("JWT bearer token", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
