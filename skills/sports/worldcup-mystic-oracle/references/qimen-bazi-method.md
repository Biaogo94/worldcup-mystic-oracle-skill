# Qi Men and Incomplete Bazi Method

Use this file as the prediction core. Remove unrelated mystical modules unless the user explicitly requests them.

## Data Required

Collect and cite:

- Official home and away order.
- Kickoff date and time in venue local time and Beijing time.
- Venue city and timezone.
- Official or expected kit colours.
- Coaches' full names and birth dates.
- Official lineup when available; otherwise official squad, matchday roster, or clearly labelled predicted lineup.
- Key-person birth dates by default: manager, goalkeeper, captain or defensive leader, primary striker, primary creator or central midfielder, and one likely impact substitute.
- Extra player birth dates only when the official lineup or roster is easy to source.
- Injuries, suspensions, and confirmed absences.

Mark each person as:

- `verified`: date confirmed by an official federation, competition page, club page, or reliable database.
- `secondary`: date from a reputable profile page or encyclopedia.
- `missing`: no reliable full date.

Report birth-date coverage as `covered / target` for each team. The default target is 6 key people per team. If a role is unknown, mark that role missing instead of silently replacing it.

## Qi Men Dun Jia Chart

Use 时家奇门 as the default.

Preferred charting standard:

- 转盘奇门 as the default football-match standard because it preserves continuous match-flow causality.
- Use kickoff time at the venue.
- Use the venue timezone.
- Use official local kickoff time by default. Use true solar time only if the user asks for high-rigor divination; if used, state the longitude correction.
- Determine 阴遁 or 阳遁 by solar term.
- Use 拆补法 by default for modern football because it switches at the actual solar-term boundary and is practical for real-time events. If the calculator uses 置闰法 or 茅山法, state that source standard and do not mix standards inside one report.
- Determine 局数 by the solar term and hour according to the charting source used.
- State whether the chart is 转盘 or 飞盘. Do not combine转盘 and飞盘 symbols unless using飞盘 as a labelled secondary check for伏吟/反吟 or extreme stagnation/shock cases.

Do not fabricate a full chart from memory. Use a reliable Qi Men calculator, library, or reference table and cite the source. If no calculator is available, label the section `简化奇门象占`, list the inputs, and avoid claiming exact palace placements.

Read `qimen-engine.md` before charting. Prefer qfdk/qimen when available:

```bash
node scripts/qimen_qfdk.js --engine-dir ~/.hermes/engines/qfdk-qimen --datetime 2026-06-14T12:00:00-05:00 --location "Houston" --pretty
```

Use the qfdk JSON as the primary structured chart. It supplies palace-level 地盘、天盘、八门、九星、八神、暗干、空亡、马星、值符、值使 fields. After charting, read `qimen-scoring.md` and convert the chart into result qi, handicap qi, goal-channel qi, tempo qi, and score-image qi.

If using saved HTML from a calculator, run:

```bash
python scripts/qimen_parse.py path/to/chart.html --json
```

Use the parsed result only when the parser returns `status: parsed` or `status: partial` with enough palace data for the主队/客队 stems. If it returns `status: failed`, use `简化奇门象占`.

## Four-Plate Judgement Model

Use the four plates as a hierarchy, not as equal keywords:

| Plate | Chinese | Football Meaning | Decision Role |
| --- | --- | --- | --- |
| 天盘 / 九星 | 天时 | macro momentum, match environment, long-range trend, team temperament | sets the background ceiling and long-term flow |
| 地盘 / 九宫 | 地利 | venue, spatial constraint, resource base, home/away settlement frame | defines the field where energy can or cannot work |
| 人盘 / 八门 | 人和 | tactical action, execution route, pressing, chance creation | decides whether the team can execute the script |
| 神盘 / 八神 | 神助 | hidden force, psychology, volatility, sudden intervention | modifies tempo, surprise, black-swan risk |

Priority rule:

- Do not decide a match from one symbol. Require at least two plates to agree for a main lean.
- 九星 gives macro trend; 八门 gives executable football action. If star is strong but door is blocked/受制, lower confidence and prefer conservative totals.
- 八神 can trigger volatility but should not overturn both star and door unless paired with 空亡、击刑、入墓、反吟, or real-world disruption.
- Use 地盘 palace element and season/month strength as the environment that amplifies or limits all other symbols.

## Energy Strength and Abnormal Fields

Before scoring, evaluate each relevant palace with this checklist:

1. 九星旺衰 by month/season:
   - 九星 follows active-release logic: `我生之月为旺`, `同我为相`, `生我为废`, `我克为休`, `克我为囚`.
   - For football, 旺/相 star increases macro momentum and sustained pressure; 囚/废 star lowers consistency even if a lucky chance appears.
2. 八门旺衰 by palace and normal five-element relation:
   - 八门 follows execution logic: `同我为旺`, `生我为相`, `我生为休`, `我克为囚`, `克我为死`.
   - Good doors under pressure are weakened; bad doors under control may not fully erupt.
3. 门迫 / 门制:
   - 门克宫 = `门迫`: subjective action damages the environment; halve that door's positive football effect and watch for internal chaos.
   - 宫克门 = `门受制`: action is suppressed by the environment; lower chance creation or execution quality.
   - Use the dialectic: `吉门受制吉不就，凶门受制凶不起`.
4. 十干克应:
   - 天盘干 = current surface action, motive, visible movement.
   - 地盘干 = underlying cause, legacy constraint, baseline condition.
   - Judge the stem relation only after palace strength; strong palace releases the克应, weak palace may reduce it to noise.
5. Energy distortion fields:
   - 击刑: structural self-damage, cards, tactical breakdown, injury, or sudden collapse. Treat as a major negative unless clearly contained.
   - 入墓: hidden, frozen, delayed, or low-expression energy. For football, maps to sterile possession, slow substitutions, trapped striker, or unclear coach intent.
   - 空亡: not absolute absence; only surface information is visible. Check whether the palace is filled/冲实 by month/day, and inspect the opposite or转宫 palace before declaring failure.
   - 马星: movement, travel, transition, counterattack, late substitution, or timing trigger. Use for tempo and half/full-time script more than final result.
6. 伏吟 / 反吟:
   - 伏吟: stagnation, repetition, low tempo,利主/守势; avoid aggressive handicap unless reality strongly disagrees.
   - 反吟: shock, fast reversal, transition chaos,利客/动势; prefer totals/tempo markets over narrow scores.

## Team Placement

Map the match consistently:

- Official Team A or listed home team = 体彩结算主队.
- Team B or listed away team = 体彩结算客队.
- For neutral World Cup matches, still use official listing order for lottery settlement.
- Prediction 主客 must also consider football posture:
  - 主 = static/defensive/settled side, lower block, home-order baseline, team trying to control risk.
  - 客 = active/attacking/moving side, pressing side, team forced to chase or expand.
  - A listed 主队 can become football 客势 if it must attack; a listed 客队 can become football 主势 if it sits deep and waits.
- 主队取值日干 or 日盘主位, 客队取值时干 or 对宫. If the charting source gives a match-divination convention, follow it and state it.
- Always state both frames: `体彩结算主客` and `奇门攻防主客`. If they differ, explain the difference before giving markets.

Recommended judgement layers:

1. 主客落宫 and strategic posture:
   - Compare palace element, 旺衰, 生克, 空亡, 入墓, 门迫, 击刑.
   - 天盘克地盘、地盘生天盘、反吟: favors 客势, proactive attack, transition, expansion, or away/active side.
   - 地盘克天盘、天盘生地盘、伏吟: favors 主势, patience, defensive control, delayed scoring, or underdog resistance.
   - 阳时 biases movement/客势; 阴时 biases containment/主势 when other signals are tied.
2. 门:
   - 开门: attack opens, early chance, tactical channel.
   - 生门: scoring opportunity, effective substitutions, favorable momentum.
   - 休门: slow tempo, control, low pressing.
   - 杜门: blocked lanes, defensive congestion, low total goals.
   - 景门: highlight shot, VAR, visible pressure.
   - 伤门: hard duels, injuries, cards, risky tackles.
   - 惊门: sudden error, penalty, late chaos.
   - 死门: sterile possession, defensive collapse, poor finishing.
3. 星:
   - 天辅/天心: organization, tactics, calm decision.
   - 天任: stability, holding structure.
   - 天冲/天英: tempo, explosive attacks, cards.
   - 天芮: illness, fatigue, error risk.
   - 天蓬: hidden danger, goalkeeper or defensive uncertainty.
4. 神:
   - 值符: command advantage, coach authority.
   - 六合: combination play, rebounds, chemistry.
   - 九地: defensive block, slow pace.
   - 九天: aerial play, long balls, fast expansion.
   - 白虎: contact, injury, red/yellow cards.
   - 玄武: hidden mistake, deceptive pass, offside/VAR fog.

## Kit Colours in the Chart

Use kit Five Elements as an auxiliary input:

- If the team's kit element generates its palace element or the active seasonal/hour element, mark `得生`.
- If the active seasonal/hour element controls the kit element, mark `受克`.
- If goalkeeper colour is generated by the match palace or protects against the opponent's attacking element, mark defensive support.
- If kit colours and Qi Men chart conflict, Qi Men chart takes priority and kit colours become a tiebreaker.

## Incomplete Four Pillars Birth-Date Analysis

For coaches and players, birth hour is usually unavailable. Use `缺时柱八字`:

- Compute or query 年柱, 月柱, 日柱 only.
- Do not infer 时柱.
- Say clearly: `时柱缺失，因此只作三柱参考`.
- Use solar terms for month-pillar calculation, not lunar calendar months.
- Use a reliable bazi calculator or library for pillars and cite the source if the calculation is not performed locally.

When Python is available, use the helper script:

```bash
python scripts/bazi_three_pillars.py --people people.json
```

Input JSON:

```json
[
  {"name": "Example Player", "team": "主队", "role": "primary striker", "birth_date": "1999-09-21", "source_status": "secondary"}
]
```

Never invent birth dates. If only age or year is known, exclude the person from bazi scoring.

## Bazi Judgement

Apply bazi as a team-strength modifier, not as the sole prediction.

Default key-person weights:

- Head coach: 25%.
- Goalkeeper: 15%.
- Captain or defensive leader: 10%.
- Primary striker: 15%.
- Primary creator or central midfielder: 15%.
- Impact substitute or remaining key starter: 20%.

If coverage is below 4/6 for either team, cap the bazi module at `±0.5`. If coverage is below 3/6, describe bazi qualitatively and do not score it.

Use these checks:

- Day master element of each key person.
- Relationship between person day master and match-day stem/branch.
- Clash, combination, harm, punishment, and break between birth day branch and match day branch.
- Whether the person's dominant element is supported or controlled by the kit element and match-time Qi Men palace.
- Whether the coach's chart supports the team's tactical element.

Football mapping:

- Coach supported: tactical clarity, substitutions work, stable selection.
- Coach clashed: wrong timing, conservative errors, poor adjustment.
- Goalkeeper supported: saves, calm handling, fewer errors.
- Goalkeeper clashed: spill, miscommunication, penalty pressure.
- Striker supported: finishing sharpness, lucky rebound, good timing.
- Striker clashed: offside, hesitation, poor shot selection.
- Midfield supported: passing rhythm, second-ball control.
- Defense clashed: cards, missed mark, late collapse.

## Scoring

Use a compact scorecard. Score only from sourced or parsed data; mark missing pieces as `not scored`.

| Module | 主队 | 客队 | Notes |
| --- | ---: | ---: | --- |
| 体彩结算主客落宫 | -2 to +2 | -2 to +2 | palace element, 生克, 空亡, 入墓 |
| 奇门攻防主客势 | -2 to +2 | -2 to +2 | 利主/利客, 阳时/阴时, 伏吟/反吟 |
| 九星天时旺衰 | -1.5 to +1.5 | -1.5 to +1.5 | month/season strength using 九星 active-release rule |
| 八门执行状态 | -1.5 to +1.5 | -1.5 to +1.5 | door quality, door strength, 门迫/门制 |
| 八神 volatility modifier | -1 to +1 | -1 to +1 | command, hidden danger, cards, chaos, defensive depth |
| 十干克应 / 异常场 | -2 to +2 | -2 to +2 | 克应, 击刑, 入墓, 空亡转宫, 马星 |
| 球衣五行入盘 | -1 to +1 | -1 to +1 | auxiliary only |
| 教练缺时柱八字 | -1 to +1 | -1 to +1 | modifier only |
| 球员缺时柱八字 | -2 to +2 | -2 to +2 | modifier only; cap by coverage |
| 现实校验 | -2 to +2 | -2 to +2 | lineup, injuries, odds, tactical facts |

Interpretation:

- Difference 4.0 or more: strong lean, but still apply confidence gates.
- Difference 2.0 to 3.9: medium lean.
- Difference below 2.0: low lean, draw-heavy, or market-specific lean only.
- If one side has strong score but the key palace is 空亡/入墓/击刑, reduce one confidence tier unless the转宫/opposite palace clearly resolves it.
- If only one plate supports a side while other plates are neutral or opposed, do not call a strong lean.

After scoring, apply confidence gates from `references/prematch-data-status.md`. Confidence gates can lower the final confidence but cannot raise it.

## Convert to Football Markets

Read `references/pre-match-market-mapping.md` before this conversion. Convert in this order: result → handicap → total goals → half/full tempo → exact score.

- Strong 主队 lean with 生门/开门 and expansion trigger active: 胜, 让胜 or 让胜/让平, totals 3/4/5, scores 2:0/3:1/4:1 plus a small 5+/胜其它 tail only if supported.
- Strong 主队 lean without expansion trigger: 胜, 让平/让负 or 让平, totals 2/3, scores 1:0/2:1.
- Medium 主队 lean: 胜防平, 让平/让负, totals 2/3, scores 1:0/2:1/1:1.
- Draw-heavy 杜门/休门: 平, totals 0/1/2, scores 0:0/1:1.
- 客队 lean with 惊门/玄武: 负 or 平负 script, scores 0:1/1:2.
- 白虎/伤门 strong: cards/injury warning, avoid overconfident exact scores; prefer total goals or no-play if chaos is high.
- 景门/天英 strong: consider totals 3/4/5 and one highlight-score pick; if favorite domination also exists, run the blowout-tail check.

Always state the uncertainty created by missing lineups, missing birth dates, simplified charting, or unavailable lottery branches.

## Reversal Check

Before finalizing, list the specific facts that would change the call:

- Official lineup differs from the key-person set.
- Kit designation changes or the team posts a different matchday kit.
- Kickoff time, venue timezone, or official home/away order changes.
- Qi Men parse is partial and the missing palace includes the home or away stem.
- Birth-date coverage is low or depends on predicted players.
