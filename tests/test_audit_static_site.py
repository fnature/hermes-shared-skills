#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "website-seo-ai-agent-readiness" / "scripts" / "audit_static_site.py"


class AuditStaticSiteTests(unittest.TestCase):
    def run_audit(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), "--json", *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_sound_source_has_no_failures_without_production_facts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                """<!doctype html><html lang="en"><head>
                <title>Home — Example</title>
                <meta name="description" content="Useful example page.">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                </head><body><main><h1>Home</h1><a href="about.html">About</a></main></body></html>""",
                encoding="utf-8",
            )
            (root / "about.html").write_text(
                """<!doctype html><html lang="en"><head>
                <title>About — Example</title>
                <meta name="description" content="About the example.">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                </head><body><main><h1 id="about">About</h1><a href="index.html">Home</a></main></body></html>""",
                encoding="utf-8",
            )
            result = self.run_audit(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"FAIL": 0', result.stdout)
            self.assertIn('"BLOCKED":', result.stdout)

    def test_broken_foundations_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<html><body><a href="missing.html">Broken</a><img src="x.jpg"></body></html>',
                encoding="utf-8",
            )
            result = self.run_audit(root)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('"status": "FAIL"', result.stdout)
            self.assertIn('"code": "broken-link"', result.stdout)
            self.assertIn('"code": "missing-alt"', result.stdout)

    def test_production_requires_discovery_files_and_canonicals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                """<!doctype html><html><head><title>Example</title>
                <meta name="description" content="Example.">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                </head><body><main><h1>Example</h1></main></body></html>""",
                encoding="utf-8",
            )
            result = self.run_audit(root, "--base-url", "https://example.com", "--production")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('"code": "canonical"', result.stdout)
            self.assertIn('"code": "robots"', result.stdout)
            self.assertIn('"code": "sitemap"', result.stdout)


if __name__ == "__main__":
    unittest.main()
