#!/usr/bin/env python3
"""Optimize one Sporttery strategy from weighted score scenarios.

The optimizer is deliberately modest: it searches small integer stake grids
and picks a plan that scores well across oracle-weighted scenarios. It does
not guarantee profit or discover arbitrage.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any


HAD_LABELS = {"h": "胜", "d": "平", "a": "负"}
HHAD_LABELS = {"h": "让胜", "d": "让平", "a": "让负"}


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def find_match(cache: dict[str, Any], match_id: int | None) -> dict[str, Any] | None:
    matches = cache.get("matches") or []
    if match_id is None:
        if matches:
            return matches[0]
        history = cache.get("fixed_bonus_history") or {}
        if len(history) == 1:
            key = next(iter(history))
            return match_from_history_entry(key, history[key])
        return None
    for match in matches:
        if match.get("match_id") == match_id:
            return match
    entry = (cache.get("fixed_bonus_history") or {}).get(str(match_id))
    if entry:
        return match_from_history_entry(str(match_id), entry)
    return None


def match_from_history_entry(match_id: str, entry: dict[str, Any]) -> dict[str, Any] | None:
    normalized = entry.get("normalized") or {}
    if not normalized:
        return None
    odds = {}
    for pool in ("HAD", "HHAD"):
        row = normalized.get(pool) or {}
        if any(row.get(key) for key in ("h", "d", "a")):
            odds[pool] = {
                "h": row.get("h"),
                "d": row.get("d"),
                "a": row.get("a"),
                "goal_line": row.get("goal_line"),
            }
    return {
        "match_id": int(match_id),
        "match_num_str": None,
        "home": {"name": normalized.get("home")},
        "away": {"name": normalized.get("away")},
        "status": "history",
        "odds": odds,
        "odds_source": "fixed_bonus_history",
        "available_pools": normalized.get("available_pools") or [],
    }


def decimal(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if out > 0 else None


def current_odd(match: dict[str, Any], pool: str, selection: str) -> tuple[float | None, str | None]:
    label_map = {"HAD": HAD_LABELS, "HHAD": HHAD_LABELS}.get(pool)
    if not label_map:
        return None, None
    key = next((key for key, label in label_map.items() if label == selection), None)
    if not key:
        return None, None
    row = (match.get("odds") or {}).get(pool) or {}
    return decimal(row.get(key)), match.get("odds_source") or "match_list"


def fixed_odd(cache: dict[str, Any], match: dict[str, Any], pool: str, selection: str) -> tuple[float | None, str | None]:
    entry = (cache.get("fixed_bonus_history") or {}).get(str(match.get("match_id"))) or {}
    normalized = entry.get("normalized") or {}
    row = normalized.get(pool) or {}
    if pool in {"HAD", "HHAD"}:
        label_map = {"HAD": HAD_LABELS, "HHAD": HHAD_LABELS}[pool]
        key = next((key for key, label in label_map.items() if label == selection), None)
        if not key:
            return None, None
        return decimal(row.get(key)), "fixed_bonus_history"
    value = ((row.get("odds") or {}).get(selection) or {}).get("odds")
    return decimal(value), "fixed_bonus_history"


def odd_for(cache: dict[str, Any], match: dict[str, Any], pool: str, selection: str) -> tuple[float | None, str | None]:
    odd, source = current_odd(match, pool, selection)
    if odd is not None:
        return odd, source
    return fixed_odd(cache, match, pool, selection)


def parse_goal_line(match: dict[str, Any]) -> float | None:
    value = ((match.get("odds") or {}).get("HHAD") or {}).get("goal_line")
    if value in (None, ""):
        entry_line = ((match.get("odds") or {}).get("HHAD") or {}).get("goalLine")
        value = entry_line
    return decimal(value)


def had_for_score(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "胜"
    if home_goals < away_goals:
        return "负"
    return "平"


def hhad_for_score(home_goals: int, away_goals: int, goal_line: float | None) -> str | None:
    if goal_line is None:
        return None
    adjusted = home_goals - away_goals + goal_line
    if adjusted > 0:
        return "让胜"
    if adjusted < 0:
        return "让负"
    return "让平"


def crs_for_score(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals and home_goals >= 5:
        return "胜其它"
    if home_goals < away_goals and away_goals >= 5:
        return "负其它"
    if home_goals == away_goals and home_goals >= 4:
        return "平其它"
    return f"{home_goals}:{away_goals}"


def ttg_for_score(home_goals: int, away_goals: int) -> str:
    total = home_goals + away_goals
    return "7+" if total >= 7 else str(total)


def normalize_scenarios(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scenarios = []
    for item in raw:
        if "score" in item:
            left, right = str(item["score"]).replace("-", ":").split(":", 1)
            home_goals = int(left)
            away_goals = int(right)
        else:
            home_goals = int(item["home_goals"])
            away_goals = int(item["away_goals"])
        weight = float(item.get("weight", 1.0))
        scenarios.append(
            {
                "label": item.get("label") or f"{home_goals}:{away_goals}",
                "home_goals": home_goals,
                "away_goals": away_goals,
                "weight": weight,
                "note": item.get("note", ""),
            }
        )
    total = sum(item["weight"] for item in scenarios) or 1.0
    for item in scenarios:
        item["probability_weight"] = item["weight"] / total
    return scenarios


def scenario_hits(scenario: dict[str, Any], goal_line: float | None) -> set[tuple[str, str]]:
    home_goals = scenario["home_goals"]
    away_goals = scenario["away_goals"]
    hits = {
        ("HAD", had_for_score(home_goals, away_goals)),
        ("TTG", ttg_for_score(home_goals, away_goals)),
        ("CRS", crs_for_score(home_goals, away_goals)),
    }
    hhad = hhad_for_score(home_goals, away_goals, goal_line)
    if hhad:
        hits.add(("HHAD", hhad))
    return hits


def build_candidates(
    cache: dict[str, Any],
    match: dict[str, Any],
    scenarios: list[dict[str, Any]],
    include_pools: set[str],
    max_candidates: int,
) -> list[dict[str, Any]]:
    goal_line = parse_goal_line(match)
    weighted: dict[tuple[str, str], float] = {}
    for scenario in scenarios:
        for key in scenario_hits(scenario, goal_line):
            if key[0] in include_pools:
                weighted[key] = weighted.get(key, 0.0) + scenario["probability_weight"]

    candidates = []
    for (pool, selection), weight in weighted.items():
        odd, source = odd_for(cache, match, pool, selection)
        if odd is None:
            continue
        candidates.append(
            {
                "pool": pool,
                "selection": selection,
                "odds": odd,
                "odds_source": source,
                "scenario_weight": round(weight, 6),
                "value_score": round(weight * odd, 6),
            }
        )
    candidates.sort(key=lambda item: (item["scenario_weight"], item["value_score"]), reverse=True)
    return candidates[:max_candidates]


def scenario_return(scenario: dict[str, Any], picks: list[dict[str, Any]], goal_line: float | None) -> float:
    hits = scenario_hits(scenario, goal_line)
    total = 0.0
    for pick in picks:
        if (pick["pool"], pick["selection"]) in hits:
            total += pick["stake"] * pick["odds"]
    return total


def score_plan(
    scenarios: list[dict[str, Any]],
    picks: list[dict[str, Any]],
    goal_line: float | None,
    exposure: float,
) -> dict[str, Any]:
    returns = []
    weighted_return = 0.0
    weighted_shortfall = 0.0
    weighted_positive = 0.0
    for scenario in scenarios:
        ret = scenario_return(scenario, picks, goal_line)
        net = ret - exposure
        weighted_return += scenario["probability_weight"] * ret
        if net < 0:
            weighted_shortfall += scenario["probability_weight"] * abs(net)
        else:
            weighted_positive += scenario["probability_weight"] * net
        returns.append(
            {
                "scenario": scenario["label"],
                "score": f"{scenario['home_goals']}:{scenario['away_goals']}",
                "probability_weight": round(scenario["probability_weight"], 4),
                "conditional_return": round(ret, 2),
                "net": round(net, 2),
                "hits": [
                    f"{pick['pool']} {pick['selection']}"
                    for pick in picks
                    if (pick["pool"], pick["selection"]) in scenario_hits(scenario, goal_line)
                ],
            }
        )
    main = max(scenarios, key=lambda item: item["probability_weight"])
    main_ret = scenario_return(main, picks, goal_line)
    min_ret = min(item["conditional_return"] for item in returns) if returns else 0.0
    hit_weight = sum(
        scenario["probability_weight"]
        for scenario, row in zip(scenarios, returns)
        if row["conditional_return"] > 0
    )
    main_coverage = main_ret / exposure if exposure else 0.0
    concentration_penalty = 0.0
    if picks:
        largest_stake = max(pick["stake"] for pick in picks)
        concentration_penalty = max(0.0, largest_stake - exposure * 0.7) * 2.0
    score = (
        hit_weight * 180.0
        + weighted_return * 0.55
        + min(main_coverage, 1.5) * 35.0
        + weighted_positive * 0.15
        - weighted_shortfall * 0.7
        + min_ret * 0.08
        - concentration_penalty
    )
    return {
        "score": round(score, 6),
        "hit_weight": round(hit_weight, 4),
        "expected_weighted_return": round(weighted_return, 2),
        "weighted_shortfall": round(weighted_shortfall, 2),
        "weighted_positive_net": round(weighted_positive, 2),
        "main_scenario_return": round(main_ret, 2),
        "min_return": round(min_ret, 2),
        "max_return": round(max(item["conditional_return"] for item in returns), 2) if returns else 0.0,
        "scenario_returns": returns,
    }


def stake_grids(n: int, exposure: int, step: int) -> list[tuple[int, ...]]:
    values = range(0, exposure + 1, step)
    grids = []
    for combo in itertools.product(values, repeat=n):
        if sum(combo) == exposure and all(value > 0 for value in combo):
            grids.append(combo)
    return grids


def optimize(
    scenarios: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    goal_line: float | None,
    exposure: int,
    step: int,
    max_picks: int,
    max_crs_stake: int,
    max_crs_total: int,
    min_anchor_stake: int,
) -> dict[str, Any]:
    best: dict[str, Any] | None = None
    min_picks = 2 if len(candidates) >= 2 else 1
    for size in range(min_picks, min(max_picks, len(candidates)) + 1):
        for chosen in itertools.combinations(candidates, size):
            pools = {candidate["pool"] for candidate in chosen}
            if len(candidates) >= 3 and len(pools) == 1:
                continue
            for stakes in stake_grids(size, exposure, step):
                if len(stakes) >= 3 and max(stakes) > exposure * 0.75:
                    continue
                picks = [{**dict(candidate), "stake": float(stake)} for candidate, stake in zip(chosen, stakes)]
                crs_total = sum(pick["stake"] for pick in picks if pick["pool"] == "CRS")
                if crs_total > max_crs_total:
                    continue
                if any(pick["pool"] == "CRS" and pick["stake"] > max_crs_stake for pick in picks):
                    continue
                anchor_total = sum(pick["stake"] for pick in picks if pick["pool"] in {"HAD", "HHAD", "TTG"})
                if any(candidate["pool"] in {"HAD", "HHAD", "TTG"} for candidate in candidates) and anchor_total < min_anchor_stake:
                    continue
                metrics = score_plan(scenarios, picks, goal_line, float(exposure))
                candidate_plan = {"picks": picks, **metrics}
                if best is None or candidate_plan["score"] > best["score"]:
                    best = candidate_plan
    return best or {"picks": [], "scenario_returns": [], "score": -math.inf}


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize one Sporttery strategy from score scenarios.")
    parser.add_argument("--odds-cache", required=True)
    parser.add_argument("--scenarios", required=True, help="JSON list or path to JSON list.")
    parser.add_argument("--match-id", type=int)
    parser.add_argument("--include-pools", default="HAD,HHAD,TTG,CRS")
    parser.add_argument("--exposure", type=int, default=100)
    parser.add_argument("--step", type=int, default=5)
    parser.add_argument("--max-candidates", type=int, default=8)
    parser.add_argument("--max-picks", type=int, default=4)
    parser.add_argument("--max-crs-stake", type=int, default=15, help="Maximum 100-unit stake for one exact-score pick.")
    parser.add_argument("--max-crs-total", type=int, default=25, help="Maximum total 100-unit stake for exact-score picks.")
    parser.add_argument("--min-anchor-stake", type=int, default=55, help="Minimum stake for HAD/HHAD/TTG anchors when available.")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--utf8", action="store_true")
    args = parser.parse_args()

    cache = load_json(args.odds_cache)
    match = find_match(cache, args.match_id)
    if not match:
        result = {"schema": "worldcup-mystic-oracle/strategy-optimizer-v1", "strategy": "不下注", "reason": "官方体彩未找到对应比赛。"}
        json.dump(result, sys.stdout, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
        print()
        return 1

    scenario_raw = load_json(args.scenarios) if Path(args.scenarios).exists() else json.loads(args.scenarios)
    scenarios = normalize_scenarios(scenario_raw)
    include_pools = {item.strip() for item in args.include_pools.split(",") if item.strip()}
    candidates = build_candidates(cache, match, scenarios, include_pools, args.max_candidates)
    goal_line = parse_goal_line(match)
    plan = optimize(
        scenarios,
        candidates,
        goal_line,
        args.exposure,
        args.step,
        args.max_picks,
        args.max_crs_stake,
        args.max_crs_total,
        args.min_anchor_stake,
    )

    result = {
        "schema": "worldcup-mystic-oracle/strategy-optimizer-v1",
        "strategy": "进退综合" if plan.get("picks") else "不下注",
        "note": "Entertainment-only. This optimizer searches conditional-return structures; it does not guarantee profit.",
        "match": {
            "match_id": match.get("match_id"),
            "match_num_str": match.get("match_num_str"),
            "home": (match.get("home") or {}).get("name"),
            "away": (match.get("away") or {}).get("name"),
            "hhad_goal_line": ((match.get("odds") or {}).get("HHAD") or {}).get("goal_line"),
        },
        "inputs": {
            "exposure": args.exposure,
            "step": args.step,
            "include_pools": sorted(include_pools),
            "constraints": {
                "max_crs_stake": args.max_crs_stake,
                "max_crs_total": args.max_crs_total,
                "min_anchor_stake": args.min_anchor_stake,
            },
            "scenarios": scenarios,
        },
        "candidate_count": len(candidates),
        "candidates": candidates,
        **plan,
    }
    json.dump(result, sys.stdout, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
