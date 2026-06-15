# Report Template

Use this structure for the final Chinese battle report. Keep it vivid but concise. The prediction core is official kit colour, Qi Men Dun Jia, and incomplete Four Pillars birth-date analysis.

## Opening

Start with:

`以下为娱乐性玄学分析，不构成投注建议或收益承诺。`

Then provide:

- Match name.
- Kickoff time in local time and Beijing time.
- Venue.
- Official home/away order.
- Report phase: `T-24h`, `T-2h`, `T-60min`, `T-15min`, or `post-lock`.
- Data status: verified, inferred, or missing.
- Official lottery odds status: source URL, retrieval time, sale status, or `中国体彩官方赔率暂不可得`.
- Official Sporttery match ID, match number, and `HHAD` handicap line when available.
- Kit colour confidence label.
- Lineup and birth-date coverage.

## 玄学总判

- 胜负倾向.
- 玄学比分主线.
- 总进球倾向.
- 半全场剧本.
- 信心等级.
- Confidence cap reason, if any.

## 事实锚点

Use a compact table:

| 项目 | 主队 | 客队 | 备注 |
| --- | --- | --- | --- |
| 官方球衣颜色 |  |  | confidence label |
| 主教练生日 |  |  | source |
| 阵容状态 |  |  | official lineup, predicted lineup, squad, or missing |
| 关键人生日覆盖 |  |  | covered / target |
| 伤停/状态 |  |  |  |
| 天气/场地 |  |  |  |

## 球衣五行入盘

Explain:

- Official colour source.
- Outfield player colour elements.
- Goalkeeper colour elements.
- How kit elements support or restrain the Qi Men chart.

## 奇门遁甲排盘

Explain:

- Charting standard, source, and whether official local time or true solar time was used.
- 起局方法: 拆补法 / 置闰法 / 茅山法 / source-specific unknown.
- Chart type: 转盘 default, or labelled 飞盘 secondary check.
- Kickoff time used for the chart.
- `体彩结算主客` and `奇门攻防主客` placement convention.
- Parser status: `parsed`, `partial`, `failed`, or external/manual.
- 主客落宫.
- Four-plate judgement: 天盘九星, 地盘九宫, 人盘八门, 神盘八神.
- 旺衰 logic: 九星月令旺衰 and 八门落宫旺衰 separately; do not merge them.
- 门迫/门制, 十干克应, 空亡, 入墓, 击刑, 马星, 伏吟/反吟 if present.
- 空亡 handling: state whether it is true/false空 by month/day fill or冲实, and whether opposite/转宫 palace changes the judgement.
- 利主/利客 posture and how it maps to football tempo: control, press, counterattack, expansion, or stalemate.
- Match-event reading.
- If exact palace placement cannot be verified, title this section `简化奇门象占` and avoid exact palace claims.

## 缺时柱八字

Explain:

- Birth-date sources.
- Which people have verified full dates.
- Which people are missing and excluded.
- Coverage ratio for each team.
- Coach comparison.
- Key player comparison: goalkeeper, captain/defensive leader, creator, striker.
- State clearly: `时柱缺失，因此只作三柱参考`.

Use a table:

| 人员 | 队伍 | 生日 | 三柱/日主 | 与比赛日关系 | 判读 |
| --- | --- | --- | --- | --- | --- |

## 综合评分

Use:

| Module | 主队 | 客队 | Notes |
| --- | ---: | ---: | --- |
| 体彩结算主客落宫 |  |  | palace element, 生克, 空亡, 入墓 |
| 奇门攻防主客势 |  |  | 利主/利客, 阳时/阴时, 伏吟/反吟 |
| 九星天时旺衰 |  |  | month/season strength |
| 八门执行状态 |  |  | door quality, 门迫/门制 |
| 八神波动修正 |  |  | command, hidden danger, cards, chaos |
| 十干克应 / 异常场 |  |  | 克应, 击刑, 入墓, 空亡转宫, 马星 |
| 球衣五行入盘 |  |  | auxiliary |
| 教练缺时柱八字 |  |  |  |
| 球员缺时柱八字 |  |  |  |
| 现实校验 |  |  | lineup, injuries, odds, tactical facts |

After the scorecard, state:

- Raw score difference.
- Confidence gate applied.
- Final confidence label.

## 比分池

Before listing exact scores, state the market-mapping result:

- 信号分桶: 胜负气 / 盘路气 / 门路开闭 / 节奏先后 / 细节成像.
- 共识陷阱: active / inactive, with one reason.
- 扩张触发: active / secondary / inactive.
- 弱方进球类型: 偷一球 / 追平球 / 反超球 / 垃圾时间球 / none.
- 主结构 and 防守结构, selected from `pre-match-market-mapping.md`.
- Top markets: two or three preferred markets; reduced markets and why.

Give three layers:

- 主线比分: 1 to 2 picks.
- 防守比分: 1 to 2 picks.
- 玄学小票: 0 to 2 high-variance picks.

Ensure the score pool matches the total-goal prediction and result lean.

If the exact-score pool would exceed three serious picks, shift coverage to 总进球 instead of adding more fixed scores.

Do not label a fixed score as a "胆" unless the final confidence is `high` and official lineups are available.

## 竞彩策略

Use at least four profiles by default. When the user asks for detailed betting strategy, include all six styles:

| 风格 | 风险 | 适用前提 | 主攻玩法 | 防守玩法 | 适合用户 |
| --- | --- | --- | --- | --- | --- |
| 保守防守型 |  |  |  |  |  |
| 均衡主线型 |  |  |  |  |  |
| 进取比分型 |  |  |  |  |  |
| 半全场剧情型 |  |  |  |  |  |
| 防冷对冲型 |  |  |  |  |  |
| 纯观赛型 |  |  |  |  |  |

Then provide a compact allocation table for each style:

| 玩法 | 选择项 | 比例 | 100单位示例 | 命中逻辑 | 风险点 | 放弃条件 |
| --- | --- | ---: | ---: | --- | --- | --- |

If the user asks for a concrete budget, convert percentages into amounts. Otherwise use percentages and `100单位示例`.

Before the allocation tables, include a compact official-odds and conflict check:

| 检查项 | 结论 |
| --- | --- |
| 中国体彩官方赔率 | available with source / unavailable |
| Sporttery match | match ID, match number, retrieved time |
| 官方让球线 | HHAD goal_line or unavailable |
| 推荐玩法销售状态 | available / partially unavailable / unavailable |
| 主比分 vs 让球 | coherent / conflict fixed |
| 主比分 vs 总进球 | coherent / conflict fixed |
| 弱方进球 vs 防冷比例 | coherent / conflict fixed |
| 是否适用杠铃模型 | yes / no / theoretical only |

If the `60/20/10/10` barbell model is used, show the main-result arithmetic using official odds. If official odds are unavailable, label the table `理论模型` and do not claim cost recovery.

If the report phase is `post-lock`, state that the tables are replay mappings only and not actionable pre-match betting.

Separate this section from the prediction with a sentence like:

`下面是把玄学剧本翻译成娱乐型体彩结构，不等于要求下注。`

## 推翻本判的条件

List concrete reversal/no-play triggers:

- Official lineup changes key-person set.
- Kit changes.
- Venue/time/home-away order changes.
- Injuries, weather, odds, or lottery availability contradicts the prediction.
- Qi Men or bazi module is too incomplete.

## 最终判词

End with a short signing-style paragraph:

- One sentence on the Qi Men verdict.
- One sentence on the likely score path.
- One sentence on how to bet responsibly or choose no-play.
