#!/usr/bin/env python3
"""Fetch official China Sports Lottery football odds from Sporttery.

This script uses the official Sporttery web API exposed by sporttery.cn. It
normalizes the current match list and optional fixed-bonus history while
preserving raw fields for auditability.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


MATCH_LIST_URL = "https://webapi.sporttery.cn/gateway/uniform/football/getMatchListV1.qry"
FIXED_BONUS_URL = "https://webapi.sporttery.cn/gateway/uniform/football/getFixedBonusV1.qry"

POOL_LABELS = {
    "HAD": "胜平负",
    "HHAD": "让球胜平负",
    "CRS": "比分固定",
    "TTG": "总进球",
    "HAFU": "半全场",
}

REQUEST_PROFILES = [
    {
        "name": "desktop-chrome",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://www.sporttery.cn/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
        },
    },
    {
        "name": "sporttery-agent",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
            "Referer": "https://www.sporttery.cn/",
            "User-Agent": "Mozilla/5.0 (compatible; worldcup-mystic-oracle/1.0)",
        },
    },
]

THREE_WAY_KEYS = {
    "HAD": {"h": "胜", "d": "平", "a": "负"},
    "HHAD": {"h": "让胜", "d": "让平", "a": "让负"},
}

CRS_LABELS = {
    "s-1sh": "胜其它",
    "s-1sd": "平其它",
    "s-1sa": "负其它",
}

HAFU_LABELS = {
    "hh": "胜胜",
    "hd": "胜平",
    "ha": "胜负",
    "dh": "平胜",
    "dd": "平平",
    "da": "平负",
    "ah": "负胜",
    "ad": "负平",
    "aa": "负负",
}


class FetchError(RuntimeError):
    pass


def configure_stdout(utf8: bool) -> None:
    if utf8 and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def fetch_json_once(url: str, timeout: float, headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
            status = getattr(response, "status", None)
    except urllib.error.HTTPError as exc:
        sample = exc.read(200).decode("utf-8", errors="replace").replace("\n", " ")
        raise FetchError(f"HTTP {exc.code} {exc.reason}: {sample}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(str(exc)) from exc

    try:
        payload = json.loads(body.decode("utf-8"))
        payload["_fetch_status"] = status
        return payload
    except json.JSONDecodeError as exc:
        sample = body[:160].decode("utf-8", errors="replace").replace("\n", " ")
        raise FetchError(f"non-json response ({content_type}): {sample}") from exc


def fetch_json(url: str, timeout: float) -> dict[str, Any]:
    attempts: list[dict[str, str]] = []
    for profile in REQUEST_PROFILES:
        try:
            payload = fetch_json_once(url, timeout, profile["headers"])
            payload["_fetch_profile"] = profile["name"]
            payload["_fetch_attempts"] = attempts + [{"profile": profile["name"], "status": "ok"}]
            return payload
        except FetchError as exc:
            attempts.append({"profile": profile["name"], "status": "failed", "reason": str(exc)})
    raise FetchError("; ".join(f"{item['profile']}: {item['reason']}" for item in attempts))


def non_empty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def decimal(value: Any) -> float | None:
    if not non_empty(value):
        return None
    try:
        return float(str(value))
    except ValueError:
        return None


def implied_probabilities(pool_code: str, odds: dict[str, Any]) -> dict[str, Any] | None:
    label_map = THREE_WAY_KEYS.get(pool_code)
    if not label_map:
        return None

    raw: dict[str, float] = {}
    for key, label in label_map.items():
        odd = decimal(odds.get(key))
        if odd and odd > 0:
            raw[label] = 1.0 / odd

    if len(raw) != 3:
        return None

    total = sum(raw.values())
    return {
        "raw": {key: round(value, 6) for key, value in raw.items()},
        "normalized": {key: round(value / total, 6) for key, value in raw.items()},
        "booksum": round(total, 6),
    }


def normalize_pool_list(pool_list: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    pools: dict[str, dict[str, Any]] = {}
    for item in pool_list or []:
        code = item.get("poolCode")
        if not code:
            continue
        pools[code] = {
            "label": POOL_LABELS.get(code, code),
            "status": item.get("poolStatus"),
            "single": item.get("cbtSingle"),
            "all_up": item.get("cbtAllUp"),
            "raw": item,
        }
    return pools


def normalize_odds_list(odds_list: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    odds_by_pool: dict[str, dict[str, Any]] = {}
    for item in odds_list or []:
        code = item.get("poolCode")
        if not code:
            continue
        odds = {
            "label": POOL_LABELS.get(code, code),
            "h": item.get("h"),
            "d": item.get("d"),
            "a": item.get("a"),
            "odds": item.get("odds"),
            "goal_line": item.get("goalLine"),
            "update_date": item.get("updateDate"),
            "update_time": item.get("updateTime"),
            "raw": item,
        }
        odds["implied_probabilities"] = implied_probabilities(code, item)
        odds_by_pool[code] = odds
    return odds_by_pool


def latest_history_row(rows: Any) -> dict[str, Any] | None:
    if not isinstance(rows, list) or not rows:
        return None
    return rows[-1] if isinstance(rows[-1], dict) else None


def normalize_fixed_ttg(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {}
    odds = {}
    for goals in range(8):
        key = f"s{goals}"
        odd = decimal(row.get(key))
        if odd:
            label = "7+" if goals == 7 else str(goals)
            odds[label] = {"odds": odd, "status_flag": row.get(f"{key}f")}
    return {
        "label": "总进球",
        "update_date": row.get("updateDate"),
        "update_time": row.get("updateTime"),
        "odds": odds,
        "raw": row,
    }


def normalize_fixed_crs(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {}
    odds = {}
    for key, value in row.items():
        if not key.startswith("s") or key.endswith("f") or key in {"goalLine"}:
            continue
        odd = decimal(value)
        if not odd:
            continue
        label = CRS_LABELS.get(key)
        if not label:
            parts = key[1:].split("s", 1)
            if len(parts) == 2 and all(part.isdigit() for part in parts):
                label = f"{int(parts[0])}:{int(parts[1])}"
        if label:
            odds[label] = {"odds": odd, "status_flag": row.get(f"{key}f")}
    return {
        "label": "比分固定",
        "update_date": row.get("updateDate"),
        "update_time": row.get("updateTime"),
        "odds": odds,
        "raw": row,
    }


def normalize_fixed_hafu(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {}
    odds = {}
    for key, label in HAFU_LABELS.items():
        odd = decimal(row.get(key))
        if odd:
            odds[label] = {"odds": odd, "status_flag": row.get(f"{key}f")}
    return {
        "label": "半全场",
        "update_date": row.get("updateDate"),
        "update_time": row.get("updateTime"),
        "odds": odds,
        "raw": row,
    }


def normalize_fixed_bonus_payload(payload: dict[str, Any]) -> dict[str, Any]:
    history = payload.get("value", {}).get("oddsHistory") or {}
    had = latest_history_row(history.get("hadList"))
    hhad = latest_history_row(history.get("hhadList"))
    normalized = {
        "match_id": history.get("matchId"),
        "home": history.get("homeTeamAllName") or history.get("homeTeamAbbName"),
        "away": history.get("awayTeamAllName") or history.get("awayTeamAbbName"),
        "HAD": {
            "label": "胜平负",
            "h": decimal((had or {}).get("h")),
            "d": decimal((had or {}).get("d")),
            "a": decimal((had or {}).get("a")),
            "update_date": (had or {}).get("updateDate"),
            "update_time": (had or {}).get("updateTime"),
            "raw": had or {},
        },
        "HHAD": {
            "label": "让球胜平负",
            "h": decimal((hhad or {}).get("h")),
            "d": decimal((hhad or {}).get("d")),
            "a": decimal((hhad or {}).get("a")),
            "goal_line": (hhad or {}).get("goalLine"),
            "update_date": (hhad or {}).get("updateDate"),
            "update_time": (hhad or {}).get("updateTime"),
            "raw": hhad or {},
        },
        "TTG": normalize_fixed_ttg(latest_history_row(history.get("ttgList"))),
        "CRS": normalize_fixed_crs(latest_history_row(history.get("crsList"))),
        "HAFU": normalize_fixed_hafu(latest_history_row(history.get("hafuList"))),
    }
    normalized["available_pools"] = [
        pool
        for pool in ("HAD", "HHAD", "TTG", "CRS", "HAFU")
        if any(normalized.get(pool, {}).get(key) for key in ("h", "d", "a"))
        or normalized.get(pool, {}).get("odds")
    ]
    return normalized


def normalize_match(match: dict[str, Any]) -> dict[str, Any]:
    pools = normalize_pool_list(match.get("poolList"))
    odds = normalize_odds_list(match.get("oddsList"))
    available_pools = []
    for code in sorted(set(pools) | set(odds)):
        pool_status = pools.get(code, {}).get("status")
        odds_row = odds.get(code, {})
        has_odds = any(non_empty(odds_row.get(key)) for key in ("h", "d", "a", "odds"))
        if pool_status == "Selling" and has_odds:
            available_pools.append(code)
    return {
        "match_id": match.get("matchId"),
        "match_num": match.get("matchNum"),
        "match_num_str": match.get("matchNumStr"),
        "match_num_date": match.get("matchNumDate"),
        "business_date": match.get("businessDate"),
        "match_date": match.get("matchDate"),
        "match_time": match.get("matchTime"),
        "league": {
            "id": match.get("leagueId"),
            "abbr": match.get("leagueAbbName"),
            "name": match.get("leagueAllName"),
        },
        "home": {
            "id": match.get("homeTeamId"),
            "abbr": match.get("homeTeamAbbName"),
            "name": match.get("homeTeamAllName"),
        },
        "away": {
            "id": match.get("awayTeamId"),
            "abbr": match.get("awayTeamAbbName"),
            "name": match.get("awayTeamAllName"),
        },
        "status": match.get("matchStatus"),
        "back_color": match.get("backColor"),
        "line_num": match.get("lineNum"),
        "pools": pools,
        "odds": odds,
        "available_pools": available_pools,
        "raw": match,
    }


def flatten_matches(payload: dict[str, Any]) -> list[dict[str, Any]]:
    groups = payload.get("value", {}).get("matchInfoList") or []
    matches: list[dict[str, Any]] = []
    for group in groups:
        for match in group.get("subMatchList") or []:
            matches.append(normalize_match(match))
    return matches


def filter_matches(matches: list[dict[str, Any]], team: str | None, match_id: int | None) -> list[dict[str, Any]]:
    if match_id is not None:
        matches = [match for match in matches if match.get("match_id") == match_id]
    if team:
        needle = team.lower()

        def has_team(match: dict[str, Any]) -> bool:
            haystack = " ".join(
                str(value or "")
                for value in (
                    match["home"].get("abbr"),
                    match["home"].get("name"),
                    match["away"].get("abbr"),
                    match["away"].get("name"),
                    match["league"].get("abbr"),
                    match["league"].get("name"),
                    match.get("match_num_str"),
                )
            ).lower()
            return needle in haystack

        matches = [match for match in matches if has_team(match)]
    return matches


def summarize(matches: list[dict[str, Any]]) -> dict[str, Any]:
    pools = sorted(POOL_LABELS)
    with_odds = {
        pool: sum(
            1
            for match in matches
            if any(non_empty(match.get("odds", {}).get(pool, {}).get(key)) for key in ("h", "d", "a", "odds"))
        )
        for pool in pools
    }
    selling = {
        pool: sum(1 for match in matches if match.get("pools", {}).get(pool, {}).get("status") == "Selling")
        for pool in pools
    }
    return {
        "total_matches": len(matches),
        "matches_with_odds_by_pool": with_odds,
        "selling_by_pool": selling,
    }


def fetch_history(match_id: int, client_code: str, timeout: float) -> dict[str, Any]:
    query = urllib.parse.urlencode({"clientCode": client_code, "matchId": str(match_id)})
    url = f"{FIXED_BONUS_URL}?{query}"
    try:
        payload = fetch_json(url, timeout)
        return {
            "status": "ok",
            "source_url": url,
            "normalized": normalize_fixed_bonus_payload(payload),
            "payload": payload,
        }
    except FetchError as exc:
        return {"status": "failed", "source_url": url, "reason": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch official Sporttery football odds.")
    parser.add_argument("--output", help="Write JSON cache to this path. Defaults to stdout.")
    parser.add_argument("--team", help="Filter by team, league, or match number text.")
    parser.add_argument("--match-id", type=int, help="Filter by Sporttery matchId.")
    parser.add_argument("--include-history", action="store_true", help="Fetch fixed-bonus history for filtered matches.")
    parser.add_argument("--client-code", default="3001")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--utf8", action="store_true", help="Emit UTF-8 characters instead of ASCII escapes.")
    args = parser.parse_args()
    configure_stdout(args.utf8)

    query = urllib.parse.urlencode({"clientCode": args.client_code})
    match_list_url = f"{MATCH_LIST_URL}?{query}"
    try:
        payload = fetch_json(match_list_url, args.timeout)
    except FetchError as exc:
        beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")
        result = {
            "schema": "worldcup-mystic-oracle/sporttery-odds-v1",
            "status": "failed",
            "source": "中国体育彩票 / Sporttery official web API",
            "source_urls": {
                "match_list": match_list_url,
                "fixed_bonus_history": f"{FIXED_BONUS_URL}?clientCode={args.client_code}&matchId=<matchId>",
            },
            "retrieved_at": {
                "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "beijing": datetime.now(beijing_tz).isoformat(timespec="seconds"),
            },
            "fetch_profiles_tried": [profile["name"] for profile in REQUEST_PROFILES],
            "filters": {"team": args.team, "match_id": args.match_id},
            "reason": str(exc),
            "note": "Mark 中国体彩官方赔率暂不可得 and do not substitute third-party odds as official.",
        }
        text = json.dumps(result, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(text + "\n", encoding="utf-8")
        else:
            sys.stdout.write(text + "\n")
        return 1

    matches = filter_matches(flatten_matches(payload), args.team, args.match_id)

    beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")
    beijing_now = datetime.now(beijing_tz)
    result: dict[str, Any] = {
        "schema": "worldcup-mystic-oracle/sporttery-odds-v1",
        "status": "ok" if payload.get("success") else "source_error",
        "source": "中国体育彩票 / Sporttery official web API",
        "source_urls": {
            "match_list": match_list_url,
            "fixed_bonus_history": f"{FIXED_BONUS_URL}?clientCode={args.client_code}&matchId=<matchId>",
        },
        "retrieved_at": {
            "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "beijing": beijing_now.isoformat(timespec="seconds"),
        },
        "fetch_profile": payload.get("_fetch_profile"),
        "fetch_attempts": payload.get("_fetch_attempts"),
        "filters": {"team": args.team, "match_id": args.match_id},
        "summary": summarize(matches),
        "matches": matches,
        "raw_error_code": payload.get("errorCode"),
        "raw_error_message": payload.get("errorMessage"),
    }

    if args.include_history:
        history_ids = {int(match["match_id"]) for match in matches if match.get("match_id") is not None}
        if args.match_id is not None:
            history_ids.add(args.match_id)
        result["fixed_bonus_history"] = {
            str(match_id): fetch_history(match_id, args.client_code, args.timeout)
            for match_id in sorted(history_ids)
        }

    text = json.dumps(result, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
