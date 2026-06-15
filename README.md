# Hermes 世界杯玄学预测 Skill

这是一个面向 Hermes Agent / Codex 兼容 Agent 的中文娱乐型足球赛前分析 Skill，用来生成「赛前玄学战报」。

它会把赛前事实数据、球衣颜色、奇门遁甲排盘、教练与关键球员的缺时柱八字，以及中国体育彩票玩法映射到一份可读的赛前报告中。所有内容都只用于娱乐分析，不构成投注建议、收益承诺或确定性预测。

## 主要能力

- 生成中文「赛前玄学战报」。
- 查询并标注赛前数据阶段：`T-24h`、`T-2h`、`T-60min`、`T-15min`、`post-lock`。
- 按官方或可信来源确认主客队、开赛时间、场地、阵容、伤停、球衣颜色。
- 使用奇门遁甲时家盘进行主客攻防、门星神、空亡、入墓、击刑、马星等象意判断。
- 对主教练与关键球员做缺时柱八字分析，只使用年柱、月柱、日柱，不推断未知时柱。
- 使用中国体育彩票官方接口获取竞彩足球赔率与销售状态。
- 将玄学剧本转换为一个默认的高命中优先投注结构，覆盖胜平负、让球胜平负、比分、总进球、半全场等玩法。
- 内置放弃条件、信心上限、资金比例和责任彩票提示。

## 目录结构

```text
skills/
  sports/
    worldcup-mystic-oracle/
      SKILL.md
      references/
      scripts/
      agents/
```

核心入口是：

```text
skills/sports/worldcup-mystic-oracle/SKILL.md
```

## 安装方式

把 Skill 目录复制到 Hermes Agent 的 skills 目录中：

```bash
mkdir -p ~/.hermes/skills/sports
cp -R skills/sports/worldcup-mystic-oracle ~/.hermes/skills/sports/
```

如果你的 Hermes Agent 支持从自定义仓库路径加载 skills，也可以直接把本仓库作为外部 skills 目录使用。

## 推荐使用方式

在 Agent 中提出类似请求：

```text
使用 worldcup-mystic-oracle，预测 德国 vs 库拉索，并给出中国体彩策略。
```

默认输出会包含：

- 娱乐性免责声明。
- 数据阶段与事实锚点。
- 球衣五行入盘。
- 奇门遁甲排盘分析。
- 主教练与关键球员缺时柱八字。
- 综合评分与比分池。
- 一个默认的主投注策略。
- 放弃条件与责任彩票提示。

默认不会输出多种投注风格菜单。除非你明确要求多个方案，否则 Skill 只给一个胜率优先、可读性优先的主策略。

如果你只想要预测，不想看到多种投注风格，可以直接说：

```text
只给我一个胜率优先的策略。
```

## 中国体育彩票官方赔率

Skill 内置脚本会优先使用中国体育彩票 / Sporttery 官方接口，不把第三方博彩公司、媒体赔率或 Polymarket 当作官方体彩赔率。

常用命令：

```bash
python skills/sports/worldcup-mystic-oracle/scripts/fetch_sporttery_odds.py \
  --team "德国" \
  --output data/sporttery_odds_cache.json \
  --pretty \
  --utf8
```

脚本会尝试获取：

- 竞彩足球赛程与当前赔率。
- 胜平负 `HAD`。
- 让球胜平负 `HHAD`。
- 官方 match ID、比赛编号、停售状态和更新时间。
- 单场固定奖金历史数据。

如果官方接口没有对应比赛或玩法停售，报告必须标注为不可用，不能用第三方赔率冒充官方赔率。

注意：让球胜平负必须读取官方 `HHAD.goal_line`，并且从体彩主队视角解释。例如 `+1.00` 代表主队受让一球，不能凭实力强弱假设成 `-1`。

## 缺时柱八字口径

公开球员和教练生日默认按公历日期输入，除非来源明确标注为农历。

八字计算口径是：

```text
公开公历生日 -> Solar.fromYmdHms(...) -> getLunar().getEightChar()
```

注意：

- 只知道生日时，只能确定年柱、月柱、日柱。
- 不知道出生时辰时，不推断时柱。
- 月柱按节气体系计算，不按农历月份直接排。
- 脚本中的 `12:00` 只是日期占位，不能当作真实时柱。
- 如果生日接近午夜、节气切换点，或缺少出生地/时区，战报应降低八字信心。

可用脚本：

```bash
python skills/sports/worldcup-mystic-oracle/scripts/bazi_three_pillars.py \
  --people people.json \
  --match-date 2026-06-15 \
  --pretty \
  --utf8
```

## 奇门遁甲排盘

Skill 优先使用结构化排盘引擎，例如 `qfdk/qimen`。如果本地没有可用引擎，可以降级为外部排盘结果或简化象占，但必须在战报里标注来源与解析状态。

推荐脚本：

```bash
node skills/sports/worldcup-mystic-oracle/scripts/qimen_qfdk.js \
  --engine-dir ~/.hermes/engines/qfdk-qimen \
  --datetime 2026-06-14T12:00:00-05:00 \
  --location "Houston" \
  --pretty
```

奇门部分会重点区分：

- 体彩结算主客与奇门攻防主客。
- 天盘九星、地盘九宫、人盘八门、神盘八神。
- 九星旺衰与八门旺衰。
- 门迫、门制、十干克应。
- 空亡、入墓、击刑、马星、伏吟、反吟。
- 这些信号如何映射到胜平负、让球、总进球、比分和半全场。

## 主策略生成

默认不再输出很多投注风格让用户选择，而是综合信号生成一个主策略。目标是优先提高命中率和可执行性，而不是追求最高赔率。

可用脚本：

```bash
python skills/sports/worldcup-mystic-oracle/scripts/primary_bet_strategy.py \
  --odds-cache data/sporttery_odds_cache.json \
  --candidates HAD:胜:1 \
  --mode single \
  --pretty \
  --utf8
```

输出应包含：

- 推荐玩法与选项。
- 官方赔率状态。
- 资金比例。
- `100单位示例`。
- 为什么不选其他玩法。
- 放弃条件。

## 依赖

Python 侧可选依赖：

```bash
python -m pip install lunar-python requests
```

Node 侧如果使用 `qfdk/qimen`，需要本地准备对应排盘项目，并将路径传给 `qimen_qfdk.js`。

## 安全边界

本项目只做娱乐型玄学分析：

- 不保证命中。
- 不承诺收益。
- 不提供投资建议。
- 不建议倍投、借钱投注、追损或重仓。
- 低信心、数据冲突、临场信息缺失或玩法停售时，应输出放弃条件。

每份战报都必须以类似文字开头：

```text
以下为娱乐性玄学分析，不构成投注建议或收益承诺。
```

## 许可证

MIT
