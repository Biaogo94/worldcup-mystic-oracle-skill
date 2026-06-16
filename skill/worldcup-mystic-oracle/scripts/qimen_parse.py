#!/usr/bin/env python3
"""Parse saved Qi Men calculator HTML into a cautious JSON summary.

The parser is intentionally conservative. It is designed for qimen.live/Kevin
Foong-style HTML where each palace is inside an `inside-table show-pop-up-dragabble`
table. If the expected structure is missing, it reports `failed` instead of
inventing a chart.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


PALACE_START_RE = re.compile(
    r'<table id="clickPopup(?P<id>\d+)"[^>]*class="inside-table show-pop-up-dragabble"[^>]*>',
    re.IGNORECASE | re.DOTALL,
)

TAG_RE = re.compile(r"<[^>]+>")

DOOR_NAMES = {
    "開": "开门",
    "开": "开门",
    "休": "休门",
    "生": "生门",
    "傷": "伤门",
    "伤": "伤门",
    "杜": "杜门",
    "景": "景门",
    "死": "死门",
    "驚": "惊门",
    "惊": "惊门",
}

STAR_NAMES = {
    "蓬": "天蓬",
    "任": "天任",
    "沖": "天冲",
    "冲": "天冲",
    "輔": "天辅",
    "辅": "天辅",
    "英": "天英",
    "芮": "天芮",
    "柱": "天柱",
    "心": "天心",
}

DEITY_NAMES = {
    "符": "值符",
    "蛇": "腾蛇",
    "陰": "太阴",
    "阴": "太阴",
    "合": "六合",
    "虎": "白虎",
    "武": "玄武",
    "地": "九地",
    "天": "九天",
    "雀": "朱雀",
    "陳": "勾陈",
    "陈": "勾陈",
}

STEMS = set("甲乙丙丁戊己庚辛壬癸")


def textify(fragment: str) -> str:
    fragment = re.sub(r"<script.*?</script>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    fragment = re.sub(r"<style.*?</style>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    text = TAG_RE.sub(" ", fragment)
    return " ".join(html.unescape(text).split())


def first_symbol(text: str, mapping: dict[str, str]) -> str | None:
    for char, name in mapping.items():
        if re.search(rf"(^|\s){re.escape(char)}(\s|$)", text):
            return name
    # Fallback for compact text where table spacing was lost.
    for char, name in mapping.items():
        if char in text:
            return name
    return None


def extract_stems(text: str) -> list[str]:
    stems: list[str] = []
    for char in text:
        if char in STEMS and char not in stems:
            stems.append(char)
    return stems


def parse(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    chart_start = raw.find("plugin-qmdj-chart")
    if chart_start < 0:
        return {
            "status": "failed",
            "reason": "No plugin-qmdj-chart marker found.",
            "source_file": str(path),
        }
    chart_end = raw.find("qmdj-info", chart_start)
    chart = raw[chart_start : chart_end if chart_end > chart_start else len(raw)]

    palaces: list[dict[str, Any]] = []
    starts = list(PALACE_START_RE.finditer(chart))
    for index, match in enumerate(starts):
        chunk_end = starts[index + 1].start() if index + 1 < len(starts) else match.end() + 9000
        chunk_end = min(chunk_end, len(chart))
        body_text = textify(chart[match.start() : chunk_end])
        palaces.append(
            {
                "popup_id": match.group("id"),
                "raw_text": body_text,
                "stems_seen": extract_stems(body_text),
                "door": first_symbol(body_text, DOOR_NAMES),
                "star": first_symbol(body_text, STAR_NAMES),
                "deity": first_symbol(body_text, DEITY_NAMES),
            }
        )

    center_match = re.search(r"Hour\s*<br\s*/?>\s*(?P<date>\d{2}/\d{2}/\d{4}).*?<a>(?P<time>\d{2}:\d{2})</a>", chart, re.DOTALL)
    selected = None
    if center_match:
        selected = {
            "date": center_match.group("date"),
            "time": center_match.group("time"),
        }

    complete_palaces = [palace for palace in palaces if palace.get("door") and palace.get("star") and palace.get("deity")]
    status = "parsed" if len(palaces) == 8 and len(complete_palaces) == 8 else "partial" if palaces else "failed"
    reason = None
    if status == "partial":
        reason = f"Expected 8 complete palaces from the HTML chart; found {len(palaces)} palaces and {len(complete_palaces)} complete palaces."
    elif status == "failed":
        reason = "No palace tables found."

    return {
        "status": status,
        "reason": reason,
        "schema": "worldcup-mystic-oracle/qimen-parse-v1",
        "source_file": str(path),
        "selected_time": selected,
        "palace_count": len(palaces),
        "palaces": palaces,
        "note": "Review raw_text before making exact palace claims. If home/away stems cannot be placed reliably, downgrade to 简化奇门象占.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse saved Qi Men calculator HTML.")
    parser.add_argument("html_file", help="Saved calculator HTML file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    parser.add_argument("--utf8", action="store_true", help="Emit UTF-8 characters instead of ASCII-safe escapes.")
    args = parser.parse_args()

    result = parse(Path(args.html_file))
    json.dump(result, sys.stdout, ensure_ascii=not args.utf8, indent=2 if args.pretty else None)
    print()


if __name__ == "__main__":
    main()
