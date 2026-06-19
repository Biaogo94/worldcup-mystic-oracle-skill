#!/usr/bin/env python3
"""Compute incomplete bazi three pillars from sourced birth dates.

This helper intentionally omits the hour pillar. Public coach/player profile
birth dates are treated as Gregorian dates in YYYY-MM-DD form unless the source
explicitly marks them as lunar dates. The Gregorian date is then converted by
the bazi library into year, month, and day pillars.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

STEM_ELEMENTS = {
    "甲": "wood",
    "乙": "wood",
    "丙": "fire",
    "丁": "fire",
    "戊": "earth",
    "己": "earth",
    "庚": "metal",
    "辛": "metal",
    "壬": "water",
    "癸": "water",
}

BRANCH_ELEMENTS = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water",
}

BRANCH_SEASON_CLIMATE = {
    "寅": {"season": "early_spring", "climate": "wood rising; residual cold", "likely_medicine_hint": "火土可作调候参考"},
    "卯": {"season": "mid_spring", "climate": "wood flourishing", "likely_medicine_hint": "金土可作平衡参考"},
    "辰": {"season": "late_spring", "climate": "damp earth with wood residue", "likely_medicine_hint": "火土金视全局参考"},
    "巳": {"season": "early_summer", "climate": "fire rising", "likely_medicine_hint": "水金可作平衡参考"},
    "午": {"season": "mid_summer", "climate": "fire flourishing and dry", "likely_medicine_hint": "水金湿土可作调候参考"},
    "未": {"season": "late_summer", "climate": "dry earth with fire residue", "likely_medicine_hint": "水木可作平衡参考"},
    "申": {"season": "early_autumn", "climate": "metal rising", "likely_medicine_hint": "火木可作平衡参考"},
    "酉": {"season": "mid_autumn", "climate": "metal flourishing", "likely_medicine_hint": "火木水视全局参考"},
    "戌": {"season": "late_autumn", "climate": "dry earth with metal residue", "likely_medicine_hint": "水木可作调候参考"},
    "亥": {"season": "early_winter", "climate": "water rising and cold", "likely_medicine_hint": "火土可作调候参考"},
    "子": {"season": "mid_winter", "climate": "water flourishing and cold", "likely_medicine_hint": "火土为优先调候参考"},
    "丑": {"season": "late_winter", "climate": "cold damp earth", "likely_medicine_hint": "火木可作调候参考"},
}

GENERATES = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood",
}

CONTROLS = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood",
}

SIX_HARMONY = {frozenset(pair) for pair in ("子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未")}
SIX_CLASH = {frozenset(pair) for pair in ("子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥")}
SIX_HARM = {frozenset(pair) for pair in ("子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌")}
PUNISH_GROUPS = [set("寅巳申"), set("丑戌未"), set("子卯")]

SOURCE_MULTIPLIERS = {
    "verified": 1.0,
    "official": 1.0,
    "reputable-secondary": 0.85,
    "secondary": 0.75,
    "missing": 0.0,
}

ROLE_RULES = [
    (("manager", "coach", "head coach", "主教练"), 0.25, "coach", "tactical clarity and substitutions"),
    (("goalkeeper", "门将"), 0.15, "goalkeeper", "saves, handling, clean-sheet and error risk"),
    (("striker", "forward", "primary striker", "前锋", "中锋"), 0.15, "striker", "finishing, rebounds, offside timing"),
    (("creator", "playmaker", "midfielder", "central midfielder", "winger", "中场", "组织"), 0.15, "midfield", "tempo, chance creation, second balls"),
    (("captain", "defensive leader", "defender", "centre-back", "center-back", "后防", "队长"), 0.10, "defense", "defensive order, cards, missed marks"),
    (("substitute", "impact", "impact substitute", "替补"), 0.20, "impact", "late swing, substitutions, bench script"),
    (("remaining key starter", "key starter", "starter", "主力"), 0.20, "impact", "remaining key starter modifier"),
]


def clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def load_json(path: str) -> Any:
    data = Path(path).read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return json.loads(data.decode(encoding))
        except UnicodeDecodeError:
            continue
    return json.loads(data.decode("utf-8", errors="replace"))


def configure_stdout(utf8: bool) -> None:
    if utf8 and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def load_people(path: str | None, demo: bool) -> list[dict[str, Any]]:
    if demo:
        return [
            {
                "name": "Example Player",
                "team": "主队",
                "role": "primary striker",
                "birth_date": "1999-09-21",
                "source_status": "secondary",
            }
        ]
    if not path:
        raise SystemExit("Provide --people people.json or use --demo.")
    data = load_json(path)
    if not isinstance(data, list):
        raise SystemExit("people.json must contain a list of people.")
    return data


def get_lunar_classes() -> Any:
    try:
        from lunar_python import Solar
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: lunar_python. Install with `python -m pip install lunar-python` "
            "or run with a Python environment that already provides it."
        ) from exc
    return Solar


def pillars_for_date(date_text: str) -> dict[str, Any]:
    if not DATE_RE.match(date_text):
        raise ValueError(f"Invalid date: {date_text}. Expected YYYY-MM-DD.")
    year, month, day = [int(part) for part in date_text.split("-")]
    Solar = get_lunar_classes()
    eight = Solar.fromYmdHms(year, month, day, 12, 0, 0).getLunar().getEightChar()
    year_pillar = eight.getYear()
    month_pillar = eight.getMonth()
    day_pillar = eight.getDay()
    return {
        "input_calendar": "gregorian",
        "input_calendar_note": "公开球员/教练生日默认按公历日期输入，除非来源明确标注农历",
        "pillar_calculation_basis": "Solar.fromYmdHms(gregorian date, 12:00 placeholder) -> getLunar().getEightChar()",
        "month_pillar_basis": "solar_terms",
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "year_ming_stem": year_pillar[0],
        "year_branch": year_pillar[1],
        "month_stem": month_pillar[0],
        "month_branch": month_pillar[1],
        "month_command_climate": BRANCH_SEASON_CLIMATE.get(month_pillar[1]),
        "day_master": day_pillar[0],
        "day_branch": day_pillar[1],
        "hour_pillar": None,
        "hour_placeholder": "12:00 is only a date-only placeholder; hour pillar is omitted and not scored",
        "note": "时柱缺失，因此只作三柱参考",
    }


def role_info(role: Any) -> dict[str, Any]:
    role_text = str(role or "").lower()
    for keywords, weight, group, football_meaning in ROLE_RULES:
        if any(keyword.lower() in role_text for keyword in keywords):
            return {
                "base_role_weight": weight,
                "role_group": group,
                "football_meaning": football_meaning,
            }
    return {
        "base_role_weight": 0.10,
        "role_group": "other",
        "football_meaning": "secondary key-person modifier",
    }


def element_relation(person_element: str | None, match_element: str | None) -> dict[str, Any]:
    if not person_element or not match_element:
        return {"type": "unknown", "score": 0.0, "text": "element unknown"}
    if person_element == match_element:
        return {"type": "same", "score": 0.30, "text": "日主与比赛日干同气"}
    if GENERATES.get(match_element) == person_element:
        return {"type": "match_generates_person", "score": 0.55, "text": "比赛日干生扶此人日主"}
    if GENERATES.get(person_element) == match_element:
        return {"type": "person_generates_match", "score": -0.20, "text": "此人日主泄气生比赛场"}
    if CONTROLS.get(person_element) == match_element:
        return {"type": "person_controls_match", "score": 0.15, "text": "此人日主可制比赛场"}
    if CONTROLS.get(match_element) == person_element:
        return {"type": "match_controls_person", "score": -0.55, "text": "比赛日干克制此人日主"}
    return {"type": "neutral", "score": 0.0, "text": "五行关系中性"}


def branch_relation(person_branch: str | None, match_branch: str | None) -> dict[str, Any]:
    if not person_branch or not match_branch:
        return {"type": "unknown", "score": 0.0, "text": "branch unknown"}
    pair = frozenset((person_branch, match_branch))
    if person_branch == match_branch:
        return {"type": "same", "score": 0.25, "text": "日支与比赛日支同气"}
    if pair in SIX_HARMONY:
        return {"type": "six_harmony", "score": 0.35, "text": "日支与比赛日支六合"}
    if pair in SIX_CLASH:
        return {"type": "six_clash", "score": -0.60, "text": "日支与比赛日支相冲"}
    if pair in SIX_HARM:
        return {"type": "six_harm", "score": -0.40, "text": "日支与比赛日支相害"}
    if any(person_branch in group and match_branch in group for group in PUNISH_GROUPS):
        return {"type": "punishment", "score": -0.30, "text": "日支与比赛日支有刑象"}
    person_element = BRANCH_ELEMENTS.get(person_branch)
    match_element = BRANCH_ELEMENTS.get(match_branch)
    relation = element_relation(person_element, match_element)
    relation_type = relation["type"]
    relation["type"] = f"branch_{relation_type}"
    relation["score"] = round(relation["score"] * 0.5, 3)
    branch_text = {
        "same": "双方日支五行同气",
        "match_generates_person": "比赛日支五行生扶此人日支",
        "person_generates_match": "此人日支五行泄气生比赛日支",
        "person_controls_match": "此人日支五行可制比赛日支",
        "match_controls_person": "比赛日支五行克制此人日支",
        "neutral": "日支五行关系中性",
    }
    relation["text"] = branch_text.get(relation_type, f"日支五行关系：{relation['text']}")
    return relation


def source_multiplier(source_status: Any) -> float:
    return SOURCE_MULTIPLIERS.get(str(source_status or "missing"), 0.0)


def source_status(value: Any) -> str:
    status = str(value or "missing")
    return status if status in SOURCE_MULTIPLIERS else "missing"


def add_role_scores(rows: list[dict[str, Any]], match_pillars: dict[str, str] | None) -> dict[str, Any]:
    if not match_pillars:
        return {
            "match": None,
            "teams": {},
            "note": "Run with --match-date YYYY-MM-DD to compute role-weighted bazi scoring.",
        }

    match_day = match_pillars["day_pillar"]
    match_day_stem = match_day[0]
    match_day_branch = match_day[1]
    match_element = STEM_ELEMENTS.get(match_day_stem)
    team_weight_totals: dict[str, float] = {}
    for row in rows:
        if row.get("status") != "computed":
            continue
        info = role_info(row.get("role"))
        row.update(info)
        team = str(row.get("team") or "unknown")
        team_weight_totals[team] = team_weight_totals.get(team, 0.0) + float(info["base_role_weight"])

    for row in rows:
        if row.get("status") != "computed":
            continue
        day_pillar = str(row.get("day_pillar") or "")
        day_stem = day_pillar[:1]
        day_branch = day_pillar[1:2]
        person_element = STEM_ELEMENTS.get(day_stem)
        stem_rel = element_relation(person_element, match_element)
        branch_rel = branch_relation(day_branch, match_day_branch)
        raw_score = clamp(float(stem_rel["score"]) + float(branch_rel["score"]))
        multiplier = source_multiplier(row.get("source_status"))
        team = str(row.get("team") or "unknown")
        normalized_weight = float(row.get("base_role_weight", 0.1)) / team_weight_totals.get(team, 1.0)
        weighted_score = raw_score * multiplier * normalized_weight
        row.update(
            {
                "day_master": day_stem,
                "day_master_element": person_element,
                "day_branch": day_branch,
                "qimen_person_anchors": {
                    "year_ming_stem": row.get("year_ming_stem"),
                    "bazi_day_master": day_stem,
                    "birth_day_branch": day_branch,
                    "month_command_climate": row.get("month_command_climate"),
                    "qimen_usage": "缺时柱时，年命天干优先用于奇门个人根本磁场；八字日主用于个人主观能力但不独断旺衰；生日支用于与比赛日支合冲刑害过滤；月令只作气候偏好和病药提示。",
                },
                "match_day_pillar": match_day,
                "match_day_stem": match_day_stem,
                "match_day_branch": match_day_branch,
                "stem_relation": stem_rel,
                "branch_relation": branch_rel,
                "raw_role_score": round(raw_score, 3),
                "source_multiplier": multiplier,
                "normalized_team_weight": round(normalized_weight, 4),
                "weighted_score": round(weighted_score, 4),
                "score_status": "scored" if multiplier > 0 else "unscored_source_missing",
            }
        )

    teams: dict[str, dict[str, Any]] = {}
    for row in rows:
        team = str(row.get("team") or "unknown")
        team_entry = teams.setdefault(
            team,
            {
                "people": 0,
                "computed": 0,
                "scored": 0,
                "source_missing": 0,
                "team_score": 0.0,
            },
        )
        team_entry["people"] += 1
        if row.get("status") == "computed":
            team_entry["computed"] += 1
        if row.get("score_status") == "scored":
            team_entry["scored"] += 1
            team_entry["team_score"] += float(row.get("weighted_score", 0.0))
        if row.get("source_multiplier") == 0.0:
            team_entry["source_missing"] += 1

    for team_entry in teams.values():
        target = max(team_entry["people"], 1)
        team_entry["team_score"] = round(team_entry["team_score"], 4)
        team_entry["scored_coverage"] = f"{team_entry['scored']}/{target}"
        if team_entry["scored"] < 3:
            team_entry["confidence_cap"] = "qualitative-only"
        elif team_entry["scored"] < 4:
            team_entry["confidence_cap"] = "low-medium"
        elif team_entry["scored"] < 6:
            team_entry["confidence_cap"] = "medium"
        else:
            team_entry["confidence_cap"] = "module-complete"

    return {
        "match": {
            "date": match_pillars.get("date"),
            "day_pillar": match_day,
            "day_stem": match_day_stem,
            "day_branch": match_day_branch,
            "day_stem_element": match_element,
        },
        "teams": teams,
        "note": "Scores are role-weighted incomplete-bazi modifiers. They are not standalone predictions.",
    }


def render_people(people: list[dict[str, Any]], match_date: str | None = None) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    match_pillars = None
    if match_date:
        match_pillars = pillars_for_date(match_date)
        match_pillars["date"] = match_date
    for person in people:
        row = {
            "name": person.get("name"),
            "team": person.get("team"),
            "role": person.get("role"),
            "birth_date": person.get("birth_date"),
            "source_status": source_status(person.get("source_status")),
            "source": person.get("source"),
        }
        birth_date = row["birth_date"]
        if not birth_date:
            row["status"] = "missing"
            missing.append(row)
            rows.append(row)
            continue
        try:
            row.update(pillars_for_date(str(birth_date)))
            row["status"] = "computed"
        except Exception as exc:  # noqa: BLE001 - surface per-person failures in JSON.
            row["status"] = "failed"
            row["error"] = str(exc)
            missing.append(row)
        rows.append(row)

    role_scoring = add_role_scores(rows, match_pillars)
    return {
        "status": "ok",
        "schema": "worldcup-mystic-oracle/bazi-three-pillars-v1",
        "match_date": match_date,
        "role_scoring": role_scoring,
        "rows": rows,
        "computed_count": sum(1 for row in rows if row.get("status") == "computed"),
        "missing_or_failed_count": len(missing),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute incomplete bazi three pillars from birth dates.")
    parser.add_argument("--people", help="Path to a JSON list of people.")
    parser.add_argument("--match-date", help="Gregorian match date in venue local time. Enables role-weighted scoring.")
    parser.add_argument("--demo", action="store_true", help="Run a built-in demo.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    parser.add_argument("--utf8", action="store_true", help="Emit UTF-8 characters instead of ASCII-safe escapes.")
    args = parser.parse_args()
    configure_stdout(args.utf8)

    result = render_people(load_people(args.people, args.demo), args.match_date)
    json.dump(result, sys.stdout, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
    print()


if __name__ == "__main__":
    main()
