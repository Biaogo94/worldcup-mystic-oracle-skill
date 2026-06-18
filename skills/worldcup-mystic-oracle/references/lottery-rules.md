# China Sports Lottery Football Rules Reference

Verify current rules and available matches with official China Sports Lottery or Sporttery pages before live use. This reference is a compact working model for battle-report generation.

For odds and sale status, read `official-sporttery-odds.md` and use the Sporttery official endpoint cache. Do not use bookmaker or exchange odds for official lottery return arithmetic.

## Stake Unit Rule

- China Sports Lottery football tickets use `2元` as the basic stake unit.
- Every recommended branch amount must be an integer multiple of `2元`.
- If a play contains multiple selections and the plan says `平均分配`, each per-selection amount must also be a `2元` multiple.
- Default examples should use `100元示例`, not abstract units. Show `金额(元)` and `注数(2元/注)`.
- If a user gives a budget that is not divisible by 2, round down to the nearest executable even-yuan amount and state the unused remainder.

## Shared Settlement Frame

- Use the official home-team perspective: "胜" means the listed home team wins, "平" means draw, "负" means the listed home team loses.
- Football lottery settlement for these plays normally uses full time: 90 minutes plus stoppage time.
- Do not include extra time or penalty shootouts unless the user asks about a special market and current official rules confirm it.
- If the match is at a neutral venue, still use the official listing order for "主队" and "客队".

## 胜平负

Predict the full-time result:

- `胜` or `3`: home team wins.
- `平` or `1`: draw.
- `负` or `0`: home team loses.

## 让球胜平负

Apply the listed handicap to the home team's score, then judge the result from the home-team perspective.

Use the official `HHAD` `goal_line` from Sporttery when available. If the user asks specifically for `-1` but the official line differs, explain the difference and treat `-1` as a theoretical mapping only.

For user-requested `-1`:

- Actual home win by 2 or more: `让胜`.
- Actual home win by exactly 1: `让平`.
- Actual draw or home loss: `让负`.

Strategy note: `-1` is often the best bridge between a Qi Men result lean and a precise score call. A one-goal signal points to `让平`; a domination signal points to `让胜`; an upset or draw signal points to `让负`.

## 比分固定

The common fixed-score board has 31 options:

Home win:

- `1:0`, `2:0`, `3:0`, `4:0`
- `2:1`, `3:1`, `3:2`
- `4:1`, `4:2`
- `5:0`, `5:1`, `5:2`
- `胜其他`

Draw:

- `0:0`, `1:1`, `2:2`, `3:3`
- `平其他`

Home loss:

- `0:1`, `0:2`, `0:3`, `0:4`
- `1:2`, `1:3`, `1:4`
- `2:3`, `2:4`
- `0:5`, `1:5`, `2:5`
- `负其他`

Use fixed scores as a small, high-variance layer. Keep the score pool consistent with the main result and total-goal oracle.

## 总进球

Predict both teams' full-time total goals:

- `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7+`

Mapping from match script:

- Closed defensive match: `0`, `1`, `2`.
- Normal tactical match: `2`, `3`.
- Open attacking match: `3`, `4`, `5`.
- Chaotic red-card or late-collapse match: `4`, `5`, `6`, `7+`.

## 半全场胜平负

Predict home-team result at half time and full time. Half-time result comes first.

- `胜胜`: home leads at half time and wins full time.
- `胜平`: home leads at half time and draws full time.
- `胜负`: home leads at half time and loses full time.
- `平胜`: draw at half time, home wins full time.
- `平平`: draw at half time and full time.
- `平负`: draw at half time, home loses full time.
- `负胜`: home trails at half time but wins full time.
- `负平`: home trails at half time but draws full time.
- `负负`: home trails at half time and loses full time.

Use 半全场 to express the battle-report plot:

- Slow-burning favorite: `平胜`.
- Early pressure maintained: `胜胜`.
- Favorite fades after strong start: `胜平` or `胜负`.
- Underdog counterattack after parity: `平负`.
- Away-side control throughout: `负负`.
