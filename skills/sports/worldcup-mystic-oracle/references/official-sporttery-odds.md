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

The history endpoint may be WAF-blocked or unavailable. If it fails, keep current odds from `getMatchListV1` and mark history as unavailable.

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
