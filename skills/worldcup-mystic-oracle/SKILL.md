---
name: worldcup-mystic-oracle
description: Use for Chinese football pre-match mystic reports and China Sports Lottery strategy. Works in Claude Code, OpenCode, Codex-compatible CLIs, and other agents. Produces entertainment-only "赛前玄学战报" using official match facts, Sporttery odds, Qi Men Dun Jia, missing-hour Bazi for coaches/key players, score scenarios, and one compact odds-aware advance-retreat strategy.
license: MIT
---

# Worldcup Mystic Oracle

Generate a Chinese `赛前玄学战报` for football matches. The skill is entertainment-only and must never promise a guaranteed hit, guaranteed profit, or investment edge.

## Default Mode

Use **fast mode** unless the user explicitly asks for a full deep report.

Fast mode output:

1. opening disclaimer;
2. match fact card;
3. key Qi Men + Bazi judgement;
4. score scenario pool;
5. exactly one official-odds strategy table;
6. no-play/reversal conditions.

Deep mode may additionally include full kit analysis, detailed Qi Men four-plate scoring, role-by-role Bazi tables, and person-event overlay tables.

## CLI-First Workflow

1. Establish phase from current time vs kickoff:
   - `early`: more than 24h before kickoff;
   - `prelineup`: 2h to 24h before kickoff;
   - `late`: 60m to 2h before kickoff;
   - `lineup`: 15m to 60m before kickoff;
   - `post-lock`: after kickoff or lottery cutoff.
2. Verify official fixture, official/listed home-away order, kickoff local time, venue, and Beijing time. Browse when current facts may have changed.
3. Fetch official Sporttery/中国体彩 odds before any staking arithmetic:

```bash
python scripts/fetch_sporttery_odds.py --team "球队名或比赛编号" --include-history --output data/sporttery_odds_cache.json --pretty --utf8
```

4. When enough inputs are known, prefer one bundle command over manual repeated steps:

```bash
python scripts/collect_match_bundle.py \
  --home "伊拉克" --away "挪威" --team "伊拉克" \
  --kickoff-local "2026-06-16T18:00:00-04:00" \
  --venue "Boston" \
  --people data/people.json \
  --include-history \
  --output-dir data/iraq-norway \
  --pretty --utf8
```

5. Use the configured `qimen` MCP first. If MCP tools are available in the agent, call them directly:

```text
qimen_calculate(datetime="2026-06-16T18:00:00-04:00", location="Boston", purpose="综合")
qimen_detect_geju(datetime="2026-06-16T18:00:00-04:00", location="Boston")
```

If direct MCP tools are not exposed, use the bundled stdio client against the local Biaogo94/qimen server:

```bash
node scripts/qimen_mcp_client.mjs --datetime 2026-06-16T18:00:00-04:00 --location "Boston" --pretty
```

Only fall back to `scripts/qimen_qfdk.js` or `简化奇门象占` when the MCP server is unavailable; lower confidence and disclose the fallback.

6. For public coach/player birthdays, treat dates as Gregorian unless explicitly marked lunar. Never infer an unknown birth hour:

```bash
python scripts/bazi_three_pillars.py --people data/people.json --match-date 2026-06-16 --pretty --utf8
```

7. Convert the oracle judgement into weighted score scenarios, then optimize official-odds staking:

```json
[
  {"score": "0:2", "weight": 0.35, "label": "主线"},
  {"score": "1:2", "weight": 0.30, "label": "主线丢球"},
  {"score": "0:1", "weight": 0.15, "label": "防守"},
  {"score": "0:3", "weight": 0.12, "label": "右端"},
  {"score": "1:1", "weight": 0.08, "label": "左端"}
]
```

```bash
python scripts/optimize_strategy.py \
  --odds-cache data/sporttery_odds_cache.json \
  --scenarios references/sample-score-scenarios.json \
  --match-id 2040179 \
  --include-pools HAD,HHAD,TTG,CRS \
  --pretty --utf8
```

Use the optimizer output as a draft, then sanity-check it against the football script. Do not buy all outcomes of the same pool unless the arithmetic genuinely supports it; usually it does not.

Default optimizer constraints intentionally keep exact-score stakes small:

- `CRS` is a tail/detail tool, not the main bankroll.
- Main anchors should normally be `HAD`, `HHAD`, or `TTG`.
- If the optimizer puts too much stake on one exact score, rerun with stricter `--max-crs-stake` / `--max-crs-total` or manually reduce the score branch.

## Required Judgement Rules

- Separate facts from symbolism.
- Official Sporttery odds are the only acceptable odds for stake-return arithmetic. Third-party odds may only be labelled context.
- Always state Sporttery home/away order and official `HHAD.goal_line`; never assume `-1`.
- If detailed `TTG/CRS/HAFU` prices come only from fixed-bonus history, say `需终端确认销售状态` before allocating units. If status is too uncertain, put them in `待确认尾部`.
- Match lean is not automatically a ticket. A low-confidence match can be `不下注 / 纯观赛`.
- Use total goals before broad exact-score wrapping. Use exact score only for a tight main score or extreme tails such as `胜其它/负其它/0:0`.
- Do not produce multiple betting styles unless the user asks for alternatives.
- China Sports Lottery stakes must be executable 2-yuan multiples. Default to a `100元示例`; every branch amount and per-pick split must be divisible by 2.
- Use `条件返还`, `条件回收`, and `净值`; do not write `保证收益`.

## Missing-Hour Bazi Protocol

For public date-only football profiles:

```text
Qi Men event chart -> 年命落宫 -> 时干/事宫 -> 年命与事宫生克
-> 月令气候偏好 -> 日主/日支 filters -> low-weight 流年共振
```

- 年命 is the primary person anchor.
- 日主 is secondary; it cannot override 年命 by itself.
- Qi Men 时干 substitutes for the missing hour-pillar result/future function.
- 月令 gives cold/heat/dry/damp tendency and possible病药 hint only.
- Do not claim complete喜用神 or大运 without full four pillars and a cited reliable calculator.

## Reference Loading

Read only what is needed:

- `references/prematch-data-status.md`: phase, confidence gates, reversal conditions.
- `references/official-sporttery-odds.md`: Sporttery endpoints and odds field mapping.
- `references/qimen-engine.md`: Biaogo94/qimen MCP usage and fallback.
- `references/qimen-bazi-method.md`: detailed Qi Men + incomplete Bazi method.
- `references/qimen-bazi-overlay.md`: person-event overlay.
- `references/qimen-scoring.md`: Qi Men scoring and market mapping.
- `references/pre-match-market-mapping.md`: score structures and conflict checks.
- `references/betting-strategies.md`: stake rules and output contract.
- `references/report-template.md`: full report template; use selectively in fast mode.

## Final Output Skeleton

Start with:

`以下为娱乐性玄学分析，不构成投注建议或收益承诺。`

Then keep the report compact:

```text
赛前状态
| 项目 | 结论 |

玄学总判
- 胜负倾向：
- 比分场景：
- 总进球：
- 半全场：
- 信心等级：

关键依据
- 奇门：
- 缺时柱八字：
- 赔率/现实校验：

唯一主策略
| 分支 | 玩法 | 选择 | 赔率 | 金额(元) | 注数(2元/注) | 条件返还 | 净值 | 作用 |

情景返还
| 场景 | 命中分支 | 条件返还 | 净值 |

放弃条件
- ...
```

If official odds are unavailable or not actionable, output `不下注 / 纯观赛` unless the user explicitly requests a theoretical model.
