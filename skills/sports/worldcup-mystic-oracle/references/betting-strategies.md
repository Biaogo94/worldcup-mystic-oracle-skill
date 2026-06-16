# Betting Strategy

Convert the Qi Men and incomplete-bazi "赛前玄学战报" into one entertainment-only China Sports Lottery structure by default. The user should not have to choose between many styles unless they explicitly ask for alternatives.

The default strategy is not a naked win/loss pick. It is one integrated `进退综合` structure:

- Main branch: highest-confidence path, sized to attempt conditional cost recovery.
- Attack branch: small upside branch for stronger-than-baseline script.
- Protect branch: small defensive branch for the most plausible adjacent miss.
- Scenario table: calculate combined returns when multiple branches can hit in the same match result, such as `HAD 负` plus `HHAD 让平/让负`.

Never promise guaranteed profit. First check whether odds math can actually cover total exposure under the main branch. If not, say so plainly and frame the plan as conditional recovery plus upside, not guaranteed收益.

## Hard Output Contract

Default betting output is one clean strategy only. It may contain 1 to 3 branches inside the same table, but do not print the optional style catalogue.

If official Sporttery odds are unavailable, the default primary strategy is:

| 项目 | 内容 |
| --- | --- |
| 主推策略 | 不下注 / 纯观赛 |
| 为什么它胜率最高 | 官方赔率或销售状态不可核验，无法确认可执行分支 |
| 玩法与选择 | 无 |
| 资金配置 | 0%，100单位示例=0 |
| 条件返还 | 不可计算 |
| 最大风险 | 用第三方或假设赔率替代官方赔率会造成错误下注映射 |
| 放弃条件 | Sporttery 官方接口仍不可用、比赛未列出、玩法未销售、官方主客/让球线未确认 |

Only if the user explicitly asks for a theoretical model despite missing official odds may output one `理论模型` table. Even then, keep it to one table and do not include multiple styles.

## Bankroll Rules

- If the user gives a budget, use that amount as the maximum exposure and convert each percentage into money.
- If no budget is given, use percentages plus a fictional `100单位示例`.
- For a single match, suggest risking only a small portion of the user's entertainment bankroll.
- Never suggest borrowing, chasing losses, martingale doubling, or all-in stakes.
- The primary strategy must include a "放弃条件".
- Separate prediction from betting. A match lean can become `no-play` when confidence gates are low.
- If final confidence is `low`, the only primary strategy is `不下注 / 纯观赛`.
- If report phase is `post-lock`, do not present pre-match betting as actionable. Use any table only as replay mapping.
- Before any staking table, read `official-sporttery-odds.md` and fetch latest official Sporttery/中国体彩 odds and sale status for the exact fixture and play types. If official odds are unavailable, mark the table `理论模型` and do not use assumed odds for cost-recovery claims.
- If official odds are unavailable and the user did not explicitly request a theoretical model, do not allocate any units.
- Use the official `HHAD` handicap line from the cache. Do not force `-1` allocations when Sporttery lists a different line; either remap to the official line or mark the `-1` branch theoretical.
- Always show conditional arithmetic for any plan that claims cost control: `stake × odds = return`. Use `返还` or `回收`, not guaranteed `盈利`, unless subtracting total exposure.
- Do not call a plan "保本" unless the shown return is at least total exposure under the stated winning condition.

## Primary Strategy Selector

Choose exactly one default strategy in this order. "进退综合" means a single structured plan that balances hit probability, conditional recovery, and upside. It is not guaranteed profit.

1. **No-play primary**
   - Use when confidence is `low`, official odds are unavailable, kickoff/lineup facts are stale, or the recommended market is not selling.
   - Output: `主推策略：不下注 / 纯观赛`.
2. **Integrated advance-retreat structure**
   - Use when official odds are available and confidence is at least `low-medium`.
   - Build one table with up to three branches: `主线回收`, `进攻增益`, `退守保护`.
   - Default allocations: `75/15/10` when the main odds are below 1.60; `65/20/15` when the main odds are 1.60 or higher.
   - If only one branch is officially priced, output `单锚`, but explain that it is too simple and cannot form an advance-retreat structure.
3. **High-probability single anchor**
   - Use only when the user explicitly asks for the simplest highest-hit branch or when no attack/protect branch has official odds.
   - Allocate 80% to 100% to the single highest-probability branch.
4. **Two/three-branch hedge**
   - Use only as one integrated table, not as separate styles.
   - Do not exceed three branches.

Selection rules:

- Prefer `胜平负` when the odds branch itself is high-probability and the return is not the user's main goal.
- Prefer `让球胜平负` when the result is clear but the winning margin is the real uncertainty.
- Prefer `总进球` only when official odds are available and the Qi Men door/tempo signal is stronger than the result signal.
- Avoid fixed score and half/full as the primary "胜率最大" strategy unless official lineup is available and the user asks for high variance.
- If the official favorite win odds are extremely low, keep it as the main recovery branch only if it is still the best hit-probability anchor. Explicitly say when the main branch cannot cover total cost.
- If the main-result branch has lower hit probability than a handicap protection branch, choose the handicap branch.
- For a clear favorite, candidate roles normally map as:
  - `main`: `HAD` favorite win.
  - `attack`: `HHAD` favorite handicap win or high-goal branch when available.
  - `protect`: `HHAD` adjacent protection, draw, or narrow-win branch.

Primary output format:

| 项目 | 内容 |
| --- | --- |
| 主推策略 | 不下注 / 进退综合 / 单锚 |
| 设计目标 | 主线条件回收 + 进攻增益 + 退守保护 |
| 官方赔率校验 | match ID, match number, sale status, HHAD line |
| 分支配置 | one table with pool, selection, role, odds, units, conditional return, net |
| 主线回收能力 | `stake × odds`, and whether it covers 100 units |
| 最佳情形 | highest conditional return among branches |
| 最大风险 | the main way it loses |
| 放弃条件 | concrete pre-kickoff trigger |

Then add:

- `为什么不选其它玩法`: one compact sentence, not a menu.
- `责任边界`: one sentence saying this is entertainment-only and can lose all units.
- `情景返还`: show combined return for the main score-difference scenarios. For example, if home is Saudi at `+1.00` and away is Uruguay, `客胜1` hits `HAD 负 + HHAD 让平`; `客胜2+` hits `HAD 负 + HHAD 让负`.

Optional helper:

```bash
python scripts/primary_bet_strategy.py \
  --odds-cache data/sporttery_odds_cache.json \
  --candidates HAD:负:1:main,HHAD:让负:0.85:attack,HHAD:让平:0.55:protect \
  --mode balanced --pretty --utf8
```

Use candidates selected by the oracle and market-mapping step. The helper ranks available official-odds branches by candidate weight and implied probability, then emits exactly one primary strategy with conditional-return arithmetic.

## Anti-Consensus Barbell Upgrade

Use this upgrade when a match has a clear favorite, but the market/commentary consensus is overly narrow, such as "强队小胜", "沉闷 1:0", or "大热艰难过关". The goal is not to chase long shots blindly; it is to keep the main bankroll on the highest-probability side while using small units to cover both tails that consensus tends to underprice.

This is a specialized variant of the default `进退综合` structure when the favorite edge is clear and the market narrative is too narrow.

Core principles:

- Flip the old `30% main / 70% upset` structure. When fundamentals still support the favorite, use `60% to 70%` as the main-result anchor and `30% to 40%` as branch capital.
- The main anchor must try to recover the full plan cost when the favorite simply wins. For example, `60 units × 1.70 = 102 units` creates a breakeven/micro-profit base before branch tickets.
- Do not only defend the underdog upset. Always ask whether the opposite extreme is live: favorite blowout, handicap win, `胜其它`, or total goals `5/6/7+`.
- Prefer total-goals coverage over excessive exact-score wrapping. Use exact scores only for a tight pool or for high-odds tail traps.
- Treat the handicap market as the script anchor. If the favorite is strong but public analysis keeps emphasizing "赢得艰难", reserve part of the branch capital for `让胜` when football logic supports a two-goal-plus win.
- Avoid low-value middle clutter such as many small stakes on `1:1`, `2:1`, `1:0`, and `2:0` when those picks cannot recover the plan cost.

Default `100单位` attack-defense model for a strong favorite with hidden blowout risk:

| Play | Selection | Allocation | Purpose |
| --- | --- | ---: | --- |
| 胜平负 | Favorite win | 60% | Base anchor; aims to breakeven or micro-profit if the main probability lands |
| 让球胜平负 | Favorite `让胜` | 20% | Captures the favorite winning by 2+ when the "艰难小胜" consensus is wrong |
| 高赔极端 | `胜其它` or 总进球 `5/6/7+` | 10% | Tail trap for 4:1, 5:0, 5:1, 4:2 and similar blowouts |
| 终极防冷 | `0:0`, underdog `0:1`, or draw/upset branch | 10% | Small insurance for a true favorite failure |

Alternative allocations:

| Scenario | Allocation | Use When |
| --- | --- | --- |
| `70/15/10/5` | 70% favorite win, 15% handicap, 10% blowout/high-goal, 5% cold | favorite edge is very clear and cold warnings are weak |
| `60/20/10/10` | 60% favorite win, 20% handicap, 10% blowout/high-goal, 10% cold | default barbell when both favorite edge and tail risk exist |
| `50/20/15/15` | 50% favorite win, 20% handicap/protection, 15% high-goal, 15% cold/draw | favorite positive but uncertainty or draw warnings are meaningful |
| `0/0/0/100 no-play` | no stake | confidence below `medium`, stale facts, or unsupported lottery options |

Arithmetic rule:

- Show the anchor return as `main stake × main odds = conditional return`.
- Show net only as `conditional return - 100 units` when using a `100单位` example.
- If the anchor return is below `100`, say: `主胜打出仍不能完全覆盖总成本，靠让胜/高赔分支改善回收`.
- Tail examples must be framed as conditional: `10 units × 40.00 = 400 units if this exact/high-goal branch lands`.

Apply cautiously:

- Use only when the favorite's factual edge remains intact after lineup, injury, weather, and odds checks.
- If the favorite edge is weak or confidence is below `medium`, do not use the 60/20/10/10 model; switch to `纯观赛型` or a reduced theoretical plan.
- If `胜` odds are too low to make the main anchor recover cost, explicitly state that the plan cannot be made breakeven by the main result alone.
- If supported high-goal or `胜其它` options are unavailable in the actual lottery terminal, replace them with total goals `5/6/7+` where available, or mark the tail branch as unavailable.
- Never describe the model as "保本" without showing the arithmetic and the condition under which it only breaks even.

## Optional Multiple Styles

Only when the user explicitly asks for multiple styles, include up to six styles:

| 风格 | Risk | Use When |
| --- | --- | --- |
| 保守防守型 | low | main lean is clear but user wants lower variance |
| 均衡主线型 | medium | main lean plus one protection branch |
| 进取比分型 | high | exact score pool is tight and confidence is at least medium |
| 半全场剧情型 | high | Qi Men script gives a clear first-half/full-time rhythm |
| 防冷对冲型 | medium-high | favorite is positive but upset/draw warnings are active |
| 纯观赛型 | minimal/no-play | confidence is low, post-lock, or user wants ritual fun only |

Each style should include:

- 适用前提.
- 总风险等级.
- 玩法组合.
- 选择项.
- 资金比例.
- `100单位示例`.
- 命中逻辑.
- 风险点.
- 放弃条件.

## Style A: 保守防守型

Use when the prediction has a clear lean but lineup, kit, or bazi uncertainty still exists.

Default allocation:

| Play | Allocation |
| --- | ---: |
| 胜平负 single or double chance | 45% |
| 让球胜平负 protection | 25% |
| 总进球 core band | 20% |
| 比分 symbolic pick | 10% |

Typical mappings:

- Favorite likely wins narrowly: 胜平负 `胜`, 让球(-1) `让平/让负`, 总进球 `2/3`, 比分 `1:0/2:1`.
- Draw-heavy: 胜平负 `平` or `胜/平`, 让球 `让负`, 总进球 `0/1/2`, 比分 `0:0/1:1`.
- Away lean: 胜平负 `负` or `平/负`, 让球 `让负`, 总进球 `1/2/3`, 比分 `0:1/1:2`.

放弃条件:

- The main lean is only `low`.
- Official lineup contradicts the key-person set.
- User cannot accept losing all allocated units.

## Style B: 均衡主线型

Use when the oracle has one main result and one protection branch. If a clear favorite remains supported and the public script is narrow or conservative, apply the `Anti-Consensus Barbell Upgrade` instead of over-covering middle scores.

Default allocation:

| Play | Allocation |
| --- | ---: |
| 胜平负 main result | 60% |
| 让球胜平负 script anchor | 20% |
| High-odds tail: `胜其它` or 总进球 `5/6/7+` | 10% |
| Draw/upset or low-score cold protection | 10% |

Typical mappings:

- Medium home lean without blowout signal: `胜` plus `平` protection; handicap `让平/让负`; totals `2/3`; scores `1:0/2:1/1:1`.
- Strong home lean with hidden blowout signal: `胜`; handicap `让胜`; tail `胜其它` or total goals `5/6/7+`; cold guard `0:0/0:1` or `平`.
- Strong home lean but only one-goal signal: `胜`; handicap `让平/让负`; totals `2/3`; keep exact scores to `1:0/2:1` rather than broad wrapping.
- Away-counter script: `负` plus `平`; handicap `让负`; totals `2/3`; scores `0:1/1:2/1:1`.

放弃条件:

- The score pool exceeds five picks.
- Qi Men and bazi disagree without a football bridge.
- The handicap offered is not the handicap assumed in the strategy.
- The main-result odds cannot recover most plan cost and no tail branch has acceptable availability.

## Style C: 进取比分型

Use when the score pool is narrow and the user wants higher variance.

Default allocation:

| Play | Allocation |
| --- | ---: |
| 比分 main pool | 40% |
| 总进球 matching band | 25% |
| 胜平负 result anchor | 20% |
| 让球胜平负 | 15% |

Score-pool sizing:

- `high` confidence with official lineup: up to 4 scores.
- `medium` confidence: 2 or 3 scores.
- `low-medium`: 1 or 2 symbolic scores only.
- `low`: do not use this style.

Typical mappings:

- Narrow favorite: scores `1:0/2:1`, totals `1/2/3`, result `胜`, handicap `让平/让负`.
- Open favorite: scores `2:0/3:1`, totals `3/4/5`, result `胜`, handicap `让胜/让平`; add `胜其它` or total goals `6/7+` only as a small tail if blowout risk is explicit.
- Blowout-tail script: result `胜`, handicap `让胜`, total goals `5/6/7+`, exact-score pool no wider than `3:0/4:1/胜其它`.
- Draw script: scores `0:0/1:1/2:2`, totals `0/2/4`, result `平`.

Conversion rule:

- When exact-score coverage grows beyond three picks, replace part of the score pool with total goals. For example, use total goals `6` instead of guessing between `5:1` and `4:2`.

放弃条件:

- Official lineup is unavailable and final confidence is below `medium`.
- Weather, referee, injury, or tactical change makes the score band too wide.
- User is using this as a recovery bet.

## Style D: 半全场剧情型

Use when Qi Men gives a clear tempo narrative.

Default allocation:

| Play | Allocation |
| --- | ---: |
| 半全场 | 35% |
| 胜平负 result anchor | 25% |
| 总进球 | 20% |
| 比分 | 20% |

Plot mappings:

- Slow favorite awakening: 半全场 `平胜`, result `胜`, scores `1:0/2:1`, totals `1/2/3`.
- Early control maintained: 半全场 `胜胜`, result `胜`, scores `2:0/3:1`, totals `2/3/4`.
- Favorite fades: 半全场 `胜平`, result `平`, scores `1:1/2:2`.
- Away counterattack: 半全场 `平负`, result `负`, scores `0:1/1:2`.
- Chaos match: half/full `胜胜/平胜/平负`, totals `4/5/6/7+`, scores `3:2/2:3/胜其他/负其他`.

放弃条件:

- First-half rhythm is unclear.
- Qi Men only supports a result lean, not a tempo script.
- User wants low variance.

## Style E: 防冷对冲型

Use when the favorite is positive but at least two cold-warning signals appear: draw door, injury/card warning, weak goalkeeper bazi, expected lineup rotation, travel fatigue, or underdog counterattack path. Do not let this style become a 70% upset chase unless the main favorite edge has actually collapsed.

Default allocation:

| Play | Allocation |
| --- | ---: |
| Favorite primary result | 50% |
| Draw or upset protection | 20% |
| 让球 protection or `让胜` script check | 15% |
| Total-goals tail or low/mid band | 10% |
| Cold score or extreme score | 5% |

Typical mappings:

- Home favorite but one-goal signal: `胜`, protect `平`; handicap `让平/让负`; score `1:1` or `2:1`.
- Strong team but defense clash: `胜` as anchor; if blowout signs also exist, use `让胜` plus total goals `5/6`; if not, use `让负` and totals `2/3`.
- Away underdog has counterattack signal: result `负/平`, handicap `让负`, scores `0:1/1:2/1:1`.
- Favorite plus double-tail warning: keep favorite anchor, split small tail units between `0:0/0:1` and `胜其它` or total goals `6/7+`.

放弃条件:

- Protection makes the plan too scattered.
- Score pool exceeds five picks.
- User wants a simple single-direction ticket.
- The plan spends more on cold branches than on the most probable result while the favorite edge remains intact.

## Style F: 纯观赛型

Use when confidence is low, the match is already post-lock, factual anchors are missing, or the user only wants ritual fun.

Default allocation:

| Play | Allocation |
| --- | ---: |
| No-play reserve | 80% to 100% |
| Symbolic result | 0% to 10% |
| Symbolic total goals | 0% to 5% |
| Symbolic exact score | 0% to 5% |

Output:

- Prefer `不下注/只看球`.
- If the user insists on a symbolic ticket, choose one result, one total-goal number, and one exact score only.

放弃条件:

- The user wants a serious financial recommendation.
- The match is already locked and the user is seeking actionable betting.

## 100 Unit Example Format

Use this compact format for every style:

| 玩法 | 选择项 | 比例 | 100单位示例 |
| --- | --- | ---: | ---: |
| 胜平负 | 胜 | 30% | 30 |
| 让球(-1) | 让平/让负 | 25% | 25 |

If the style has multiple picks under one play, either split the units per pick or state `平均分配`.

## Closing Note

End betting sections with:

`玄学只负责让观赛更有仪式感，资金纪律负责让明天还能舒服地看球。`
