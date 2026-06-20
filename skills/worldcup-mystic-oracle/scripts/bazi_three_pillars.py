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

STEM_POLARITY = {
    "甲": "yang",
    "乙": "yin",
    "丙": "yang",
    "丁": "yin",
    "戊": "yang",
    "己": "yin",
    "庚": "yang",
    "辛": "yin",
    "壬": "yang",
    "癸": "yin",
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

BRANCH_HIDDEN_STEMS = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "戊", "庚"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

HIDDEN_STEM_WEIGHTS = (0.7, 0.2, 0.1)

MONTH_ELEMENT_STATES = {
    "寅": {"wood": "旺", "fire": "相", "water": "休", "metal": "囚", "earth": "死"},
    "卯": {"wood": "旺", "fire": "相", "water": "休", "metal": "囚", "earth": "死"},
    "辰": {"earth": "旺", "wood": "相", "water": "休", "fire": "休", "metal": "囚"},
    "巳": {"fire": "旺", "earth": "相", "wood": "休", "water": "囚", "metal": "死"},
    "午": {"fire": "旺", "earth": "相", "wood": "休", "water": "囚", "metal": "死"},
    "未": {"earth": "旺", "fire": "相", "wood": "休", "water": "囚", "metal": "死"},
    "申": {"metal": "旺", "water": "相", "earth": "休", "fire": "囚", "wood": "死"},
    "酉": {"metal": "旺", "water": "相", "earth": "休", "fire": "囚", "wood": "死"},
    "戌": {"earth": "旺", "metal": "相", "fire": "休", "water": "囚", "wood": "死"},
    "亥": {"water": "旺", "wood": "相", "metal": "休", "earth": "囚", "fire": "死"},
    "子": {"water": "旺", "wood": "相", "metal": "休", "earth": "囚", "fire": "死"},
    "丑": {"earth": "旺", "water": "相", "metal": "休", "fire": "囚", "wood": "死"},
}

MONTH_STATE_SCORES = {"旺": 0.18, "相": 0.10, "休": -0.03, "囚": -0.12, "死": -0.16}

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

TEN_GOD_HINTS = {
    "比肩": "competition, self-drive, duels",
    "劫财": "risk-taking, rivalry, chance-stealing",
    "食神": "smooth output, finishing touch, calm creativity",
    "伤官": "aggressive expression, surprise, tactical rebellion",
    "偏财": "opportunistic gain, transition chance, bold conversion",
    "正财": "steady conversion, possession value, controlled gain",
    "七杀": "pressure, aggression, crisis handling",
    "正官": "discipline, structure, authority under rules",
    "偏印": "unorthodox reading, isolation, hidden calculation",
    "正印": "protection, composure, learning, system support",
}

ROLE_TEN_GOD_WEIGHTS = {
    "coach": {"正官": 0.12, "正印": 0.12, "偏印": 0.07, "七杀": 0.05, "伤官": -0.04, "劫财": -0.05},
    "goalkeeper": {"正印": 0.10, "正官": 0.10, "七杀": 0.04, "伤官": -0.06, "劫财": -0.04, "偏财": -0.02},
    "defense": {"正官": 0.11, "正印": 0.09, "七杀": 0.05, "比肩": 0.03, "伤官": -0.05, "劫财": -0.04},
    "striker": {"食神": 0.10, "伤官": 0.08, "偏财": 0.06, "正财": 0.04, "正印": -0.02, "偏印": -0.05},
    "midfield": {"食神": 0.08, "伤官": 0.08, "正印": 0.06, "正官": 0.04, "偏印": 0.03, "劫财": -0.02},
    "impact": {"伤官": 0.08, "七杀": 0.06, "偏财": 0.06, "比肩": 0.03, "正印": -0.02},
    "other": {"正印": 0.03, "正官": 0.03, "食神": 0.03, "伤官": 0.02},
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


def rounded_scores(scores: dict[str, float]) -> dict[str, float]:
    return {key: round(value, 3) for key, value in sorted(scores.items())}


def stem_element(stem: str | None) -> str | None:
    return STEM_ELEMENTS.get(str(stem or "")[:1])


def branch_element(branch: str | None) -> str | None:
    return BRANCH_ELEMENTS.get(str(branch or "")[:1])


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
                "source": "https://example.com/profile",
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


def ten_god(day_master: str | None, other_stem: str | None) -> str | None:
    day_master = str(day_master or "")[:1]
    other_stem = str(other_stem or "")[:1]
    day_element = stem_element(day_master)
    other_element = stem_element(other_stem)
    if not day_element or not other_element:
        return None
    same_polarity = STEM_POLARITY.get(day_master) == STEM_POLARITY.get(other_stem)
    if day_element == other_element:
        return "比肩" if same_polarity else "劫财"
    if GENERATES.get(other_element) == day_element:
        return "偏印" if same_polarity else "正印"
    if GENERATES.get(day_element) == other_element:
        return "食神" if same_polarity else "伤官"
    if CONTROLS.get(other_element) == day_element:
        return "七杀" if same_polarity else "正官"
    if CONTROLS.get(day_element) == other_element:
        return "偏财" if same_polarity else "正财"
    return None


def pillar_stem_branch(pillar: str) -> tuple[str, str]:
    pillar = str(pillar or "")
    return pillar[:1], pillar[1:2]


def stem_branch_internal_status(pillar: str) -> dict[str, Any]:
    stem, branch = pillar_stem_branch(pillar)
    stem_el = stem_element(stem)
    branch_el = branch_element(branch)
    if not stem_el or not branch_el:
        return {"status": "unknown", "score": 0.0, "text": "干支不完整"}
    if stem_el == branch_el:
        return {"status": "same", "score": 0.08, "text": "干支同气，输出稳定"}
    if GENERATES.get(branch_el) == stem_el:
        return {"status": "rooted", "score": 0.08, "text": "支生干，表象有根"}
    if GENERATES.get(stem_el) == branch_el:
        return {"status": "leaking_to_branch", "score": -0.03, "text": "干生支，表象泄向根基"}
    if CONTROLS.get(stem_el) == branch_el:
        return {"status": "covering", "score": -0.08, "text": "盖头：干克支，地支能量受压"}
    if CONTROLS.get(branch_el) == stem_el:
        return {"status": "cutting", "score": -0.10, "text": "截脚：支克干，天干表象失根"}
    return {"status": "neutral", "score": 0.0, "text": "干支内部关系中性"}


def branch_hidden_ten_gods(day_master: str, branch: str) -> list[dict[str, Any]]:
    hidden = []
    for index, hidden_stem in enumerate(BRANCH_HIDDEN_STEMS.get(branch, [])):
        hidden.append(
            {
                "stem": hidden_stem,
                "element": stem_element(hidden_stem),
                "ten_god": ten_god(day_master, hidden_stem),
                "weight": HIDDEN_STEM_WEIGHTS[min(index, len(HIDDEN_STEM_WEIGHTS) - 1)],
            }
        )
    return hidden


def six_character_profile(year_pillar: str, month_pillar: str, day_pillar: str) -> dict[str, Any]:
    pillars = {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
    }
    day_master, day_branch = pillar_stem_branch(day_pillar)
    visible_elements: dict[str, float] = {}
    hidden_elements: dict[str, float] = {}
    ten_gods: dict[str, Any] = {}
    hidden_ten_gods: dict[str, Any] = {}
    internal_status: dict[str, Any] = {}

    for label, pillar in pillars.items():
        stem, branch = pillar_stem_branch(pillar)
        for element in (stem_element(stem), branch_element(branch)):
            if element:
                visible_elements[element] = visible_elements.get(element, 0.0) + 1.0
        if label != "day":
            tg = ten_god(day_master, stem)
            ten_gods[f"{label}_stem"] = {
                "stem": stem,
                "ten_god": tg,
                "hint": TEN_GOD_HINTS.get(tg or ""),
            }
        ten_gods[f"{label}_branch_main"] = {
            "branch": branch,
            "main_element": branch_element(branch),
            "hidden_stems": branch_hidden_ten_gods(day_master, branch),
        }
        hidden_ten_gods[label] = ten_gods[f"{label}_branch_main"]["hidden_stems"]
        for index, hidden in enumerate(BRANCH_HIDDEN_STEMS.get(branch, [])):
            element = stem_element(hidden)
            if element:
                hidden_elements[element] = hidden_elements.get(element, 0.0) + HIDDEN_STEM_WEIGHTS[min(index, len(HIDDEN_STEM_WEIGHTS) - 1)]
        internal_status[label] = stem_branch_internal_status(pillar)

    weighted = visible_elements.copy()
    for element, value in hidden_elements.items():
        weighted[element] = weighted.get(element, 0.0) + value
    all_elements = ("wood", "fire", "earth", "metal", "water")
    dominant = sorted(weighted.items(), key=lambda item: item[1], reverse=True)
    month_branch = pillar_stem_branch(month_pillar)[1]
    month_states = MONTH_ELEMENT_STATES.get(month_branch, {})
    day_master_state = month_states.get(stem_element(day_master))
    return {
        "day_master": day_master,
        "day_master_element": stem_element(day_master),
        "day_branch": day_branch,
        "visible_element_counts": rounded_scores(visible_elements),
        "hidden_element_weights": rounded_scores(hidden_elements),
        "weighted_element_profile": rounded_scores(weighted),
        "dominant_elements": [element for element, value in dominant[:2] if value > 0],
        "missing_elements": [element for element in all_elements if weighted.get(element, 0.0) == 0.0],
        "month_element_states": month_states,
        "day_master_month_state": day_master_state,
        "day_master_month_state_score": MONTH_STATE_SCORES.get(day_master_state or "", 0.0),
        "ten_gods": ten_gods,
        "hidden_ten_gods": hidden_ten_gods,
        "pillar_internal_status": internal_status,
        "profile_limits": "缺出生时辰和出生地，不能完整判定旺衰、格局、喜用神或大运；此画像仅用于球员/教练事件适配过滤。",
    }


def pillars_for_date(date_text: str) -> dict[str, Any]:
    if not DATE_RE.match(date_text):
        raise ValueError(f"Invalid date: {date_text}. Expected YYYY-MM-DD.")
    year, month, day = [int(part) for part in date_text.split("-")]
    Solar = get_lunar_classes()
    eight = Solar.fromYmdHms(year, month, day, 12, 0, 0).getLunar().getEightChar()
    year_pillar = eight.getYear()
    month_pillar = eight.getMonth()
    day_pillar = eight.getDay()
    six_profile = six_character_profile(year_pillar, month_pillar, day_pillar)
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
        "six_character_profile": six_profile,
        "visible_element_counts": six_profile["visible_element_counts"],
        "weighted_element_profile": six_profile["weighted_element_profile"],
        "dominant_elements": six_profile["dominant_elements"],
        "missing_elements": six_profile["missing_elements"],
        "day_master_month_state": six_profile["day_master_month_state"],
        "ten_god_profile": six_profile["ten_gods"],
        "pillar_internal_status": six_profile["pillar_internal_status"],
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
        return {"type": "same", "score": 0.30, "text": "本命天干与事件天干同气"}
    if GENERATES.get(match_element) == person_element:
        return {"type": "match_generates_person", "score": 0.55, "text": "事件天干生扶本命天干"}
    if GENERATES.get(person_element) == match_element:
        return {"type": "person_generates_match", "score": -0.20, "text": "本命天干泄气生事件场"}
    if CONTROLS.get(person_element) == match_element:
        return {"type": "person_controls_match", "score": 0.15, "text": "本命天干可制事件场"}
    if CONTROLS.get(match_element) == person_element:
        return {"type": "match_controls_person", "score": -0.55, "text": "事件天干克制本命天干"}
    return {"type": "neutral", "score": 0.0, "text": "五行关系中性"}


def branch_relation(person_branch: str | None, match_branch: str | None) -> dict[str, Any]:
    if not person_branch or not match_branch:
        return {"type": "unknown", "score": 0.0, "text": "branch unknown"}
    pair = frozenset((person_branch, match_branch))
    if person_branch == match_branch:
        return {"type": "same", "score": 0.25, "text": "本命地支与事件地支同气"}
    if pair in SIX_HARMONY:
        return {"type": "six_harmony", "score": 0.35, "text": "本命地支与事件地支六合"}
    if pair in SIX_CLASH:
        return {"type": "six_clash", "score": -0.60, "text": "本命地支与事件地支相冲"}
    if pair in SIX_HARM:
        return {"type": "six_harm", "score": -0.40, "text": "本命地支与事件地支相害"}
    if any(person_branch in group and match_branch in group for group in PUNISH_GROUPS):
        return {"type": "punishment", "score": -0.30, "text": "本命地支与事件地支有刑象"}
    person_element = BRANCH_ELEMENTS.get(person_branch)
    match_element = BRANCH_ELEMENTS.get(match_branch)
    relation = element_relation(person_element, match_element)
    relation_type = relation["type"]
    relation["type"] = f"branch_{relation_type}"
    relation["score"] = round(relation["score"] * 0.5, 3)
    branch_text = {
        "same": "本命地支与事件地支五行同气",
        "match_generates_person": "事件地支五行生扶本命地支",
        "person_generates_match": "本命地支五行泄气生事件地支",
        "person_controls_match": "本命地支五行可制事件地支",
        "match_controls_person": "事件地支五行克制本命地支",
        "neutral": "本命地支与事件地支五行关系中性",
    }
    relation["text"] = branch_text.get(relation_type, f"地支五行关系：{relation['text']}")
    return relation


def pillar_interaction(person_pillar: str, match_pillar: str, label: str, weight: float) -> dict[str, Any]:
    person_stem, person_branch = pillar_stem_branch(person_pillar)
    match_stem, match_branch = pillar_stem_branch(match_pillar)
    stem_rel = element_relation(stem_element(person_stem), stem_element(match_stem))
    branch_rel = branch_relation(person_branch, match_branch)
    person_internal = stem_branch_internal_status(person_pillar)
    match_internal = stem_branch_internal_status(match_pillar)
    heavenly_clash = (
        stem_rel["type"] == "match_controls_person"
        and branch_rel["type"] == "six_clash"
    )
    score = (float(stem_rel["score"]) * 0.45) + (float(branch_rel["score"]) * 0.45)
    if heavenly_clash:
        score -= 0.25
    if person_internal["status"] in {"covering", "cutting"}:
        score -= 0.04
    if match_internal["status"] in {"covering", "cutting"}:
        score -= 0.03
    return {
        "label": label,
        "person_pillar": person_pillar,
        "match_pillar": match_pillar,
        "stem_relation": stem_rel,
        "branch_relation": branch_rel,
        "person_internal_status": person_internal,
        "match_internal_status": match_internal,
        "heavenly_stem_branch_clash": heavenly_clash,
        "raw_score": round(clamp(score), 3),
        "weighted_score": round(clamp(score) * weight, 3),
        "weight": weight,
    }


def role_ten_god_modifier(row: dict[str, Any], role_group: str) -> dict[str, Any]:
    profile = row.get("six_character_profile") or {}
    day_master_state = profile.get("day_master_month_state")
    ten_gods = profile.get("ten_gods") or {}
    weights = ROLE_TEN_GOD_WEIGHTS.get(role_group, ROLE_TEN_GOD_WEIGHTS["other"])
    hits: list[dict[str, Any]] = []
    score = MONTH_STATE_SCORES.get(day_master_state or "", 0.0)
    if day_master_state:
        hits.append(
            {
                "source": "day_master_month_state",
                "value": day_master_state,
                "score": round(MONTH_STATE_SCORES.get(day_master_state, 0.0), 3),
                "text": "日主得令/失令的弱参考，缺时柱不作完整旺衰",
            }
        )
    for source, item in ten_gods.items():
        if not isinstance(item, dict):
            continue
        tg = item.get("ten_god")
        if tg in weights:
            delta = float(weights[tg])
            score += delta
            hits.append(
                {
                    "source": source,
                    "ten_god": tg,
                    "score": round(delta, 3),
                    "hint": TEN_GOD_HINTS.get(tg),
                }
            )
        for hidden in item.get("hidden_stems", []) or []:
            tg_hidden = hidden.get("ten_god")
            if tg_hidden in weights:
                delta = float(weights[tg_hidden]) * float(hidden.get("weight", 0.0)) * 0.35
                score += delta
                hits.append(
                    {
                        "source": f"{source}.hidden",
                        "stem": hidden.get("stem"),
                        "ten_god": tg_hidden,
                        "score": round(delta, 3),
                        "hint": TEN_GOD_HINTS.get(tg_hidden),
                    }
                )
    return {
        "role_group": role_group,
        "score": round(clamp(score, -0.35, 0.35), 3),
        "hits": hits[:8],
        "note": "角色十神修正只作低权重适配过滤，不等同完整格局喜忌。",
    }


def event_resonance(row: dict[str, Any], match_pillars: dict[str, Any]) -> dict[str, Any]:
    interactions = [
        pillar_interaction(str(row.get("year_pillar") or ""), str(match_pillars.get("year_pillar") or ""), "year_vs_match_year", 0.18),
        pillar_interaction(str(row.get("month_pillar") or ""), str(match_pillars.get("month_pillar") or ""), "month_vs_match_month", 0.22),
        pillar_interaction(str(row.get("day_pillar") or ""), str(match_pillars.get("day_pillar") or ""), "day_vs_match_day", 0.40),
    ]
    total = sum(float(item["weighted_score"]) for item in interactions)
    pressure_flags = [
        item["label"]
        for item in interactions
        if item.get("heavenly_stem_branch_clash") or item["branch_relation"].get("type") in {"six_clash", "six_harm", "punishment"}
    ]
    support_flags = [
        item["label"]
        for item in interactions
        if item["branch_relation"].get("type") in {"six_harmony", "same"} or item["stem_relation"].get("type") in {"match_generates_person", "same"}
    ]
    return {
        "score": round(clamp(total, -0.5, 0.5), 3),
        "interactions": interactions,
        "pressure_flags": pressure_flags,
        "support_flags": support_flags,
        "note": "这是流年/流月/比赛日共振，不是精确大运。",
    }


def source_multiplier(source_status: Any, source: Any = None) -> float:
    multiplier = SOURCE_MULTIPLIERS.get(str(source_status or "missing"), 0.0)
    if multiplier > 0 and not str(source or "").strip():
        return 0.0
    return multiplier


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

    match_year = match_pillars["year_pillar"]
    match_month = match_pillars["month_pillar"]
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
        role_group = str(row.get("role_group") or "other")
        role_modifier = role_ten_god_modifier(row, role_group)
        resonance = event_resonance(row, match_pillars)
        raw_score = clamp(
            float(stem_rel["score"])
            + float(branch_rel["score"])
            + float(role_modifier["score"])
            + float(resonance["score"])
        )
        multiplier = source_multiplier(row.get("source_status"), row.get("source"))
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
                    "six_character_profile": "藏干、十神、月令旺衰、盖头截脚只用于六字结构画像；缺时柱时不作完整格局或大运断语。",
                    "qimen_usage": "缺时柱时，年命天干优先用于奇门个人根本磁场；八字日主用于个人主观能力但不独断旺衰；生日支用于与比赛日支合冲刑害过滤；月令只作气候偏好和病药提示。",
                },
                "match_year_pillar": match_year,
                "match_month_pillar": match_month,
                "match_day_pillar": match_day,
                "match_day_stem": match_day_stem,
                "match_day_branch": match_day_branch,
                "stem_relation": stem_rel,
                "branch_relation": branch_rel,
                "role_ten_god_modifier": role_modifier,
                "event_resonance": resonance,
                "raw_role_score": round(raw_score, 3),
                "source_multiplier": multiplier,
                "normalized_team_weight": round(normalized_weight, 4),
                "weighted_score": round(weighted_score, 4),
                "score_status": "scored" if multiplier > 0 else "unscored_source_missing",
                "source_gate": "ok" if multiplier > 0 else "missing_or_untrusted_source",
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
            "year_pillar": match_year,
            "month_pillar": match_month,
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
        "schema": "worldcup-mystic-oracle/bazi-three-pillars-v2",
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
