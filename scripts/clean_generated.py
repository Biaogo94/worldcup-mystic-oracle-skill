#!/usr/bin/env python3
"""Remove generated local artifacts before packaging."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    removed = []
    for pycache in ROOT.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            removed.append(str(pycache.relative_to(ROOT)))
    for pyc in ROOT.rglob("*.pyc"):
        if pyc.exists():
            pyc.unlink()
            removed.append(str(pyc.relative_to(ROOT)))
    if removed:
        print("Removed generated files:")
        for item in removed:
            print(f"- {item}")
    else:
        print("No generated files to remove.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
