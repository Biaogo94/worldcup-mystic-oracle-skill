# Qi Men + Bazi Overlay

Use this file when combining Qi Men Dun Jia with coaches' and key players' incomplete bazi. The overlay answers: `这场比赛/这个时间点对这个具体人是否有利`.

Keep this module confidence-limited. Public football data usually lacks birth hour, birthplace, and current luck-cycle details, so use three-pillar bazi as a filter, not as a standalone fate judgement.

## Missing-Hour Protocol

When only 年/月/日 are known, change the analysis priority:

1. **Qi Men first, bazi second.** Qi Men is the event field for the exact kickoff. Bazi only personalizes who can carry or suffer that field.
2. **Raise 年命 weight.** `year_ming_stem` is the most stable person anchor. Prefer it over a speculative day-master旺衰 judgement.
3. **Use Qi Men 时干 as the event "result" substitute.** The missing bazi hour pillar is not guessed. Instead, use the Qi Men hour stem/event palace to represent the matter's future tendency and final route.
4. **Use 月令 to set climate, not final喜忌.** The birth month branch gives cold/heat/dry/damp bias and possible medicine hints, but not a definitive喜用神 without full four pillars.
5. **Use Qi Men reverse calibration cautiously.** If the person's palace is severely empty, trapped, dead-door, or struck, infer current low-state for this event only. Do not turn that into a permanent natal judgement.

Missing-hour priority order:

```text
Qi Men event chart -> 年命落宫 -> 时干/事宫 -> 年命与事宫生克
-> 月令气候偏好 -> 日主/日支 filters -> low-weight流年共振
```

This replaces any attempt to force exact full-bazi喜忌 from three pillars.

## Anchor Selection

For each key person, define person anchors:

| Anchor | Source | Meaning | Use |
| --- | --- | --- | --- |
| 年命 | birth `year_ming_stem` | personal root qi carried into the event | primary marker when hour is missing |
| 八字日主 | birth `day_master` | subjective will, ability, and personal capacity | secondary marker; do not overrule年命 when旺衰 is uncertain |
| 生日支 | birth `day_branch` | body/field contact point | clash, combination, harm, punishment against match day |
| 月令气候 | birth `month_command_climate` | cold/heat/dry/damp tendency | rough病药 clue only |
| 六字结构 | birth `six_character_profile` | hidden stems, ten gods, month-state, internal stem-branch pressure | role-fit filter only; no full格局 |

For the event, define event anchors:

| Anchor | Source | Meaning | Use |
| --- | --- | --- | --- |
| 时干 | Qi Men match hour stem | the concrete match event and result path | main event marker |
| 专属用神 | role-specific palace/symbol | football function | role judgement |
| 比赛日干支 | match local date bazi | day-level field | bazi relationship filter |

Role-specific event anchors:

| Role | Event Symbol |
| --- | --- |
| Coach | 值符, 天辅, 天心, 开门 |
| Goalkeeper | 天蓬, 天芮, 死门, 玄武 |
| Defender/captain | 杜门, 九地, 天任 |
| Creator/midfield | 开门, 六合, 天辅 |
| Striker | 生门, 景门, 九天 |
| Impact substitute | 马星, 生门, 值使门 |

## Person Palace vs Event Palace

After the Qi Men chart is parsed, locate:

- the palace containing the person's `year_ming_stem` if available;
- the palace containing the person's `day_master` if available;
- the event palace containing `时干` or the role-specific event symbol.

If the chart cannot locate a stem or role symbol, mark `overlay_status: partial` and do not score that row.

Judge palace element relation:

| Relation | Meaning | Football Interpretation |
| --- | --- | --- |
| 事生人 | event palace generates person palace | role receives the match, confidence rises |
| 人克事 | person palace controls event palace | can succeed through effort; laborious but usable |
| 比和 | same element | stable, smooth, moderate positive |
| 人生事 | person palace generates event palace | person is drained by the role/task |
| 事克人 | event palace controls person palace | role is under pressure; major error or low output risk |

Use this as a direction filter, not an automatic result pick.

When birth hour is missing, judge `年命宫 vs 时干/事宫` first. Use `日主宫 vs 事宫` only as a secondary confirmation or contradiction.

## Bazi Preference Filter

Full喜用神 requires serious birth-time and season analysis. For this skill:

- If exact birth time is missing, do not claim a definitive喜用神.
- Use day-master relation, season/month pillar, and match-day relation as `provisional element tendency`.
- Use `month_command_climate` from the bazi helper to describe `月令气候偏好`, such as winter cold needing fire as a possible medicine hint.
- Use `day_master_month_state` only as rough 得令/失令 signal. It cannot decide旺衰 without the hour pillar and full root analysis.
- Use `ten_god_profile` by role:
  - coach: 官印 and command-support symbols;
  - goalkeeper/defense: 官印 stability vs 伤官/劫财 error risk;
  - striker: 食伤/财星 output vs 枭印压制;
  - creator/midfield: 食伤 creativity balanced by 印星;
  - substitute: 伤官/七杀/偏财 volatility only when Qi Men also shows movement.
- Use `pillar_internal_status` to flag 盖头/截脚 as energy friction. Do not turn it into permanent fate judgement.
- Say `喜忌未完整判定` unless the user supplies a reliable full bazi or you cite a reliable full-bazi calculator.

Practical filter:

- If event palace element supports the person's likely useful element, raise that role's confidence slightly.
- If event palace element looks like a likely忌神 or repeats a known clash, lower that role's confidence.
- If bazi and Qi Men disagree, Qi Men decides the event path; bazi decides whether this person can carry that path.

## Luck-Cycle Filter

大运 is unavailable from public date-only profiles because birth time and full bazi are missing.

Allowed:

- Compare match year pillar, match month pillar, and match day pillar with the person's year/month/day pillars.
- Compare current流年/流月/比赛日 with the person's year/month/day pillars for obvious 天克地冲, 合冲刑害, repeated same element, or event-stem support/pressure.
- Flag strong clashes, harms, punishments, combinations, or repeated elements.
- Use as a low-weight macro filter.
- Use the script's `event_resonance` field when available.

Not allowed:

- Claim precise大运 quality without full bazi and a cited calculator.
- Say a player is in a certain ten-year luck cycle from birthday alone.
- Use `岁运并临` language unless a real 大运 is known. With public dates, say `流年/流月/比赛日重复共振` instead.

## Qi Men Reverse Calibration

Use reverse calibration only as event-state evidence:

- If 年命宫 is empty, tombed, struck, under死门, or heavily controlled, mark the person as low-state for this match.
- If 年命宫 receives 时干/事宫 support and has usable door/star/deity, mark the person as able to receive the event.
- If the person's month-climate hint is answered by the event palace element, raise confidence slightly. Example: cold winter chart with event palace fire can be a medicine-like support.
- If the event palace worsens the obvious month-climate problem, lower confidence slightly.

Do not say this proves the person's permanent喜忌. Phrase it as `本场奇门反推：...`.

## Overlay Scoring

Use this compact row for each scored person:

| Item | Range | Rule |
| --- | ---: | --- |
| 年命/日主落宫 | -1 to +1 | palace strength and person-event relation |
| 年命宫 vs 事宫 | -2 to +2 | primary when hour is missing; 事生人 / 人克事 / 比和 / 人生事 / 事克人 |
| 日主宫 vs 事宫 | -1 to +1 | secondary confirmation only |
| 角色专属用神 | -1 to +1 | whether role symbol supports that person |
| 月令气候/日主月令状态 | -0.5 to +0.5 | rough climate and 得令/失令 hint; not full喜忌 |
| 十神角色适配 | -0.5 to +0.5 | role-ten-god fit from six-character profile; low-weight only |
| 盖头截脚/藏干结构 | -0.5 to +0.5 | structural friction or hidden support; narration/filter only |
| 八字日主/日支过滤 | -1 to +1 | day-master element and day-branch relation to match day |
| 流年/流月/比赛日共振 | -0.5 to +0.5 | low-weight only; use `event_resonance` |
| 数据置信 | multiplier | official 1.0, reputable-secondary 0.85, secondary 0.75, missing 0 |

Cap rules:

- missing birth date: no score;
- no Qi Men palace location: qualitative only;
- birth date coverage below 4/6 for a team: team overlay cap `low-medium`;
- no birth hour: never exceed `medium` from bazi overlay alone;
- no大运: do not use macro-luck claims for betting aggression.

## Report Language

Use precise wording:

- Good: `乌拉圭门将年命/日主与门将用神形成事生人，门将稳定性上调。`
- Good: `沙特前锋人生事，进攻责任消耗本人，射门效率不宜高估。`
- Bad: `此人八字大吉，必进球。`
- Bad: `大运极佳` without full bazi and cited calculation.

Final integration:

- Qi Men decides match-event structure.
- Bazi overlay decides which coach/player can carry or fail that structure.
- Reality and official odds decide whether the symbolic structure is actionable.
