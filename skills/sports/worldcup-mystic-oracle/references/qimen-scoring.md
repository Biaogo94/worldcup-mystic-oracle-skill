# Qi Men Scoring

Use this file after obtaining a Qi Men chart. It turns the chart from narrative symbols into a constrained scoring model.

The model is entertainment-only. It can support market prioritization, but not guaranteed betting decisions.

## Use-God Anchors

Do not rely on one anchor only. Use at least two anchors for each team when data permits.

| Role | Primary Anchor | Secondary Anchors | Notes |
| --- | --- | --- | --- |
| 主队 | 日干 | official Team A palace, team-name element, kit element | if anchors conflict, cap confidence at `medium` |
| 客队 | 时干 | opposing palace, team-name element, kit element | if anchors conflict, cap confidence at `medium` |
| 主帅 | 值符 | 天辅, 天心, coach bazi | affects result qi and tempo qi |
| 门将 | 天蓬/天芮 | 死门, 玄武, goalkeeper bazi, GK kit element | affects clean sheet, error, and weak-side scoring |
| 进攻通道 | 开门/生门/景门 | 天英, 天冲, 九天 | affects goal-channel qi and handicap qi |
| 防守通道 | 杜门/死门/休门 | 九地, 天任 | affects low goals, blocks, and draw tendency |
| 事故通道 | 伤门/惊门 | 白虎, 玄武, 腾蛇 | affects cards, penalty, VAR, sudden goal |

If only one anchor is available, use `简化奇门象占` and do not produce a high-confidence handicap strategy.

## Palace Scoring

Score each team palace and key functional palace using the same rows:

| Item | Range | Positive Signals | Negative Signals |
| --- | ---: | --- | --- |
| 落宫旺衰 | -2 to +2 | season/hour supports palace or stem | season/hour controls palace or stem |
| 门吉凶 | -2 to +2 | 开, 生, 景 for attack; 休 for control | 死, 惊, 伤; 杜 when chasing goals |
| 星象功能 | -1 to +1 | 天辅, 天心, 天任, 天英/天冲 for attack | 天芮, 天蓬 when linked to GK/defense |
| 神煞风险 | -1 to +1 | 值符, 六合, 九天, 九地 when role-appropriate | 白虎, 玄武, 腾蛇, 勾陈 when causing delay/error |
| 生克关系 | -2 to +2 | team anchor generates/controls opponent constructively | team anchor is controlled, drained, or trapped |
| 特殊格局 | -2 to 0 | none | 空亡, 入墓, 门迫, 击刑, 反吟, 伏吟 if confirmed |

If the chart source or parser cannot confirm a row, mark it `unknown` and do not score that row.

## Door/Star/Deity Market Mapping

| Signal | Primary Market | Secondary Market | Caution |
| --- | --- | --- | --- |
| 开门 | total goals, result qi | handicap | good for chances; not always goals if star/deity weak |
| 生门 | scoring, substitutions | handicap | strong with 值符/六合/九天 |
| 景门 | visible pressure, VAR, highlight | totals, score image | can mean spectacle rather than dominance |
| 休门 | control, slow tempo | half/full draw at HT | supports low tempo unless attack stars override |
| 杜门 | blocked lanes | low totals | bad if favorite needs expansion |
| 死门 | sterile attack, collapse | underdog scoring against weak defense | severe for team attack if it is the team's anchor |
| 伤门 | cards, injury, aggressive duels | chaos totals | do not overtrust exact scores |
| 惊门 | sudden mistake, penalty, VAR | weak-side goal | not automatically upset |
| 天辅/天心 | organization | coach support | favors structured teams |
| 天任 | stability | defense/control | favors holding a lead |
| 天英/天冲 | speed and explosions | totals/handicap | can also create cards |
| 天芮/天蓬 | illness/error/GK hidden risk | both teams to score | use carefully with goalkeeper anchor |
| 值符 | command | result qi, coach | strongest when on favorite or coach anchor |
| 六合 | chemistry/rebounds | scoring | helps combination play |
| 九天 | expansion/aerial/direct play | handicap | raises blowout chance |
| 九地 | block/low tempo | totals | supports defending, not chasing |
| 白虎 | contact/injury/cards | chaos | avoid heavy exact score |
| 玄武/腾蛇 | hidden error/VAR/fog | weak-side goal | classify before altering result |

## Match-Level Qi Men Output

Every final report should summarize:

- Team anchor method: e.g. `主队=日干+球衣五行`, `客队=时干+对宫`.
- Team palace scores, with unknown rows excluded.
- Functional signals:
  - result qi.
  - handicap qi.
  - goal-channel qi.
  - tempo qi.
  - image qi.
- Confidence cap:
  - `high` only if at least two anchors per team agree and key palace rows are known.
  - `medium` if anchors are partial or parser lacks special-pattern rows.
  - `low-medium` if only simplified charting is available.
  - `low` if kickoff time, timezone, or team placement is uncertain.

## Strategy Support Rule

Qi Men can support:

- preferred result direction;
- preferred market ordering;
- score structure;
- whether to raise or lower handicap aggression.

Qi Men alone cannot support:

- all-in staking;
- exact unit size;
- guaranteed score;
- high-confidence handicap when special-pattern rows are unknown.

Always combine Qi Men with reality checks, kit colour, bazi role modifiers, official Sporttery odds, and `pre-match-market-mapping.md`.

## Qi Men + Bazi Overlay Scoring

Use this only after `qimen-bazi-overlay.md` is read and the parsed chart can locate person/event anchors.

| Overlay Row | Range | Positive | Negative |
| --- | ---: | --- | --- |
| 人宫状态 | -1 to +1 | 年命/日主落旺宫, 吉门吉星扶身 | 空亡, 入墓, 受制, 凶门凶神压身 |
| 事宫状态 | -1 to +1 | 角色用神得门星神支持 | 角色用神受克, 门迫, 击刑 |
| 人事生克 | -2 to +2 | 事生人, 人克事, 比和 | 人生事, 事克人 |
| 角色专属用神 | -1 to +1 | coach/GK/striker/etc. symbol supports person | role symbol clashes or drains person |
| 八字过滤 | -1 to +1 | 日主/日支与比赛日形成 support/combine | clash, harm, punishment, repeated忌象 |
| 流年/比赛日共振 | -0.5 to +0.5 | low-weight positive resonance | low-weight negative resonance |

Cap rules:

- If birth hour is missing, overlay contribution cannot exceed `medium` confidence.
- If no full-bazi喜用神 is available, write `喜忌未完整判定` and do not use喜忌 as a decisive score.
- If大运 is not computed from a cited full chart, do not claim macro luck quality.
- If person/event palaces are unknown, overlay is qualitative and cannot alter betting strategy by itself.

Market impact:

- Coach overlay changes tactical clarity and half/full-time confidence.
- Goalkeeper overlay changes clean-sheet, weak-side-goal, and exact-score risk.
- Striker overlay changes finishing, handicap, and right-tail probability.
- Midfield overlay changes tempo and total-goals band.
- Defender overlay changes cards, set-piece risk, and late-collapse probability.
