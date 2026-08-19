#!/usr/bin/env python3
"""Ensure every existing Hermes profile scans the canonical shared skill directory.

The editor is intentionally conservative and dependency-free. It only modifies a
config when the canonical path is absent and refuses ambiguous duplicate top-level
skills blocks.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SHARED = "/workspace/dev/hermes-shared-skills/skills"


def profile_homes(root: Path) -> list[Path]:
    homes = [root]
    profiles = root / "profiles"
    if profiles.is_dir():
        homes.extend(sorted(p for p in profiles.iterdir() if p.is_dir()))
    return [p for p in homes if (p / "config.yaml").is_file()]


def ensure_config(path: Path, apply: bool) -> str:
    text = path.read_text(encoding="utf-8")
    list_entry = re.compile(rf"(?m)^\s*-\s*{re.escape(SHARED)}\s*$")
    scalar_entry = re.compile(
        rf"(?m)^\s*external_dirs:\s*['\"]?{re.escape(SHARED)}['\"]?\s*$"
    )
    if list_entry.search(text) or scalar_entry.search(text):
        return "already configured"

    malformed_entry = re.compile(
        rf"(?m)^(?P<indent>[ \t]*)external_dirs:\s*['\"]?\[.*{re.escape(SHARED)}.*\]['\"]?\s*$"
    )
    malformed = malformed_entry.search(text)
    if malformed:
        indent = malformed.group("indent")
        updated = (
            text[: malformed.start()]
            + f"{indent}external_dirs: {SHARED}"
            + text[malformed.end() :]
        )
        if apply:
            path.write_text(updated, encoding="utf-8")
            return "repaired quoted JSON external_dirs value"
        return "would repair quoted JSON external_dirs value"
    skills = list(re.finditer(r"(?m)^skills:\s*$", text))
    if len(skills) > 1:
        raise RuntimeError(f"ambiguous duplicate top-level skills blocks: {path}")
    if not skills:
        addition = f"\nskills:\n  external_dirs: {SHARED}\n"
        updated = text.rstrip() + addition
    else:
        start = skills[0].end()
        next_top = re.search(r"(?m)^\S[^\n]*:\s*(?:#.*)?$", text[start:])
        end = start + next_top.start() if next_top else len(text)
        block = text[start:end]
        external = re.search(r"(?m)^  external_dirs:\s*$", block)
        if external:
            insertion = start + external.end()
            updated = text[:insertion] + f"\n  - {SHARED}" + text[insertion:]
        else:
            updated = text[:start] + f"\n  external_dirs:\n  - {SHARED}" + text[start:]
    if apply:
        path.write_text(updated, encoding="utf-8")
        return "updated"
    return "would update"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hermes-root", type=Path, default=Path.home() / ".hermes")
    parser.add_argument("--apply", action="store_true", help="Write changes; default is dry-run")
    args = parser.parse_args()
    for home in profile_homes(args.hermes_root.expanduser()):
        cfg = home / "config.yaml"
        print(f"{cfg}: {ensure_config(cfg, args.apply)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
