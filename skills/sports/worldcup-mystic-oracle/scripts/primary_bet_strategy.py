#!/usr/bin/env python3
"""Build one primary betting strategy from official Sporttery odds.

The helper cannot guarantee profit. It can format either a single high-hit
anchor or a balanced structure that shows conditional recovery and upside.
"""

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


def pool_label(pool: str) -> str:
    return {
        "HAD": "胜平负",
        "HHAD": "让球胜平负",
        "CRS": "比分",
        "TTG": "总进球",
        "HAFU": "半全场",
    }.get(pool, pool)


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
                "role": str(item.get("role", "") or ""),
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
                        "role": pieces[3] if len(pieces) >= 4 else "",
                    }
                )
    if not isinstance(raw, list):
        raise SystemExit("Candidates must be a JSON list, a file containing a JSON list, or shorthand pool:selection:weight.")
    return normalize_candidates(raw)


def enrich_candidates(match: dict[str, Any], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for candidate in candidates:
        odd = odd_for(match, candidate["pool"], candidate["selection"])
        if odd is None:
            continue
        implied = 1.0 / odd if odd > 0 else 0.0
        score = candidate["weight"] * implied
        enriched.append({**candidate, "odds": odd, "implied": implied, "score": score})
    return sorted(enriched, key=lambda item: item["score"], reverse=True)


def pick_by_role(enriched: list[dict[str, Any]], role: str) -> dict[str, Any] | None:
    for item in sorted(enriched, key=lambda candidate: candidate["weight"], reverse=True):
        if item.get("role") == role:
            return item
    return None


def strategy_match_info(match: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_id": match.get("match_id"),
        "match_num_str": match.get("match_num_str"),
        "home": (match.get("home") or {}).get("name"),
        "away": (match.get("away") or {}).get("name"),
        "status": match.get("status"),
        "hhad_goal_line": ((match.get("odds") or {}).get("HHAD") or {}).get("goal_line"),
    }


def allocation_row(pick: dict[str, Any], pct: float, purpose: str) -> dict[str, Any]:
    conditional_return = round(pct * pick["odds"], 2)
    return {
        "pool": pick["pool"],
        "pool_label": pool_label(pick["pool"]),
        "selection": pick["selection"],
        "purpose": purpose,
        "percentage": pct,
        "stake_100_units": pct,
        "odds": pick["odds"],
        "conditional_return_100_units": conditional_return,
        "net_if_only_this_branch_hits": round(conditional_return - 100.0, 2),
        "oracle_reason": pick.get("reason", ""),
    }


def parse_goal_line(match: dict[str, Any]) -> float | None:
    value = ((match.get("odds") or {}).get("HHAD") or {}).get("goal_line")
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def had_selection_for_diff(diff: int) -> str:
    if diff > 0:
        return "胜"
    if diff < 0:
        return "负"
    return "平"


def hhad_selection_for_diff(diff: int, goal_line: float) -> str:
    adjusted = diff + goal_line
    if adjusted > 0:
        return "让胜"
    if adjusted < 0:
        return "让负"
    return "让平"


def scenario_label(diff: int) -> str:
    if diff >= 3:
        return "主胜3+"
    if diff == 2:
        return "主胜2"
    if diff == 1:
        return "主胜1"
    if diff == 0:
        return "平局"
    if diff == -1:
        return "客胜1"
    if diff == -2:
        return "客胜2"
    return "客胜3+"


def hit_selection_for_pick(pick: dict[str, Any], diff: int, goal_line: float | None) -> str | None:
    if pick["pool"] == "HAD":
        return had_selection_for_diff(diff)
    if pick["pool"] == "HHAD" and goal_line is not None:
        return hhad_selection_for_diff(diff, goal_line)
    return None


def scenario_returns(match: dict[str, Any], allocations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    goal_line = parse_goal_line(match)
    if not allocations:
        return []

    scenarios = []
    for diff in (3, 2, 1, 0, -1, -2, -3):
        hits = []
        total_return = 0.0
        for row in allocations:
            expected = hit_selection_for_pick(row, diff, goal_line)
            if expected == row["selection"]:
                total_return += float(row["stake_100_units"]) * float(row["odds"])
                hits.append(f"{row['pool_label']} {row['selection']}")
        scenarios.append(
            {
                "scenario": scenario_label(diff),
                "goal_diff_home_minus_away": diff,
                "hits": hits,
                "conditional_return_100_units": round(total_return, 2),
                "net_100_units": round(total_return - 100.0, 2),
            }
        )
    return scenarios


def choose_balanced_strategy(match: dict[str, Any], enriched: list[dict[str, Any]]) -> dict[str, Any]:
    if not enriched:
        return {"strategy": "不下注", "reason": "候选玩法没有官方可用赔率。", "allocations": []}

    main = pick_by_role(enriched, "main") or enriched[0]
    attack = pick_by_role(enriched, "attack")
    protect = pick_by_role(enriched, "protect")

    picks: list[tuple[dict[str, Any], float, str]] = []
    main_odd = main["odds"]

    if attack and protect:
        if main_odd >= 1.60:
            main_pct = 65.0
            attack_pct = 20.0
            protect_pct = 15.0
        else:
            main_pct = 75.0
            attack_pct = 15.0
            protect_pct = 10.0
        picks = [
            (main, main_pct, "主线回收锚点"),
            (attack, attack_pct, "进攻增益分支"),
            (protect, protect_pct, "退守保护分支"),
        ]
    elif attack:
        if main_odd >= 1.60:
            main_pct = 75.0
            attack_pct = 25.0
        else:
            main_pct = 85.0
            attack_pct = 15.0
        picks = [
            (main, main_pct, "主线回收锚点"),
            (attack, attack_pct, "进攻增益分支"),
        ]
    elif protect:
        picks = [
            (main, 80.0, "主线回收锚点"),
            (protect, 20.0, "退守保护分支"),
        ]
    else:
        picks = [(main, 100.0, "主线单锚")]

    allocations = [allocation_row(pick, pct, purpose) for pick, pct, purpose in picks]
    scenarios = scenario_returns(match, allocations)
    main_hit_scenarios = []
    if scenarios:
        main_pool_label = allocations[0]["pool_label"]
        main_selection = allocations[0]["selection"]
        main_hit = f"{main_pool_label} {main_selection}"
        main_hit_scenarios = [scenario for scenario in scenarios if main_hit in scenario["hits"]]

    if main_hit_scenarios:
        min_main_return = min(scenario["conditional_return_100_units"] for scenario in main_hit_scenarios)
        max_main_return = max(scenario["conditional_return_100_units"] for scenario in main_hit_scenarios)
        if min_main_return >= 100:
            recovery_note = (
                f"主线命中路径最低返还 {min_main_return} 单位、最高返还 {max_main_return} 单位，"
                f"均覆盖 100 单位成本。"
            )
        else:
            recovery_note = (
                f"主线命中路径最低返还 {min_main_return} 单位、最高返还 {max_main_return} 单位；"
                "部分主线情景不能覆盖 100 单位成本。"
            )
    else:
        main_return = allocations[0]["conditional_return_100_units"]
        if main_return >= 100:
            recovery_note = f"主线命中时返还 {main_return} 单位，覆盖 100 单位成本后净 {round(main_return - 100, 2)}。"
        else:
            recovery_note = (
                f"主线命中时返还 {main_return} 单位，不能覆盖 100 单位成本；"
                "这是高胜率低赔率结构，收益依赖进攻分支。"
            )

    all_returns = [scenario["conditional_return_100_units"] for scenario in scenarios] or [
        row["conditional_return_100_units"] for row in allocations
    ]
    return {
        "strategy": "进退综合",
        "reason": "以官方赔率计算主线条件回收，再用少量分支覆盖进攻或退守路径；不能保证收益。",
        "match": strategy_match_info(match),
        "recovery_note": recovery_note,
        "best_case_return_100_units": max(all_returns),
        "worst_case_net_100_units": round(min(all_returns) - 100.0, 2),
        "allocations": allocations,
        "scenario_returns": scenarios,
    }


def choose_strategy(match: dict[str, Any] | None, candidates: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    if not match:
        return {"strategy": "不下注", "reason": "官方体彩未找到对应比赛。", "allocations": []}
    if not candidates:
        return {"strategy": "不下注", "reason": "没有可执行候选分支。", "allocations": []}

    enriched = enrich_candidates(match, candidates)

    if not enriched:
        return {"strategy": "不下注", "reason": "候选玩法没有官方可用赔率。", "allocations": []}

    if mode == "balanced":
        return choose_balanced_strategy(match, enriched)

    if mode == "single" or len(enriched) == 1:
        picks = [(enriched[0], 100.0)]
        strategy = "单锚"
    elif mode == "three" and len(enriched) >= 3:
        picks = [(enriched[0], 60.0), (enriched[1], 25.0), (enriched[2], 15.0)]
        strategy = "三分支覆盖"
    else:
        picks = [(enriched[0], 70.0), (enriched[1], 30.0)]
        strategy = "双分支覆盖"

    allocations = [allocation_row(pick, pct, "命中概率优先分支") for pick, pct in picks]

    return {
        "strategy": strategy,
        "reason": "按候选权重与官方赔率隐含概率选择命中概率优先分支。",
        "match": strategy_match_info(match),
        "allocations": allocations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create one primary Sporttery strategy.")
    parser.add_argument("--odds-cache", required=True)
    parser.add_argument("--candidates", required=True, help="JSON list, path to JSON list, or shorthand like HAD:负:1,HHAD:让平:0.8")
    parser.add_argument("--match-id", type=int)
    parser.add_argument("--mode", choices=["auto", "balanced", "single", "two", "three"], default="auto")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--utf8", action="store_true")
    args = parser.parse_args()

    cache = load_json(args.odds_cache)
    mode = "balanced" if args.mode == "auto" else args.mode
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
