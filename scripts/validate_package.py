#!/usr/bin/env python3
"""Validate package layout for the universal skill."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "package.json",
    "bin/install-skill.mjs",
    "skill/worldcup-mystic-oracle/SKILL.md",
    "skill/worldcup-mystic-oracle/scripts/fetch_sporttery_odds.py",
    "skill/worldcup-mystic-oracle/scripts/collect_match_bundle.py",
    "skill/worldcup-mystic-oracle/scripts/optimize_strategy.py",
    "skill/worldcup-mystic-oracle/references/betting-strategies.md",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    skill = (ROOT / "skill/worldcup-mystic-oracle/SKILL.md").read_text(encoding="utf-8")
    errors = []
    if missing:
        errors.append(f"missing files: {missing}")
    if "bin" not in package or "worldcup-mystic-oracle-skill" not in package["bin"]:
        errors.append("package.json lacks expected bin entry")
    if "description:" not in skill.split("---", 2)[1]:
        errors.append("SKILL.md frontmatter lacks description")
    if "Hermes" in skill:
        errors.append("SKILL.md should not be Hermes-specific")
    try:
        npm_command = ["cmd", "/c", "npm"] if os.name == "nt" else ["npm"]
        pack = subprocess.run(
            [*npm_command, "pack", "--dry-run", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if pack.returncode != 0:
            errors.append(f"npm pack dry-run failed: {pack.stderr[:400]}")
        else:
            stdout = pack.stdout.strip()
            json_start = stdout.find("[")
            if json_start < 0:
                errors.append(f"npm pack did not emit JSON: {stdout[:400]}")
                packed = {"files": []}
            else:
                packed = json.loads(stdout[json_start:])[0]
            bad_entries = [
                item["path"]
                for item in packed.get("files", [])
                if "__pycache__" in item["path"]
                or item["path"].endswith(".pyc")
                or item["path"].startswith("data/")
            ]
            if bad_entries:
                errors.append(f"npm package contains generated files: {bad_entries}")
    except FileNotFoundError:
        errors.append("npm is not available; cannot validate npx package contents")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Package layout is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
