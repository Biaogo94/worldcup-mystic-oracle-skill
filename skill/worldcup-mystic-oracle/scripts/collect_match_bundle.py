#!/usr/bin/env python3
"""Collect a reusable pre-match bundle for the oracle skill.

This script intentionally does not browse the web for narrative facts. It
collects deterministic local/API artifacts that CLI agents can reuse:
Sporttery odds, optional qfdk Qi Men chart, and optional three-pillar bazi.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def run_command(command: list[str], output_path: Path | None = None) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if output_path and result.stdout:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.stdout, encoding="utf-8")
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_path": str(output_path) if output_path else None,
        "stdout_preview": result.stdout[:800],
        "stderr_preview": result.stderr[:800],
        "status": "ok" if result.returncode == 0 else "failed",
    }


def json_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "path": str(path)}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"status": "unreadable", "path": str(path), "reason": str(exc)}
    return {
        "status": payload.get("status", "ok"),
        "path": str(path),
        "schema": payload.get("schema"),
        "summary": payload.get("summary"),
        "retrieved_at": payload.get("retrieved_at"),
        "matches": len(payload.get("matches") or []),
    }


def infer_match_date(kickoff_local: str | None) -> str | None:
    if not kickoff_local:
        return None
    text = kickoff_local.strip().replace(" ", "T")
    date_part = text.split("T", 1)[0]
    try:
        datetime.fromisoformat(date_part)
    except ValueError:
        return None
    return date_part


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect worldcup-mystic-oracle pre-match bundle.")
    parser.add_argument("--home", help="Official/listed home team name for the bundle metadata.")
    parser.add_argument("--away", help="Official/listed away team name for the bundle metadata.")
    parser.add_argument("--team", help="Sporttery team/match-number search text. Defaults to home or away.")
    parser.add_argument("--match-id", type=int, help="Sporttery matchId.")
    parser.add_argument("--kickoff-local", help="Venue-local kickoff datetime, e.g. 2026-06-16T18:00:00-04:00.")
    parser.add_argument("--venue", help="Venue/city text for metadata and qimen disclosure.")
    parser.add_argument("--people", help="people.json for bazi_three_pillars.py.")
    parser.add_argument("--qimen-engine-dir", help="Local qfdk/qimen checkout.")
    parser.add_argument("--output-dir", default="data/oracle-bundle")
    parser.add_argument("--include-history", action="store_true", help="Fetch Sporttery fixed-bonus history.")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--utf8", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    steps: dict[str, Any] = {}
    sporttery_path = output_dir / "sporttery_odds.json"
    odds_command = [
        sys.executable,
        str(SCRIPT_DIR / "fetch_sporttery_odds.py"),
        "--output",
        str(sporttery_path),
        "--pretty",
        "--utf8",
    ]
    if args.match_id is not None:
        odds_command += ["--match-id", str(args.match_id)]
    else:
        search_text = args.team or args.home or args.away
        if search_text:
            odds_command += ["--team", search_text]
    if args.include_history:
        odds_command.append("--include-history")
    steps["sporttery"] = run_command(odds_command)

    qimen_path = output_dir / "qimen.json"
    if args.kickoff_local and args.qimen_engine_dir:
        qimen_command = [
            "node",
            str(SCRIPT_DIR / "qimen_qfdk.js"),
            "--engine-dir",
            args.qimen_engine_dir,
            "--datetime",
            args.kickoff_local,
            "--location",
            args.venue or "",
            "--pretty",
        ]
        steps["qimen"] = run_command(qimen_command, qimen_path)
    else:
        steps["qimen"] = {
            "status": "skipped",
            "reason": "Provide both --kickoff-local and --qimen-engine-dir to generate qimen.json.",
            "stdout_path": str(qimen_path),
        }

    bazi_path = output_dir / "bazi_three_pillars.json"
    match_date = infer_match_date(args.kickoff_local)
    if args.people and match_date:
        bazi_command = [
            sys.executable,
            str(SCRIPT_DIR / "bazi_three_pillars.py"),
            "--people",
            args.people,
            "--match-date",
            match_date,
            "--pretty",
            "--utf8",
        ]
        steps["bazi"] = run_command(bazi_command, bazi_path)
    else:
        steps["bazi"] = {
            "status": "skipped",
            "reason": "Provide --people and --kickoff-local to generate bazi_three_pillars.json.",
            "stdout_path": str(bazi_path),
        }

    bundle = {
        "schema": "worldcup-mystic-oracle/match-bundle-v1",
        "status": "ok",
        "metadata": {
            "home": args.home,
            "away": args.away,
            "team_search": args.team,
            "sporttery_match_id": args.match_id,
            "kickoff_local": args.kickoff_local,
            "venue": args.venue,
        },
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "artifacts": {
            "sporttery": json_status(sporttery_path),
            "qimen": json_status(qimen_path),
            "bazi": json_status(bazi_path),
        },
        "steps": steps,
        "next": [
            "Use sporttery_odds.json for official odds arithmetic.",
            "Use qimen.json only if status is parsed.",
            "Use bazi_three_pillars.json as missing-hour three-pillar support only.",
            "Create weighted score scenarios, then run optimize_strategy.py.",
        ],
    }

    text = json.dumps(bundle, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
    (output_dir / "bundle.json").write_text(text + "\n", encoding="utf-8")
    sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
