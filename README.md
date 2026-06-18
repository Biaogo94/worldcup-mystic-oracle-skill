# worldcup-mystic-oracle

一个通用 CLI Skill，用来生成中文足球「赛前玄学战报」和中国体育彩票娱乐型策略。它适配 Claude Code、OpenCode、Codex 兼容 CLI，以及任何能读取 `SKILL.md` 的本地 Agent。

所有内容只用于娱乐分析，不构成投注建议、收益承诺或确定性预测。

## 安装

使用标准 Skills 安装器安装：

```bash
npx skills add https://github.com/Biaogo94/hermes-worldcup-mystic-oracle --skill worldcup-mystic-oracle
```

本地开发时可以在仓库根目录验证或安装：

```bash
npx skills add . --list
npx skills add . --skill worldcup-mystic-oracle
```

这个仓库不提供自定义 npm 安装脚本。Claude Code、OpenCode、Codex 等 CLI 的目标目录由 `skills` 安装器自动处理。

## 目录结构

```text
skills/
  worldcup-mystic-oracle/
    SKILL.md
    references/
    scripts/
    agents/
AGENTS.md
```

## 使用方式

在 Claude Code / OpenCode / Codex 中说：

```text
使用 worldcup-mystic-oracle，预测 伊拉克 vs 挪威，并给出中国体彩策略。
```

默认是快速模式，输出：

- 娱乐性免责声明；
- 赛前事实卡；
- 奇门 + 缺时柱八字关键判断；
- 比分场景池；
- 一个结合官方赔率的主策略；
- 情景返还和放弃条件。

如果要完整术数过程，可以说：

```text
使用 worldcup-mystic-oracle 深度模式，展开奇门四盘、八字叠盘和策略计算过程。
```

## 核心脚本

抓取中国体彩官方赔率：

```bash
python skills/worldcup-mystic-oracle/scripts/fetch_sporttery_odds.py \
  --team "伊拉克" \
  --include-history \
  --output data/sporttery_odds_cache.json \
  --pretty \
  --utf8
```

一键生成赛前数据包：

```bash
python skills/worldcup-mystic-oracle/scripts/collect_match_bundle.py \
  --home "伊拉克" \
  --away "挪威" \
  --team "伊拉克" \
  --kickoff-local "2026-06-16T18:00:00-04:00" \
  --venue "Boston" \
  --people data/people.json \
  --include-history \
  --output-dir data/iraq-norway \
  --pretty \
  --utf8
```

根据比分场景和官方赔率优化一个主策略：

```bash
python skills/worldcup-mystic-oracle/scripts/optimize_strategy.py \
  --odds-cache data/sporttery_odds_cache.json \
  --scenarios skills/worldcup-mystic-oracle/references/sample-score-scenarios.json \
  --include-pools HAD,HHAD,TTG,CRS \
  --pretty \
  --utf8
```

## 设计原则

- 官方 Sporttery / 中国体彩赔率是唯一可用于返还计算的赔率源。
- 固定奖金历史接口中的 `TTG/CRS/HAFU` 可用于尾部计算，但需要注明「以临场终端销售状态为准」。
- 不默认输出多种投注风格，只给一个综合主策略。
- 不默认全包同一玩法的三个结果，因为这通常不是高效策略。
- 总进球优先用于覆盖大比分区间，比分只用于强脚本或极端尾部。
- 中国体彩按 `2元` 为基本投注单位，所有策略金额默认按 `100元示例` 输出，分支金额和均分到单选项的金额都必须是 `2元` 整数倍。
- 公开球员和教练生日按公历处理；缺出生时辰时只作三柱参考，不推断时柱。
- 奇门×八字叠盘采用：年命优先、时干补果、月令定气候。

## 依赖

Python：

```bash
python -m pip install lunar-python
```

奇门排盘推荐使用 `Biaogo94/qimen` MCP：

```bash
git clone https://github.com/Biaogo94/qimen.git ~/.codex/mcp/qimen
cd ~/.codex/mcp/qimen
npm ci
npm test
```

Codex MCP 配置示例：

```toml
[mcp_servers.qimen]
command = "node"
args = ['C:\Users\Administrator\.codex\mcp\qimen\mcp\server.mjs']
```

如果当前 Agent 没有直接暴露 MCP 工具，`collect_match_bundle.py` 会通过 `qimen_mcp_client.mjs` 调用上述 stdio server。

## 安全边界

本项目不保证命中，不承诺收益，不建议倍投、借钱投注、追损或重仓。低信心、官方赔率不可用、玩法停售、临场信息冲突时，默认策略应为 `不下注 / 纯观赛`。
