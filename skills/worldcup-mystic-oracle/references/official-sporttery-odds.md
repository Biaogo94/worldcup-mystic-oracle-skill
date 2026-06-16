# Official Sporttery Odds

Use this file whenever producing China Sports Lottery strategy. Official odds mean 中国体育彩票 / Sporttery only. Do not treat bookmaker aggregators, media odds, exchanges, or Polymarket as official lottery odds.

## Required Fetch

Before allocating units, run or replicate:

```bash
python scripts/fetch_sporttery_odds.py --output data/sporttery_odds_cache.json --pretty --utf8
```

Filter when the fixture is known:

```bash
python scripts/fetch_sporttery_odds.py --team "德国" --output data/sporttery_odds_cache.json --pretty --utf8
python scripts/fetch_sporttery_odds.py --match-id 2040174 --output data/sporttery_odds_cache.json --pretty --utf8
```

Official current match-list endpoint:

- `https://webapi.sporttery.cn/gateway/uniform/football/getMatchListV1.qry?clientCode=3001`

Optional fixed-bonus history endpoint:

- `https://webapi.sporttery.cn/gateway/uniform/football/getFixedBonusV1.qry?clientCode=3001&matchId=<matchId>`

The history endpoint may be WAF-blocked or unavailable. If it fails, keep current odds from `getMatchListV1` and mark history as unavailable. If it succeeds, use the normalized `fixed_bonus_history` fields for detailed `CRS`, `TTG`, and `HAFU` prices when the match-list response has blank detailed odds.

## Field Mapping

Use the normalized cache fields first:

| Cache Field | Meaning |
| --- | --- |
| `retrieved_at.beijing` | Beijing retrieval time for the report |
| `matches[].match_id` | Sporttery match identifier |
| `matches[].match_num_str` | Lottery match number, e.g. `周一013` |
| `matches[].home.name` / `away.name` | Official lottery home/away perspective |
| `matches[].status` | Match sale/listing status |
| `matches[].pools[pool].status` | Sale status by play type |
| `matches[].odds[pool].h` | Home-side win selection for `HAD`; handicap home-side win for `HHAD` |
| `matches[].odds[pool].d` | Draw selection |
| `matches[].odds[pool].a` | Away-side win selection |
| `matches[].odds[pool].goal_line` | Handicap line for `HHAD` |
| `matches[].odds[pool].implied_probabilities` | Raw and normalized implied probabilities for three-way pools |
| `fixed_bonus_history[matchId].normalized.TTG.odds` | Detailed total-goals prices, including `5`, `6`, and `7+` |
| `fixed_bonus_history[matchId].normalized.CRS.odds` | Detailed exact-score prices, including `胜其它`, `平其它`, `负其它` |
| `fixed_bonus_history[matchId].normalized.HAFU.odds` | Detailed half/full prices |

Pool codes:

| Pool | Chinese |
| --- | --- |
| `HAD` | 胜平负 |
| `HHAD` | 让球胜平负 |
| `CRS` | 比分固定 |
| `TTG` | 总进球 |
| `HAFU` | 半全场 |

For `HAD`: `h=胜`, `d=平`, `a=负`.

For `HHAD`: `h=让胜`, `d=让平`, `a=让负`; always state the official `goal_line` instead of assuming `-1`.

Interpret `HHAD.goal_line` from the official lottery home-team perspective:

- `goal_line = -1.00` means the lottery home team starts at `-1`; `让胜` requires home win by 2+.
- `goal_line = +1.00` means the lottery home team starts at `+1`; `让负` requires the away team to win by 2+.
- Never infer the handicap from team reputation. If the user asks for `让球(-1)` but the official line is `+1.00`, say the requested `-1` line is not the official Sporttery line for this fixture and remap strategy to the official line.

Treat a pool as actionable only when both conditions are true:

- `matches[].pools[pool].status == "Selling"`.
- The normalized odds row has a non-empty price for the recommended selection.

Some pools can be marked `Selling` while the current match-list response omits detailed prices, especially `CRS`, `TTG`, or `HAFU`. In that case, run `--include-history` and use fixed-bonus history prices only if the strategy labels them `需终端确认销售状态`. If terminal confirmation is impossible or the status flags look contradictory, list the branch as `待确认尾部` and do not allocate units.

For barbell strategy, prefer detailed official prices in this order:

1. Current match-list `HAD/HHAD` for main and handicap branches.
2. Fixed-bonus history `TTG` for total-goals tails.
3. Fixed-bonus history `CRS` for exact-score extremes such as `胜其它`, `负其它`, or `0:0`.
4. Fixed-bonus history `HAFU` only when the Qi Men tempo script clearly supports a half/full branch.

When `TTG/CRS/HAFU` history prices are used, add this note to the report:

`总进球/比分/半全场明细来自体彩固定奖金历史接口，需以临场终端销售状态为准。`

## Implied Probability

For decimal odds:

```text
raw probability = 1 / odds
normalized probability = raw probability / sum(raw probabilities for the pool)
```

Use normalized probability only as a market-temperature check. It is not a mystical prediction and it does not override the Qi Men judgement by itself.

## Report Rules

- Include source URL, retrieval time, match ID, lottery match number, and sale status.
- Use official home/away order from the Sporttery record when mapping 胜/平/负.
- If official odds are missing, stale, or the fixture is not listed, state `中国体彩官方赔率暂不可得`.
- If a recommended play type is not selling or has blank odds, remove it from actionable tables or mark the table `理论模型`.
- Do not use third-party odds for stake-return arithmetic.
- If the official handicap is not `-1`, map strategy to the official handicap and only discuss `-1` as a user-requested theoretical variant.
