# Report Template

Use this structure for the final Chinese battle report. Keep it vivid but concise. The prediction core is official kit colour, Qi Men Dun Jia, and incomplete Four Pillars birth-date analysis.

## Readability Contract

- Use neutral professional Chinese. Do not address the user with nicknames, roleplay titles, or filler.
- Prefer compact tables over repeated loose bullets.
- Do not output empty labels such as `风格:` or `风险:` with no value.
- Do not list multiple betting styles by default. The betting section must contain exactly one primary strategy table unless the user explicitly asks for alternatives.
- If official data cannot be fetched, show the attempted source and one clear consequence: confidence cap, no-play, or theoretical-only. Do not pad with unverified details.

## Opening

Start with:

`以下为娱乐性玄学分析，不构成投注建议或收益承诺。`

Then provide:

Use this compact table:

| 项目 | 结论 |
| --- | --- |
| 比赛 |  |
| 体彩结算主客 | 主队 / 客队 |
| 开球 | local time / Beijing time |
| 场地 |  |
| 当前阶段 | `early` / `prelineup` / `late` / `lineup` / `final-check` / `post-lock` |
| 赛程来源 |  |
| 中国体彩官方赔率 | source URL + retrieval time + status, or unavailable |
| Sporttery 信息 | match ID / match number / HHAD goal_line / sale status |
| 球衣与阵容 | kit confidence + lineup status |
| 八字覆盖 | home covered/target; away covered/target |

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

If a key fact is missing, add a short `数据缺口` table:

| 缺口 | 影响 | 处理 |
| --- | --- | --- |
| 官方球衣未确认 | 球衣五行不入重分 | 降权为叙事 |
| 官方赔率不可得 | 不做可执行下注表 | 输出不下注或理论模型 |

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
- Input calendar: public coach/player profile birth dates are treated as Gregorian dates unless the source explicitly says lunar.
- Conversion basis: Gregorian date -> bazi/eight-character pillars; month pillar uses solar terms, not lunar calendar month.
- Source status for each birth date: `verified`, `secondary`, or `missing`.
- Which people have verified full dates.
- Which people are missing and excluded.
- Coverage ratio for each team.
- Coach comparison.
- Key player comparison by role: goalkeeper, captain/defensive leader, creator or central midfielder, striker, impact substitute or remaining key starter.
- Role-weighted bazi score and whether each row was `scored` or `computed but unscored`.
- State clearly: `时柱缺失，因此只作三柱参考`.
- Missing-hour handling: `奇门为主、年命优先、时干补果、月令定气候、六字作结构过滤`.
- Month-command climate: report the birth month branch's cold/heat/dry/damp tendency and possible病药 hint, but do not call it definitive喜用神.
- Six-character structure: use `six_character_profile` to summarize hidden stems, weighted five-element tendency, ten-god role fit, and 盖头/截脚. Do not call it complete格局.
- Event timing: use `event_resonance` to summarize 流年/流月/比赛日共振. Do not call it 大运.

Use a table:

| 角色 | 人员 | 队伍 | 生日来源 | 三柱/年命/日主 | 六字结构 | 月令/十神角色适配 | 流年流月比赛日共振 | 权重/状态 | 判读 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

After the table, state:

- Calendar audit: whether all computed rows used public Gregorian dates and whether any row is near a midnight or solar-term boundary that lowers confidence.
- Team bazi coverage and scored coverage.
- Coach edge.
- Goalkeeper risk.
- Midfield/creator edge.
- Striker finishing edge.
- How the role bazi changes the score pool or handicap strategy.
- What was deliberately not used: exact时柱, complete喜用神, exact大运, or permanent fate judgement.

If most dates are computed from unsourced or unverified inputs, say `八字只作叙事，不进入下注权重`.

## 奇门×八字叠盘

Explain:

- Overlay status: `parsed`, `partial`, or `qualitative-only`.
- Missing-hour protocol: `奇门为主、年命优先、时干补果、月令只作气候偏好`.
- Person anchors used: 年命天干 as primary, 八字日主 as secondary, 生日支 as clash/combine filter, 月令气候 as rough病药 hint.
- Event anchors used: 时干 as result-path anchor, role-specific symbol, and match-day pillar.
- Whether full喜用神 or大运 is available. If not, state `喜忌未完整判定；大运不作断语；仅使用流年/流月/比赛日共振`.

Use a compact table:

| 角色 | 人员 | 年命/日主/月令 | 年命宫 | 时干/事宫/用神 | 年命宫vs事宫 | 日主/日支过滤 | 十神/盖头截脚 | 流年流月比赛日 | 叠盘判读 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 主教练 |  |  | parsed/partial | 时干 + 值符/天辅/天心 | 事生人/人克事/etc. | 喜忌未完整判定 |  |  |
| 门将 |  |  | parsed/partial | 时干 + 天蓬/天芮/玄武 |  |  |  |  |
| 前锋 |  |  | parsed/partial | 时干 + 生门/景门/九天 |  |  |  |  |

After the table, state:

- Which specific person can carry the Qi Men script.
- Which role is drained or pressured by the event field.
- How the overlay changes markets: result, handicap, total goals, score tail, or no change.
- Confidence cap caused by missing birth hour, missing palace location, or missing full-bazi喜用神.

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
| 奇门×八字叠盘 |  |  | 年命宫 vs 时干/事宫 primary; 日主/月令/流年 low-weight filters |
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
- 直觉叠加: first impression / omen / qimen image used, affected scenarios, and max boost. If unused, state `未使用，避免主观加码`.

Give three layers:

- 主线比分: 1 to 2 picks.
- 防守比分: 1 to 2 picks.
- 玄学小票: 0 to 2 high-variance picks.

Ensure the score pool matches the total-goal prediction and result lean.

If the exact-score pool would exceed three serious picks, shift coverage to 总进球 instead of adding more fixed scores.

Do not label a fixed score as a "胆" unless the final confidence is `high` and official lineups are available.

If `intuition_boost` is used, show one compact line after the score pool:

`直觉叠加：第一念=...；外应=...；加权=0:2 +10%, 0:3 +20%；上限=25%；仅影响场景权重，不覆盖事实与赔率。`

## 竞彩策略

Use exactly one primary strategy by default. Do not present several styles unless the user explicitly asks for alternatives. The primary strategy should be an integrated advance-retreat structure when official odds are available: main recovery branch, attack branch, and protect branch.

Do not promise guaranteed收益. If the odds cannot cover the total exposure under the main branch, say `主线不能覆盖总成本`.

If the user asks for a concrete budget, convert percentages into executable amounts. Otherwise use a `100元示例`. China Sports Lottery stakes must be `2元` multiples; show `金额(元)` and `注数(2元/注)`.

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
| 收益目标 | balanced / upside; if upside, state `条件收益上行优先，非保证盈利` |
| 直觉权重 | unused / used, max boost, affected scores |

If the `60/20/10/10` barbell model is used, show the main-result arithmetic using official odds. If official odds are unavailable, label the table `理论模型` and do not claim cost recovery.

If `scripts/optimize_strategy.py` is used, state the scenario file or scenario weights in one compact line and use the optimizer's scenario-return table after sanity-checking it against the declared score pool.

Do not use the same pool's full three-result cover as the default strategy. If the optimizer or manual plan selects all three `HAD` or all three `HHAD` outcomes, explain why this is exceptional; otherwise reduce it to the coherent one or two branches.

If the report phase is `post-lock`, state that the tables are replay mappings only and not actionable pre-match betting.

Separate this section from the prediction with a sentence like:

`下面是把玄学剧本翻译成娱乐型体彩结构，不等于要求下注。`

Then provide the primary strategy table:

| 项目 | 内容 |
| --- | --- |
| 主推策略 | 不下注 / 进退综合 / 单锚 |
| 设计目标 | 主线条件回收 + 进攻增益 + 退守保护 |
| 官方赔率校验 | match ID, match number, sale status, HHAD line |
| 主线回收能力 | `金额 × 赔率 = 返还`; state whether it covers total exposure |
| 最佳情形 | highest branch conditional return |
| 最大风险 | one concrete losing path |
| 放弃条件 | concrete pre-kickoff trigger |

Then provide one branch allocation table:

| 分支 | 玩法 | 选择 | 赔率 | 比例 | 金额(元) | 注数(2元/注) | 条件返还 | 净值 | 作用 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 主线回收 |  |  |  |  |  |  |  |  |  |
| 进攻增益 |  |  |  |  |  |  |  |  |  |
| 退守保护 |  |  |  |  |  |  |  |  |  |
| 右端尾部 | 总进球 / 比分 |  |  |  |  |  |  |  | 捕捉极端大比分 |
| 左端尾部 | 比分 / 总进球 |  |  |  |  |  |  |  | 防极端冷门 |

Then provide the combined scenario return table whenever `HAD` and `HHAD` can both hit:

| 情景 | 命中分支 | 条件返还 | 100元净值 | 判读 |
| --- | --- | ---: | ---: | --- |
| 客胜2+ / 主胜2+ / etc. |  |  |  |  |
| 客胜1 / 主胜1 / etc. |  |  |  |  |
| 平局或冷门 |  |  |  |  |

Then add a tail-source note:

`总进球/比分尾部：已取得官方明细赔率并参与计算 / 官方明细赔率待确认，暂不分配资金。`

When fixed-bonus history is used for `TTG/CRS/HAFU`, use:

`总进球/比分/半全场明细来自体彩固定奖金历史接口，需以临场终端销售状态为准。`

After the table, add one line:

`为什么不选其它玩法：...`

Do not list six styles unless the user explicitly asks.
Do not output partial loose rows such as `25` followed by empty `风格` or `风险`; every allocation must live inside the single table.

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
