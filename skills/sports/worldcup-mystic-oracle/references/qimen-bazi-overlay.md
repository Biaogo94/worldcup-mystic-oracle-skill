# Qi Men + Bazi Overlay

Use this file when combining Qi Men Dun Jia with coaches' and key players' incomplete bazi. The overlay answers: `这场比赛/这个时间点对这个具体人是否有利`.

Keep this module confidence-limited. Public football data usually lacks birth hour, birthplace, and current luck-cycle details, so use three-pillar bazi as a filter, not as a standalone fate judgement.

## Anchor Selection

For each key person, define person anchors:

| Anchor | Source | Meaning | Use |
| --- | --- | --- | --- |
| 年命 | birth `year_ming_stem` | personal root qi carried into the event | preferred Qi Men personal marker |
| 八字日主 | birth `day_master` | subjective will, ability, and personal capacity | deep bazi-person marker |
| 生日支 | birth `day_branch` | body/field contact point | clash, combination, harm, punishment against match day |

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

## Bazi Preference Filter

Full喜用神 requires serious birth-time and season analysis. For this skill:

- If exact birth time is missing, do not claim a definitive喜用神.
- Use day-master relation, season/month pillar, and match-day relation as `provisional element tendency`.
- Say `喜忌未完整判定` unless the user supplies a reliable full bazi or you cite a reliable full-bazi calculator.

Practical filter:

- If event palace element supports the person's likely useful element, raise that role's confidence slightly.
- If event palace element looks like a likely忌神 or repeats a known clash, lower that role's confidence.
- If bazi and Qi Men disagree, Qi Men decides the event path; bazi decides whether this person can carry that path.

## Luck-Cycle Filter

大运 is unavailable from public date-only profiles because birth time and full bazi are missing.

Allowed:

- Compare match year pillar and match day pillar with the person's year/day pillars.
- Flag strong clashes, harms, punishments, combinations, or repeated elements.
- Use as a low-weight macro filter.

Not allowed:

- Claim precise大运 quality without full bazi and a cited calculator.
- Say a player is in a certain ten-year luck cycle from birthday alone.

## Overlay Scoring

Use this compact row for each scored person:

| Item | Range | Rule |
| --- | ---: | --- |
| 年命/日主落宫 | -1 to +1 | palace strength and person-event relation |
| 事宫对人宫 | -2 to +2 | 事生人 / 人克事 / 比和 / 人生事 / 事克人 |
| 角色专属用神 | -1 to +1 | whether role symbol supports that person |
| 八字日主/日支过滤 | -1 to +1 | day-master element and day-branch relation to match day |
| 流年/比赛日共振 | -0.5 to +0.5 | low-weight only |
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
