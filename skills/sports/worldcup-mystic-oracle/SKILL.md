---
name: worldcup-mystic-oracle
description: Create a Chinese "赛前玄学战报" for World Cup or football matches using a reproducible pre-match data status check, verified kit colours, Qi Men Dun Jia match-time charts, and incomplete Four Pillars birth-date analysis for coaches and key players when hour data is missing. Use for entertainment-oriented match narratives, confidence-limited score pools, and one integrated China Sports Lottery advance-retreat strategy across 胜平负, 让球胜平负, 比分, 总进球, and 半全场, not for factual certainty or guaranteed betting advice.
license: MIT
metadata:
  version: 1.0.0
  author: Codex
  platforms:
    - hermes
    - codex-compatible
  hermes:
    category: sports
    tags:
      - football
      - world-cup
      - qimen-dunjia
      - bazi
      - china-sports-lottery
      - chinese
    language: zh-CN
    entrypoint: SKILL.md
    safety: entertainment-only
---

# Worldcup Mystic Oracle

## Purpose

Generate a Chinese "赛前玄学战报" that anchors on verified match facts, uses official kit colours, builds a Qi Men Dun Jia match-time judgement, compares coaches and key players through incomplete Four Pillars birth-date data, and converts the resulting match script into entertainment-only China Sports Lottery strategy tables.

Always separate verified facts from symbolic interpretation. Never claim a guaranteed hit, sure profit, or investment edge.

## Required Workflow

1. Read `references/prematch-data-status.md` and set the report phase:
   - `T-24h`: fixture, venue, kit, coach, expected roster, predicted lineup.
   - `T-2h`: re-check kit, injuries, weather, tactical news.
   - `T-60min`: official lineup if available.
   - `T-15min`: final contradiction check and no-play decision.
   - If the exact phase is unclear, infer it from kickoff time and state the inference.
2. Collect the factual match anchors:
   - Teams, official home/away order, competition stage, kickoff time, venue, local time, Beijing time.
   - Official or confirmed kit colours, national flag colours, coach, official squad, likely starters, confirmed lineups when available, recent injuries or suspensions, weather, and pitch or stadium orientation if relevant.
   - Current odds, official lottery availability, and lineup news only when sourced. Browse when the facts may have changed.
   - For China Sports Lottery strategy, read `references/official-sporttery-odds.md` and fetch the latest official Sporttery/中国体彩 odds and sale status first whenever available. Use `--include-history` when constructing betting strategy so detailed `TTG`, `CRS`, and `HAFU` prices can be used for tail branches. Include source URL and retrieval time, and mark odds unavailable instead of using stale or third-party numbers.
3. State the settlement frame:
   - China Sports Lottery football results are interpreted from the official home-team perspective.
   - Use 90 minutes plus stoppage time unless the user explicitly asks for a different market.
   - Exclude extra time and penalty shootouts for the listed play types unless current rules say otherwise.
4. Read `references/kit-colour-query.md` before doing kit-colour or Five Elements analysis.
5. Query coach and key-player birth dates:
   - Use the official lineup if available.
   - Treat public coach/player profile birth dates as Gregorian dates unless the source explicitly says lunar. Do not convert them into lunar calendar months for month-pillar calculation; bazi month pillars must use solar terms.
   - Default to the key-person set: manager, goalkeeper, captain or defensive leader, primary striker, primary creator or central midfielder, and one likely impact substitute.
   - Collect more players only when official lineup or roster data is easy to source.
   - Mark missing or uncertain dates; do not substitute age-only data.
   - Store or pass a `source_status` for every date. If `source_status` is missing, bazi may be computed but must not be used as a weighted betting modifier.
   - Report birth-date coverage as a ratio for each team.
6. Read `references/qimen-engine.md`, `references/qimen-bazi-method.md`, `references/qimen-bazi-overlay.md`, and `references/qimen-scoring.md` before producing the prediction. For Qi Men, use qfdk/qimen as the preferred structured engine when available, then explicitly apply the high-order method: charting standard, four-plate hierarchy, separate 九星/八门旺衰, 主客攻防势, 门迫/门制, 十干克应, 空亡/入墓/击刑/马星, and confidence reduction for unresolved abnormal fields. After the standalone Qi Men and standalone bazi checks, run the overlay: locate person anchors (`year_ming_stem`, `day_master`) and event anchors (`时干`, role-specific symbols), judge person-palace vs event-palace relation, and cap confidence when the chart cannot locate anchors.
7. Use helper scripts when useful:
   - `scripts/fetch_sporttery_odds.py` to fetch official Sporttery match-list odds into a local cache before betting-strategy arithmetic. Add `--include-history` when total-goals, exact-score, or half/full branches may be used.
   - `scripts/qimen_qfdk.js` to call qfdk/qimen and emit structured Qi Men JSON. This is preferred over HTML parsing.
   - `scripts/qimen_parse.py` to parse saved Qi Men calculator HTML into JSON only as a fallback. If parsing is incomplete, label the section `简化奇门象占`.
   - `scripts/bazi_three_pillars.py` to compute 年柱/月柱/日柱 and role-weighted bazi modifiers from sourced birth dates. Pass `--match-date` when the match local date is known. If the dependency is missing, install or use a reliable external calculator and cite it.
   - `scripts/primary_bet_strategy.py` to format one high-probability primary strategy from official odds and oracle-selected candidate branches.
8. Build the battle report with only these prediction modules:
   - 球衣五行入盘.
   - 奇门遁甲时家排盘.
   - 主教练与球员缺时柱八字.
   - 奇门×八字叠盘.
   - 现实校验.
9. Apply the confidence gates in `references/prematch-data-status.md` before writing the final lean, score pool, or betting packs.
10. Read `references/lottery-rules.md` before producing betting strategy content.
11. Read `references/pre-match-market-mapping.md` before selecting score structures or staking profiles:
   - Classify each signal into result, handicap, goal-channel, tempo, or image buckets.
   - Run the consensus-trap, favorite-expansion, weak-side-goal, and conflict checks.
   - Rank the top markets and explicitly reduce markets that contradict the chosen script.
12. Convert the oracle into one primary betting strategy by default. The primary strategy should be an integrated advance-retreat structure when official odds are available: main recovery branch, attack branch, and protect branch. Use multiple styles only if the user explicitly asks for alternatives.
13. Read `references/betting-strategies.md` before creating the staking table.
14. Use `references/report-template.md` for the final answer structure.
15. Before final output, run the Hermes readability check:
   - No nicknames, roleplay address, or filler such as `大王`.
   - No bullet fragments with empty `风格` or `风险` fields.
   - No more than one primary betting strategy unless the user explicitly requested multiple styles. A single strategy may contain up to three branches in one table.
   - If official odds fetching fails, say what was attempted and output either `不下注 / 纯观赛` or one clearly labelled `理论模型` table, not a menu.
   - If kit, lineup, bazi, or Qi Men data is missing, use a compact `缺口` row and reduce confidence instead of padding the report.

## Output Rules

- Open with: "以下为娱乐性玄学分析，不构成投注建议或收益承诺。"
- Mark missing facts as missing; do not invent them.
- If using current fixtures, team news, rules, odds, weather, venue, kit colours, lineup data, or birth dates, cite the source links.
- Use "主队" and "客队" consistently according to the official fixture order, not reputation or geography.
- For a neutral World Cup match, still treat the first listed team as the lottery home team unless a source says otherwise.
- Separate prediction from betting strategy: a match lean is not automatically a recommended ticket.
- Always include data phase, lineup status, birth-date coverage, confidence level, and reversal/no-play conditions.
- Always include a role-based bazi table for coaches and key players when bazi is used: coach, goalkeeper, defensive leader/captain, creator or central midfielder, striker, and impact substitute or remaining key starter.
- When bazi is used, disclose `input_calendar`, conversion basis, and month-pillar basis. Public profile dates should be labelled as Gregorian/public-date inputs.
- Use a neutral professional tone. Do not address the user with nicknames or roleplay titles.
- Do not include astrology, biorhythm, aura reading, animal oracles, random omens, or broad feng shui unless the user explicitly asks for an extra entertainment appendix.
- Do not invent birth dates, lineups, kit colours, Qi Men chart values, or bazi pillars. Mark unknown data as missing.
- If only birth date is available, call the chart "缺时柱八字" or "三柱参考"; never infer an unknown birth hour.
- When combining Qi Men and bazi, state whether 年命/日主落宫 and 事宫 are parsed. If not parsed, label the overlay `partial` and keep it qualitative.
- Do not claim definitive喜用神 or大运 unless full four pillars and a cited reliable calculator are available. With date-only public profiles, write `喜忌未完整判定`.
- Give exactly one primary strategy by default. Do not make the user choose.
- Do not output `Optional Multiple Styles` content from `betting-strategies.md` unless the user explicitly asks for multiple strategies.
- When official odds are available, include conditional-return arithmetic for the strategy: `stake × odds = return`, plus net result against the full 100-unit exposure.
- Use total-goals and exact-score as small barbell tail branches when official detailed odds are available. Prefer total-goals over broad exact-score wrapping; use exact score for `胜其它/负其它/0:0` style extremes.
- If `TTG/CRS/HAFU` are selling but detailed official odds are missing, list them as `待确认尾部` and do not allocate units.
- Never write or imply guaranteed profit. Use `条件回收`, `条件返还`, and `净值` instead of `保证收益`.
- Include the rejected alternatives only as a one-line "为什么不选" note when useful.
- Include a "放弃条件" for the primary strategy.
- Include percentage allocation and a `100单位示例` for the primary strategy unless the user provides a specific bankroll.
- Include bankroll limits and responsible lottery language.
- Avoid recommending martingale, borrowing money, chasing losses, or all-in stakes.

## Optional Helper Script

Use `scripts/fetch_sporttery_odds.py` before any China Sports Lottery staking arithmetic:

```bash
python scripts/fetch_sporttery_odds.py --team "德国" --include-history --output data/sporttery_odds_cache.json --pretty --utf8
```

Use `scripts/qimen_qfdk.js` when a local qfdk/qimen engine checkout is available:

```bash
node scripts/qimen_qfdk.js --engine-dir ~/.hermes/engines/qfdk-qimen --datetime 2026-06-14T12:00:00-05:00 --location "Houston" --pretty
```

Use `scripts/bazi_three_pillars.py` with a match date to produce auditable role-weighted bazi:

```bash
python scripts/bazi_three_pillars.py --people people.json --match-date 2026-06-15 --pretty --utf8
```

Use `scripts/primary_bet_strategy.py` when the oracle has selected candidate betting branches and the user wants one primary strategy:

```bash
python scripts/primary_bet_strategy.py --odds-cache data/sporttery_odds_cache.json --candidates references/sample-barbell-candidates.json --mode balanced --pretty --utf8
```

Use `scripts/bet_plan.py` when the user wants a neat stake table from a JSON plan. The script summarizes total exposure, pick counts, and per-pick stake. It does not validate whether a real lottery terminal supports a specific ticket combination.

Example:

```bash
python scripts/bet_plan.py --demo
```

## Reference Files

- `references/prematch-data-status.md`: timing phases, confidence caps, and reversal conditions.
- `references/official-sporttery-odds.md`: official Sporttery odds endpoints, cache schema, sale-status checks, and implied-probability arithmetic.
- `references/kit-colour-query.md`: official kit-colour lookup workflow and confidence levels.
- `references/qimen-engine.md`: preferred qfdk/qimen engine setup, disclosure, and fallback order.
- `references/qimen-bazi-method.md`: Qi Men Dun Jia match chart and incomplete Four Pillars workflow.
- `references/qimen-bazi-overlay.md`: person-event overlay using 年命/日主, 事宫, role-specific symbols,喜忌 limits, and流年 filters.
- `references/qimen-scoring.md`: use-god anchors, palace scoring rows, and market mapping from Qi Men signals.
- `references/lottery-rules.md`: China Sports Lottery play type definitions and option lists.
- `references/pre-match-market-mapping.md`: market-signal buckets, consensus-trap detection, favorite expansion, weak-side goal classification, score-structure tree, and pre-bet conflict checks.
- `references/betting-strategies.md`: strategy packs and stake allocation logic.
- `references/report-template.md`: final "赛前玄学战报" output template.
