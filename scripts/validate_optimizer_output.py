#!/usr/bin/env python3
"""Validate optimizer output shape for smoke tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_optimizer_output.py path/to/output.json")
        return 2
    data = json.loads(read_text(Path(sys.argv[1])))
    picks = data.get("picks") or []
    if data.get("strategy") != "进退综合":
        print(f"ERROR: unexpected strategy {data.get('strategy')!r}")
        return 1
    if len(picks) < 2:
        print("ERROR: optimizer should return at least two picks in this smoke case")
        return 1
    if any(pick.get("pool") == "CRS" and float(pick.get("stake", 0)) > 15 for pick in picks):
        print("ERROR: CRS stake exceeds default cap")
        return 1
    print(
        "Optimizer output is valid:",
        data.get("strategy"),
        len(picks),
        data.get("hit_weight"),
        data.get("min_return"),
        data.get("max_return"),
    )
    print([(pick["pool"], pick["selection"], pick["stake"]) for pick in picks])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
