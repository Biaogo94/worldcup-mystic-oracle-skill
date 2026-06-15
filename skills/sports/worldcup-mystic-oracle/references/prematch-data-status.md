# Prematch Data Status

Use this file before producing any prediction, score pool, or betting strategy.

## Timing Phases

Determine the report phase from the current time relative to kickoff:

| Phase | Time Window | Allowed Inputs | Output Limit |
| --- | --- | --- | --- |
| `T-24h` | more than 2 hours before kickoff | official fixture, venue, official or designated kits, coach, squad, predicted lineup, injuries, weather forecast | pre-match lean only; no "confirmed lineup" wording |
| `T-2h` | 2 hours to 60 minutes before kickoff | re-check kits, absences, venue weather, reliable lineup leaks | medium confidence cap unless official lineup is out |
| `T-60min` | 60 to 15 minutes before kickoff | official lineup, match sheet, final kit photos | highest available confidence, still entertainment-only |
| `T-15min` | final 15 minutes before kickoff | only material changes and contradiction checks | simplify output; do not rebuild a long report unless needed |
| `post-lock` | after kickoff or lottery cutoff | analysis only; do not present as actionable pre-match betting |

If kickoff time or current time is uncertain, state the uncertainty and cap the report at `low`.

## Data Status Labels

Use these labels in the report:

- `official`: official competition, federation, team, match centre, team sheet, or lottery source.
- `official-odds`: latest odds and sale status from official Sporttery/中国体彩网 or its official match/odds endpoint.
- `official-designation`: official competition kit-colour designation.
- `reputable-secondary`: reliable database, specialist site, or major media page.
- `predicted`: predicted lineup or preview claim.
- `inferred`: logical inference from home/away kit norms or team status.
- `missing`: no reliable source.

## Official Lottery Odds Requirement

When producing China Sports Lottery strategy, fetch the latest official odds and sale status before allocating units.

Read `official-sporttery-odds.md` and run `scripts/fetch_sporttery_odds.py` when possible. The current match-list endpoint is the primary source for official current odds:

```bash
python scripts/fetch_sporttery_odds.py --output data/sporttery_odds_cache.json --pretty --utf8
```

Source priority:

1. Official 中国体彩网 / 体彩竞彩足球 pages or official Sporttery pages.
2. Official lottery match list, odds, or sale-status endpoints exposed by those pages.
3. If the official page is unreachable, state `中国体彩官方赔率暂不可得` and do not substitute third-party odds as if they were official.
4. Third-party odds may only be used as context and must be labelled `third-party context`, never as the staking arithmetic base.

Required output when odds are available:

- Retrieval time and timezone.
- Source URL.
- Match ID or fixture identifier if shown.
- Sale status for each recommended play type.
- Odds used in every arithmetic line.
- Official handicap line for `HHAD`; do not assume `-1` if the endpoint lists another line.

If official odds are missing or stale, cap betting-strategy confidence at `theoretical` and avoid saying any plan can recover cost.

## Confidence Gates

Set the final confidence level after scoring:

| Missing or Weak Input | Maximum Confidence |
| --- | --- |
| official fixture/order missing | no prediction |
| settlement frame unclear | no betting strategy |
| kit colour not official or official-pre-match | `medium` |
| only predicted lineup available | `medium` |
| no lineup or squad birth-date coverage below 50% of key-person set | `low-medium` |
| bazi dates are computed but source_status is mostly missing | bazi cannot raise confidence; betting confidence max `medium` |
| Qi Men chart not parsed and only simplified symbolism is used | `medium` |
| Qi Men and bazi point opposite directions without a football bridge | `low-medium` |
| major injury/lineup news is missing within 2 hours of kickoff | `low` |

Confidence labels:

- `high`: official lineup, official kit, parsed Qi Men chart, key-person birth coverage at least 5/6 for both teams, no major contradictions.
- `medium`: reliable fixture and kit, predicted lineup or partial birth coverage, Qi Men chart parsed or reasonably simplified.
- `low-medium`: useful narrative but at least one core module is provisional.
- `low`: facts too thin, recommend no-play or symbolic tiny stake only.

## Reversal Conditions

Every report must list what would overturn or weaken the call. Use concrete match facts, not vague bad luck.

Common reversal conditions:

- Official lineup removes the primary striker, goalkeeper, captain, or playmaker used in bazi scoring.
- Team wears a different outfield or goalkeeper kit than the chart used.
- The official home/away order differs from the source used for lottery perspective.
- Venue, kickoff time, or timezone changes.
- Severe weather, late injury, red-card-prone referee profile, or tactical formation change materially alters the match script.
- Odds or lottery availability move sharply and the user wanted a betting strategy, not only a narrative.

If two or more reversal conditions are active, recommend `no-play` or `纯观赛仪式`.

## Prediction vs Betting

Keep these separate:

- Prediction: the symbolic match lean, score path, total-goal tendency, and half/full-time script.
- Betting strategy: optional entertainment allocation under bankroll limits.

Do not translate a prediction into a single "must buy" ticket. Always show at least one conservative or no-play alternative.
