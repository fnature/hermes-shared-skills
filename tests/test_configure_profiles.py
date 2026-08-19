#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "configure_all_profiles.py"
spec = importlib.util.spec_from_file_location("configure_all_profiles", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ConfigureProfilesTests(unittest.TestCase):
    def test_adds_scalar_to_config_without_skills_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.yaml"
            config.write_text("model:\n  default: example\n", encoding="utf-8")
            self.assertEqual(module.ensure_config(config, True), "updated")
            self.assertIn(
                f"skills:\n  external_dirs: {module.SHARED}\n",
                config.read_text(encoding="utf-8"),
            )
            self.assertEqual(module.ensure_config(config, False), "already configured")

    def test_appends_to_existing_external_dirs_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.yaml"
            config.write_text(
                "skills:\n  external_dirs:\n  - /another/shared/skills\n",
                encoding="utf-8",
            )
            self.assertEqual(module.ensure_config(config, True), "updated")
            self.assertIn(f"  - {module.SHARED}", config.read_text(encoding="utf-8"))

    def test_repairs_quoted_json_scalar_created_by_config_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.yaml"
            config.write_text(
                f"skills:\n  external_dirs: '[\"{module.SHARED}\"]'\n",
                encoding="utf-8",
            )
            self.assertEqual(
                module.ensure_config(config, False),
                "would repair quoted JSON external_dirs value",
            )
            self.assertEqual(
                module.ensure_config(config, True),
                "repaired quoted JSON external_dirs value",
            )
            self.assertIn(
                f"external_dirs: {module.SHARED}",
                config.read_text(encoding="utf-8"),
            )
            self.assertEqual(module.ensure_config(config, False), "already configured")


if __name__ == "__main__":
    unittest.main()
