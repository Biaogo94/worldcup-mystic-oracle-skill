#!/usr/bin/env python3
"""Build one high-probability primary betting strategy from official odds."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def find_match(cache: dict[str, Any], match_id: int | None) -> dict[str, Any] | None:
    matches = cache.get("matches") or []
    if match_id is None:
        return matches[0] if matches else None
    for match in matches:
        if match.get("match_id") == match_id:
            return match
    return None


def odd_for(match: dict[str, Any], pool: str, selection: str) -> float | None:
    odds = (match.get("odds") or {}).get(pool) or {}
    key_map = {
        "HAD": {"胜": "h", "平": "d", "负": "a"},
        "HHAD": {"让胜": "h", "让平": "d", "让负": "a"},
    }
    key = key_map.get(pool, {}).get(selection)
    if not key:
        return None
    value = odds.get(key)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def normalize_candidates(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = []
    for item in raw:
        pool = item.get("pool")
        selection = item.get("selection")
        if not pool or not selection:
            raise SystemExit("Each candidate requires pool and selection.")
        candidates.append(
            {
                "pool": pool,
                "selection": selection,
                "weight": float(item.get("weight", 1.0)),
                "reason": item.get("reason", ""),
            }
        )
    return candidates


def parse_candidates(value: str) -> list[dict[str, Any]]:
    path = Path(value)
    if path.exists():
        raw = load_json(value)
    else:
        try:
            raw = json.loads(value)
        except json.JSONDecodeError:
            raw = []
            for part in value.split(","):
                if not part.strip():
                    continue
                pieces = [piece.strip() for piece in part.split(":")]
                if len(pieces) < 2:
                    raise SystemExit("Candidate shorthand must look like HAD:负:1 or HHAD:让平:0.8.")
                raw.append(
                    {
                        "pool": pieces[0],
                        "selection": pieces[1],
                        "weight": float(pieces[2]) if len(pieces) >= 3 and pieces[2] else 1.0,
                    }
                )
    if not isinstance(raw, list):
        raise SystemExit("Candidates must be a JSON list, a file containing a JSON list, or shorthand pool:selection:weight.")
    return normalize_candidates(raw)


def choose_strategy(match: dict[str, Any] | None, candidates: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    if not match:
        return {"strategy": "不下注", "reason": "官方体彩未找到对应比赛。", "allocations": []}
    if not candidates:
        return {"strategy": "不下注", "reason": "没有可执行候选分支。", "allocations": []}

    enriched = []
    for candidate in candidates:
        odd = odd_for(match, candidate["pool"], candidate["selection"])
        if odd is None:
            continue
        implied = 1.0 / odd if odd > 0 else 0.0
        score = candidate["weight"] * implied
        enriched.append({**candidate, "odds": odd, "implied": implied, "score": score})

    if not enriched:
        return {"strategy": "不下注", "reason": "候选玩法没有官方可用赔率。", "allocations": []}

    enriched.sort(key=lambda item: item["score"], reverse=True)
    if mode == "single" or len(enriched) == 1:
        picks = [(enriched[0], 100.0)]
        strategy = "单锚"
    elif mode == "three" and len(enriched) >= 3:
        picks = [(enriched[0], 60.0), (enriched[1], 25.0), (enriched[2], 15.0)]
        strategy = "三分支覆盖"
    else:
        picks = [(enriched[0], 70.0), (enriched[1], 30.0)]
        strategy = "双分支覆盖"

    allocations = []
    for pick, pct in picks:
        allocations.append(
            {
                "pool": pick["pool"],
                "selection": pick["selection"],
                "percentage": pct,
                "stake_100_units": pct,
                "odds": pick["odds"],
                "conditional_return_100_units": round(pct * pick["odds"], 2),
                "oracle_reason": pick.get("reason", ""),
            }
        )

    return {
        "strategy": strategy,
        "reason": "按候选权重与官方赔率隐含概率选择命中概率优先分支。",
        "match": {
            "match_id": match.get("match_id"),
            "match_num_str": match.get("match_num_str"),
            "home": (match.get("home") or {}).get("name"),
            "away": (match.get("away") or {}).get("name"),
            "status": match.get("status"),
            "hhad_goal_line": ((match.get("odds") or {}).get("HHAD") or {}).get("goal_line"),
        },
        "allocations": allocations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create one primary Sporttery strategy.")
    parser.add_argument("--odds-cache", required=True)
    parser.add_argument("--candidates", required=True, help="JSON list, path to JSON list, or shorthand like HAD:负:1,HHAD:让平:0.8")
    parser.add_argument("--match-id", type=int)
    parser.add_argument("--mode", choices=["auto", "single", "two", "three"], default="auto")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--utf8", action="store_true")
    args = parser.parse_args()

    cache = load_json(args.odds_cache)
    mode = "single" if args.mode == "auto" else args.mode
    result = {
        "schema": "worldcup-mystic-oracle/primary-bet-strategy-v1",
        "odds_retrieved_at": cache.get("retrieved_at"),
        **choose_strategy(find_match(cache, args.match_id), parse_candidates(args.candidates), mode),
        "note": "Entertainment-only. This helper formats the chosen strategy; it does not guarantee results.",
    }
    json.dump(result, sys.stdout, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
