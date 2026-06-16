#!/usr/bin/env python3
"""Render a simple stake summary for a mystical football lottery plan.

The script summarizes exposure only. It does not verify live lottery availability,
odds, pass types, or whether a terminal supports a specific combination.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


DEMO_PLAN: dict[str, Any] = {
    "bankroll": 100,
    "unit_name": "元",
    "plans": [
        {
            "name": "稳健小注",
            "items": [
                {"play": "胜平负", "picks": ["胜"], "stake": 45},
                {"play": "让球胜平负(-1)", "picks": ["让平"], "stake": 25},
                {"play": "总进球", "picks": ["2", "3"], "stake": 20},
                {"play": "比分", "picks": ["1:0", "2:1"], "stake": 10},
            ],
        }
    ],
}


def money(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def load_plan(path: str | None, demo: bool) -> dict[str, Any]:
    if demo:
        return DEMO_PLAN
    if not path:
        raise SystemExit("Provide --file plan.json or use --demo.")
    return json.loads(Path(path).read_text(encoding="utf-8"))


def render(plan: dict[str, Any]) -> str:
    bankroll = money(plan.get("bankroll", 0))
    unit_name = str(plan.get("unit_name", "units"))
    lines = [
        "# Bet Plan Summary",
        "",
        f"Bankroll cap: {bankroll} {unit_name}",
        "",
    ]

    grand_total = Decimal("0.00")
    for plan_item in plan.get("plans", []):
        name = plan_item.get("name", "Unnamed plan")
        lines.extend([f"## {name}", "", "| Play | Picks | Stake | Per Pick |", "| --- | --- | ---: | ---: |"])
        subtotal = Decimal("0.00")
        for item in plan_item.get("items", []):
            play = str(item.get("play", ""))
            picks = [str(pick) for pick in item.get("picks", [])]
            if not picks:
                raise SystemExit(f"{name}/{play} has no picks.")
            stake = money(item.get("stake", 0))
            if stake < 0:
                raise SystemExit(f"{name}/{play} has a negative stake.")
            per_pick = (stake / Decimal(len(picks))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            subtotal += stake
            lines.append(f"| {play} | {', '.join(picks)} | {stake} | {per_pick} |")
        pct = (subtotal / bankroll * Decimal("100")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) if bankroll else Decimal("0.0")
        lines.extend(["", f"Subtotal: {subtotal} {unit_name} ({pct}% of bankroll cap)", ""])
        grand_total += subtotal

    grand_pct = (grand_total / bankroll * Decimal("100")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) if bankroll else Decimal("0.0")
    lines.extend([f"Grand total: {grand_total} {unit_name} ({grand_pct}% of bankroll cap)", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a simple football lottery stake summary.")
    parser.add_argument("--file", help="Path to a JSON stake plan.")
    parser.add_argument("--demo", action="store_true", help="Render a built-in demo plan.")
    args = parser.parse_args()
    print(render(load_plan(args.file, args.demo)))


if __name__ == "__main__":
    main()
